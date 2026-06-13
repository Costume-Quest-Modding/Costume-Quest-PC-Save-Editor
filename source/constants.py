# constants.py
import re
import os
import sys

# =========================
# PATHS / ENVIRONMENT
# =========================

BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
CARDS_DIR = os.path.join(BASE_DIR, "images", "cards")
STAMP_DIR = os.path.join(BASE_DIR, "images", "battle_stamps")

# =========================
# GAME PROGRESSION
# =========================

NAMES = ["Reynold/Wren", "Everett", "Lucy"]

XP_THRESHOLDS = {
    1: 0, 2: 2500, 3: 6000, 4: 12000, 5: 20000,
    6: 31000, 7: 45000, 8: 62000, 9: 82000, 10: 105000,
    11: 130000, 12: 160000, 13: 200000, 14: 250000
}

# =========================
# QUEST DATA
# =========================

QUEST_FLAG_MAP = {
    # Individual component quests
    "Door N Skeleton - First Door": ["DoorNSkeleton_FirstDoor"],
    "Door N Skeleton - Second Door": ["DoorNSkeleton_SecondDoor"],
    "Suburbs MQ1 - Car Wreck": ["Burbs_MQ1_CarWreck"],
    "L_010 - No Costume Started": ["L_010_NoCostumeStarted"],

    # Parent quests
    # Robot Repair
    "Robot Repair": {
        "started": [
            "DoorNSkeleton_FirstDoor",
            "DoorNSkeleton_SecondDoor",
            "Burbs_MQ1_CarWreck",
            "L_010_NoCostumeStarted"
        ],
        "completed": [
            "DoorNSkeleton_FirstDoor",
            "DoorNSkeleton_SecondDoor",
            "Burbs_MQ1_CarWreck",
            "L_010_NoCostumeStarted",
            "L_010_BashTutorialDone",
            "RobotPiece_TreasureChest1",
            "RobotPiece_TreasureChest2",
            "RobotPiece_TreasureChest3",
            "L_010_TreasureTutorialDone",
            "Burbs_MQ1_Ramp",
            "RobotRamp"
        ]
    }
}


