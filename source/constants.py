# constants.py
import re
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARDS_DIR = os.path.join(BASE_DIR, "images", "cards")
STAMP_DIR = os.path.join(BASE_DIR, "images", "battle_stamps")

XP_THRESHOLDS = {
    1: 0, 2: 2500, 3: 6000, 4: 12000, 5: 20000,
    6: 31000, 7: 45000, 8: 62000, 9: 82000, 10: 105000,
    11: 130000, 12: 160000, 13: 200000, 14: 250000,
}

NAMES = ["Reynold/Wren", "Everett", "Lucy"]

DEBUG_TELEPORTS = {
    "Suburbs": {
        "Reynold & Wren's House": (-25.5, 3.3, 33.3),
        "Bobbing for Apples": (126.0, 4.0, 60.0),
        "First Storm Drain": (117.0, 3.5, 161.0),
        "Second Storm Drain": (157.0, 3.5, -5.0),
        "Cemetery/Scarecrow": (67.0, 9.0, -77.0),
    },
    "Autumn Haven Mall": {
        "Mall Entrance": (-103.5, 55.5, 119.5),
        "Central Station": (153.1, 39.4, -185.6),
        "Mall (Second Floor)": (194.0, 38.5, -140.0),
        "Mall (Third Floor)": (117.5, 45.0, -147.0),
    },
    "Fall Valley": {
        "Vine Cage": (-22.5, 37.5, 117.3),
        "Fry Stand": (-49.0, 2.5, -32.0),
        "Carnival": (-8.0, 6.3, 62.0),
        "Scarecrow": (33.0, 6.0, 41.0),
        "Maze (Center)": (106.5, 3.5, 38.0),
        "Maze (End)": (60.0, 5.0, 93.5),
        "Dorsilla/Big Bones": (-12.0, 36.0, 122.0),
    },
}

WORLD_PATHS = {
    "Suburbs": "worlds/cq_suburbs/cq_suburbs",
    "Autumn Haven Mall": "worlds/cq_mall_interior/cq_mall_interior",
    "Fall Valley": "worlds/cq_fallvalley/cq_fallvalley",
}

COSTUME_OPTIONS = [
    "Costume_Robot", "Costume_Knight", "Costume_StatueOfLiberty",
    "Costume_SpaceWarrior", "Costume_Ninja", "Costume_Unicorn",
    "Costume_Pumpkin", "Costume_Vampire", "Costume_FrenchFries",
    "Costume_BlackCat", "Costume_Grubbin"
]

COSTUME_DISPLAY_NAMES = {
    "Costume_Robot": "Robot",
    "Costume_Knight": "Knight",
    "Costume_StatueOfLiberty": "Statue of Liberty",
    "Costume_SpaceWarrior": "Space Warrior",
    "Costume_Ninja": "Ninja",
    "Costume_Unicorn": "Unicorn",
    "Costume_Pumpkin": "Pumpkin",
    "Costume_Vampire": "Vampire",
    "Costume_FrenchFries": "French Fries",
    "Costume_BlackCat": "Black Cat",
    "Costume_Grubbin": "Grubbin"
}

CARD_PATTERN = re.compile(
    r'(TrickyTreatCard_(\d+)=InventoryItem\{[^}]*CurrentAmount=)(\d+)(;[^}]*\})'
)

CARD_NAMES = {
    1: "Raz-Ums",
    2: "Glop",
    3: "Wobblers",
    4: "Choconana",
    5: "Shimmerfizz",
    6: "Chunkwutter",
    7: "Candy Hair",
    8: "Moops",
    9: "Chocolate Carrot",
    10: "Fuds",
    11: "Sweet Tooth",
    12: "Jammie Jams",
    13: "Lollopops",
    14: "Fruity Foam",
    15: "Swedish Noses",
    16: "Box Cake",
    17: "Gooz",
    18: "Fee-Fi-Fo-Fudge",
    19: "Slime Beetles",
    20: "Sour Feet",
    21: "Fish Head",
    22: "Gummy Water",
    23: "Licorice Cables",
    24: "Cinnamon Brain",
    25: "Mossy Log",
    26: "Wood Chips",
    27: "Pizza Sundae",
    28: "Sweet Fat",
    29: "Pimples",
    30: "Frozen Butter",
    31: "Edible Hat",
    32: "Sludge",
    33: "Coffee Toffee Taffee",
    34: "Banana Beard",
    35: "Broccoli Wafers",
    36: "Gingerbread Ham",
    37: "Mice Crispy Treat",
    38: "Jaw Hurters",
    39: "Blobbles",
    40: "Barf Roll-Ups",
    41: "Chocolate Hamburger",
    42: "Clippingz",
    43: "Salmon Rings",
    44: "Street Chews",
    45: "Fried Popcorn",
    46: "Coconuts & Bolts",
    47: "Jelly Has-Beens",
    48: "Unicorn Pellets",
    49: "Misfortune Cookie",
    50: "Sugar Bucket",
    51: "Old Lady Fingers",
    52: "Boogie Pie",
    53: "Human Crackers",
    54: "Gloop"
}

