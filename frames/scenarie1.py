import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from frames.scenarie_base import ScenarieFrame


class Scenarie1(ScenarieFrame):
    """
    Scenarie 1: Iterated Elimination of Dominated Strategies (IESDS)

    Brugeren kan:
    - Indtaste et 2x2 eller 3x2 spil i normal form
    - Visualisere den oprindelige udbytte-matrix
    - Udføre itereret elimination trinvist
    """

    def __init__(self, parent, controller):
        # Kald superklassen (ScenarieFrame), som opsætter titel, plotFrame og back-knap
        super().__init__(parent, controller,
                         "Itereret elimination (trin-for-trin)")

        frame = self.body

        # Inputfelter til udbyttematrix
        ttk.Label(
            frame,
            text="Skriv 2x2 udbytte (format: 'P1 P2')"
        ).pack(anchor="w")

        # Grid til payoff-cellerne
        grid = ttk.Frame(frame)
        grid.pack(anchor="w", pady=5)

        # Liste til at gemme Entry-widgets
        self.entries = []

        # Opretter 2x2 inputfelter
        for i in range(2):
            row = []
            for j in range(2):
                e = ttk.Entry(grid, width=12)
                e.insert(0, "0 0")
                e.grid(row=i, column=j, padx=4, pady=4)
                row.append(e)
            self.entries.append(row)

        # Ekstra række til 3x2 spil
        extra = ttk.Frame(frame)
        extra.pack(anchor="w", pady=4)

        self.extra_var = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            extra,
            text="Inkluder ekstra række (3x2)",
            variable=self.extra_var
        ).pack(side="left")

        # Inputfelter til den ekstra række
        self.extra_entries = [
            ttk.Entry(frame, width=12),
            ttk.Entry(frame, width=12)
        ]

        for e in self.extra_entries:
            e.insert(0, "0 0")
            e.pack(anchor="w")

        # Knapper
        btns = ttk.Frame(frame)
        btns.pack(pady=6)

        ttk.Button(
            btns,
            text="Plot udbyttematrix",
            command=self.plot_matrices
        ).pack(side="left", padx=4)

        ttk.Button(
            btns,
            text="Start elimination",
            command=self.start_elimination
        ).pack(side="left", padx=4)

        ttk.Button(
            btns,
            text="Næste eliminering",
            command=self.next_elimination_step
        ).pack(side="left", padx=4)

        # Intern Tilstand
        # Disse matricer gemmer den nuværende reducerede version af spillet
        self.current_P1 = None
        self.current_P2 = None

    # læs udbyttematrix fra GUI
    def read_matrix(self):
        """
        Læser udbyttematrixen fra inputfelterne
        og returnerer to matricer:
        - P1: Udbytte for spiller 1
        - P2: Udbytte for spiller 2
        """
        try:
            P1 = np.zeros((2, 2))
            P2 = np.zeros((2, 2))

            # Læs 2x2 inputfelter
            for i in range(2):
                for j in range(2):
                    p = self.entries[i][j].get().split()
                    if len(p) != 2:
                        raise ValueError(
                            "Hver celle skal indeholde 'P1 P2'"
                        )
                    P1[i, j] = float(p[0])
                    P2[i, j] = float(p[1])

            # Hvis ekstra række er valgt -> lav 3x2 spil
            if self.extra_var.get():
                e0 = self.extra_entries[0].get().split()
                e1 = self.extra_entries[1].get().split()

                if len(e0) != 2 or len(e1) != 2:
                    raise ValueError(
                        "Ekstra række skal have 'P1 P2'"
                    )

                P1 = np.vstack(
                    [P1, [float(e0[0]), float(e1[0])]]
                )
                P2 = np.vstack(
                    [P2, [float(e0[1]), float(e1[1])]]
                )

            return P1, P2

        except Exception as ex:
            messagebox.showerror("Fejl", str(ex))
            return None, None

    # til plotting af matrix
    def plot_matrices(self):
        """Plotter den oprindelige udbyttematrix."""
        P1, P2 = self.read_matrix()
        if P1 is None:
            return

        self.plotFrame.clear()

        ax1 = self.plotFrame.fig.add_subplot(1, 2, 1)
        ax2 = self.plotFrame.fig.add_subplot(1, 2, 2)

        # heatmap til cellerne
        ax1.imshow(P1, cmap="Oranges")
        ax2.imshow(P2, cmap="PuRd")

        # Skriv udbytteværdier i hver celle
        for i in range(P1.shape[0]):
            for j in range(P1.shape[1]):
                ax1.text(j, i, f"{P1[i, j]:.1f}",
                         ha="center", va="center")
                ax2.text(j, i, f"{P2[i, j]:.1f}",
                         ha="center", va="center")

        ax1.set_title("Player 1 payoff")
        ax2.set_title("Player 2 payoff")

        self.plotFrame.fig.tight_layout()
        self.plotFrame.draw()

    def plot_current(self):
        """Plotter den aktuelt reducerede matrix."""
        self.plotFrame.clear()

        ax1 = self.plotFrame.fig.add_subplot(1, 2, 1)
        ax2 = self.plotFrame.fig.add_subplot(1, 2, 2)

        ax1.imshow(self.current_P1, cmap="Oranges")
        ax2.imshow(self.current_P2, cmap="PuRd")

        for i in range(self.current_P1.shape[0]):
            for j in range(self.current_P1.shape[1]):
                ax1.text(j, i,
                         f"{self.current_P1[i, j]:.1f}",
                         ha="center", va="center")
                ax2.text(j, i,
                         f"{self.current_P2[i, j]:.1f}",
                         ha="center", va="center")

        ax1.set_title("P1 (reduceret)")
        ax2.set_title("P2 (reduceret)")

        self.plotFrame.fig.tight_layout()
        self.plotFrame.draw()

    # IEDS
    def start_elimination(self):
        """
        initialiserer eliminationsprocessen.
        starter fra den fulde matrix.
        """
        P1, P2 = self.read_matrix()
        if P1 is None:
            return

        self.current_P1 = P1.copy()
        self.current_P2 = P2.copy()

        self.plot_current()

    def next_elimination_step(self):
        """
        Eliminerer 1 strategi af gangen, enten række eller kolonne
        """
        if self.current_P1 is None:
            messagebox.showinfo(
                "Info",
                "Tryk 'Start elimination' først."
            )
            return

        result = self.find_one_dominated(
            self.current_P1,
            self.current_P2
        )

        if result is None:
            messagebox.showinfo(
                "Færdig",
                "Ingen flere dominerede strategier."
            )
            return

        kind, idx = result

        # fjern række eller kolonne
        if kind == "row":
            self.current_P1 = np.delete(
                self.current_P1, idx, axis=0
            )
            self.current_P2 = np.delete(
                self.current_P2, idx, axis=0
            )

        elif kind == "col":
            self.current_P1 = np.delete(
                self.current_P1, idx, axis=1
            )
            self.current_P2 = np.delete(
                self.current_P2, idx, axis=1
            )

        self.plot_current()

    # IEDS logik
    def find_one_dominated(self, P1, P2):
        """
        Finder en strictly dominated strategi
        Returnerer:
        - ("row", i)  -> Player 1's strategi i er domineret
        - ("col", j)  -> Player 2's strategi j er domineret
        - None        -> ingen flere dominerede strategier
        """

        # Tjek Player 1's rækker
        for i in range(P1.shape[0]):
            for k in range(P1.shape[0]):
                if i == k:
                    continue
                if (np.all(P1[k] >= P1[i]) and
                        np.any(P1[k] > P1[i])):
                    return ("row", i)

        # Tjek Player 2's kolonner
        for j in range(P2.shape[1]):
            for l in range(P2.shape[1]):
                if j == l:
                    continue
                col_j = P2[:, j]
                col_l = P2[:, l]
                if (np.all(col_l >= col_j) and
                        np.any(col_l > col_j)):
                    return ("col", j)

        return None
