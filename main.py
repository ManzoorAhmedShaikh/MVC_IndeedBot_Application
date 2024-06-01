from customtkinter import *

from Controller import Controller
from Model import Model
from View import View
import os

if __name__ == '__main__':
    root = CTk()
    view = View.View(root)
    model = Model.Model()
    controller = Controller.Controller(model, view)
    root.mainloop()
    os.system("taskkill /f /im chromedriver.exe /T")
