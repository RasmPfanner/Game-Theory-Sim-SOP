import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from frames.scenarie_base import ScenarieFrame

class Scenarie2(ScenarieFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller,
                         "2A — Mixed strategy sensitivity")

        frame = self.body

        # tekst over inputfelter
        ttk.Label(frame, text="Enter Player 1 payoffs (a,b,c,d):").pack(anchor="w")
        row = ttk.Frame(frame); row.pack()

        # inputfelter
        self.a = ttk.Entry(row, width=8); self.a.insert(0,"3")
        self.b = ttk.Entry(row, width=8); self.b.insert(0,"1")
        self.c = ttk.Entry(row, width=8); self.c.insert(0,"0")
        self.d = ttk.Entry(row, width=8); self.d.insert(0,"2")

        self.a.pack(side="left", padx=3)
        self.b.pack(side="left", padx=3)
        self.c.pack(side="left", padx=3)
        self.d.pack(side="left", padx=3)

        # tekst og dropdown menu
        ttk.Label(frame, text="Sweep payoff:").pack(anchor="w", pady=(8,0))
        self.sweep_var = tk.StringVar(value="b")
        ttk.Combobox(frame, values=["a","b","c","d"], textvariable=self.sweep_var,
                     width=5).pack(anchor="w")

        ttk.Label(frame, text="Range (min,max,steps):").pack(anchor="w", pady=(8,0))
        r = ttk.Frame(frame); r.pack()
        self.tmin = ttk.Entry(r, width=8); self.tmin.insert(0,"-1")
        self.tmax = ttk.Entry(r, width=8); self.tmax.insert(0,"3")
        self.tsteps = ttk.Entry(r, width=8); self.tsteps.insert(0,"150")

        self.tmin.pack(side="left", padx=2)
        self.tmax.pack(side="left", padx=2)
        self.tsteps.pack(side="left", padx=2)

        # knap der kører plot_curve metode
        ttk.Button(frame, text="Plot p*(q*) vs parameter",
                   command=self.plot_curve).pack(pady=6)

    # metode til at vise den varierede parameter
    def plot_curve(self):
        # henter de forskellige parametrer og grafintervallet
        try:
            a = float(self.a.get())
            b = float(self.b.get())
            c = float(self.c.get())
            d = float(self.d.get())
            key = self.sweep_var.get()
            tmin = float(self.tmin.get())
            tmax = float(self.tmax.get())
            steps = int(self.tsteps.get())
        except Exception as ex:
            messagebox.showerror("Error", ex)
            return

        # array der holder alle punkterne
        ts = np.linspace(tmin, tmax, steps)
        p_vals = np.full_like(ts, np.nan)
        q_vals = np.full_like(ts, np.nan)

        # laver lokale kopier af parametrerne. Sammenligner disse med den valgte parameter
        for i, t in enumerate(ts):
            aa, bb, cc, dd = a,b,c,d
            if key == "a": aa = t
            elif key == "b": bb = t
            elif key == "c": cc = t
            elif key == "d": dd = t

            # nævner i funktionen
            denom_p = aa - bb - cc + dd
            denom_q = aa - cc - bb + dd

            # funktionsforskrifterne
            p_vals[i] = (dd - bb) / denom_p if denom_p != 0 else np.nan
            q_vals[i] = (dd - cc) / denom_q if denom_q != 0 else np.nan

        self.plotFrame.clear()
        ax = self.plotFrame.fig.add_subplot(1,1,1)
        ax.plot(ts, p_vals, label="p* (P2 mixes)")
        ax.plot(ts, q_vals, label="q* (P1 mixes)")
        ax.set_xlabel(key)
        ax.set_ylabel("Mixing probability")
        ax.legend()
        ax.grid()

        self.plotFrame.fig.tight_layout()
        self.plotFrame.draw()
