# Plan
# Grab screenshot of game every so often
# Resize it to small part in front of dino
# If majority or specefic pixel black, tell pyautogui to press space bar
# While loop unless program stopped


from PIL import ImageGrab
import pyautogui
import pygetwindow as gw
import time


win = next(w for w in gw.getWindowsWithTitle("DINO") if w.title == "DINO")
print(win)
hwnd = win._hWnd

#
# snapshot = ImageGrab.grab(bbox=[100, 500,204, 535], all_screens=False, xdisplay=None, window=hwnd)
# snapshot.show()
# print(snapshot.get_flattened_data())

win.activate()
time.sleep(0.5)

game_view_x_right = 125

while True:
    jump_snapshot = ImageGrab.grab(bbox=[100, 500,game_view_x_right, 535], all_screens=False, xdisplay=None,
                          window=hwnd)
    stage_snapshot = ImageGrab.grab(bbox=[300, 560,400, 590], all_screens=False, xdisplay=None, window=hwnd)

    stage_pixels = stage_snapshot.get_flattened_data()
    jump_pixels = jump_snapshot.get_flattened_data()

    avg_stage_brightness = sum((r + g + b) / 3 for r, g, b in stage_pixels) / len(stage_pixels)
    is_night = avg_stage_brightness < 128

    if is_night:
        obstacle_pixels = sum(1 for r, g, b in jump_pixels if r > 150 and g > 150 and b > 150)
    else:
        obstacle_pixels = sum(1 for r, g, b in jump_pixels if r < 100 and g < 100 and b < 100)

    if obstacle_pixels > 5:

        pyautogui.press("space")
        game_view_x_right += 1
        print(game_view_x_right)

    time.sleep(0.02)

