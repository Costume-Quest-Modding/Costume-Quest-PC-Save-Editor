QUESTS = {
    "Suburbs": {
        # World 1 Info Finished and Correct
        # Now adding Quest Flags
        "Robot Repair": {
            "questtype": "Main",
            "description": "Dorsilla ruined my costume! I need to rebuild it!",
            "how_to_complete": [
                "Open all 3 treasure coffins in the alley to rebuild the Robot costume.",
            ],
            "reward": "300 XP",

            "flags": {
                "started": [
                    "DoorNSkeleton_FirstDoor",
                    "DoorNSkeleton_SecondDoor",
                    "Burbs_MQ1_CarWreck",
                    "L_010_NoCostumeStarted"
                ],
                "completed": [
                    "DoorNSkeleton_FirstDoor", # First Door Completed
                    "DoorNSkeleton_SecondDoor", # Second Door Completed
                    "Burbs_MQ1_CarWreck",
                    "L_010_NoCostumeStarted",
                    "L_010_BashTutorialDone",
                    "RobotPiece_TreasureChest1", # Aluminum Foil
                    "RobotPiece_TreasureChest2", # 
                    "RobotPiece_TreasureChest3", # 
                    "L_010_TreasureTutorialDone",
                    "Burbs_MQ1_Ramp",
                    "RobotRamp"
                ]
            }
        },
        "Programmed for Protection": {
            "questtype": "Main",
            "description": "Bullies are oppressing the weak in Auburn Pines! They must be stopped!",
            "how_to_complete": [
                "Talk to Travis to get the quest.",
                "Talk to Travis again to start the chase.",
                "Run away from him using the Robot's Boost ability."
            ],
            "reward": "300 XP",

            "flags": {
                "started": [
                    "Burbs_MQ_02_Started" # Quest Started
                ],
                "completed": [
                    "Burbs_MQ_02_Started", # Quest Started
                    "Burbs_MQ_02_RaceInProgress", # Race in Progress
                    "Burbs_MQ_02_WinCutscene", # Win Cutscene
                    "BMQ2_RaceOver", # Race Finished
                    "L01_bAlreadyInteracted", 
                    "L01_bEverettJoinedParty"
                ]
            }
        },
        "Pie for the Putterpam": {
            "questtype": "Main",
            "description": "Mrs. Putterpam is in need of a pie ingredient.",
            "how_to_complete": [
                "Talk to Mrs. Putterpam to get the quest.",
                "Find her the missing ingredient (Cherries). (Must complete \"The Patriot's Party\" first.)",
                "Talk to her to return the ingredient."
            ],
            "reward": "300 XP",
            "flags": {
                "started": [],
                "completed": []
            }
        },
        "The Patriot's Party": {
            "questtype": "Main",
            "description": "Russell won't let us into his awesome party.",
            "how_to_complete": [
                "Talk to Russell to get the quest.",
                "Talk to 4 NPCs to build the Liberty Costume. (One has a Costume Pattern and 3 have Costume Pieces)",
                "Talk again to Russell (as the Liberty Costume) to enter the party."
            ],
            "reward": "300 XP",

            "flags": {
                "started": [
                    "Burbs_MQ_04_Started" # Quest Started
                ],
                "completed": [
                    "Burbs_MQ_04_Started", # Quest Started
                    "Burbs_MQ_04_Lackey1", # Lackey 1
                    "Burbs_MQ_04_Lackey2", # Lackey 2
                    "Burbs_MQ_04_Lackey3", # Lackey 3
                    "Suburbs_OpenedManholeB", # Manhole B Opened
                    "StatuePiece_TreasureChest1", # Liberty Costume Piece 1
                    "StatuePiece_TreasureChest2", # Liberty Costume Piece 2
                    "PatriotQuestRamp", # Ramp 1
                    "PatriotQuestRamp2", # Ramp 2
                    "BMQ4_bEverettHint" # Everett Hint for Liberty Costume
                ]
            }
        },
        "These Tombstones Aren't Styrofoam": {
            "questtype": "Main",
            "description": "Get through the cemetery and find Monster HQ!",
            "how_to_complete": [
                "Open the Monster Gate and enter the Cemetery to start the quest.",
                "Trigger the cutscene at the end of the Cemetery to finish the quest."
            ],
            "reward": "300 XP",

            "flags": {
                "started": [],
                "completed": []
            }
        },
        "Suburbs Bobbing for Apples": {
            "questtype": "Side",
            "description": "Bob for Apples!",
            "how_to_complete": [
                "Complete 3 rounds of Apple Bobbing to finish the quest."
            ],
            "reward": "\n- 20 Candy (Round 1)"
            "\n- 50 Candy (Round 2)"
            "\n- Sweet Tooth Creepy Treat Card (Round 3)",

            "flags": {
                "started": [
                    "Burbs_SQ_01_Started" # Quest Started
                ],
                "completed": [
                    "Burbs_SQ_01_Started", # Quest Started
                    "Burbs_SQ_01_Compl_1", # Round 1 Completed
                    "Burbs_SQ_01_Compl_2", # Round 2 Completed
                    "Burbs_SQ_01_Compl_3" # Round 3 Completed
                ]
            }
        },
        "Auburn Pines Hide 'n' Seek": {
            "questtype": "Side",
            "description": "Find all six kids hiding in Auburn Pines.",
            "how_to_complete": [
                "Find/Talk to all six kids playing hide and seek around Auburn Pines."
            ],
            "reward": "\n- Candy Pail Upgrade: Tote Bag\n- 500 XP\n +3 AP",

            # Note: This quest gives 300 XP in-game, but visually shows 500 XP for some reason
            # (likely the text wasn't updated before release).
            
            "flags": {
                "started": [],
                "completed": []
            }
        },
        "This Card Is So Rare": {
            "questtype": "Side",
            "description": "Trade with a fellow Creepy Treat collector to get a rare card! ",
            "how_to_complete": [
                "Trade Scott your duplicate Glop Creepy Treat Card."
            ],
            "reward": "\n- 200 XP\n- Choconana Creepy Treat Card",

            "flags": {
                "started": [],
                "completed": []
            }
        },
        "Suburbs Collect 'em All": {
            "questtype": "Side",
            "description": "Trade with a fellow Creepy Treat collector!",
            "how_to_complete": [
                "Trade Austin your duplicate Fruity Foam Creepy Treat Card."
            ],
            "reward": "\n- 200 XP\n- Jelly Has-Beens Creepy Treat Card",

            "flags": {
                "started": [],
                "completed": []
            }
        }
    },
    "Autumn Haven Mall": {
        # World 2 Info NEEDS FINISHED AND VERIFIED
        "Tickets for Treats": {
            "questtype": "Main",
            "description": "Free the kids from their indentured gaming.",
            "how_to_complete": [
                "Talk to one of the kids playing games in the Arcade to get the quest.",
                "Talk to BoJonn or his assistant and defeat them to complete the quest."
            ],
            "reward": "\n- Costume Material: Scarf\n- 300 XP",

            "flags": {
                "started": [],
                "completed": []
            }
        },
        "Earn Your Monster Slayer Badge": {
            "questtype": "Main",
            "description": "Prove you're a Monster Slayer by defeating enemies on the second floor of the Mall and collecting their MONSTER HORNS.",
            "how_to_complete": [
                "Talk to Pablo or Derek to trigger the quest.",
                "Defeat 3 enemies and collect their Monster Horns from Mall's second floor.",
                "Talk to Pablo or Derek again to complete the quest."
            ],
            "reward": "\n- Access to 3rd Floor\n- Ninja Costume\n- 300 XP",

            "flags": {
                "started": [],
                "completed": []
            }
        },
        "The Mall-O-Rail is Broken": {
            "questtype": "Main",
            "description": "Help Sid fix the Mall-O-Rail.",
            "how_to_complete": [
                "Enter Light Mall and Talk to Sid to get the quest.",
                "Head to the Arcade and complete \"The Patriot's Party\" quest to access BoJonn 3.)",
                "Take the Mall-O-Rail and Talk to Sid again to complete the quest."
            ],
            "reward": "\n- Costume Material: Rope\n- 300 XP",

            "flags": {
                "started": [],
                "completed": []
            }
        },
        "The Dark Side of the Mall": {
            "questtype": "Main",
            "description": "The Light Side of the Mall awaits.",
            "how_to_complete": [
                "Head through the Dark Mall and collect the Costume Pattern from the Security Guard",
                "Collect all 3 Costume Pieces from the 3 NPCs.",
                "Trigger the cutscene at the end of the Cemetery to finish the quest."
            ],
            "reward": "300 XP",

            "flags": {
                "started": [],
                "completed": []
            }
        },
        "Extreme Costume Challenge!": {
            "questtype": "Side",
            "description": "If we win, we might get awesome prizes!",
            "how_to_complete": [
                "Talk to the Announcer to obtain the Quest."
                "\nNeed Lucy (to trigger quest) and Liberty Costume (to complete it.)",
                "Find and Talk to all 3 Judges.",
                "Equip \"Robot\",  \"Knight\" and \"Statue of Liberty\" costumes for the Contest",
                "Talk to the Announcer again."
            ],
            "reward": "\n- Unicorn Costume Pattern\n- 300 XP",

            "flags": {
                "started": [],
                "completed": []
            }
        },
        "This Card Is Rarer": {
            "questtype": "Side",
            "description": "Trade with a fellow Creepy Treat collector to get a rare card!",
            "how_to_complete": [
                "Trade Carlos your duplicate Cinnamon Brain Creepy Treat Card."
            ],
            "reward": "\n- 200 XP\n- Gummy Water Creepy Treat Card",

            "flags": {
                "started": [],
                "completed": []
            }
        },
        "Mall Collect 'em All": {
            "questtype": "Side",
            "description": "[TODO]",
            "how_to_complete": [
                "[TODO]"
            ],
            "reward": "[TODO]",

            "flags": {
                "started": [],
                "completed": []
            }
        },
        "Mall Bobbing for Apples": {
            "questtype": "Side",
            "description": "Bob for Apples!",
            "how_to_complete": [
                "Complete 3 rounds of Apple Bobbing to finish the quest."
            ],
            "reward": "\n- 20 Candy (Round 1)"
            "\n- 50 Candy (Round 2)"
            "\n- Pizza Sundae Creepy Treat Card (Round 3)",

            "flags": {
                "started": [],
                "completed": []
            }
        },
        "Mall Hide 'n' Seek": {
            "questtype": "Side",
            "description": "Find all six kids hiding in Autumn Haven Mall.",
            "how_to_complete": [
                "Find/Talk to all six kids playing hide and seek around Autumn Haven Mall."
            ],
            "reward": "\n- Candy Pail Upgrade: Pumpkin Pail\n 500 XP\n +5 AP",

            # Note: This quest gives 300 XP in-game, but visually shows 500 XP for some reason
            # (likely the text wasn't updated before release).

            "flags": {
                "started": [],
                "completed": []
            }
        }
    },
    "Fall Valley": {
        "The Original Costume Quest": {
            "questtype": "Main",
            "description": "Get our costumes back from the Repugians!",
            "how_to_complete": [
                "Head to Town and obtain the Fry Costume from Chip.",
                "Head back to the Repugians and use the Fry Costume to lure both of them into the barn.",
                "Open the Treasure Coffin nearby to retrieve your costumes.",
                "Lure 3 customers to Chip's Fry Stand while wearing the Fry Costume.",
                "Talk to Henry to enter the Carnival.",
                "Battle the Monsters near the Ferris Wheel.",
                "Use the Ninja Costume to sneak past Orzo.",
                "Use the Space Warrior Costume to get through the Darkness to finish the quest."
            ],
            "reward": "300 XP",

            "flags": {
                "started": [],
                "completed": []
            }
        },
        "All's Fair That Ends Fare": {
            "questtype": "Main",
            "description": "Something fishy is afoot at the Carnival.",
            "how_to_complete": [
                "[TODO]",
            ],
            "reward": "[TODO]",

            "flags": {
                "started": [],
                "completed": []
            }
        },
        "Children of the High Fructose Corn Syrup": {
            "questtype": "Main",
            "description": "[TODO]",
            "how_to_complete": [
                "Enter the Maze and talk to the Grubbin. (Triggers quest and gives the Grubbin Costume Pattern.)",
                "Find the 3 Grubbin Costume Pieces by talking to NPCs in the Maze.",
                "Equip the Grubbin Costume.",
                "Head/Talk to the Repugian Guard blocking one of the Maze paths to finish the quest."
            ],
            "reward": "300 XP",

            "flags": {
                "started": [],
                "completed": []
            }
        },
        "Fall Valley Hide 'n' Seek": {
            "questtype": "Side",
            "description": "Find all six kids hiding in Fall Valley.",
            "how_to_complete": [
                "Talk to six kids hiding around Fall Valley."
            ],
            "reward": "\n- 300 XP\n- Candy Pail Upgrade: Bat Bucket.",

            # Note: This quest gives 300 XP in-game, but visually shows 500 XP for some reason
            # (likely the text wasn't updated before release).

            "flags": {
                "started": [],
                "completed": []
            }
        },
        "Fall Valley Bobbing for Apples": {
            "questtype": "Side",
            "description": "Bob for Apples!",
            "how_to_complete": [
                "Complete 3 rounds of Apple Bobbing to finish the quest."
            ],
            "reward": "\n- 20 Candy (Round 1)"
            "\n- 50 Candy (Round 2)"
            "\n- Sugar Bucket Creepy Treat Card (Round 3)",

            "flags": {
                "started": [],
                "completed": []
            }
        },
        "This Card Is The Rarest": {
            "questtype": "Side",
            "description": "Trade with a fellow Creepy Treat collector to get a rare card!",
            "how_to_complete": [
                "Trade Nathan your duplicate Street Chews Creepy Treat Card."
            ],
            "reward": "\n- 200 XP\n- Mice Crispy Treat Creepy Treat Card",

            "flags": {
                "started": [],
                "completed": []
            }
        },
        "Fall Valley Collect 'em All": {
            "questtype": "Side",
            "description": "Trade with a fellow Creepy Treat collector!",
            "how_to_complete": [
                "Trade Rebecca your duplicate Unicorn Pellets Creepy Treat Card."
            ],
            "reward": "\n- 200 XP\n- Jelly Has-Beens Creepy Treat Card",

            "flags": {
                "started": [],
                "completed": []
            }
        }
    }
}