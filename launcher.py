"""Launcher for PyInstaller builds.

The app lives in the `source` package (run with `python -m source.main`
in dev). PyInstaller needs a plain entry script, so this thin wrapper
imports and runs it.
"""
from source.main import main

if __name__ == "__main__":
    main()