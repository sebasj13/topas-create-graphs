# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 12:47:50 2021

@author: Sebastian Schäfer
@institution: Martin-Luther-Universität Halle-Wittenberg
@email: sebastian.schaefer@student.uni-halle.de
"""

import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import PhotoImage

from src.classes.install_dnd import InstallDnD
from src.classes.main_viewer import MainApplication


def topasgraphsim():

    try:
        import TkinterDnD2 as dnd
    except ImportError:

        drag = InstallDnD()

        if drag.install_success == True:
            python = sys.executable
            os.execl(python, python, *sys.argv)
            return

    modulename = "TkDnD2"
    if modulename not in sys.modules:
        root = tk.Tk()
    else:
        root = dnd.TkinterDnD.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = screen_width // 2
    height = screen_height // 2
    x = screen_width // 2 - width // 2
    y = screen_height // 2 - height // 2
    root.minsize(width + 50, height)
    root.geometry(f"{width+50}x{height}+{x-25}+{y}")
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

    root.after(
        50,
        root.iconphoto(
            True,
            PhotoImage(
                file=os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "src",
                    "resources",
                    "icon.png",
                ),
                master=root,
            ),
        ),
    )
    root.mainloop()


if __name__ == "__main__":
    topasgraphsim()
