from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.properties import (StringProperty, ObjectProperty)
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.card import MDCard
from kivy.uix.floatlayout import FloatLayout

import tkinter
from tkinter import filedialog


class ProjectCard(MDCard, RoundedRectangularElevationBehavior):
    text = StringProperty()
    newPath = ObjectProperty()

    def open_project(self):
        tkinter.Tk().withdraw()
        folder_path = filedialog.askdirectory()
        self.newPath.set_text(self, folder_path)
        print(folder_path)
        return

    def toMain(self):
        MDApp.get_running_app().root.statedata.newFolderPath = {"text": self.newPath.text}
        MDApp.get_running_app().root.statedata.some_value = "Teste 123"
        MDApp.get_running_app().root.current = "main"


class NewProject(FloatLayout):
    outerBox = ObjectProperty(None)
    box = ObjectProperty(None)

    # def on_size(self, *args):
    #     maxH = 650
    #     maxW = 400
    #     # Max height in porportion to width (5 height to 3 width)
    #     calc_maxH = 1.625*self.box.size[0]
    #     # Max width in porportion to height (3 width to 5 heigth)
    #     calc_maxW = 0.615*self.box.size[1]

    #     if(self.box.size[0] > maxW and self.box.size[1] > maxH):
    #         self.box.size = (maxW, maxH)
    #     elif(self.box.size[0] > calc_maxW or self.box.size[0] > maxW):
    #         self.box.size[0] = calc_maxW if calc_maxW < maxW else maxW
    #     elif(self.box.size[1] > calc_maxH or self.box.size[1] > maxH):
    #         self.box.size[1] = calc_maxH if calc_maxH < maxH else maxH


class NewProjectScreen(Screen):
    pass
