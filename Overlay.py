import threading
import tkinter as tk
import pygetwindow as gw


class Overlay(threading.Thread):
    def __init__(self, win):
        threading.Thread.__init__(self)
        self.root = None
        self.label = None
        self.daemon = True
        self.win = win
        self.start()
        self.overlay_width = 950
        self.overlay_height = 40

    def run(self):
        # Get MapleStory window position
        x, y, w, h = self.win.left, self.win.top, self.win.width, self.win.height

        # Position overlay at center-top of game window
        pos_x = x + (w // 2) - (self.overlay_width // 2)
        pos_y = y+80  # top edge

        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.5)  # 0 = fully transparent, 1 = opaque
        self.root.attributes("-transparentcolor", "pink")
        self.root.configure(bg="black")
        self.root.geometry(f"{self.overlay_width}x{self.overlay_height}+{pos_x}+{pos_y}")

        self.label = tk.Label(self.root, text="XP/hour: 0", font=("Arial", 12), fg="white", bg="black")
        self.label.pack(expand=True)

        self.root.mainloop()

    def update_text(self, text):
        # Must be called from the main thread using .after
        # Position overlay at center-top of game window
        pos_x = self.win.left + (self.win.width // 2) - (self.overlay_width // 2)
        pos_y = self.win.top + 80  # top edge

        self.root.attributes("-topmost", True)
        self.root.geometry(f"{self.overlay_width}x{self.overlay_height}+{pos_x}+{pos_y}")
        self.root.after(0, lambda: self.label.config(text=text))
