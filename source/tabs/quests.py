import tkinter as tk
from tkinter import ttk
from state import AppState
from constants import (QUESTS)

class QuestsTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="Quests").grid(
            row=0, column=0, sticky="w", padx=10, pady=5
        )

        # === Scrollable Canvas ===
        canvas = tk.Canvas(self, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=canvas.yview)

        scrollable = ttk.Frame(canvas)
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # === Mouse wheel support ===

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # === Toggle helper ===

        def toggle_frame(frame, label=None, title=None):
            if frame.winfo_viewable():
                frame.grid_remove()
                if label and title:
                    label.config(text=f"▶ {title}")
            else:
                frame.grid()
                if label and title:
                    label.config(text=f"▼ {title}")

        # === Build Quest Log ===
        row = 0

        for world, quests in QUESTS.items():
            # ----- World header -----
            world_lbl = ttk.Label(
                scrollable,
                text=f"▶ {world}",
                cursor="hand2",
                font=("Segoe UI", 10, "bold")
            )
            world_lbl.grid(row=row, column=0, sticky="w", padx=15, pady=4)
            row += 1

            world_frame = ttk.Frame(scrollable)
            world_frame.grid(row=row, column=0, sticky="w", padx=30)
            # collapsed by default # world_frame.grid_remove() to collapse
            world_frame.grid_remove()
            world_lbl.bind(
                "<Button-1>",
                lambda e, f=world_frame, l=world_lbl, t=world: toggle_frame(
                    f, l, t)
            )
            row += 1
            qrow = 0

            for quest_name, data in quests.items():
                # ----- Quest header -----
                quest_lbl = ttk.Label(
                    world_frame,
                    text=f"▶ {quest_name}",
                    cursor="hand2",
                    font=("Segoe UI", 9, "bold")
                )
                quest_lbl.grid(row=qrow, column=0, sticky="w", padx=5, pady=2)

                quest_frame = ttk.Frame(world_frame)
                quest_frame.grid(row=qrow+1, column=0, sticky="w", padx=20)
                # collapsed by default  # quest_frame.grid_remove() to collapse
                quest_frame.grid_remove()
                quest_lbl.bind(
                    "<Button-1>",
                    lambda e, f=quest_frame, l=quest_lbl, t=quest_name: toggle_frame(
                        f, l, t)
                )
                qrow += 2

                # ----- Status -----
                status_var = tk.StringVar(value="❌ Not Started")
                # Quests Flags
                if "flags" in data:
                    flags = data["flags"]

                    def make_flag_updater(s=status_var, f=flags):
                        def inner(*_):
                            accomplished = AppState.quest_flags

                            started = f.get("started", [])
                            completed = f.get("completed", [])

                            if completed and all(flag in accomplished for flag in completed):
                                s.set("✅ Completed")
                            elif any(flag in accomplished for flag in started):
                                s.set("▶ In Progress")
                            else:
                                s.set("❌ Not Started")

                        AppState.quest_flags_var.trace_add("write", lambda *args: inner())
                        inner()

                    make_flag_updater()

                ttk.Label(quest_frame, textvariable=status_var).grid(
                    row=0, column=0, sticky="w", pady=(0, 2))

                # ----- Description -----
                ttk.Label(
                    quest_frame,
                    text=f"Description: {data.get('description') or 'N/A'}",
                    wraplength=550
                ).grid(row=1, column=0, sticky="w")

                # ----- How to complete -----
                ttk.Label(
                    quest_frame,
                    text=f"How to complete: {data.get('how_to_complete') or 'N/A'}",
                    wraplength=550
                ).grid(row=2, column=0, sticky="w", pady=(2, 2))

                # ----- Reward -----
                ttk.Label(
                    quest_frame,
                    text=f"Reward: {data.get('reward') or 'N/A'}",
                    wraplength=550
                ).grid(row=3, column=0, sticky="w", pady=(2, 2))