# ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import saveio
from constants import THEMES, NAMES, COSTUME_OPTIONS, CARD_NAMES, BATTLE_ITEM_NAMES, WORLD_PATHS

# keep a module-level theme name
_current_theme_name = "light"

def current_theme():
    return THEMES[_current_theme_name]

def apply_theme(root, theme_name):
    global _current_theme_name
    _current_theme_name = theme_name
    theme = THEMES[theme_name]
    style = ttk.Style()
    style.theme_use(theme["style_theme"])

    style.configure("TNotebook", background=theme.get("notebook_bg", theme["bg"]), borderwidth=0)
    style.configure("TNotebook.Tab",
                    background=theme["tab_bg"],
                    foreground=theme["tab_fg"],
                    padding=6)
    style.map("TNotebook.Tab",
              background=[("selected", theme["tab_selected_bg"])],
              foreground=[("selected", theme["tab_selected_fg"])])
    style.configure("TFrame", background=theme["bg"])
    style.configure("TLabel", background=theme["bg"], foreground=theme["fg"])
    style.configure("TEntry",
                    fieldbackground=theme["entry_bg"],
                    foreground=theme["entry_fg"],
                    background=theme["entry_bg"])
    root.configure(bg=theme["bg"])
    root.set_theme(theme["root_theme"])

def toggle_theme(root):
    apply_theme(root, "dark" if _current_theme_name == "light" else "light")

# ---------- small widgets ----------
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        try:
            x, y, cx, cy = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 20
            y += self.widget.winfo_rooty() + 10
        except Exception:
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + 10
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

def create_vector_editor(parent, label_text, variables, state="normal"):
    frame = ttk.Frame(parent)
    frame.columnconfigure(1, weight=1)
    ttk.Label(frame, text=label_text).grid(row=0, column=0, sticky="w", padx=(10, 5))
    for i, (axis, var) in enumerate(zip(["X", "Y", "Z"], variables)):
        ttk.Label(frame, text=f"{axis}:").grid(row=i + 1, column=0, padx=10, pady=2, sticky="e")
        ttk.Entry(frame, textvariable=var, state=state).grid(row=i + 1, column=1, padx=5, pady=2, sticky="we")
    return frame

# ---------- UI builder ----------
def create_menu(root, frames_refs):
    theme = THEMES[_current_theme_name]

    def make_menu(parent):
        return tk.Menu(parent,
                       background=theme["menu_bg"],
                       foreground=theme["menu_fg"],
                       activebackground=theme["menu_active_bg"],
                       activeforeground=theme["menu_active_fg"],
                       tearoff=0)

    menu_bar = make_menu(root)

    file_menu = make_menu(menu_bar)
    file_menu.add_command(label="Open", command=lambda: _open_and_fill(frames_refs))
    file_menu.add_command(label="Save", command=lambda: saveio.save_changes(frames_refs["Cards"].entries, frames_refs["Battle Stamps"].entries))
    file_menu.add_command(label="Save As...", command=lambda: saveio.save_as(frames_refs["Cards"].entries, frames_refs["Battle Stamps"].entries))
    file_menu.add_command(label="Backup Save File", command=saveio.backup_save)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    options_menu = make_menu(menu_bar)
    options_menu.add_command(label="Toggle Light/Dark Mode", command=lambda: toggle_theme(root))
    menu_bar.add_cascade(label="Options", menu=options_menu)

    help_menu = make_menu(menu_bar)
    help_menu.add_command(
        label="How to Use",
        command=lambda: messagebox.showinfo(
            "How to Use",
            "Use the main tabs to navigate. Use the dropdown tabs/textboxes to edit save file information.\n\n"
            "'File Options'\n\n"
            "'Open' - Open existing save file.\n\n"
            "'Save' - Save changes to current save.\n\n"
            "'Save As...' - Choose where to save your file.\n(Try saving as a .json or .txt)\n\n"
            "'Backup Save File' - Makes a backup of currently loaded save."
        )
    )
    help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Costume Quest PC Save Editor\nAlpha Version by DeathMaster001"))
    menu_bar.add_cascade(label="Help", menu=help_menu)

    root.config(menu=menu_bar)

def _open_and_fill(frames_refs):
    ok = saveio.open_save_dialog()
    if not ok:
        return
    saveio.populate_entries_from_state(frames_refs["Cards"].entries, frames_refs["Battle Stamps"].entries)
    if hasattr(frames_refs["Battle Stamps"], "update_progress"):
        frames_refs["Battle Stamps"].update_progress()
    if hasattr(frames_refs["100% Tracker"], "update_applebobbing_progress"):
        frames_refs["100% Tracker"].update_applebobbing_progress()

