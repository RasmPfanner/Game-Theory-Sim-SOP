# denne klasse er et template for de scenarierne

from tkinter import ttk
from plotting.plot_frame import PlotFrame

class ScenarieFrame(ttk.Frame):
    def __init__(self, parent, controller, title="Scenario"):
        super().__init__(parent)
        self.controller = controller

        header = ttk.Label(self, text=title, font=("TkDefaultFont", 14, "bold"))
        header.pack(pady=6)

        self.body = ttk.Frame(self)
        self.body.pack(fill="x", pady=8) #fylder frame ud på x-aksen, bestemt højde y-akse

        # plot frame fra plot_frame bliver embedded
        self.plotFrame = PlotFrame(self.body, figsize=(6,4))
        self.plotFrame.pack(fill="both", expand=True, padx=8, pady=8)

        # tilbageknap
        nav = ttk.Frame(self)
        nav.pack(fill="x", padx=8, pady=6)
        back = ttk.Button(nav, text="Back", command=lambda: controller.show_frame("MainMenu")) # selve knappen
        back.pack(side="right")