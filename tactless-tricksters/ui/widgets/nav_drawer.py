from kivy.uix.anchorlayout import AnchorLayout
from kivy.app import App
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerIconButton, \
                                     NavigationLayout
from kivymd.toolbar import MDToolbar

class ContentNavigationDrawer(MDNavigationDrawer):
    def __init__(self, nav_layout):
        super(ContentNavigationDrawer, self).__init__()
        self.nav_layout = nav_layout
        self.use_logo = 'logo'
        self.drawer_logo = 'ui/img/nav_drawer_logo.png'
        self.home = NavigationDrawerIconButton(text="Home", icon='home',
                                               on_release=lambda x: self.scr_chng('welcome', self.home))
        self.encode = NavigationDrawerIconButton(text="Encode", icon='login',
                                                 on_release=lambda x: self.scr_chng('encode', self.encode))
        self.decode = NavigationDrawerIconButton(text="Decode", icon='logout',
                                                 on_release=lambda x: self.scr_chng('decode', self.decode))
        self.add_widget(self.home)
        self.add_widget(self.encode)
        self.add_widget(self.decode)

    def scr_chng(self, screen, nav_item):
        self.nav_layout.toggle_nav_drawer()
        # I have to manually reset the color back to white
        # because it's not doing it on its own
        nav_item._active_color = [1, 1, 1, 1]
        App.get_running_app().root.content.current = screen

class MyNavigationLayout(NavigationLayout):
    def __init__(self):
        super(MyNavigationLayout, self).__init__()
        self.content_nav_drawer = ContentNavigationDrawer(self)
        self.add_widget(self.content_nav_drawer)
        toolbar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        toolbar = MDToolbar(title='Enigma')
        toolbar.anchor_title = 'center'
        toolbar.md_bg_color = App.get_running_app().theme_cls.primary_color
        toolbar.left_action_items = [['menu', lambda x: self.toggle_nav_drawer()]]
        toolbar_anchor.add_widget(toolbar)
        self.add_widget(toolbar_anchor)
