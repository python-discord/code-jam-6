import pickle
from datetime import timedelta, datetime

from kivy.animation import Animation
from kivy.core.window import Window
from kivy.properties import NumericProperty, Clock
from kivy.uix.effectwidget import EffectWidget, EffectBase
from kivy.uix.floatlayout import FloatLayout
from suntime import SunTimeException, Sun

hv_blur = """
vec4 effect(vec4 color, sampler2D texture, vec2 tex_coords, vec2 coords)
{{
    float dt = ({} / 4.0) * 1.0 / resolution.x;
    vec4 sum = vec4(0.0);
    sum += texture2D(texture, vec2(tex_coords.x - 4.0*dt, tex_coords.y))
                     * 0.05;
    sum += texture2D(texture, vec2(tex_coords.x - 3.0*dt, tex_coords.y))
                     * 0.09;
    sum += texture2D(texture, vec2(tex_coords.x - 2.0*dt, tex_coords.y))
                     * 0.12;
    sum += texture2D(texture, vec2(tex_coords.x - dt, tex_coords.y))
                     * 0.15;
    sum += texture2D(texture, vec2(tex_coords.x, tex_coords.y))
                     * 0.16;
    sum += texture2D(texture, vec2(tex_coords.x + dt, tex_coords.y))
                     * 0.15;
    sum += texture2D(texture, vec2(tex_coords.x + 2.0*dt, tex_coords.y))
                     * 0.12;
    sum += texture2D(texture, vec2(tex_coords.x + 3.0*dt, tex_coords.y))
                     * 0.09;
    sum += texture2D(texture, vec2(tex_coords.x + 4.0*dt, tex_coords.y))
                     * 0.05;
    sum += texture2D(texture, vec2(tex_coords.x, tex_coords.y - 4.0*dt))
                     * 0.05;
    sum += texture2D(texture, vec2(tex_coords.x, tex_coords.y - 3.0*dt))
                     * 0.09;
    sum += texture2D(texture, vec2(tex_coords.x, tex_coords.y - 2.0*dt))
                     * 0.12;
    sum += texture2D(texture, vec2(tex_coords.x, tex_coords.y - dt))
                     * 0.15;
    sum += texture2D(texture, vec2(tex_coords.x, tex_coords.y))
                     * 0.16;
    sum += texture2D(texture, vec2(tex_coords.x, tex_coords.y + dt))
                     * 0.15;
    sum += texture2D(texture, vec2(tex_coords.x, tex_coords.y + 2.0*dt))
                     * 0.12;
    sum += texture2D(texture, vec2(tex_coords.x, tex_coords.y + 3.0*dt))
                     * 0.09;
    sum += texture2D(texture, vec2(tex_coords.x, tex_coords.y + 4.0*dt))
                     * 0.05;
    return vec4(sum.xyz, color.w);
}}
"""


