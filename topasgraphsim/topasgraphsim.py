# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 12:47:50 2021

@author: Sebastian Schäfer
@institution: Martin-Luther-Universität Halle-Wittenberg
@email: sebastian.schaefer@student.uni-halle.de
"""

import os
import tkinter as tk
import tkinter.ttk as ttk

from src.classes.main_viewer import MainApplication


def topasgraphsim():

    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = screen_width // 2
    height = screen_height // 2
    x = screen_width // 2 - width // 2
    y = screen_height // 2 - height // 2
    root.minsize(width + 50, height)
    root.geometry("%dx%d+%d+%d" % (width + 50, height, x - 25, y))
    ttk.Style(root)
    root.tk.call(
        "source",
        str(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "src",
                "Azure-ttk-theme",
                "azure.tcl",
            )
        ),
    )
    MainApplication(root)

    icon = ("@resources", "icon.xbm")
    if "nt" == os.name:
        icon = ("resources", "icon.ico")
    root.after(
        50,
        root.wm_iconbitmap(
            bitmap=str(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), "src", icon[0], icon[1]
                )
            )
        ),
    )
    root.mainloop()


if __name__ == "__main__":
    topasgraphsim()