QUESTS = {
    "Suburbs": {
        # World 1 Info Finished and Correct
        "Robot Repair": {
            "questtype": "Main",
            "description": "Dorsilla ruined my costume! I need to rebuild it!",
            "how_to_complete": "\n- Open all 3 treasure coffins in the alley to rebuild the Robot costume.",
            "reward": "300 XP"
        },
        "Programmed for Protection": {
            "questtype": "Main",
            "description": "Bullies are oppressing the weak in Auburn Pines! They must be stopped!",
            "how_to_complete": "\n- Talk to Travis get the quest."
            "\n- Talk to Travis again to start the chase."
            "\n- Run away from him using the Robot's Boost ability.",
            "reward": "300 XP"
        },
        "Pie for the Putterpam": {
            "questtype": "Main",
            "description": "Mrs. Putterpam is in need of a pie ingredient.",
            "how_to_complete": "\n- Talk to Mrs. Putterpam to get the quest."
            "\n- Find her the missing ingredient (Cherries). (Must complete \"The Patriot's Party\" first.)"
            "\n- Talk to her to return the ingredient.",
            "reward": "300 XP"
        },
        "The Patriot's Party": {
            "questtype": "Main",
            "description": "Russell won't let us into his awesome party.",
            "how_to_complete": "\n- Talk to Russell to get the quest."
            "\n- Talk to 4 NPCs to build the Liberty Costume. (One has a Costume Pattern and 3 have Costume Pieces)"
            "\n- Talk again to Russell (as the Liberty Costume) to enter the party.",
            "reward": "300 XP"
        },
        "These Tombstones Aren't Styrofoam": {
            "questtype": "Main",
            "description": "Get through the cemetery and find Monster HQ!",
            "how_to_complete": "\n- Open the Monster Gate and enter the Cemetery to start the quest."
            "\n- Trigger the cutscene at the end of the Cemetery to finish the quest.",
            "reward": "300 XP"
        },
        "Suburbs Bobbing for Apples": {
            "questtype": "Side",
            "description": "Bob for Apples!",
            "how_to_complete": "\n- Complete 3 rounds of Apple Bobbing to finish the quest.",
            "reward": "\n- 20 Candy (Round 1)"
            "\n- 50 Candy (Round 2)"
            "\n- Sweet Tooth Creepy Treat Card (Round 3)"
        },
        "Auburn Pines Hide 'n' Seek": {
            "questtype": "Side",
            "description": "Find all six kids hiding in Auburn Pines.",
            "how_to_complete": "\n- Find/Talk to all six kids playing hide and seek around Auburn Pines.",
            "reward": "\n- Candy Pail Upgrade: Tote Bag\n- 500 XP\n +3 AP"# The game actually gives 300XP for this quest, but for consistency with other Hide 'n Seek quests, it's set to 500XP here.
        },
        "This Card Is So Rare": {
            "questtype": "Side",
            "description": "Trade with a fellow Creepy Treat collector to get a rare card! ",
            "how_to_complete": "\n- Trade Scott your duplicate Glop Creepy Treat Card.",
            "reward": "\n- 200 XP\n- Choconana Creepy Treat Card"
        },
        "Suburbs Collect 'em All": {
            "questtype": "Side",
            "description": "Trade with a fellow Creepy Treat collector!",
            "how_to_complete": "\n- Trade Austin your duplicate Fruity Foam Creepy Treat Card.",
            "reward": "\n- 200 XP\n- Jelly Has-Beens Creepy Treat Card"
        }
    },
    "Autumn Haven Mall": {
        # World 2 Info NEEDS FINISHED AND VERIFIED
        "Tickets for Treats": {
            "questtype": "Main",
            "description": "Free the kids from their indentured gaming.",
            "how_to_complete": "\n- Talk to one of the kids playing games in the Arcade to get the quest."
            "\n- Talk to BoJonn or his assistant and defeat them to complete the quest.",
            "reward": "\n- Costume Material: Scarf\n- 300 XP"
        },
        "Earn Your Monster Slayer Badge": {
            "questtype": "Main",
            "description": "Prove you're a Monster Slayer by defeating enemies on the second floor of the Mall and collecting their MONSTER HORNS.",
            "how_to_complete": "\n- Talk to Pablo or Derek to trigger the quest."
            "\n- Defeat 3 enemies and collect their Monster Horns from Mall's second floor."
            "\n- Talk to Pablo or Derek again to complete the quest.",
            "reward": "\n- Access to 3rd Floor\n- Ninja Costume\n- 300 XP"
        },
        "The Mall-O-Rail is Broken": {
            "questtype": "Main",
            "description": "Help Sid fix the Mall-O-Rail.",
            "how_to_complete": "\n- Enter Light Mall and Talk to Sid to get the quest."
            "\n- Head to the Arcade and complete \"The Patriot's Party\" quest to access BoJonn 3.)"
            "\n- Take the Mall-O-Rail and Talk to Sid again to complete the quest.",
            "reward": "\n- Costume Material: Rope\n- 300 XP"
        },
        "The Dark Side of the Mall": {
            "questtype": "Main",
            "description": "The Light Side of the Mall awaits.",
            "how_to_complete": "\n- Head through the Dark Mall and collect the Costume Pattern from the Security Guard"
            "\n- Collect all 3 Costume Pieces from the 3 NPCs."
            "\n- Trigger the cutscene at the end of the Cemetery to finish the quest.",
            "reward": "300 XP"
        },
        "Extreme Costume Challenge!": {
            "questtype": "Side",
            "description": "If we win, we might get awesome prizes!",
            "how_to_complete": "\n- Talk to the Announcer to obtain the Quest. (Must have Lucy to trigger the quest and must havethe Liberty Costume to complete the quest.)"
            "\n- Find and Talk to all 3 Judges."
            "\n- Equip \"Robot\",  \"Knight\" and \"Statue of Liberty\" for the Contest and talk to the Announcer again to complete the quest.",
            "reward": "\n- Unicorn Costume Pattern\n- 300 XP"
        },
        "This Card Is Rarer": {
            "questtype": "Side",
            "description": "Trade with a fellow Creepy Treat collector to get a rare card!",
            "how_to_complete": "\n- Trade Carlos your duplicate Cinnamon Brain Creepy Treat Card.",
            "reward": "\n- 200 XP\n- Gummy Water Creepy Treat Card"
        },
        "Mall Collect 'em All": {
            "questtype": "Side",
            "description": "[TODO]",
            "how_to_complete": "[TODO]",
            "reward": "[TODO]"
        },
        "Mall Bobbing for Apples": {
            "questtype": "Side",
            "description": "Bob for Apples!",
            "how_to_complete": "\n- Complete 3 rounds of Apple Bobbing to finish the quest.",
            "reward": "\n- 20 Candy (Round 1)"
            "\n- 50 Candy (Round 2)"
            "\n- Pizza Sundae Creepy Treat Card (Round 3)"
        },
        "Mall Hide 'n' Seek": {
            "questtype": "Side",
            "description": "Find all six kids hiding in Autumn Haven Mall.",
            "how_to_complete": "\n- Find/Talk to all six kids playing hide and seek around Autumn Haven Mall.",
            "reward": "\n- Candy Pail Upgrade: Pumpkin Pail\n 500 XP\n +5 AP",
            # The game actually gives 300XP for this quest, but for consistency with other Hide 'n Seek quests, it's set to 500XP here.
        }
    },
    "Fall Valley": {
        "The Original Costume Quest": {
            "questtype": "Main",
            "description": "Get our costumes back from the Repugians!",
            "how_to_complete": "\n- Head to Town and obtain the Fry Costume from Chip."
            "\n- Head back to the Repugians and use the Fry Costume to lure both of them into the barn."
            "\n- Open the Treasure Coffin nearby to retrieve your costumes."
            "\n- Lure 3 customers to Chip's Fry Stand while wearing the Fry Costume."
            "\n- Talk to Henry to enter the Carnival."
            "\n- Battle the Monsters near the Ferris Wheel."
            "\n- Use the Ninja Costume to sneak past Orzo."
            "\n- Use the Space Warrior Costume to get through the Darkness to finish the quest.",
            "reward": "300 XP"
        },
        "All's Fair That Ends Fare": {
            "questtype": "Main",
            "description": "Something fishy is afoot at the Carnival.",
            "how_to_complete": "[TODO]",
            "reward": "[TODO]"
        },
        "Children of the High Fructose Corn Syrup": {
            "questtype": "Main",
            "description": "[TODO]",
            "how_to_complete": "\n- Enter the Maze area and talk to the Grubbin to get the quest and Grubbin Costume Pattern."
            "\n- Find the Grubbin Costume Pieces by talking to 3 NPCs in Maze."
            "\n- Head to the Repugian Guard blocking one of the Maze paths and while wearing the Grubbin Costume to finish the quest.",
            "reward": "300 XP"
        },
        "Fall Valley Hide 'n' Seek": {
            "questtype": "Side",
            "description": "Find all six kids hiding in Fall Valley.",
            "how_to_complete": "\n- Talk to six kids hiding around Fall Valley.",
            "reward": "\n- 500 XP\n- Candy Pail Upgrade: Bat Bucket."
            "\n\nNote: Completing this quest actually gives 300XP in-game, but for consistency with other Hide 'n Seek quests, it's set to 500XP here."
        },
        "Fall Valley Bobbing for Apples": {
            "questtype": "Side",
            "description": "Bob for Apples!",
            "how_to_complete": "\n- Complete 3 rounds of Apple Bobbing to finish the quest.",
            "reward": "\n- 20 Candy (Round 1)"
            "\n- 50 Candy (Round 2)"
            "\n- Sugar Bucket Creepy Treat Card (Round 3)"
        },
        "This Card Is The Rarest": {
            "questtype": "Side",
            "description": "Trade with a fellow Creepy Treat collector to get a rare card!",
            "how_to_complete": "\n- Trade Nathan your duplicate Street Chews Creepy Treat Card.",
            "reward": "\n- 200 XP\n- Mice Crispy Treat Creepy Treat Card"
        },
        "Fall Valley Collect 'em All": {
            "questtype": "Side",
            "description": "Trade with a fellow Creepy Treat collector!",
            "how_to_complete": "\n- Trade Rebecca your duplicate Unicorn Pellets Creepy Treat Card.",
            "reward": "\n- 200 XP\n- Jelly Has-Beens Creepy Treat Card"
        }
    },
    "Repugia": {
        "Viva Repugia": {
            "questtype": "Main",
            "description": "The revolutionaries need more recruits to join their cause.",
            "how_to_complete": "[TODO]",
            "reward": "[TODO]"
        },
        "Hook, Line & Freethinker": {
            "questtype": "Main",
            "description": "[TODO]",
            "how_to_complete": "[TODO]",
            "reward": "[TODO]"
        },
        "Grubbin Lovin'": {
            "questtype": "Main",
            "description": "How can we get the Grubbin Elder to open the Trowbog Gate?",
            "how_to_complete": "[TODO]",
            "reward": "[TODO]"
        },
        "Tome of the Trowbogs": {
            "questtype": "Main",
            "description": "[TODO]",
            "how_to_complete": "[TODO]",
            "reward": "[TODO]"
        },
        "The Case of the Missing Yeti": {
            "questtype": "Main",
            "description": "[TODO]",
            "how_to_complete": "[TODO]",
            "reward": "[TODO]"
        },
        "Save the Escapees": {
            "questtype": "Main",
            "description": "[TODO]",
            "how_to_complete": "[TODO]",
            "reward": "[TODO]"
        },
        "Bobbing for Eyeballs": {
            "questtype": "Side",
            "description": "[TODO]",
            "how_to_complete": "[TODO]",
            "reward": "[TODO]"
        },
        "This Card is ULTRA Rare": {
            "questtype": "Main",
            "description": "[TODO]",
            "how_to_complete": "[TODO]",
            "reward": "[TODO]"
        },
        "Repugia Collect 'em All": {
            "questtype": "Main",
            "description": "[TODO]",
            "how_to_complete": "[TODO]",
            "reward": "[TODO]"
        }
    }
}

