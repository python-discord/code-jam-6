from kivy.uix.anchorlayout import AnchorLayout
from kivy.app import App
from kivy.clock import Clock
from kivymd.uix.navigationdrawer import MDNavigationDrawer, NavigationDrawerIconButton, \
    NavigationLayout
from kivymd.uix.toolbar import MDToolbar


class ContentNavigationDrawer(MDNavigationDrawer):
    def __init__(self, nav_layout):
        super(ContentNavigationDrawer, self).__init__()
        self.nav_layout = nav_layout
        self.use_logo = 'logo'
        self.drawer_logo = 'ui/img/nav_drawer_logo.png'
        self.home = NavigationDrawerIconButton(text="Home", icon='home',
                                               on_press=lambda x:
                                               self.scr_chng('welcome', self.home))
        self.encode = NavigationDrawerIconButton(text="Encode", icon='database-import',
                                                 on_press=lambda x:
                                                 self.scr_chng('encode', self.encode))
        self.decode = NavigationDrawerIconButton(text="Decode", icon='database-export',
                                                 on_press=lambda x:
                                                 self.scr_chng('decode', self.decode))
        self.message = NavigationDrawerIconButton(text="Messages", icon='message',
                                                  on_press=lambda x:
                                                  self.scr_chng('message', self.message))
        self.training = NavigationDrawerIconButton(text="Training", icon='dumbbell',
                                                   on_press=lambda x:
                                                   self.scr_chng('training', self.training))
        self.add_widget(self.home)
        self.add_widget(self.encode)
        self.add_widget(self.decode)
        self.add_widget(self.message)
        self.add_widget(self.training)

    def scr_chng(self, screen, nav_item):
        self.nav_layout.toggle_nav_drawer()
        # I have to manually reset the color back to white
        # because it's not doing it on its own
        nav_item._active_color = [1, 1, 1, 1]
        if screen == 'message' and App.get_running_app().util.auth_token == '':
            App.get_running_app().root.content.current = 'sign_in'
        else:
            App.get_running_app().root.content.current = screen


class MyNavigationLayout(NavigationLayout):
    def __init__(self, scroll_view=None):
        super(MyNavigationLayout, self).__init__()
        self.content_nav_drawer = ContentNavigationDrawer(self)
        self.drawer_open = False
        self.scroll_view = scroll_view

        self.add_widget(self.content_nav_drawer)
        toolbar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        self.toolbar = MDToolbar(title='Enigma')
        self.toolbar.anchor_title = 'center'
        self.toolbar.md_bg_color = App.get_running_app().theme_cls.primary_color
        self.toolbar.left_action_items = [['menu', lambda x: self.toggle_nav_drawer()]]
        toolbar_anchor.add_widget(self.toolbar)
        self.add_widget(toolbar_anchor)

        # This is here because on scroll views the buttons behind the nav bar
        # will count as being pressed instead of the nav drawer buttons
        if self.scroll_view:
            Clock.schedule_interval(self.disable_scroll_buttons, 0.1)

    def disable_scroll_buttons(self, dt):
        if self.state == 'open':
            self.scroll_view.disabled = True
        else:
            self.scroll_view.disabled = False
