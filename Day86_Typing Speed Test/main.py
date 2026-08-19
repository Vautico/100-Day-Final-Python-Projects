import tkinter as tk
from tkinter import ttk, Text
import time
import json
from urllib.error import URLError
from urllib.request import urlopen

# Use api to get random list of words (100 words)
try:
    with urlopen("https://random-word-api.herokuapp.com/word?number=100", timeout=5) as response:
        words = json.load(response)
except (URLError, TimeoutError, json.JSONDecodeError):
    words = "python tkinter window typing speed practice keyboard display function layout variable".split()

paragraph = ""

for word in words:
    paragraph += f"{word} "

word_avg = sum(len(word) for word in words) / len(words)

# # print(paragraph)

#-----------------------------------------------------------------------------------

# Grab time inbetween key presses.
# Add number to list
# average that time every 0.1 seconds . this is seconds per characters every 0.1 seconds.
# turn spc to cps through division. average cps 0.1 seconds.
# turn that time into characters per second by using average number of words per character

# function that returns an integer, that is the average wpm

first_key = True

t_i = 0
t_f = 0

deltaT = 0
avg_list = []
avg_deltaT = 0

avg_wpm = 0
count = 0

# -----------------------------------

def time_inbetween_key(i):
    global t_i, t_f, deltaT, avg_deltaT, avg_wpm, first_key

    if first_key:
        t_i = i
        first_key = False
        return

    t_f = i
    deltaT = t_f - t_i
    avg_list.append(deltaT)

    avg_deltaT = sum(avg_list) / len(avg_list)
    avg_wpm = ((1 / avg_deltaT) * 60) / (word_avg + 1)

    t_i = t_f

#------------------------------------------------------------------------------------------
# Use tk to desplay words at top
# On bottom, display textbox to get user input


root = tk.Tk()
root.title("Speed Test")
root.geometry("800x500")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=1)

text_frame = ttk.LabelFrame(root, borderwidth=5, text="Text to Type", padding=15)
text_frame.grid(row=0, column=0, sticky="ew")


text_frame.columnconfigure(0, weight=1)
text_frame.rowconfigure(0, weight=1)

text_display = Text(
    text_frame,
    wrap="word",
    font=("Arial", 16),
    padx=12,
    pady=12
)
text_display.insert("1.0", paragraph)
text_display.config(state="disabled")
text_display.grid(row=0, column=0, sticky="nsew")


input_frame = ttk.LabelFrame(root, borderwidth=5, text="Type Here", padding=15)
input_frame.grid(row=1, column=0, sticky="nsew")

input_frame.columnconfigure(0, weight=1)  # textbox grows
input_frame.columnconfigure(1, weight=0)  # WPM stays fixed width
input_frame.rowconfigure(0, weight=1)

typing_box = Text(
    input_frame,
    wrap="word",
    font=("Arial", 16),
    padx=12,
    pady=12
)
typing_box.grid(row=0, column=0, sticky="nsew")

wpm_label = ttk.Label(input_frame, text="0 WPM", font=("Arial", 20))
wpm_label.grid(row=0, column=1, sticky="n", padx=(15, 0))

def update_wpm(event):
    time_inbetween_key(time.perf_counter())
    wpm_label.config(text=f"{round(avg_wpm)} WPM")

typing_box.bind("<KeyRelease>", update_wpm)

root.mainloop()
#------------------------------------------------------------------------------------------