# Widget element things #
class DialWidget(FloatLayout):
    """
    Speed will become a fixed value of 86400 once completed.
    Image should, i suppose, be a fixed image?
    At some point we'll need to add a tuple(?) for sunrise / sunset times.
    """
    angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super(DialWidget, self).__init__(**kwargs)

        # Widget properties
        self.day_length = 86400
        self.date_increase = 1
        self.dial_size = (0.8, 0.8)
        self.date = datetime.now()

        self.midnight = (self.date + timedelta(days=1))
        self.midnight_delta = (datetime(year=self.midnight.year, month=self.midnight.month,
                                        day=self.midnight.day, hour=0, minute=0, second=0) - self.date).seconds

        # Split suntime tuple into named variables
        self.sun_angles = self.sun_time()
        self.sunrise = self.sun_angles[0]
        self.sunset = self.sun_angles[1]

        # Shading widget
        self.dial_shading = DialEffectWidget((self.sunrise, self.sunset))

        # Add icons that can be arbitrarily rotated on canvas.
        self.sun_rise_marker = SunRiseMarker(self.sunrise)
        self.sun_set_marker = SunSetMarker(self.sunset)

        # Add widgets
        self.add_widget(self.dial_shading)
        self.add_widget(self.sun_rise_marker)
        self.add_widget(self.sun_set_marker)

        self.animate_dial()
        self.clock = Clock.schedule_interval(self.redraw, self.midnight_delta)

    def animate_dial(self):
        anim = Animation(angle=359, duration=self.day_length)
        anim += Animation(angle=359, duration=self.day_length)
        anim.repeat = True
        anim.start(self)

    def redraw(self, a=None):
        # Split suntime tuple into named variables
        sun_angles = self.sun_time()
        self.sunrise = sun_angles[0]
        self.sunset = sun_angles[1]

        # Remove widgets
        self.remove_widget(self.dial_shading)
        self.remove_widget(self.sun_rise_marker)
        self.remove_widget(self.sun_set_marker)

        # Shading widget
        self.dial_shading = DialEffectWidget((self.sunrise, self.sunset))

        # Add icons that can be arbitrarily rotated on canvas.
        self.sun_rise_marker = SunRiseMarker(self.sunrise)
        self.sun_set_marker = SunSetMarker(self.sunset)

        # Add widgets
        self.add_widget(self.dial_shading)
        self.add_widget(self.sun_rise_marker)
        self.add_widget(self.sun_set_marker)

        # Restart the clock!
        self.clock.cancel()
        self.clock = Clock.schedule_interval(self.redraw, self.midnight_delta)

    def sun_time(self):
        with open('latlong.tmp', 'rb') as f:
            lat_long = pickle.load(f)

        sun_time = Sun(lat_long[0], lat_long[1])
        self.date = self.date + timedelta(days=self.date_increase)

        try:
            today_sunrise = sun_time.get_sunrise_time(self.date)
        except SunTimeException:
            raise ValueError("AINT NO SUNSHINE WHEN SHE'S GONE")

        try:
            today_sunset = sun_time.get_sunset_time(self.date)
        except SunTimeException:
            raise ValueError("HOLY SHIT TOO MUCH SUNSHINE WHEN SHE'S HERE")

        # This is *super* ugly, I'm sure we can find a more elegant way to do this
        now = datetime.utcnow() - timedelta(hours=0)
        today_sunrise = today_sunrise.replace(tzinfo=None)
        today_sunset = today_sunset.replace(tzinfo=None)

        # After Sunrise, after Sunset
        if now > today_sunrise and today_sunset:
            # Get timedelta for each
            today_sunrise = now - today_sunrise
            today_sunset = now - today_sunset

            # Convert timedelta into minutes and rClock.schedule_interval(self.redraw, self.midnight_delta)ound
            today_sunrise = round(today_sunrise.seconds / 60)
            today_sunset = round(today_sunset.seconds / 60)

            # Convert minutes into angles
            today_sunrise = today_sunrise * 0.25
            today_sunset = today_sunset * 0.25

        # Before Sunrise, after Sunset
        elif now < today_sunrise and today_sunset:
            today_sunrise = today_sunrise - now
            today_sunset = today_sunset - now

            today_sunrise = round(today_sunrise.seconds / 60)
            today_sunset = round(today_sunset.seconds / 60)

            today_sunrise = 360 - (today_sunrise * 0.25)
            today_sunset = 360 - (today_sunset * 0.25)

        # After Sunrise, before Sunset
        else:
            today_sunrise = now - today_sunrise
            today_sunset = today_sunset - now

            today_sunrise = round(today_sunrise.seconds / 60)
            today_sunset = round(today_sunset.seconds / 60)

            today_sunrise = today_sunrise * 0.25
            today_sunset = 360 - (today_sunset * 0.25)

        return today_sunrise, today_sunset

    def on_angle(self, item, angle):
        if angle == 359:
            item.angle = 0
            self.redraw()


class DoubleVision(EffectBase):
    size = NumericProperty(4.0)

    def __init__(self, *args, **kwargs):
        super(DoubleVision, self).__init__(*args, **kwargs)
        self.do_glsl()

    def on_size(self, *args):
        self.do_glsl()

    def do_glsl(self):
        self.glsl = hv_blur.format(float(self.size))


class DialEffectWidget(EffectWidget):
    def __init__(self, angles, **kwargs):
        super(DialEffectWidget, self).__init__(**kwargs)

        self.shade_size = Window.height * 0.8, Window.height * 0.8
        self.add_widget(SunShading(angles))
        self.effects = [DoubleVision(size=50.0)]
        self.opacity = 0.25

    def _pos_check(self):
        if Window.width > Window.height:
            self.shade_size = Window.height * 0.8, Window.height * 0.8
        else:
            self.shade_size = Window.width * 0.8, Window.width * 0.8


class SunShading(FloatLayout):
    def __init__(self, angles, **kwargs):
        super(SunShading, self).__init__(**kwargs)

        rise_angle = angles[0]
        set_angle = angles[1]

        sun_colour = (0.9, 0.9, 0.08, 1)
        shade_colour = (0.0, 0.2, 0.4, 1)

        # More of bisks brutally ugly work
        if rise_angle < set_angle:
            self.shade_one_angle_start = 360 - set_angle
            self.shade_one_angle_stop = 360 - rise_angle
            self.shade_one_color = shade_colour

            self.sun_one_angle_start = 0
            self.sun_one_angle_stop = 360 - set_angle
            self.sun_one_color = sun_colour
            self.sun_two_angle_start = 360 - rise_angle
            self.sun_two_angle_stop = 360
            self.sun_two_color = sun_colour

        elif rise_angle > set_angle:
            self.shade_one_angle_start = 360 - set_angle
            self.shade_one_angle_stop = 360
            self.shade_one_color = shade_colour
            self.shade_two_angle_start = 360 - rise_angle
            self.shade_two_angle_stop = 0
            self.shade_two_color = shade_colour

            self.sun_one_angle_start = 360 - rise_angle
            self.sun_one_angle_stop = 360 - set_angle
            self.sun_one_color = sun_colour

        self.shade_size = Window.height * 0.8, Window.height * 0.8

    def _size_check(self):
        self.shade_size = Window.height * 0.8, Window.height * 0.8


class SunRiseMarker(FloatLayout):
    def __init__(self, rot_angle, **kwargs):
        super(SunRiseMarker, self).__init__(**kwargs)
        self.rot_angle = rot_angle


class SunSetMarker(FloatLayout):
    def __init__(self, rot_angle, **kwargs):
        super(SunSetMarker, self).__init__(**kwargs)
        self.rot_angle = rot_angle


class NowMarker(FloatLayout):
    pass
