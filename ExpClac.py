from collections import deque
from datetime import datetime, timedelta
from time import sleep
import numpy as np
import pytesseract
import pyautogui
import pygetwindow as gw
import time
from PIL import Image
import cv2

import Overlay
import Utils

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
windows = gw.getWindowsWithTitle("Maplestory Worlds-Artale(Global)")  # Replace with part of your window's title
if not windows:
    print("Window not found.")
    exit()

win = windows[0]
win.activate()

# Step 2: Get window bounds
#x, y = win.left, win.top
#w, h = win.width, win.height

history = []

## Max exp jump per second
MAX_ALLOWED_EXP_JUMP = 100_000

# Store (timestamp, exp_percent) tuples
short_window = deque(maxlen=120)  # ~2 minutes if updating every second
long_window = deque(maxlen=600)   # ~10 minutes if updating every second

def update_exp(exp_value, exp_percent):
    """Call this every time you get a new EXP reading from OCR."""
    now = time.time()
    short_window.append((now, [exp_value, exp_percent]))
    long_window.append((now, [exp_value, exp_percent]))

def calc_exp_per_10(window):
    """Calculate EXP/hour for given window data."""
    if len(window) < 2:
        return 0.0

    start_time = window[0][0]
    start_exp = window[0][1]

    end_time = window[-1][0]
    end_exp = window[-1][1]

    elapsed_seconds = end_time - start_time
    gained_exp = end_exp[0] - start_exp[0]
    gained_pc = end_exp[1] - start_exp[1]

    exp_per_10 = (gained_exp / elapsed_seconds) * (10*60)
    exp_pc_per_10 = (gained_pc / elapsed_seconds) * (10*60)
    return [exp_per_10, exp_pc_per_10]

def get_rates():
    """Return short-term and long-term EXP/hour."""
    return calc_exp_per_10(short_window), calc_exp_per_10(long_window)

def get_game_exp(exp_region):
    screenshot = pyautogui.screenshot(region=exp_region)
    # screenshot = screenshot.convert('RGB')
    #screenshot.show()

    #gray = screenshot.convert("L")  # "L" mode = 8-bit pixels, black and white

    # Convert Pillow → NumPy array (so OpenCV can process it)
    img = np.array(screenshot)

    # Scale up 2x
    img = cv2.resize(img, None, fx=8, fy=8, interpolation=cv2.INTER_LINEAR)

    # Threshold (binarize)
    _, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)

    # Convert OpenCV image to PIL format
    pil_img = Image.fromarray(img)

    text = pytesseract.image_to_string(pil_img, config='--psm 6 -c tessedit_char_whitelist=0123456789P[.%/]')
    return Utils.extract_exp(text)

def main():
    overlay = Overlay.Overlay(win)

    exp_last = 0
    start_exp = 0
    pc_start = 0
    exp_at_time=[]
    best_10 = [0,0]

    while 1:
        x, y = win.left, win.top
        w, h = win.width, win.height
        exp_region = (x + int(w * 0.5), y + int(h * 0.92), int(w * 0.2), int(h * 0.04))

        try:
            text = get_game_exp(exp_region)
            print(text)

            if not Utils.validate_exp_string(text):
                sleep(1)
                continue

            exp_current = int(text[:text.index("[")])
            pc_current = float(text[text.index("[")+1:text.index("%")])

            ## prevent exp loss - possible to lose exp due to dying but meh.
            if exp_last > exp_current:
                continue

            gain_exp = exp_current-exp_last

            ## allow for upto 100k exp
            if gain_exp > MAX_ALLOWED_EXP_JUMP and start_exp != 0:
                continue

            if start_exp == 0:
                start_exp = exp_current
                pc_start = pc_current

            exp_last = exp_current

            pc_total = pc_current - pc_start
            exp_at_time.append({int(time.time()), exp_current})

            pc = "%0.2f" % pc_total
            print(f"Exp Gain: {gain_exp} {pc} %")
            update_exp(exp_current, pc_current)
            change = update_history(exp_current, pc_current)
            change2 = get_rates()

            print(f"Change in last 10 minutes: {change[0]} {as_percent(change[1])}%")

            if change2[1][0] > best_10[0]:
                best_10 = [change2[1][0], change2[1][1]]

            ttl = Utils.calc_time_to_level(pc_current, change2[1][1])

            print(f"Best 10: { best_10[0]} {as_percent(best_10[1])}%")
            print(f"Time to Level: {ttl} ")
            overlay.update_text(f"B10: {short_num(best_10[0])} ({as_percent(best_10[1])}%) | E10: {short_num(change2[0][0])} ({as_percent(change2[0][1])}%| C10: {short_num(change2[1][0])} ({as_percent(change2[1][1])}% ) | TTL: {ttl}")

            print(get_rates())
            sleep(1)
        except:
            sleep(1)

def short_num(n: int) -> str:
    suffixes = ['', 'K', 'M', 'B', 'T']
    num = float(n)
    idx = 0

    while abs(num) >= 1000 and idx < len(suffixes) - 1:
        num /= 1000.0
        idx += 1

    # Format to keep <= 4 chars
    if num >= 100:
        s = f"{int(num)}{suffixes[idx]}"
    elif num >= 10:
        s = f"{num:.1f}{suffixes[idx]}".rstrip('0').rstrip('.')
    else:
        s = f"{num:.2f}{suffixes[idx]}".rstrip('0').rstrip('.')

    return s

def as_percent(val):
    return "%0.2f" % val

def update_history(new_value: int, pc: float):
    now = datetime.now()
    change = 0

    # Add new value
    history.append((now, [new_value, pc]))

    # Remove entries older than 10 minutes
    ten_minutes_ago = now - timedelta(minutes=10)
    while history and history[0][0] < ten_minutes_ago:
        history.pop(0)

    # Calculate change
    if len(history) >= 2:
        exp_change = history[-1][1][0] - history[0][1][0]
        pc_change = history[-1][1][1] - history[0][1][1]
        return [exp_change, pc_change]
    return [0, 0]

if __name__ == "__main__":
    main()
