import re
import shutil
from datetime import datetime
from tkinter import filedialog, messagebox
from save_state import AppState
from constants import WORLD_PATHS, BATTLE_ITEM_NAMES


# ---------------- helpers ----------------

def get_level_path_from_selected_world(AppState):
    world_name = AppState.selected_world.get()
    return WORLD_PATHS.get(world_name, WORLD_PATHS["Suburbs"])


def update_or_add_field(text, field_name, new_value):
    is_vector = field_name in ["PlayerPosition", "CameraPosition"]

    if is_vector and isinstance(new_value, (tuple, list)):
        value_str = f"<{new_value[0]},{new_value[1]},{new_value[2]}>"
        pattern = fr"{field_name}=<[-.\d]+,[-.\d]+,[-.\d]+>"
        replacement = f"{field_name}={value_str}"

    elif isinstance(new_value, (int, float)):
        value_str = str(new_value)
        if not value_str.endswith(";"):
            value_str += ";"
        pattern = fr"{field_name}\s*=\s*-?\d+(?:\.\d+)?;"
        replacement = f"{field_name}={value_str}"

    else:
        value_str = str(new_value)
        if not value_str.endswith(";"):
            value_str += ";"
        pattern = fr"{field_name}\s*=\s*.*?;"
        replacement = f"{field_name}={value_str}"

    if re.search(pattern, text):
        return re.sub(pattern, replacement, text, count=1)

    insert_point = text.find("EquippedCostumes=")
    insert_text = replacement + "\n"

    if insert_point != -1:
        return text[:insert_point] + insert_text + text[insert_point:]

    return text.strip() + "\n" + insert_text


def update_save_data(
    text,
    AppState,
    new_level,
    xp,
    new_candy,
    new_total,
    player_pos,
    camera_pos,
    costumes,
    robotjumps,
    monsterbashes,
    suburbsbobbing,
    mallbobbing,
    countrybobbing
):
    text = update_or_add_field(text, "Level", get_level_path_from_selected_world(AppState))
    text = update_or_add_field(text, "ExperiencePoints", xp)
    text = update_or_add_field(text, "CandyAmount", new_candy)
    text = update_or_add_field(text, "TotalCandyAmount", new_total)
    text = update_or_add_field(text, "PlayerPosition", player_pos)
    text = update_or_add_field(text, "CameraPosition", camera_pos)

    costume_str = ",".join(
        f"Costume_{c}" if not c.startswith("Costume_") else c
        for c in costumes if c
    )
    text = re.sub(
        r"EquippedCostumes=\[[^\]]*\];",
        f"EquippedCostumes=[{costume_str}];",
        text
    )

    text = update_or_add_field(text, "RobotRampJumos", robotjumps)
    text = update_or_add_field(text, "MonsterPailBashes", monsterbashes)
    text = update_or_add_field(text, "SuburbsBobbingHighScore", suburbsbobbing)
    text = update_or_add_field(text, "MallBobbingHighScore", mallbobbing)
    text = update_or_add_field(text, "CountryBobbingHighScore", countrybobbing)

    return text


# ---------------- inventory replacements ----------------

def replace_cards(text, cards_entries):
    updated = text
    for card_num, entry in cards_entries.items():
        val = entry.get().strip()
        if not val.isdigit():
            raise ValueError(f"Card {card_num} invalid value {val}")

        pattern = re.compile(
            rf'(TrickyTreatCard_{card_num}=InventoryItem\{{[^}}]*CurrentAmount=)(\d+)(;[^}}]*\}})'
        )
        updated = pattern.sub(rf'\g<1>{val}\g<3>', updated, count=1)
    return updated


def replace_battle(text, battle_entries):
    updated = text
    for item_key, entry in battle_entries.items():
        val = entry.get().strip()
        if not val.isdigit():
            raise ValueError(
                f"{BATTLE_ITEM_NAMES.get(item_key, item_key)} invalid value {val}"
            )

        pattern = re.compile(
            rf'(BattleItem_{item_key}=InventoryItem\{{[^}}]*?CurrentAmount=)(\d+)(;[^}}]*\}})'
        )
        updated = pattern.sub(rf'\g<1>{val}\g<3>', updated, count=1)

    return updated


def replace_quests(text, quest_flags):
    quest_str = ",".join(quest_flags)

    if re.search(r"QuestAccomplishments=\[.*?\];", text):
        return re.sub(
            r"QuestAccomplishments=\[.*?\];",
            f"QuestAccomplishments=[{quest_str}];",
            text
        )

    insert_point = text.find("EquippedCostumes=")
    insert_text = f"QuestAccomplishments=[{quest_str}];\n"

    if insert_point != -1:
        return text[:insert_point] + insert_text + text[insert_point:]

    return text.strip() + "\n" + insert_text


# ---------------- public API ----------------

def save_changes(AppState, cards_entries, battle_entries):
    path = AppState.save_path.get()
    if not path:
        messagebox.showerror("Error", "No save loaded")
        return False

    try:
        updated = AppState.save_text_data

        updated = replace_cards(updated, cards_entries)
        updated = replace_battle(updated, battle_entries)
        updated = replace_quests(updated, AppState.quest_flags)

        updated = update_save_data(
            updated,
            AppState,
            int(AppState.level_var.get()),
            int(AppState.xp_var.get()),
            int(AppState.candy_var.get()),
            int(AppState.total_candy_var.get()),
            tuple(v.get() for v in AppState.player_position_vars),
            tuple(v.get() for v in AppState.camera_position_vars),
            [v.get() for v in AppState.costume_vars],
            int(AppState.robotjumps_var.get()),
            int(AppState.monsterbashes_var.get()),
            int(AppState.suburbsbobbing_var.get()),
            int(AppState.mallbobbing_var.get()),
            int(AppState.countrybobbing_var.get()),
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
        messagebox.showerror("Error", "No save loaded")
        return False

    path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("JSON", "*.json"), ("Text", "*.txt"), ("All", "*.*")]
    )

    if not path:
        return False

    try:
        updated = replace_cards(updated, AppState.save_text_data, cards_entries)
        updated = replace_battle(updated, AppState.save_text_data, battle_entries)
        updated = replace_quests(updated, AppState.quest_flags)

        if path.endswith(".json"):
            import json
            json.dump({
                "Level": int(AppState.level_var.get()),
                "XP": int(AppState.xp_var.get()),
                "Candy": int(AppState.candy_var.get()),
                "TotalCandy": int(AppState.total_candy_var.get()),
            }, open(path, "w"), indent=4)

        elif path.endswith(".txt"):
            open(path, "w", encoding="utf-8").write(updated)

        else:
            with open(path, "wb") as f:
                f.write(AppState.save_header)
                f.write(updated.encode("utf-8"))

        messagebox.showinfo("Saved", f"Saved to {path}")
        return True

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False


def backup_save(AppState):
    path = AppState.save_path.get()
    if not path:
        messagebox.showerror("Error", "No save loaded")
        return False

    try:
        backup_path = f"{path}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(path, backup_path)
        messagebox.showinfo("Backup", backup_path)
        return True
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False