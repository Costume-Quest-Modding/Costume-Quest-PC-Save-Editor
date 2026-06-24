# save_state.py
import tkinter as tk
from save_data import calculate_level_from_xp


class AppState:
    save_header = b""
    save_text_data = ""
    loading_save = False

    original_candy_value = 0
    last_total_candy = 0

    save_path = None
    total_candy_var = None
    candy_var = None
    level_var = None
    xp_var = None

    robotjumps_var = None
    monsterbashes_var = None
    suburbsbobbing_var = None
    mallbobbing_var = None
    countrybobbing_var = None

    selected_world = None

    costume_vars = None
    player_position_vars = None
    camera_position_vars = None
    card_vars = None

    quest_flags = []
    quest_flags_var = None

    @classmethod
    def init_vars(cls, root):
        cls.save_path = tk.StringVar()

        cls.total_candy_var = tk.StringVar(value="0")
        cls.candy_var = tk.StringVar(value="0")

        cls.level_var = tk.StringVar(value="1")
        cls.xp_var = tk.StringVar(value="0")

        cls.robotjumps_var = tk.StringVar(value="0")
        cls.monsterbashes_var = tk.StringVar(value="0")
        cls.suburbsbobbing_var = tk.StringVar(value="0")
        cls.mallbobbing_var = tk.StringVar(value="0")
        cls.countrybobbing_var = tk.StringVar(value="0")

        cls.selected_world = tk.StringVar(value="Suburbs")

        cls.costume_vars = [tk.StringVar(value="") for _ in range(3)]
        cls.player_position_vars = [tk.DoubleVar(value=0.0) for _ in range(3)]
        cls.camera_position_vars = [tk.DoubleVar(value=0.0) for _ in range(3)]

        cls.card_vars = {i + 1: tk.IntVar(value=0) for i in range(54)}

        cls.quest_flags = []
        cls.quest_flags_var = tk.StringVar()