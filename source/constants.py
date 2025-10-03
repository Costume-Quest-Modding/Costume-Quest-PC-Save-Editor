# constants.py
import re
import os
import sys

XP_THRESHOLDS = {
    1: 0, 2: 2500, 3: 6000, 4: 12000, 5: 20000,
    6: 31000, 7: 45000, 8: 62000, 9: 82000, 10: 105000,
    11: 130000, 12: 160000, 13: 200000, 14: 250000,
}

NAMES = ["Reynold/Wren", "Everett", "Lucy"]

DEBUG_TELEPORTS = {
    "Suburbs": {
        "Bobbing for Apples": (126.0, 4.0, 60.0),
        "Second Storm Drain": (157.0, 3.5, -5.0),
        "Cemetery/Scarecrow": (67.0, 9.0, -77.0),
    },
    "Autumn Haven Mall": {
        "temp": (0.0, 0.0, 0.0),
        "temp": (0.0, 0.0, 0.0),
    },
    "Fall Valley": {
        "Carnival": (-8.0, 6.3, 62.0),
        "Scarecrow": (33.0, 6.0, 41.0),
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

# Helper for icon path if needed when packaged
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))