import tkinter as tk
from tkinter import ttk, Text
import time
import requests

# Text() object left, timer right
# 10 second timer auto starts
# Function checks every so often (always?) if there was a word added using api
# have before text and after text.
# subtract texts. If the remaing words from after text are actual words than reset timer. Else, dont stop time.
# while loop?
# If timer hits 0, delete text and reset timer
# ----------------------------------------------------------------------------------------------------------------------
time_limit = 10
deadline = None
timer_running = False
previous_word_count = 0

def reset_timer(event=None):
    global deadline, timer_running

    deadline = time.perf_counter() + time_limit

    if not timer_running:
        timer_running = True
        update_timer()

def update_timer():
    global timer_running

    if deadline is None:
        return

    remaining = deadline - time.perf_counter()


    if remaining <= 0:
        text_display.delete("1.0", "end")
        timer.config(text="0")
        timer_running = False
        return

    timer.config(text=str(round(remaining, 1)))
    root.after(100, update_timer)

def check_for_new_word(event=None):
    global previous_word_count

    raw_text = text_display.get("1.0", "end-1c")
    words = raw_text.split()
    current_word_count = len(words)

    if current_word_count > previous_word_count:
        reset_timer()

    previous_word_count = current_word_count

# ----------------------------------------------------------------------------------------------------------------------
root = tk.Tk()
root.title("Write or Die")


root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=0)

text_frame = tk.LabelFrame(root, text="Write Here!", padx=10, pady=10)
text_frame.grid(column=0, row=0, sticky="nsw")

text_display = Text(
    text_frame,
    wrap="word",
    font=("Arial", 16),
    padx=12,
    pady=12
)
text_display.grid(row=0, column=0, sticky="nsew")


right_frame = tk.LabelFrame(root, text="Timer", padx=10, pady=10)
right_frame.grid(column=3, row=0, sticky="nse")

timer = tk.Label(right_frame, text=f"10", font=("Arial", 48), padx=10, pady=10)
timer.grid(column=0, row=0, sticky="n")

start_btn = tk.Button(right_frame, text="Start", padx=10, pady=10, command=reset_timer)
start_btn.grid(column=0, row=1, sticky="s")

text_display.bind("<KeyRelease>", check_for_new_word)
root.mainloop()