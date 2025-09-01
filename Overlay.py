import tkinter as tk
import threading
import pygetwindow as gw
import time

class Overlay(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        # Get MapleStory window position
        try:
            win = gw.getWindowsWithTitle("Maplestory Worlds-Artale(Global)")[0]  # Replace with part of your window's title

            x, y, w, h = win.left, win.top, win.width, win.height
        except IndexError:
            print("MapleStory window not found!")
            return

        # Position overlay at center-top of game window
        overlay_width = 850
        overlay_height = 40
        pos_x = x + (w // 2) - (overlay_width // 2)
        pos_y = y+80  # top edge

        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.5)  # 0 = fully transparent, 1 = opaque
        self.root.attributes("-transparentcolor", "pink")
        self.root.configure(bg="black")
        self.root.geometry(f"{overlay_width}x{overlay_height}+{pos_x}+{pos_y}")

        self.label = tk.Label(self.root, text="XP/hour: 0", font=("Arial", 12), fg="white", bg="black")
        self.label.pack(expand=True)

        self.root.mainloop()

    def update_text(self, text):
        # Must be called from the main thread using .after
        self.root.after(0, lambda: self.label.config(text=text))
