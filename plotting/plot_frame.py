from tkinter import ttk
from matplotlib.figure import Figure # til plotting af grafer
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# denne klasse skal bruges til at lave grafer

class PlotFrame(ttk.Frame):
    def __init__(self, parent, figsize=(5,4)): # definerer størrelsen af framen
        super().__init__(parent)
        self.fig = Figure(figsize=figsize, dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

    def clear(self): # hvisk figur ud
        self.fig.clf()
        self.canvas.draw()

    def draw(self): # tegn figuren
        self.canvas.draw()