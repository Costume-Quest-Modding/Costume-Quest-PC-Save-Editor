# Costume-Quest-PC-Save-Editor

A Python GUI save editor/viewer for the Costume Quest PC (Steam) release — view and edit save data safely, with save backups and a simple UI.

> ⚠️ **Note:** DLC save files are not supported yet.
>
![CQ PC Save Editor Summary](https://i.imgur.com/h0Txpdp.png)

---

## 🚀 Features
- **Edit:** Player Level, Experience, Current Candy, World, Player / Camera Position, Equipped Costumes, Cards, Battle Stamps.  
- **Summary:** View all important save info in one convenient tab.  
- **UI:** Interactive Map (WIP), Save/Save As (.json, .txt, or binary), Manual backups (recommended before editing).  
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
2. Edit fields in the main UI (levels, candy, world, positions, costumes).  
3. Use **Save** to save changes or **Save As...** to export to `.json`, `.txt`, or binary. Backups are manual; use the Backup option before editing (recommended).

---

## ⚠️ Known limitations
- DLC saves are not supported currently (tracked for future work).  
- On Linux, tkinter may not be installed by default — install the distribution package (e.g., `sudo apt install python3-tk`).
