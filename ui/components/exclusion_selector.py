import tkinter as tk
from typing import List

import customtkinter as ctk

from models.exercices import Exercise


class ExclusionSelector(ctk.CTkFrame):
    def __init__(self, master, all_exercices: List[Exercise], excluded_ids: List[int]):
        super().__init__(master)
        self.available = [e for e in all_exercices if e.id not in excluded_ids]
        self.excluded = [e for e in all_exercices if e.id in excluded_ids]

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        left = ctk.CTkFrame(self)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(left, text="Exercices Disponibles").pack()
        self.search_left = ctk.CTkEntry(left)
        self.search_left.pack(fill="x", padx=5, pady=(5, 5))
        self.list_left = tk.Listbox(left, selectmode=tk.SINGLE)
        self.list_left.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        center = ctk.CTkFrame(self)
        center.grid(row=0, column=1, padx=5, pady=5, sticky="ns")
        ctk.CTkButton(center, text=">", width=40, command=self.add, font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"])).pack(pady=(40, 5))
        ctk.CTkButton(center, text="<", width=40, command=self.remove, font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"])).pack()

        right = ctk.CTkFrame(self)
        right.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        ctk.CTkLabel(right, text="Exercices Exclus").pack()
        self.search_right = ctk.CTkEntry(right)
        self.search_right.pack(fill="x", padx=5, pady=(5, 5))
        self.list_right = tk.Listbox(right, selectmode=tk.SINGLE)
        self.list_right.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        self.search_left.bind("<KeyRelease>", lambda e: self._refresh())
        self.search_right.bind("<KeyRelease>", lambda e: self._refresh())
        self._refresh()

    def _filtered_available(self) -> List[Exercise]:
        term = self.search_left.get().lower()
        return [e for e in self.available if term in e.nom.lower()]

    def _filtered_excluded(self) -> List[Exercise]:
        term = self.search_right.get().lower()
        return [e for e in self.excluded if term in e.nom.lower()]

    def _refresh(self):
        self.list_left.delete(0, tk.END)
        for ex in self._filtered_available():
            self.list_left.insert(tk.END, f"{ex.nom}")
        self.list_right.delete(0, tk.END)
        for ex in self._filtered_excluded():
            self.list_right.insert(tk.END, f"{ex.nom}")

    def add(self):
        sel = self.list_left.curselection()
        if not sel:
            return
        ex = self._filtered_available()[sel[0]]
        self.available.remove(ex)
        self.excluded.append(ex)
        self._refresh()

    def remove(self):
        sel = self.list_right.curselection()
        if not sel:
            return
        ex = self._filtered_excluded()[sel[0]]
        self.excluded.remove(ex)
        self.available.append(ex)
        self._refresh()

    def get_excluded_ids(self) -> List[int]:
        return [e.id for e in self.excluded]

