import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from frames.scenarie_base import ScenarieFrame

class Scenarie1(ScenarieFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Iterated Elimination")

        frame = self.body
        ttk.Label(frame, text="Skriv 2x2 udbytte (format: 'P1 P2')").pack(anchor="w")

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

        extra = ttk.Frame(frame)
        extra.pack(anchor="w", pady=4)
        self.extra_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(extra, text="Inkluder extra række",
                        variable=self.extra_var).pack(side="left")

        self.extra_entries = [ttk.Entry(frame, width=12), ttk.Entry(frame, width=12)]
        self.extra_entries[0].insert(0, "0 0")
        self.extra_entries[1].insert(0, "0 0")
        self.extra_entries[0].pack(anchor="w")
        self.extra_entries[1].pack(anchor="w")

        btns = ttk.Frame(frame)
        btns.pack(pady=5)

        ttk.Button(btns, text="Plot udbyttematrix", command=self.plot_matrices).pack(side="left", padx=4)
        ttk.Button(btns, text="Plot efter elimination", command=self.plot_elimination).pack(side="left", padx=4)

    def read_matrix(self):
        try:
            P1 = np.zeros((2,2))
            P2 = np.zeros((2,2))

            for i in range(2):
                for j in range(2):
                    p = self.entries[i][j].get().split()
                    if len(p) < 2:
                        raise ValueError("Each cell must contain two numbers: 'P1 P2'")
                    P1[i,j] = float(p[0])
                    P2[i,j] = float(p[1])

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

    def plot_matrices(self):
        P1, P2 = self.read_matrix()
        if P1 is None:
            return

        self.plotFrame.clear()
        ax1 = self.plotFrame.fig.add_subplot(1,2,1)
        ax2 = self.plotFrame.fig.add_subplot(1,2,2)

        ax1.imshow(P1, cmap="viridis")
        ax2.imshow(P2, cmap="plasma")

        for i in range(P1.shape[0]):
            for j in range(P1.shape[1]):
                ax1.text(j, i, f"{P1[i, j]:.1f}", ha="center", va="center", color="black")
                ax2.text(j, i, f"{P2[i, j]:.1f}", ha="center", va="center", color="black")

        ax1.set_title("P1 udbytte")
        ax2.set_title("P2 udbytte")

        self.plotFrame.fig.tight_layout()
        self.plotFrame.draw()

    def plot_elimination(self):
        P1, P2 = self.read_matrix()
        if P1 is None:
            return

        # Run iterated elimination
        P1e, P2e = self.eliminate_dominated(P1.copy(), P2.copy())

        # If nothing removed, inform user
        if P1e.shape == P1.shape and P2e.shape == P2.shape:
            messagebox.showinfo("Info", "Ingen strategier blev elimineret ved itereret dominans.")
        # Plot the reduced matrices (even if unchanged)
        self.plotFrame.clear()
        ax1 = self.plotFrame.fig.add_subplot(1,2,1)
        ax2 = self.plotFrame.fig.add_subplot(1,2,2)

        ax1.imshow(P1e, cmap="viridis")
        ax2.imshow(P2e, cmap="plasma")

        for i in range(P1e.shape[0]):
            for j in range(P1e.shape[1]):
                ax1.text(j, i, f"{P1e[i, j]:.1f}", ha="center", va="center", color="black")
                ax2.text(j, i, f"{P2e[i, j]:.1f}", ha="center", va="center", color="black")

        ax1.set_title("Efter itereret elimination (P1)")
        ax2.set_title("Efter itereret elimination (P2)")

        self.plotFrame.fig.tight_layout()
        self.plotFrame.draw()

    def eliminate_dominated(self, P1, P2):
        """
        Iterated elimination of (weakly) dominated strategies.
        We remove strictly-or-weakly dominated rows for P1 and columns for P2.
        A row i is dominated by row k if P1[k, j] >= P1[i, j] for all j and >
        for at least one j. Similar for columns (compare column vectors of P2).
        """
        changed = True
        # We'll loop until no deletions occur
        while changed:
            changed = False

            rows_to_delete = set()
            cols_to_delete = set()

            # Check dominated rows for Player 1
            n_rows = P1.shape[0]
            for i in range(n_rows):
                for k in range(n_rows):
                    if i == k:
                        continue
                    # row k dominates row i?
                    ge = np.all(P1[k, :] >= P1[i, :])   # >= for all columns
                    gt = np.any(P1[k, :] > P1[i, :])    # strictly greater for at least one
                    if ge and gt:
                        rows_to_delete.add(i)
                        break  # no need to check other k's for this i

            # Check dominated columns for Player 2
            n_cols = P2.shape[1]
            for j in range(n_cols):
                for l in range(n_cols):
                    if j == l:
                        continue
                    # column l dominates column j?
                    ge = np.all(P2[:, l] >= P2[:, j])  # >= for all rows
                    gt = np.any(P2[:, l] > P2[:, j])   # strictly greater for >= one
                    if ge and gt:
                        cols_to_delete.add(j)
                        break

            # If there are deletions, apply them (delete rows first then columns).
            # Use sorted lists to have deterministic behavior.
            if rows_to_delete:
                # np.delete accepts list of indices
                P1 = np.delete(P1, sorted(rows_to_delete), axis=0)
                P2 = np.delete(P2, sorted(rows_to_delete), axis=0)
                changed = True

            if cols_to_delete:
                P1 = np.delete(P1, sorted(cols_to_delete), axis=1)
                P2 = np.delete(P2, sorted(cols_to_delete), axis=1)
                changed = True

        return P1, P2