# =========================
# WORLD / TELEPORTS
# =========================

DEBUG_TELEPORTS = {
    "Suburbs": {
        "Reynold & Wren's House": (-25.5, 3.3, 33.3),
        "Everett/Knight Costume": (11.3,2.9,22.2),
        "Bobbing for Apples": (126.0, 4.0, 60.0),
        "First Storm Drain": (117.0, 3.5, 161.0),
        "Second Storm Drain": (157.0, 3.5, -5.0),
        "Cemetery/Scarecrow": (67.0, 9.0, -77.0)
    },
    "Autumn Haven Mall": {
        "Mall Entrance": (-103.5, 55.5, 119.5),
        "Central Station": (153.1, 39.4, -185.6),
        "Mall (Second Floor)": (194.0, 38.5, -140.0),
        "Mall (Third Floor)": (117.5, 45.0, -147.0)
    },
    "Fall Valley": {
        "Vine Cage": (-22.5, 37.5, 117.3),
        "Fry Stand": (-49.0, 2.5, -32.0),
        "Carnival": (-8.0, 6.3, 62.0),
        "Scarecrow": (33.0, 6.0, 41.0),
        "Maze (Center)": (106.5, 3.5, 38.0),
        "Maze (End)": (60.0, 5.0, 93.5),
        "Dorsilla/Big Bones": (-12.0, 36.0, 122.0)
    },
    "Repugia": {
        "Main Area": (-90.9, 53.3, -0.4),
        "Grubbin Elder": (-23.4, 53.3, -7.2),
        "Trowbow Elder": (52.4, 60.7, 21.1),
        "Crestwailer Elder": (29.7, 69.0, -26.0),
        "Araxia": (-29.5, 77.1, -29.8)
    },
}

