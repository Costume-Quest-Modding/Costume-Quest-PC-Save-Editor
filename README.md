# Costume-Quest-PC-Save-Editor

A Python GUI Save Editor/Viewer for the Steam release of Costume Quest — Edit and view save data safely, with save backups and a simple UI.

Supports Costume Quest save files. Currently doesn't support Grubbins on Ice and Costume Quest 2.

![CQ PC Save Editor Summary](https://i.imgur.com/MAhnfn8.png)

---

## 🚀 Features
- **Summary:** See all your progress from one convenient tab.
- **Edit:** Player Level, Experience, Candy, World/Location, Battle Stamp, Cards and Equipped Costumes.
- **View:** View any active/finished Quests (WIP).
- **UI:** Save/Save As (.json, .txt, or binary), automatic backups with a File menu toggle.
- **Save Safety:** Existing save file required for writing; editor avoids overwriting by default.

   - **Auto-backup on save** (File menu, on by default): A timestamped copy of your original save is made before every write. Turn it off if you're saving constantly.
   - **Atomic writes:** Saves go to a temp file first, then swap into place — a crash mid-save can never leave you with a half-written file.
   - **Validation:** Your edited data is re-parsed before anything is written. If it doesn't parse, the save aborts instead of writing a broken file.


---

## 🧰 Prerequisites
- **Python 3.11+** (tested on Windows)
- Pillow (PIL) — for image handling
- tkinter

---

## 🛠️ Installation (local dev)
1. Clone project:
   ```bash
   git clone https://github.com/Costume-Quest-Modding/Costume-Quest-PC-Save-Editor.git
   cd Costume-Quest-PC-Save-Editor
   ```
2. Create & activate venv:
   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
3. Install deps:
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Run the app

```bash
python -m source.main
```
(Run from the project root.)

---

## 🧭 Quick usage
1. Open an existing Costume Quest save file.  
2. Edit fields in the main UI (level, candy, world, positions, costumes etc.).  
3. Use **Save** to save changes or Save As... to export to `.json`, `.txt`, or binary. A timestamped backup is made automatically before every save (toggleable in the File menu).

---

## ⚠️ Known limitations
- DLC support is on hold. This will be brought back after Main Game is finished and v1.0 is released.
