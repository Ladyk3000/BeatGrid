import tkinter as tk
import random


def create_sound_button(parent, sound_file, sound_path, index,
                        select_sound_callback):
    color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255),
                                         random.randint(0, 255),
                                         random.randint(0, 255))
    button = tk.Button(parent, text=sound_file, bg=color,
                       command=lambda: select_sound_callback(sound_path,
                                                             button))
    button.grid(row=index // 2, column=index % 2, padx=5, pady=5, sticky='ew')


def create_pitch_slider(parent, label_text, row, command):
    label = tk.Label(parent, text=label_text)
    label.pack(pady=2)
    slider = tk.Scale(parent, from_=-12, to=12, orient=tk.HORIZONTAL,
                      command=lambda value: command(row, value))
    slider.pack(pady=2)
    return slider