WORLD_PATHS = {
    "Suburbs": "worlds/cq_suburbs/cq_suburbs",
    "Autumn Haven Mall": "worlds/cq_mall_interior/cq_mall_interior",
    "Fall Valley": "worlds/cq_fallvalley/cq_fallvalley",
    "Repugia": "worlds/cq_repugia/cq_repugia"
}

# =========================
# COSTUMES
# =========================

COSTUME_OPTIONS = [
    # Base Game Costumes
    "Robot", "Knight", "Statue Of Liberty",
    "Space Warrior", "Ninja", "Unicorn",
    "Pumpkin", "Vampire", "French Fries",
    "Black Cat", "Grubbin",
    
    #DLC Costumes
    "Pirate", "Eyeball", "Yeti"
]

COSTUME_DISPLAY_NAMES = {
    # Base Game Costumes
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
    "Costume_Grubbin": "Grubbin",

    #DLC Costumes
    "Costume_Pirate": "Pirate",
    "Costume_Eyeball": "Eyeball",
    "Costume_Yeti": "Yeti"
}

# =========================
# CARDS
# =========================

CARD_NAMES = {
    # Base Game Cards
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
    54: "Gloop",

    #DLC Cards
    55: "Nutty Dumdums",
    56: "Strawberry Smackdown",
    57: "Cuttin' Candy",
    58: "Cake Cod",
    59: "Dietetic Marzipan",
    60: "Fansy Dollups",
    61: "Bubble Onions",
    62: "Glazed Butter Cubes",
    63: "Wikkids",
    64: "Dreamy Dipz",
    65: "Rainbow Whipz",
    66: "KLORKS!",
    67: "Caramold",
    68: "Sweet Wet Wheat",
    69: "Maple Crusties",
    70: "2-Headed Toddlers",
    71: "Red Hot Foam",
    72: "Wiggly Woozers"
}

