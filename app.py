# importer tkinter så jeg kan have GUI
import tkinter as tk
from tkinter import ttk

# importer fra de andre klasser
from frames.main_menu import MainMenu
from frames.scenarie1 import Scenarie1

class SpilteoriSim(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Spilteori Simulator")
        self.geometry("900x650")
        self.resizable(True, True)

        container = ttk.Frame(self)
        container.pack(fill = tk.BOTH, expand = True)

        self.frames = {}
        for F, name in [
            (MainMenu, "MainMenu"),
            (Scenarie1, "Scenarie1")
        ]:

            frame = F(container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

if __name__ == "__main__":
    app = SpilteoriSim()
    app.mainloop()