CARD_IMAGES = {
    num: os.path.join(CARDS_DIR, f"trickcard_{num:03}.png")
    for num in CARD_NAMES.keys()
}

BATTLE_ITEM_PATTERN = re.compile(
    r'(BattleItem_(\w+)=InventoryItem\{[^}]*?CurrentAmount=)(\d+)(;[^}]*\})'
)

BATTLE_ITEM_NAMES = {
    "FangOfTheWolf": "Fang of the Wolf",
    "BlackCat": "Black Cat",
    "MovingTombstone": "Moving Tombstone",
    "Egg": "Egg",
    "DisembodiedHand": "Disembodied Hand",
    "PumpkinGuts": "Pumpkin Guts",
    "ScreamingSpider": "Screaming Spider",
    "BloodshotEyeballs": "Bloodshot Eyeballs",
    "ToiletPaper": "Toilet Paper",
    "OneEyedVampireBat": "One-Eyed Vampire Bat",
    "WitchesBrew": "Witch's Brew",
    "JawboneOfTheWolf": "Jawbone of the Wolf",
    "AlbinoBlackCat": "Albino Black Cat",
    "Banshee": "Banshee",
    "FlyingTombstone": "Flying Tombstone",
    "RottenEgg": "Rotten Egg",
    "SixFingeredHand": "Disembodied Six Fingered Hand",
    "MoldyPumpkinGuts": "Moldy Pumpkin Guts",
    "YodelingWidow": "Yodeling Black Widow",
    "TwoPlyToiletPaper": "2-Ply Toilet Paper",
    "HeadlessBanshee": "Headless Banshee",
    "VegetarianBrew": "Vegetarian Witch's Brew",
    "NoEyedVampireBat": "No-Eyed Vampire Bat",
    "BowlOfEyeballs": "Bowl of Bloodshot Eyeballs"
}


BATTLE_STAMP_IMAGES = {
    key: os.path.join(STAMP_DIR, f"stamp_{i+1:03}.png")
    for i, key in enumerate(BATTLE_ITEM_NAMES.keys())
}


THEMES = {
    "dark": {
        "root_theme": "black",
        "style_theme": "xpnative",
        "bg": "#1e1e1e",
        "fg": "#e0e0e0",
        "notebook_bg": "#2a2a2a",
        "menu_bg": "#2a2a2a",
        "menu_fg": "#dddddd",
        "menu_active_bg": "#444444",
        "menu_active_fg": "#80c0ff",
        "entry_bg": "#2a2a2a",
        "entry_fg": "#e0e0e0",
        "tab_bg": "#2a2a2a",
        "tab_fg": "#cccccc",
        "tab_selected_bg": "#444444",
        "tab_selected_fg": "#ffffff"
    },
    "light": {
        "bg": "#E3F2FD",
        "fg": "#0D47A1",
        "root_theme": "winxpblue",
        "style_theme": "xpnative",
        "notebook_bg": "#BBDEFB",
        "menu_bg": "#BBDEFB",
        "menu_fg": "#0D47A1",
        "menu_active_bg": "#90CAF9",
        "menu_active_fg": "#0D47A1",
        "entry_bg": "#FFFFFF",
        "entry_fg": "#0D47A1",
        "tab_bg": "#BBDEFB",
        "tab_fg": "#0D47A1",
        "tab_selected_bg": "#90CAF9",
        "tab_selected_fg": "#0D47A1",
    }
}

# Helper for icon path if needed when packaged
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
