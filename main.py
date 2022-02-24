from kivymd.app import MDApp
from kivy.properties import (StringProperty, ObjectProperty, DictProperty, ListProperty)
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.event import EventDispatcher
from kivy.clock import Clock

from kivy.uix.image import Image 
from kivy.graphics.texture import Texture
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout


import weakref
from tkinter import filedialog
import tkinter
import json
import scrcpy
import cv2
from functools import partial
from os import path

import phoneCommands
import newProj
Builder.load_file('newProj.kv')


Window.minimum_width = 1345
Window.minimum_height = 800
Window.size = (1345, 800)

ready = 0
key = 0
pop = 0
storedFrame = []

client = scrcpy.Client(device="PL2GAR9830701342")
client.max_fps = 60
client.max_width= 800


class ImgCard(MDCard, RectangularElevationBehavior):
    img = StringProperty("")


class BookTitle(MDLabel):
    pass
    #bookName = StringProperty("Teste123")


class IconLabel(MDBoxLayout):
    icon_name = StringProperty("")
    label_text = StringProperty("####/####")


class LeftPannel(MDBoxLayout):
    mainObj = ObjectProperty()


class RightPannel(MDBoxLayout):
    videoFrame = ObjectProperty()
    bookLabel = ObjectProperty()
    bookName = StringProperty()
    label_text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bookName = "Book Title"
        #partial_pageChange = partial(self.pageChange, self = self )
        client.add_listener(scrcpy.EVENT_FRAME, self.storeFrame)
        Clock.schedule_interval(self.pageChange, 1/60)


    def headerChange(self, projectData):
        rightPannelObj = self.mainObj.ids.main_layout.ids.right_side
        rightPannelObj.bookLabel.adaptive_size = "False"
        rightPannelObj.bookName = projectData["book_name"]
        rightPannelObj.bookLabel.adaptive_size = "True"
        rightPannelObj.label_text = f'{projectData["cur_page"]*100/projectData["page_number"]} % ({projectData["cur_page"]}/{projectData["page_number"]})'
    
    def storeFrame(self, frame):
        global storedFrame
        if frame is not None:
            storedFrame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    def pageChange(self, *args):
        global storedFrame
        if storedFrame != []:
            image = cv2.flip(storedFrame, 0)
            buf = image.tostring()
            image_texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.videoFrame.texture = image_texture


class SettingsBox(MDBoxLayout):
    mainPath = ObjectProperty()
    currentPage = ObjectProperty()
    currentChap = ObjectProperty()
    mainObj = ObjectProperty()
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def test(self):
        print(phoneCommands.checkFiles())

    def open_project(self):
        tkinter.Tk().withdraw()
        folder_path = filedialog.askdirectory()
        self.mainPath.set_text(self, folder_path)
        print(folder_path)
        return

    def new_project(self):
        self.mainObj.ids.main_layout.bind(disabled=self.on_property)
        popup = newProj.NewProject(
            mainObj=self.mainObj
        )
        self.mainObj.add_widget(popup)
        self.mainObj.ids.main_layout.disabled = 'True'
        self.mainObj.ids["new_project"] = weakref.ref(popup)
        print("Teste1")

    def apply_configs(self):
        global ready
        if not(path.isfile(f'{self.mainPath.text}/configs.json')):
            return
        f = open(f'{self.mainPath.text}/configs.json')
        project = json.load(f)

        self.currentPage.set_text(self,  str(project["cur_page"]))
        self.currentChap.set_text(self,  str(project["cur_chap"]))
        RightPannel.headerChange(self, project)
        MDApp.get_running_app().root.statedata.project = project
        print(project)
        ready = 1


    def on_property(self, obj, value):
        global pop
        print(value, pop)
        if not(value) and pop == 0:
            projectData = MDApp.get_running_app().root.statedata.newProject
            self.mainPath.set_text(self, projectData["proj_path"])
            self.currentPage.set_text(self, str(projectData["cur_page"]))
            self.currentChap.set_text(self, str(projectData["cur_chap"]))
            pop == 1
        else:
            pop == 0


class MainLayout(MDBoxLayout):
    leftSide = ObjectProperty()
    rightSide = ObjectProperty()
    mainObj = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        Window.bind(on_key_down=self.key_down)

    def key_down(self, instance, keyboard, keycode, text, modifiers):
        global ready
        print(keycode)
        if ready == 1:
            projectData = MDApp.get_running_app().root.statedata.project
            if keycode == 80:  # New Chapter Left Side
                res = phoneCommands.bulkPull(
                    projectData["proj_path"], projectData["cur_chap"], False, projectData["cur_page"])
                projectData["cur_page"] = res[0]
                projectData["left_page"] = res[1]
                projectData["right_page"] = res[2]
                RightPannel.pageChange(self.mainObj, res[1], res[2])
                MDApp.get_running_app().root.statedata.project = projectData                
                phoneCommands.removeFiles()
            elif keycode == 82:  # New Chapter Right Side
                res = phoneCommands.bulkPull(
                    projectData["proj_path"], projectData["cur_chap"], False, projectData["cur_page"])
                projectData["cur_page"] = res[0]
                projectData["left_page"] = res[1]
                projectData["right_page"] = res[2]
                RightPannel.pageChange(self.mainObj, res[1], res[2])
                MDApp.get_running_app().root.statedata.project = projectData
                phoneCommands.removeFiles()
            elif keycode == 79:  # Normal Scan
                phoneCommands.sendInput()


            print("Captured after confirmation")


class MainScreen(Screen):
    mainObj = ObjectProperty()
    pass


class varsBetweenScreens(EventDispatcher):
    #newFolderObj = ObjectProperty(MDLabel)
    newProject = DictProperty()
    project = DictProperty()
    some_value = StringProperty()


class MyScreenManager(ScreenManager):
    statedata = ObjectProperty(varsBetweenScreens())
    pass


class MainApp(MDApp):


    def build(self):
        Window.bind(on_request_close=self.on_request_close)
        self.theme_cls.theme_style = "Dark"
        sm = MyScreenManager(transition=FadeTransition())
        sm.add_widget(MainScreen(name="main"))
        return sm
    
    def on_request_close(self, *args):
        client.stop()
        self.stop()


client.start(threaded=True)
MainApp().run()
