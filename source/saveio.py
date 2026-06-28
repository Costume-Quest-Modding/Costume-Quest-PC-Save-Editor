import re
import shutil
from datetime import datetime
from tkinter import filedialog, messagebox
import tkinter as tk
import save_data
from save_data import extract_save_data, extract_quests, calculate_level_from_xp
from state import AppState
from constants import (
    XP_THRESHOLDS, WORLD_PATHS, CARD_PATTERN,
    BATTLE_ITEM_NAMES, BATTLE_ITEM_PATTERN
)

# ---------------- utility / parsing ----------------

def update_current_candy(text, new_value):
    "Update only the CurrentCandy field without touching other MaxCandyAmount fields."
    candy_matches = list(re.finditer(r"CandyAmount\s*=\s*(\d+);", text))
    if not candy_matches:
        # No CandyAmount found, append new field
        insert_point = text.find("EquippedCostumes=")
        new_line = f"CandyAmount={new_value};\n"
        if insert_point != -1:
            return text[:insert_point] + new_line + text[insert_point:]
        else:
            return text.strip() + "\n" + new_line

    # Replace only the last occurrence
    last_match = candy_matches[-1]
    start, end = last_match.span(1)  # only the number itself
    updated_text = text[:start] + str(new_value) + text[end:]
    return updated_text


def on_candy_change(*args):
    if AppState.loading_save:
        return
    try:
        new_candy = int(AppState.candy_var.get())
        delta = new_candy - AppState.original_candy_value
        total = int(AppState.total_candy_var.get()) + delta
        AppState.total_candy_var.set(str(total))
        total = max(0, total)
        AppState.total_candy_var.set(total)
        AppState.original_candy_value = new_candy
    except ValueError:
        pass


def update_xp_from_level(*args):
    try:
        level = int(AppState.level_var.get())
        xp = XP_THRESHOLDS.get(level, 0)
        AppState.xp_var.set(str(xp))
    except ValueError:
        AppState.level_var.set("")


def update_level_from_xp(*args):
    try:
        xp = int(AppState.xp_var.get())
        level = calculate_level_from_xp(xp)
        AppState.level_var.set(str(level))
    except ValueError:
        pass


# ---------------- file operations (UI calls these) ----------------


def open_save_dialog():
    """Open file dialog, read file, parse and populate AppState variables.
       Returns True on success, False otherwise."""
    path = filedialog.askopenfilename(
        title="Open Costume Quest Save File", filetypes=[("All Files", "*.*")])
    if not path:
        return False
    try:
        with open(path, "rb") as f:
            binary_data = f.read()
        header = binary_data[:8]
        raw = binary_data[8:]
        # decode whole raw text
        raw_text = raw.decode(errors="ignore")

        parsed = extract_save_data(raw_text)
    except Exception as e:
        messagebox.showerror("Load Error", f"Failed to parse save file:\n{e}")
        return False

    # set state
    AppState.loading_save = True
    AppState.total_candy_var.set(str(parsed.total_candy))
    AppState.candy_var.set(str(parsed.current_candy))
    AppState.original_candy_value = parsed.current_candy
    AppState.xp_var.set(str(parsed.experience_points))
    AppState.level_var.set(str(calculate_level_from_xp(parsed.experience_points)))
    AppState.robotjumps_var.set(str(parsed.robot_ramp_jumps))
    AppState.monsterbashes_var.set(str(parsed.monster_pail_bashes))
    AppState.suburbsbobbing_var.set(str(parsed.suburbs_bobbing_high_score))
    AppState.mallbobbing_var.set(str(parsed.mall_bobbing_high_score))
    AppState.countrybobbing_var.set(str(parsed.country_bobbing_high_score))
    # --- QUESTS ---
    AppState.quest_flags = extract_quests(raw_text)
    AppState.quest_flags_var.set(",".join(AppState.quest_flags))

    for i in range(3):
        AppState.costume_vars[i].set(parsed.equipped_costumes[i] if i < len(parsed.equipped_costumes) else "")
        AppState.player_position_vars[i].set(parsed.player_position[i])
        AppState.camera_position_vars[i].set(parsed.camera_position[i])

    # Debug prints
    print("Loaded Quest Flags:", AppState.quest_flags)

    AppState.selected_world.set(parsed.world)
    AppState.save_path.set(path)
    AppState.save_header = header
    AppState.save_text_data = raw_text
    AppState.loading_save = False
    return True

def build_save_text(text, AppState, cards_entries, battle_entries):
    text = save_data.replace_cards(text, cards_entries)
    text = save_data.replace_battle(text, battle_entries)
    text = save_data.replace_quests(text, AppState.quest_flags)

    text = save_data.update_save_data(
        text,
        AppState.selected_world.get(),
        new_level = int(AppState.level_var.get()),
        xp = int(AppState.xp_var.get()),
        new_candy = int(AppState.candy_var.get()),
        new_total = int(AppState.total_candy_var.get()),
        player_pos= tuple(v.get() for v in AppState.player_position_vars),
        camera_pos= tuple(v.get() for v in AppState.camera_position_vars),
        costumes = [v.get() for v in AppState.costume_vars],
        robotjumps = int(AppState.robotjumps_var.get()),
        monsterbashes = int(AppState.monsterbashes_var.get()),
        suburbsbobbing = int(AppState.suburbsbobbing_var.get()),
        mallbobbing = int(AppState.mallbobbing_var.get()),
        countrybobbing = int(AppState.countrybobbing_var.get()),
    )

    return text

