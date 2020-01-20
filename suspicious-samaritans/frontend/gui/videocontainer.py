"""Module for the video player classes"""

from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.video import Video
from kivy.uix.widget import Widget

from backend.video.main import create_thumbnail
from frontend.gui.custom_widgets import ColorBoxLayout


class ContainerWidget(Widget):
    """Base class for all video container elements like the thumbnail and the video"""

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.parent.parent.toggle_videoplay()


class Thumbnail(Image, ContainerWidget):
    """Thumbnail for the video currently in editor"""
    pass


class EditorVideo(Video, ContainerWidget):
    """Video widget for the editor"""

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                self.parent.parent.change_screen()
            else:
                self.parent.parent.toggle_videoplay()


class VideoContainer(ColorBoxLayout):
    """Container for the video and the video controls"""

    container = ObjectProperty()
    play_button = ObjectProperty()
    volume_button = ObjectProperty()
    screen_button = ObjectProperty()
    video = ObjectProperty()
    source = StringProperty("frontend/assets/sample.mkv")
    thumbnail = StringProperty("frontend/assets/playscreen.png")
    play_icon = "frontend/assets/play.png"
    pause_icon = "frontend/assets/pause.png"
    stop_icon = "frontend/assets/stop.png"
    full_volume_icon = "frontend/assets/full_sound.png"
    half_volume_icon = "frontend/assets/half_sound.png"
    small_volume_icon = "frontend/assets/small_sound.png"
    mute_icon = "frontend/assets/no_sound.png"
    stop_icon = "frontend/assets/stop.png"
    fullscreen_icon = "frontend/assets/full_screen.png"
    smallscreen_icon = "frontend/assets/small_screen.png"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.is_fullscreen = False
        self.siblings = []

    def on_container(self, instance, value):
        if self.source:
            self.on_source(self, self.source)
        else:
            self.add_thumbnail()

    def add_thumbnail(self):
        """Add thumbnail to the container"""
        self.container.clear_widgets()
        self.image = Thumbnail(source=self.thumbnail)
        self.container.add_widget(self.image)

    def on_source(self, instance, value):
        """Create a thumbnail for the new video"""
        create_thumbnail(value)
        self.thumbnail = ".thumbnail.png"
        self.add_thumbnail()

    def create_video(self):
        """Create the video object for the container"""
        self.video = EditorVideo(source=self.source, state="play")
        self.play_button.source = self.pause_icon
        self.container.clear_widgets()
        self.container.add_widget(self.video)

    def toggle_videoplay(self):
        """Play the video if its paused"""
        if self.video:
            if self.video.state == "play":
                self.video.state = "pause"
                self.play_button.source = self.play_icon
            elif self.video.state == "pause":
                self.video.state = "play"
                self.play_button.source = self.pause_icon
            elif self.video.state == "stop":
                self.create_video()
        elif self.source:
            self.create_video()
        else:
            print("No source is specified")

    def stop_video(self):
        """Stop the video playing and reset to show the thumbnail"""
        if self.video:
            self.video.state = "stop"
            self.play_button.source = self.play_icon
            self.container.clear_widgets()
            self.container.add_widget(self.image)

    def change_volume(self):
        """Mute if unmuted and unmute if muted"""
        if self.video:
            if self.video.volume >= 0.8:
                self.video.volume = 0.5
                self.volume_button.source = self.half_volume_icon
            elif self.video.volume >= 0.5:
                self.video.volume = 0.25
                self.volume_button.source = self.small_volume_icon
            elif self.video.volume > 0:
                self.video.volume = 0
                self.volume_button.source = self.mute_icon
            else:
                self.video.volume = 1
                self.volume_button.source = self.full_volume_icon

    def change_screen(self):
        """Expand video to fullscreen or bring it back to normal"""
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.screen_button.source = self.fullscreen_icon
            for sibling in self.siblings:
                self.parent.add_widget(sibling)
        else:
            self.is_fullscreen = True
            self.screen_button.source = self.smallscreen_icon
            self.siblings = [child for child in self.parent.children if child != self]
            for sibling in self.siblings:
                self.parent.remove_widget(sibling)
