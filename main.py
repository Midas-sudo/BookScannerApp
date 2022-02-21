from kivymd.app import MDApp
from kivy.properties import (StringProperty, ObjectProperty, DictProperty)
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.event import EventDispatcher


import newProj
Builder.load_file('newProj.kv')

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.behaviors import RectangularElevationBehavior

import tkinter
from tkinter import filedialog


Window.minimum_width = 1345
Window.minimum_height = 800
Window.size = (1345, 800)

ready = 0
key = 0


class ImgCard(MDCard, RectangularElevationBehavior):
    img = StringProperty("")


class IconLabel(MDBoxLayout):
    icon_name = StringProperty("")
    label_text = StringProperty("")


class RightPannel(MDBoxLayout):
    pageNumber = ObjectProperty()
    completionPercent = ObjectProperty()
    leftPage = ObjectProperty()
    rightPage = ObjectProperty()


class SettingsBox(MDBoxLayout):
    mainPath = ObjectProperty()
    currentPage = ObjectProperty()
    currentChap = ObjectProperty()
    newProjectBTN = ObjectProperty()

    def open_project(self):
        tkinter.Tk().withdraw()
        folder_path = filedialog.askdirectory()
        self.mainPath.set_text(self, folder_path)
        print(folder_path)
        return

    def new_project(self):
        MDApp.get_running_app().root.current = "new_project" 
        #print(MainApp, MainApp.sm)
        print("Teste1")

    def apply_configs(self):
        print("Teste2")


class MainLayout(MDBoxLayout):
    leftSide = ObjectProperty()
    rightSide = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        Window.bind(on_key_down=self.key_down)

    def key_down(self, instance, keyboard, keycode, text, modifiers):
        global key

        if key == 0:
            print(self, keyboard, instance, keycode, text, modifiers)
            key = 1
        elif key == 1:
            key = 0
        if ready == 1:
            print("Captured after confirmation")
        #print(self.leftSide.focus, self.rightSide.focus)


class MainScreen(Screen):
    def on_enter(self, *largs):
        print(self.manager.statedata.some_value, self.manager.statedata.newFolderPath)
        if len(self.manager.statedata.newFolderPath) != 0:
            print(self.manager.statedata.newFolderPath, self.manager.statedata.newFolderPath["text"])
    pass

class varsBetweenScreens(EventDispatcher):
    #newFolderObj = ObjectProperty(MDLabel)
    newFolderPath = DictProperty()
    some_value = StringProperty()


class MyScreenManager(ScreenManager):
    statedata = ObjectProperty(varsBetweenScreens())
    # def __init__(self, **kwargs):
    #     super(MyScreenManager, self).__init__(**kwargs)
    #     Clock.schedule_once(self.switch_new_project, 5)

    # def switch_new_project(self, dt):
    #     print(self)
    #     self.current = "new_project"
    
    pass

    
    

class MainApp(MDApp):
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        sm = MyScreenManager(transition=FadeTransition())
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(newProj.NewProjectScreen(name="new_project"))
        return sm


MainApp().run()
