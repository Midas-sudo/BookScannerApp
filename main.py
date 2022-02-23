from kivymd.app import MDApp
from kivy.properties import (StringProperty, ObjectProperty, DictProperty)
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.event import EventDispatcher

from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout


import weakref
from tkinter import filedialog
import tkinter
import json

import phoneCommands
import newProj
Builder.load_file('newProj.kv')


Window.minimum_width = 1345
Window.minimum_height = 800
Window.size = (1345, 800)

ready = 0
key = 0
pop = 0


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
    leftPage = ObjectProperty()
    rightPage = ObjectProperty()
    bookLabel = ObjectProperty()
    bookName = StringProperty()
    label_text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bookName = "Book Title"
        print(self)

    def headerChange(self, projectData):
        rightPannelObj = self.mainObj.ids.main_layout.ids.right_side
        print(rightPannelObj)
        rightPannelObj.bookLabel.adaptive_size = "False"
        rightPannelObj.bookName = projectData["book_name"]
        rightPannelObj.bookLabel.adaptive_size = "True"
        rightPannelObj.label_text = f'{projectData["cur_page"]*100/projectData["page_number"]} % ({projectData["cur_page"]}/{projectData["page_number"]})'

    def pageChange(mainObj, leftPath, rightPath):
        print(mainObj)
        rightPannelObj = mainObj.ids.main_layout.ids.right_side

        rightPannelObj.leftPage.img = leftPath
        rightPannelObj.rightPage.img = rightPath


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
                # phoneCommands.sendInput()
                # files = phoneCommands.checkFiles()
                # while not(files):
                #     files = phoneCommands.checkFiles()
                #     pass
                # projectData["cur_chap"] += 1
                # result = phoneCommands.pullFiles(
                #     projectData["proj_path"], projectData["cur_chap"], projectData["cur_chap"], projectData["cur_page"])
                # if result[0] == "ERROR":
                #     projectData["cur_chap"] -= 1
                #     #SHOW WARNING#
                #     return
                # projectData["cur_page"] += 2
                # projectData["left_page"] = result[0]
                # projectData["right_page"] = result[1]
                # RightPannel.pageChange(self.mainObj, result[0], result[1])
                # MDApp.get_running_app().root.statedata.project = projectData
            elif keycode == 82:  # New Chapter Right Side
                res = phoneCommands.bulkPull(
                    projectData["proj_path"], projectData["cur_chap"], False, projectData["cur_page"])
                
                projectData["cur_page"] = res[0]
                projectData["left_page"] = res[1]
                projectData["right_page"] = res[2]
                RightPannel.pageChange(self.mainObj, res[1], res[2])
                MDApp.get_running_app().root.statedata.project = projectData
                phoneCommands.removeFiles()
                # phoneCommands.sendInput()
                # files = phoneCommands.checkFiles()
                # while not(files):
                #     files = phoneCommands.checkFiles()
                #     pass
                # result = phoneCommands.pullFiles(projectData["proj_path"], projectData["cur_chap"]+1, projectData["cur_chap"], projectData["cur_page"])
                # if result[0] == "ERROR":
                #     #SHOW WARNING#
                #     return
                # else:
                #     projectData["cur_chap"] += 1
                # projectData["cur_page"] +=2
                # projectData["left_page"] = result[0]
                # projectData["right_page"] = result[1]
                # RightPannel.pageChange(self.mainObj, result[0], result[1])
                # MDApp.get_running_app().root.statedata.project = projectData
            elif keycode == 79:  # Normal Scan
                phoneCommands.sendInput()
                # files = phoneCommands.checkFiles()
                # while not(files):
                #     files = phoneCommands.checkFiles()
                #     pass
                # result = phoneCommands.pullFiles(projectData["proj_path"], projectData["cur_chap"], projectData["cur_chap"], projectData["cur_page"])
                # if result[0] == "ERROR":
                #     #SHOW WARNING#
                #     return
                # projectData["cur_page"] +=2
                # projectData["left_page"] = result[0]
                # projectData["right_page"] = result[1]
                # RightPannel.pageChange(self.mainObj, result[0], result[1])
                # MDApp.get_running_app().root.statedata.project = projectData

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
        self.theme_cls.theme_style = "Dark"
        sm = MyScreenManager(transition=FadeTransition())
        sm.add_widget(MainScreen(name="main"))
        return sm


MainApp().run()
