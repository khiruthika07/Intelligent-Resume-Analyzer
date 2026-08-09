"""
INTELLIGENT RESUME ANALYZER
Main Entry Point
Launch command: python main.py
Uses ONLY Python 3 Standard Library + Tkinter.
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox

from gui import IntelligentResumeAnalyzerGUI


def ensure_directories():
    """Ensures required application directories exist."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dirs = [
        os.path.join(base_dir, "data"),
        os.path.join(base_dir, "data", "sample_resumes"),
        os.path.join(base_dir, "results"),
        os.path.join(base_dir, "results", "reports")
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)


def main():
    """Initializes and runs Intelligent Resume Analyzer application."""
    ensure_directories()

    # Enable High-DPI scaling on Windows if supported
    if os.name == 'nt':
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    root = tk.Tk()

    # Set icon if available or handle window initialization
    try:
        app = IntelligentResumeAnalyzerGUI(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Application error encountered:\n{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
