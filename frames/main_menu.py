from tkinter import ttk

class MainMenu(ttk.Frame): #opretter MainMenu som en frame
    def __init__(self, parent, controller): #
        super().__init__(parent)
        self.controller = controller

        # tekstfelter til tekst
        ttk.Label(self, text="Spilteori Simulator",
                  font=("TkDefaultFont", 16, "bold")).pack(pady=12)

        ttk.Label(self, text="Vælg en simulation").pack(pady=(0,6))

        # opretter en frame til buttons
        btns = ttk.Frame(self)
        btns.pack()

        # Knapper der tager hen til forskellige simulationsscenarier
        ttk.Button(btns, text="Iterated Elimination", width=24,
                   command=lambda: controller.show_frame("Scenarie1")).grid(row=0, column=0, pady=4)

        ttk.Button(btns, text="Mixed NE Sensitivity", width=24,
                   command=lambda: controller.show_frame("Scenario2")).grid(row=1, column=0, pady=4)

        ttk.Button(btns, text="Signaling Phase Diagram", width=24,
                   command=lambda: controller.show_frame("Scenario3")).grid(row=2, column=0, pady=4)

        ttk.Button(btns, text="Repeated PD", width=24,
                   command=lambda: controller.show_frame("Scenario4")).grid(row=3, column=0, pady=4)

        # Luk applikation
        ttk.Button(self, text="Luk", command=controller.quit).pack(pady=10)