CARD_IMAGES = {
    num: os.path.join(CARDS_DIR, f"trickcard_{num:03}.png")
    for num in CARD_NAMES.keys()
}

CARD_PATTERN = re.compile(
    r'(TrickyTreatCard_(\d+)=InventoryItem\{[^}]*CurrentAmount=)(\d+)(;[^}]*\})'
)

# =========================
# BATTLE ITEMS / STAMPS
# =========================

BATTLE_ITEM_NAMES = {
    # Base Game Stamps
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
    "BowlOfEyeballs": "Bowl of Bloodshot Eyeballs",

    # DLC Stamps
    "MummyGauze": "Mummy Gauze",
    "GalvanizedGauze": "Galvanized Mummy Gauze",
    "BlackRose": "Black Rose",
    "DeviledEgg": "Deviled Egg",
    "HeadlessBat": "Headless Vampire Bat",
    "MultiWingBat": "Multi-Winged Vampire Bat",
    "SkeletonOfWolf": "Skeleton of the Wolf",
    "RottenPumpGuts": "Rotten Pumpkin Guts"
}

BATTLE_STAMP_IMAGES = {
    key: os.path.join(STAMP_DIR, f"stamp_{i+1:03}.png")
    for i, key in enumerate(BATTLE_ITEM_NAMES.keys())
}

BATTLE_ITEM_PATTERN = re.compile(
    r'(BattleItem_(\w+)=InventoryItem\{[^}]*?CurrentAmount=)(\d+)(;[^}]*\})'
)