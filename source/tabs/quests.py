import tkinter as tk
from tkinter import ttk
from state import AppState
from quests_info import (QUESTS)

class QuestsTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="Quests").grid(
            row=0, column=0, sticky="w", padx=10, pady=5
        )

        quest_summary_var = tk.StringVar(
            value="Completed: 0 / 0    In Progress: 0    Not Started: 0"
        )

        ttk.Label(self, textvariable=quest_summary_var).grid(
            row=0, column=0, sticky="e", padx=10, pady=5
        )

        # === Scrollable Canvas ===
        style = ttk.Style()
        clam_bg = style.lookup("TFrame", "background")

        canvas = tk.Canvas(
            self,
            highlightthickness=0,
            bg=clam_bg
        )
        scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=canvas.yview)

        scrollable = ttk.Frame(canvas)
        scrollable.columnconfigure(0, weight=1)
        scrollable.bind(
            "<Configure>",
            lambda e: update_scrollregion()
        )

        canvas_window = canvas.create_window((0, 0), window=scrollable, anchor="nw")

        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

        canvas.configure(yscrollcommand=scrollbar.set)

        # === Update Scroll Region ===
        def update_scrollregion():
            scrollable.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))


        canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # === Mouse wheel support ===

        def _on_mousewheel(event):
            first, last = canvas.yview()

            if first > 0.0 or last < 1.0:
                canvas.yview_scroll(
                    int(-1 * (event.delta / 120)),
                    "units"
                )

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

            update_scrollregion()

        # === Build Quest Log ===
        total_quests = sum(len(quests) for quests in QUESTS.values())

        def update_quest_summary():
            completed = 0
            in_progress = 0
            not_started = 0

            accomplished = AppState.quest_flags

            for world, quests in QUESTS.items():
                for quest_name, data in quests.items():
                    flags = data.get("flags", {})

                    started = flags.get("started", [])
                    completed_flags = flags.get("completed", [])

                    if completed_flags and all(
                        flag in accomplished for flag in completed_flags
                    ):
                        completed += 1
                    elif any(flag in accomplished for flag in started):
                        in_progress += 1
                    else:
                        not_started += 1

            quest_summary_var.set(
                f"Completed: {completed} / {total_quests}    "
                f"In Progress: {in_progress}    "
                f"Not Started: {not_started}"
            )

        update_quest_summary()

        row = 0

        for world, quests in QUESTS.items():
            # ----- World header -----
            world_lbl = ttk.Label(
                scrollable,
                text=world,
                font=("Segoe UI", 10, "bold")
            )
            world_lbl.grid(
                row=row,
                column=0,
                sticky="w",
                padx=15,
                pady=(8, 4)
            )
            row += 1

            for quest_name, data in quests.items():
                # ----- Quest header -----
                quest_lbl = ttk.Label(
                    scrollable,
                    text=f"▶ {quest_name}",
                    cursor="hand2",
                    font=("Segoe UI", 9, "bold")
                )
                quest_lbl.grid(
                    row=row,
                    column=0,
                    sticky="w",
                    padx=30,
                    pady=2
                )

                # ----- Status -----
                status_var = tk.StringVar(value="❌ Not Started")

                status_lbl = ttk.Label(
                    scrollable,
                    textvariable=status_var
                )
                status_lbl.grid(
                    row=row,
                    column=1,
                    sticky="e",
                    padx=30,
                    pady=2
                )

                quest_frame = ttk.Frame(scrollable)
                quest_frame.grid(
                    row=row + 1,
                    column=0,
                    sticky="w",
                    padx=50
                )

                # Collapsed by default
                quest_frame.grid_remove()

                quest_lbl.bind(
                    "<Button-1>",
                    lambda e, f=quest_frame, l=quest_lbl, t=quest_name:
                        toggle_frame(f, l, t)
                )

                row += 2

                # Quests Flags
                if "flags" in data:
                    flags = data["flags"]

                    def make_flag_updater(s=status_var, f=flags):
                        def inner(*_):
                            accomplished = AppState.quest_flags

                            started = f.get("started", [])
                            completed = f.get("completed", [])

                            if completed and all(
                                flag in accomplished for flag in completed
                            ):
                                s.set("✅ Completed")
                            elif any(
                                flag in accomplished for flag in started
                            ):
                                s.set("▶ In Progress")
                            elif not started and not completed:
                                s.set("📝 TODO")
                            else:
                                s.set("❌ Not Started")

                        def on_flags_changed(*_):
                            inner()
                            update_quest_summary()

                        AppState.quest_flags_var.trace_add(
                            "write",
                            on_flags_changed
                        )

                        inner()

                    make_flag_updater()

                # ----- Description -----
                ttk.Label(
                    quest_frame,
                    text=f"{data.get('description') or 'N/A'}",
                    wraplength=550
                ).grid(row=0, column=0, sticky="w")

                # ----- How to complete -----
                how_to_frame = ttk.Frame(quest_frame)

                how_to_label = ttk.Label(
                    quest_frame,
                    text="▶ How to complete",
                    cursor="hand2",
                    font=("Segoe UI", 9, "bold")
                )
                how_to_label.grid(
                    row=1,
                    column=0,
                    sticky="w",
                    pady=(4, 2)
                )

                how_to_frame.grid(
                    row=2,
                    column=0,
                    sticky="w",
                    padx=20
                )

                how_to_frame.grid_remove()

                how_to_label.bind(
                    "<Button-1>",
                    lambda e, f=how_to_frame, l=how_to_label:
                        toggle_frame(f, l, "How to complete")
                )

                how_to_steps = data.get("how_to_complete") or []

                if how_to_steps:
                    for step_index, step in enumerate(how_to_steps):
                        ttk.Label(
                            how_to_frame,
                            text=f"• {step}",
                            wraplength=550
                        ).grid(
                            row=step_index,
                            column=0,
                            sticky="w",
                            pady=1
                        )
                else:
                    ttk.Label(
                        how_to_frame,
                        text="N/A"
                    ).grid(
                        row=0,
                        column=0,
                        sticky="w"
                    )

                # ----- Reward -----
                ttk.Label(
                    quest_frame,
                    text=f"Reward: {data.get('reward') or 'N/A'}",
                    wraplength=550
                ).grid(
                    row=3,
                    column=0,
                    sticky="w",
                    pady=(2, 2)
                )

        update_scrollregion()