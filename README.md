# Costume-Quest-PC-Save-Editor

A Python GUI Save Editor/Viewer for the Steam release of Costume Quest — Edit and view save data safely, with save backups and a simple UI.

Supports Costume Quest and Grubbins on Ice save files. Currently doesn't support Costume Quest 2.
> ⚠️ **Note:** DLC save file support is still in the works. Alpha 1.2 is out NOW.

![CQ PC Save Editor Summary](https://i.imgur.com/fymJ6kZ.png)

---

## 🚀 Features
- **Summary:** See all your progress from one convenient tab.
- **Edit:** Player Level, Experience, Candy, World/Location, Battle Stamp, Cards and Equipped Costumes.
- **View:** View any active/finished Quests (WIP).
- **UI:** Save/Save As (.json, .txt, or binary), Manual backups (recommended before editing).
- **Safety:** Existing save file required for writing; editor avoids overwriting by default.

---

## 🧰 Prerequisites
- **Python 3.11+** (tested on Windows)
- Pillow (PIL) — for image handling
- tkinter (usually bundled with OS Python; on Linux you may need `python3-tk`)

---

## 🛠️ Installation (local dev)
1. Clone project:
   ```bash
   git clone https://github.com/<your-user>/Costume-Quest-PC-Save-Editor.git
   cd Costume-Quest-PC-Save-Editor
   ```
2. Create & activate venv:
   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - macOS/Linux:
     ```bash
     python -m venv .venv
     source .venv/bin/activate
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

(or `python source/main.py` if you prefer direct execution)

---

## 🧭 Quick usage
1. Open an existing Costume Quest save file.  
2. Edit fields in the main UI (level, candy, world, positions, costumes).  
3. Use **Save** to save changes or **Save As...** to export to `.json`, `.txt`, or binary. Backups are manual; use the Backup option before editing (recommended).

---

## ⚠️ Known limitations
- DLC support is in the works. Expect bugs while things get ironed out.  
- On Linux, tkinter may not be installed by default — install the distribution package (e.g., `sudo apt install python3-tk`).