def save_changes(AppState, cards_entries, battle_entries):
    path = AppState.save_path.get()
    if not path:
        messagebox.showerror("Error", "No save file loaded")
        return False

    try:
        updated = build_save_text(
            AppState.save_text_data,
            AppState,
            cards_entries,
            battle_entries
        )

        with open(path, "wb") as f:
            f.write(AppState.save_header)
            f.write(updated.encode("utf-8"))

        AppState.save_text_data = updated
        messagebox.showinfo("Saved", "Save file updated!")
        return True

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False


def save_as(AppState, cards_entries, battle_entries):
    if not AppState.save_text_data:
        messagebox.showerror("Error", "No save file loaded")
        return False

    path = filedialog.asksaveasfilename(
        defaultextension=".",
        filetypes=[("JSON", "*.json"), ("Plain Text", "*.txt"), ("All", "*.*")]
    )

    if not path:
        return False

    try:
        updated = build_save_text(
            AppState.save_text_data,
            AppState,
            cards_entries,
            battle_entries
        )

        if path.endswith(".json"):
            import json
            json.dump({
                "Level": int(AppState.level_var.get()),
                "ExperiencePoints": int(AppState.xp_var.get()),
                "CandyAmount": int(AppState.candy_var.get()),
                "TotalCandyAmount": int(AppState.total_candy_var.get()),
                "SelectedWorld": str(AppState.selected_world.get()),
                "PlayerPosition": [v.get() for v in AppState.player_position_vars],
                "CameraPosition": [v.get() for v in AppState.camera_position_vars],
                "EquippedCostumes": [v.get() for v in AppState.costume_vars],
                "RobotRampJumps": int(AppState.robotjumps_var.get()),
                "MonsterPailBashes": int(AppState.monsterbashes_var.get()),
                "SuburbsBobbingHighScore": int(AppState.suburbsbobbing_var.get()),
                "MallBobbingHighScore": int(AppState.mallbobbing_var.get()),
                "CountryBobbingHighScore": int(AppState.countrybobbing_var.get()),
            }, open(path, "w"), indent=4)

        elif path.endswith(".txt"):
            data = [
                f"Level: {AppState.level_var.get()}",
                f"Experience Points: {AppState.xp_var.get()}",
                f"Current Candy Amount: {AppState.candy_var.get()}",
                f"Total Candy Amount: {AppState.total_candy_var.get()}",
                f"Selected World: {AppState.selected_world.get()}",
                f"Player Position: {[v.get() for v in AppState.player_position_vars]}",
                f"Camera Position: {[v.get() for v in AppState.camera_position_vars]}",
                f"Equipped Costumes: {', '.join(v.get() for v in AppState.costume_vars)}",
                f"Robot Ramp Jumps: {AppState.robotjumps_var.get()}",
                f"Monster Pail Bashes: {AppState.monsterbashes_var.get()}",
                f"Suburbs Bobbing High Score: {AppState.suburbsbobbing_var.get()}",
                f"Mall Bobbing High Score: {AppState.mallbobbing_var.get()}",
                f"Country Bobbing High Score: {AppState.countrybobbing_var.get()}",
            ]
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(data))

        else:
            with open(path, "wb") as f:
                f.write(AppState.save_header)
                f.write(updated.encode("utf-8"))

        messagebox.showinfo("Success", f"File successfully saved to {path}")
        return True

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save: {e}")
        return False


def backup_save():
    path = AppState.save_path.get()
    if not path:
        messagebox.showerror("Error", "No save file loaded")
        return False

    try:
        backup_path = f"{path}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(path, backup_path)
        messagebox.showinfo("Backup Created", f"Backup saved as:{backup_path}")
        return True
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False

def populate_entries_from_state(cards_entries, battle_entries):
    if not AppState.save_text_data:
        return

    AppState.loading_save = True  # prevent trace updates

    # --- Update battle items ---
    battle_frame_ref = None
    for match in BATTLE_ITEM_PATTERN.finditer(AppState.save_text_data):
        stamp_num = match.group(2)
        current_amount = match.group(3)
        if stamp_num in battle_entries:
            entry = battle_entries[stamp_num]
            entry.delete(0, tk.END)
            entry.insert(0, current_amount)
            if not battle_frame_ref:
                battle_frame_ref = entry.master  # assign the parent frame

    # --- update the progress bar directly ---
    if battle_frame_ref and hasattr(battle_frame_ref, "update_progress"):
        battle_frame_ref.update_progress()

    # force update missing battle stamps after loading
    if battle_frame_ref and hasattr(battle_frame_ref, "update_missing_stamps"):
        battle_frame_ref.update_missing_stamps()

    # --- Update cards ---
    cards_frame_ref = None
    for match in CARD_PATTERN.finditer(AppState.save_text_data):
        card_num = int(match.group(2))
        current_amount = int(match.group(3))
        if card_num in cards_entries:
            entry = cards_entries[card_num]
            entry.delete(0, tk.END)
            entry.insert(0, str(current_amount))
            # store a reference to the parent frame
            if not cards_frame_ref:
                cards_frame_ref = entry.master

        if card_num in AppState.card_vars:
            AppState.card_vars[card_num].set(1 if current_amount > 0 else 0)

    # trigger variable traces
    for var in AppState.card_vars.values():
        var.set(var.get())

    AppState.loading_save = False

    # --- update the progress bar directly ---
    if cards_frame_ref and hasattr(cards_frame_ref, "update_progress"):
        cards_frame_ref.update_progress()

    # force update missing cards after loading
    if cards_frame_ref and hasattr(cards_frame_ref, "update_missing_cards"):
        cards_frame_ref.update_missing_cards()