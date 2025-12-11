import numpy as np
from  tkinter import ttk, messagebox, BooleanVar # kan vise beskeder
from frames.scenarie_base import ScenarieFrame # importer template

class Scenarie1(ScenarieFrame): # nedarver fra scenarie_base
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Iterated Elimination")

        frame = self.body
        ttk.Label(frame, text="Skriv 2x2 udbytte (format: 'P1, P2')").pack(anchor="w") # centrer teksten vertikalt

        grid = ttk.Frame(frame)
        grid.pack(anchor="w", pady=5)

        self.entries = []
        for i in range(2):
            row = []
            for j in range(2):
                e = ttk.Entry(grid, width=12)
                e.insert(0, "0 0")
                e.grid(row=i, column=j, pady=4, padx=4)
                row.append(e)
            self.entries.append(row)

        # yderligere række for weakly dominated rækkke
        extra = ttk.Frame(frame)
        extra.pack(anchor="w", pady=4)
        self.extra_var = BooleanVar(value=False)
        ttk.Checkbutton(extra, text="Inkluder extra række",
                        variable=self.extra_var).pack(side="left")

        self.extra_entries = [ttk.Entry(frame, width=12), ttk.Entry(frame, width=12)]
        self.extra_entries[0].insert(0, "0 0")
        self.extra_entries[1].insert(0, "0 0")
        self.extra_entries[0].pack(anchor="w")
        self.extra_entries[1].pack(anchor="w")

        btns = ttk.Frame(frame)
        btns.pack(pady=5)

        ttk.Button(btns, text = "Plot udbyttematrix", command = self.plot_matrices).pack(side="left", padx=4)
        ttk.Button(btns, text = "Plot efter elimination", command = self.plot_elimination).pack(side="left", padx=4)

    def read_matrix(self):
        try:
            P1 = np.zeros((2,2))
            P2 = np.zeros((2,2))

            for i in range(2):
                for j in range(2):
                    p = self.entries[i][j].get().split()
                    P1[i,j] = float(p[0])
                    P2[i,j] = float(p[1])

            if self.extra_var.get():
                e0 = self.extra_entries[0].get().split()
                e1 = self.extra_entries[1].get().split()
                P1 = np.vstack([P1, [float(e0[0]), float(e1[0])]])
                P2 = np.vstack([P2, [float(e0[1]), float(e1[1])]])

            return P1, P2
        except:
            messagebox.showerror("Error", "Invalid udbytte format.")
            return None, None

    def plot_matrices(self):
        P1, P2 = self.read_matrix()
        if P1 is None: return

        self.plotFrame.clear()
        ax1 = self.plotFrame.fig.add_subplot(1,2,1)
        ax2 = self.plotFrame.fig.add_subplot(1,2,2)

        ax1.imshow(P1, cmap="viridis")
        ax2.imshow(P2, cmap="plasma")

        ax1.set_title("P1 udbytte")
        ax2.set_title("P2 udbytte")

        self.plotFrame.fig.tight_layout()
        self.plotFrame.draw()

    def plot_elimination(self):
        P1, P2 = self.read_matrix()
        if P1 is None: return

        if P1.shape[0] == 2:
            messagebox.showinfo("Info", "Ingen ekstra række at eliminere")
            return

        P1core = P1[:-1,:]
        P2core = P2[:-1,:]

        self.plotFrame.clear()
        ax1 = self.plotFrame.fig.add_subplot(1,2,1)
        ax2 = self.plotFrame.fig.add_subplot(1,2,2)

        ax1.imshow(P1core, cmap="viridis")
        ax2.imshow(P2core, cmap="plasma")

        ax1.set_title("Efter elimination (P1)")
        ax2.set_title("Efter elimination (P2)")

        self.plotFrame.fig.tight_layout()
        self.plotFrame.draw()