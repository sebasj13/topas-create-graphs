from tkinter import Frame
from .tabview_v2 import TabView

class MainViewer(Frame):
    
    """The main viewer of the TGS application.
    """
    
    def __init__(self, parent):
        
        self.parent = parent
        super().__init__(self.parent, border=1, bg="#E5E5E5")
        self.tabview = TabView(self)
        self.tabview.pack(fill="both", expand=True)
        self.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.register_drop_target("*")
        self.bind("<<Drop>>", self.drop)


    def drop(self, event):
        if len(self.tabview.tabnames) == 0:
            self.tabview.add_tab(name = True)

        else:
            print(self.tabview.tabnames[self.tabview.tabnames.index(self.tabview.get())])