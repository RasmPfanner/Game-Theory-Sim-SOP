import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from frames.scenarie_base import ScenarieFrame

class Scenarie1(ScenarieFrame):

    '''
    Scenarie 1: Iterated Elimation of Dominated Strategies IESDS/IEWDS

    Her kan spillere
    - Opstille en 2x2, og 3x2 matrix
    - visualisere den originale udbytte-matrix
    - visualisere matrixen efter elimation er fundet sted.
    '''
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Iterated Elimination")

        frame = self.body
        ttk.Label(frame, text="Skriv 2x2 udbytte (format: 'P1 P2')").pack(anchor="w")

        # Grid af celler som matrixen sidder i
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

        # den ekstra række der kan tlføjse
        extra = ttk.Frame(frame)
        extra.pack(anchor="w", pady=4)
        self.extra_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(extra, text="Inkluder extra række",
                        variable=self.extra_var).pack(side="left")

        # tilhørende kolonner til den ekstra række
        self.extra_entries = [ttk.Entry(frame, width=12), ttk.Entry(frame, width=12)]
        self.extra_entries[0].insert(0, "0 0")
        self.extra_entries[1].insert(0, "0 0")
        self.extra_entries[0].pack(anchor="w")
        self.extra_entries[1].pack(anchor="w")

        # knapper til plotting
        btns = ttk.Frame(frame)
        btns.pack(pady=5)

        ttk.Button(btns, text="Plot udbyttematrix", command=self.plot_matrices).pack(side="left", padx=4)
        ttk.Button(btns, text="Plot efter elimination", command=self.plot_elimination).pack(side="left", padx=4)


    # læser payoff matrix fra inputfields
    def read_matrix(self):
        '''
        Læser payoff fra inputfelterne i GUI, og konstruere
        to udbyttematricer P1 og P2.
        Returner P1, P2, eller None, None hvis formattering er forkert
        '''

        try:
            # start med 2x2 matrix fra inputfelterne
            P1 = np.zeros((2,2))
            P2 = np.zeros((2,2))

            # læs input fra felterne
            for i in range(2):
                for j in range(2):
                    p = self.entries[i][j].get().split()
                    if len(p) < 2:
                        raise ValueError("Each cell must contain two numbers: 'P1 P2'")
                    P1[i,j] = float(p[0])
                    P2[i,j] = float(p[1])

            # læser også hvis der er en trædje kolonne
            if self.extra_var.get():
                e0 = self.extra_entries[0].get().split()
                e1 = self.extra_entries[1].get().split()
                if len(e0) < 2 or len(e1) < 2:
                    raise ValueError("Extra entries must contain 'P1 P2' pairs")
                # Append an extra row (third row)
                P1 = np.vstack([P1, [float(e0[0]), float(e1[0])]])
                P2 = np.vstack([P2, [float(e0[1]), float(e1[1])]])

            return P1, P2
        except Exception as ex:
            messagebox.showerror("Error", f"Invalid udbytte format: {ex}")
            return None, None


    # Funktion der plotter matricerne
    def plot_matrices(self):
        P1, P2 = self.read_matrix()
        if P1 is None:
            return

        self.plotFrame.clear()
        ax1 = self.plotFrame.fig.add_subplot(1,2,1)
        ax2 = self.plotFrame.fig.add_subplot(1,2,2)

        ax1.imshow(P1, cmap="viridis")
        ax2.imshow(P2, cmap="plasma")

        # laver teksten i hver celle med dens udbytte
        for i in range(P1.shape[0]):
            for j in range(P1.shape[1]):
                ax1.text(j, i, f"{P1[i, j]:.1f}", ha="center", va="center", color="black")
                ax2.text(j, i, f"{P2[i, j]:.1f}", ha="center", va="center", color="black")

        # laver titlerne til de to matricer
        ax1.set_title("P1 udbytte")
        ax2.set_title("P2 udbytte")

        self.plotFrame.fig.tight_layout()
        self.plotFrame.draw()

    # plot matricer efter IESDS/IEWDS
    def plot_elimination(self):
        P1, P2 = self.read_matrix()
        if P1 is None:
            return

        # Kør iterated elimination
        P1e, P2e = self.eliminate_dominated(P1.copy(), P2.copy())

        # Sig til brugeren hvis der ingen dominerede strategier var
        if P1e.shape == P1.shape and P2e.shape == P2.shape:
            messagebox.showinfo("Info", "Ingen strategier blev elimineret ved itereret dominans.")

        # Plot matricerne
        self.plotFrame.clear()
        ax1 = self.plotFrame.fig.add_subplot(1,2,1)
        ax2 = self.plotFrame.fig.add_subplot(1,2,2)

        ax1.imshow(P1e, cmap="viridis")
        ax2.imshow(P2e, cmap="plasma")

        # tegn udbytte i matricerne
        for i in range(P1e.shape[0]):
            for j in range(P1e.shape[1]):
                ax1.text(j, i, f"{P1e[i, j]:.1f}", ha="center", va="center", color="black")
                ax2.text(j, i, f"{P2e[i, j]:.1f}", ha="center", va="center", color="black")

        ax1.set_title("Efter itereret elimination (P1)")
        ax2.set_title("Efter itereret elimination (P2)")

        self.plotFrame.fig.tight_layout()
        self.plotFrame.draw()

    def eliminate_dominated(self, P1, P2, mode="strict"):
        """
        Perform iterated elimination of dominated strategies.
        P1: payoff matrix for Player 1 (rows = P1 strategies, columns = P2 strategies)
        P2: payoff matrix for Player 2 (same size as P1)
        mode: "strict" or "weak"
        """

        def row_dominated(i, k, P):
            """
            Is row i dominated by row k in matrix P?
            """
            row_i = P[i, :]
            row_k = P[k, :]

            ge = np.all(row_k >= row_i)
            gt = np.any(row_k > row_i)

            if mode == "strict":
                return ge and gt
            else:  # weak
                return ge and gt  # (same logic, but IEWDS may eliminate more through iteration)

        def col_dominated(j, l, P):
            """
            Is column j dominated by column l in matrix P?
            """
            col_j = P[:, j]
            col_l = P[:, l]

            ge = np.all(col_l >= col_j)
            gt = np.any(col_l > col_j)

            if mode == "strict":
                return ge and gt
            else:  # weak
                return ge and gt

        changed = True
        while changed:
            changed = False
            rows_to_delete = set()
            cols_to_delete = set()

            # --- Check Player 1 dominated rows (use P1) ---
            n_rows = P1.shape[0]
            for i in range(n_rows):
                for k in range(n_rows):
                    if i == k:
                        continue
                    if row_dominated(i, k, P1):
                        rows_to_delete.add(i)
                        break

            # --- Check Player 2 dominated columns (use P2) ---
            n_cols = P2.shape[1]
            for j in range(n_cols):
                for l in range(n_cols):
                    if j == l:
                        continue
                    if col_dominated(j, l, P2):
                        cols_to_delete.add(j)
                        break

            # --- Delete rows first ---
            if rows_to_delete:
                P1 = np.delete(P1, sorted(rows_to_delete), axis=0)
                P2 = np.delete(P2, sorted(rows_to_delete), axis=0)
                changed = True

            # --- Then delete columns ---
            if cols_to_delete:
                P1 = np.delete(P1, sorted(cols_to_delete), axis=1)
                P2 = np.delete(P2, sorted(cols_to_delete), axis=1)
                changed = True

        return P1, P2