def create_tabs(root):
    notebook = ttk.Notebook(root)
    frames = {
        "Summary": ttk.Frame(notebook),
        "100% Tracker": ttk.Frame(notebook),
        "Stats & World": ttk.Frame(notebook),
        "Battle Stamps": ttk.Frame(notebook),
        "Cards": ttk.Frame(notebook),
        "Costumes": ttk.Frame(notebook),
        "Quests": ttk.Frame(notebook),
    }
    for name, frame in frames.items():
        notebook.add(frame, text=name)

    # ---------- Summary Frame ----------
    summary_frame = frames["Summary"]
    row = 0
    ttk.Label(summary_frame, text="Main Stats").grid(row=row, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(summary_frame, text="Misc. Stats").grid(row=row, column=2, sticky="w", padx=10, pady=5)
    row += 1

    #Summary Level
    ttk.Label(summary_frame, text="Level:").grid(row=row, column=0, sticky="w", padx=25)
    ttk.Label(summary_frame, textvariable=saveio.AppState.level_var, width=33).grid(row=row, column=1, padx=25)
    row += 1

    # Summary XP
    ttk.Label(summary_frame, text="Experience Points (XP):").grid(row=row, column=0, sticky="w", padx=25)
    ttk.Label(summary_frame, textvariable=saveio.AppState.xp_var, width=33).grid(row=row, column=1, padx=25)
    row += 1

    # Summary CurrentCandy
    ttk.Label(summary_frame, text="Current Candy:").grid(row=row, column=0, sticky="w", padx=25)
    ttk.Label(summary_frame, textvariable=saveio.AppState.candy_var, width=33).grid(row=row, column=1, padx=25)
    row += 1

    ttk.Label(summary_frame, text="Total Candy:").grid(row=row, column=0, sticky="w", padx=25)
    ttk.Label(summary_frame, textvariable=saveio.AppState.total_candy_var, width=33).grid(row=row, column=1, padx=25)
    row += 1

    # Summary Misc. Stats
    misc_stats = [
        ("Robot Ramp Jumps:", saveio.AppState.robotjumps_var),
        ("Monster Pail Bashes:", saveio.AppState.monsterbashes_var),
        ("Suburbs Bobbing High Score:", saveio.AppState.suburbsbobbing_var),
        ("Autumn Haven Mall Bobbing High Score:", saveio.AppState.mallbobbing_var),
        ("Fall Valley Bobbing High Score:", saveio.AppState.countrybobbing_var)
    ]
    row = 1
    for label_text, var in misc_stats:
        ttk.Label(summary_frame, text=label_text).grid(row=row, column=2, sticky="w", padx=25, pady=5)
        ttk.Label(summary_frame, textvariable=var, width=33, anchor="w").grid(row=row, column=3, sticky="w", padx=25, pady=5)
        row += 1

    ttk.Label(summary_frame, text="World:").grid(row=row, column=0, sticky="w", padx=25)
    ttk.Label(summary_frame, textvariable=saveio.AppState.selected_world, width=33).grid(row=row, column=1, padx=25)
    row += 1

    player_position_frame = create_vector_editor(summary_frame, "Player Position:", saveio.AppState.player_position_vars)
    player_position_frame.grid(row=row, column=0, columnspan=2, sticky="w", padx=25, pady=5)
    row += 2

    camera_position_frame = create_vector_editor(summary_frame, "Camera Position:", saveio.AppState.camera_position_vars)
    camera_position_frame.grid(row=row, column=0, columnspan=2, sticky="w", padx=25, pady=5)
    row += 1

    ttk.Label(summary_frame, text="Costumes:").grid(row=row, column=0, sticky="w", padx=25, pady=5)
    row += 1
    ttk.Label(summary_frame, text="Equipped Costumes:").grid(row=row, column=0, padx=35, pady=5)

    saveio.AppState.costume_display_vars = [tk.StringVar() for _ in NAMES]
    for i, name in enumerate(NAMES):
        if not saveio.AppState.costume_vars[i].get():
            saveio.AppState.costume_vars[i].set(COSTUME_OPTIONS[i])
        saveio.AppState.costume_display_vars[i].set(f"{name}: {saveio.AppState.costume_vars[i].get()}")
        ttk.Label(summary_frame, textvariable=saveio.AppState.costume_display_vars[i]).grid(
            row=row, column=1, padx=10, pady=5, sticky="w"
        )
        saveio.AppState.costume_vars[i].trace_add(
            "write",
            lambda *args, idx=i, nm=name: saveio.AppState.costume_display_vars[idx].set(
                f"{nm}: {saveio.AppState.costume_vars[idx].get()}"
            ),
        )
        row += 1

    # ---------- Stats & World Frame ----------
    stats_frame = frames["Stats & World"]
    ttk.Label(stats_frame, text="Stats").grid(row=row, column=0, sticky="w", padx=10, pady=5)
    row += 1

    ttk.Label(stats_frame, text="Level:").grid(row=row, column=0, sticky="w", padx=25, pady=5)
    level_dropdown = ttk.Combobox(
        stats_frame,
        textvariable=saveio.AppState.level_var,
        values=[""] + [str(i) for i in range(1, 11)],
        width=31,
        state="readonly",
    )
    level_dropdown.grid(row=row, column=1, sticky="w", padx=25, pady=5)
    for event in ("<<ComboboxSelected>>", "<FocusOut>", "<Return>"):
        level_dropdown.bind(event, saveio.update_xp_from_level)
    row += 1

    ttk.Label(stats_frame, text="Experience Points (XP):").grid(row=row, column=0, sticky="w", padx=25, pady=5)
    ttk.Entry(stats_frame, textvariable=saveio.AppState.xp_var, width=33).grid(row=row, column=1, padx=25, pady=5, sticky="w")
    row += 1

    ttk.Label(stats_frame, text="Current Candy:").grid(row=row, column=0, sticky="w", padx=25, pady=5)
    ttk.Entry(stats_frame, textvariable=saveio.AppState.candy_var, width=33).grid(row=row, column=1, padx=25, pady=5, sticky="w")
    row += 2

    ttk.Label(stats_frame, text="World and Position").grid(row=row, column=0, padx=10, pady=5, sticky="w")
    row += 1
    ttk.Label(stats_frame, text="World:").grid(row=row, column=0, padx=25, pady=5, sticky="w")
    ttk.Combobox(stats_frame, textvariable=saveio.AppState.selected_world, values=list(WORLD_PATHS.keys()), width=31, state="readonly").grid(row=row, column=1, padx=25, pady=5, sticky="w")
    row += 1

    player_position_frame2 = create_vector_editor(stats_frame, "Player Position:", saveio.AppState.player_position_vars)
    player_position_frame2.grid(row=row, column=0, columnspan=2, sticky="w", padx=40, pady=5)
    row += 1

    camera_position_frame2 = create_vector_editor(stats_frame, "Camera Position:", saveio.AppState.camera_position_vars)
    camera_position_frame2.grid(row=row, column=0, columnspan=2, sticky="w", padx=40, pady=5)

    # ---------- Costumes Frame ----------
    costumes_frame = frames["Costumes"]
    ttk.Label(costumes_frame, text="Equipped Costumes:").grid(row=0, column=0, padx=10, pady=5)
    for i, name in enumerate(NAMES):
        ttk.Label(costumes_frame, text=name).grid(row=i, column=1, padx=10, pady=5)
        ttk.Combobox(costumes_frame, textvariable=saveio.AppState.costume_vars[i], values=COSTUME_OPTIONS, width=30).grid(row=i, column=2, sticky="w", padx=10, pady=5)

    # ---------- Cards frame ----------
    cards_frame = frames["Cards"]
    cards_frame.entries = {}
    cards_per_col = 18
    for i in range(54):
        card_num = i + 1
        col = i // cards_per_col * 2
        row = (i % cards_per_col) + 1
        card_name = CARD_NAMES.get(card_num, f"Card {card_num}")
        label = ttk.Label(cards_frame, text=f"{card_name}")
        label.grid(row=row, column=col, sticky='e', padx=5, pady=2)
        entry = tk.Entry(cards_frame, width=8)
        entry.grid(row=row, column=col + 1, sticky='w', padx=5, pady=2)
        cards_frame.entries[card_num] = entry

    # ---------- Battle Stamps ----------
    battle_frame = frames["Battle Stamps"]
    battle_frame.entries = {}
    battle_frame.progress_var = tk.DoubleVar()
    battle_frame.toggle_all_var = tk.IntVar()

    def update_battle_item_progress():
        total = len(battle_frame.entries)
        collected = sum(1 for e in battle_frame.entries.values() if e.get().strip().isdigit() and int(e.get().strip()) > 0)
        percentage = (collected / total) * 100 if total > 0 else 0
        battle_frame.progress_var.set(percentage)
        if hasattr(battle_frame, "progress_label"):
            battle_frame.progress_label.config(text=f"Collected: {collected} / {total} ({percentage:.0f}%)")

    def toggle_all_battle_items():
        val = "1" if battle_frame.toggle_all_var.get() else "0"
        for entry in battle_frame.entries.values():
            entry.delete(0, tk.END)
            entry.insert(0, val)
        update_battle_item_progress()

    ttk.Checkbutton(battle_frame, text="Toggle All", variable=battle_frame.toggle_all_var, command=toggle_all_battle_items).grid(row=0, column=0, columnspan=4, pady=10)

    items_per_col = 9
    for i, (key, name) in enumerate(BATTLE_ITEM_NAMES.items()):
        col = (i // items_per_col) * 2
        row = (i % items_per_col) + 1
        ttk.Label(battle_frame, text=name).grid(row=row, column=col, sticky='e', padx=5, pady=2)
        entry = tk.Entry(battle_frame, width=8)
        entry.grid(row=row, column=col + 1, sticky='w', padx=5, pady=2)
        entry.bind("<KeyRelease>", lambda e: update_battle_item_progress())
        battle_frame.entries[key] = entry

    battle_frame.progress_label = ttk.Label(battle_frame, text="Collected: 0 / 0 (0%)")
    battle_frame.progress_label.grid(row=21, column=2, columnspan=4, sticky="w")
    battle_frame.progress = ttk.Progressbar(battle_frame, variable=battle_frame.progress_var, maximum=100, length=200)
    battle_frame.progress.grid(row=21, column=0, columnspan=2, padx=10, pady=10, sticky="w")
    battle_frame.update_progress = update_battle_item_progress

    # ---------- 100% tracker frame ----------
    tracker_frame = frames["100% Tracker"]
    ttk.Label(tracker_frame, text="Battle Stamps").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(tracker_frame, text="Costumes").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(tracker_frame, text="Creepy Treat Cards").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(tracker_frame, text="Level").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(tracker_frame, text="Quests").grid(row=4, column=0, sticky="w", padx=10, pady=5)

    bobbing_label = ttk.Label(tracker_frame, text="Apple Bobbing:")
    bobbing_label.grid(row=5, column=0, sticky="w", padx=25, pady=5)
    ToolTip(bobbing_label, "Complete 3 rounds of Apple Bobbing at each location, doing so will complete these quests!\nFirst 2 rounds give Candy, 3rd gives a Creepy Treat Card.")
    misc_stats1 = [
        ("Suburbs High Score:", saveio.AppState.suburbsbobbing_var),
        ("Autumn Haven Mall High Score:", saveio.AppState.mallbobbing_var),
        ("Fall Valley High Score:", saveio.AppState.countrybobbing_var),
    ]

    bobbing_thresholds = {
        "Suburbs High Score:": 30,
        "Autumn Haven Mall High Score:": 35,
        "Fall Valley High Score:": 40,
    }

    tracker_frame.applebobbing_entries = {}
    tracker_frame.progress_var = tk.DoubleVar()
    applebobbingprogress = ttk.Label(tracker_frame, text="Completed: 0 / 0 (0%)")
    applebobbingprogress.grid(row=6, column=0, columnspan=4, padx=40, pady=10, sticky="w")
    applebobbingprogressbar = ttk.Progressbar(tracker_frame, variable=tracker_frame.progress_var, maximum=100, length=200)
    applebobbingprogressbar.grid(row=6, column=1, columnspan=2, padx=40, pady=10, sticky="w")

    def update_applebobbing_progress():
        total = len(tracker_frame.applebobbing_entries)
        collected = sum(1 for var, threshold in tracker_frame.applebobbing_entries.values()
                if int(var.get() or 0) >= threshold)        
        percentage = (collected / total) * 100 if total > 0 else 0
        tracker_frame.progress_var.set(percentage)
        applebobbingprogress.config(text=f"Completed: {collected} / {total} ({percentage:.0f}%)")
    
    r = 7
    for label_text, var in misc_stats1:
        display_label = label_text.replace(" High Score:", "")
        ttk.Label(tracker_frame, text=display_label).grid(row=r, column=0, sticky="w", padx=40, pady=5)
        def make_status_var(v=var, threshold=bobbing_thresholds[label_text]):
            s = tk.StringVar()
            def update_status(*_):
                score = int(v.get() or 0)
                s.set("✅ Completed" if score >= threshold else "❌ Incomplete")
                update_applebobbing_progress()
            v.trace_add("write", update_status)
            update_status()
            return s
        
        status_var = make_status_var()
        ttk.Label(tracker_frame, textvariable=status_var).grid(row=r, column=2, sticky="w", padx=10, pady=5)
        tracker_frame.applebobbing_entries[label_text] = (var, bobbing_thresholds[label_text])
        r += 1
    # Initial update
    update_applebobbing_progress()

    # Quests tab placeholder
    ttk.Label(frames["Quests"], text="Not implemented yet.", anchor="center", justify="center").pack(expand=True, fill='both')

    # return the notebook and a map of frames so main can keep references
    frames["Cards"] = cards_frame
    frames["Battle Stamps"] = battle_frame
    frames["100% Tracker"] = tracker_frame
    return notebook, frames