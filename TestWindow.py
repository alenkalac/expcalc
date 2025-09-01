
import pyautogui
import pygetwindow as gw


#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
windows = gw.getWindowsWithTitle("Maplestory Worlds-Artale(Global)")  # Replace with part of your window's title
if not windows:
    print("Window not found.")
    exit()

win = windows[0]
win.activate()

# Step 2: Get window bounds
x, y = win.left, win.top
w, h = win.width, win.height

region = (x, y, w, h)