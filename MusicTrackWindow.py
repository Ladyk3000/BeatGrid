
import tkinter as tk
from tkinter import filedialog, messagebox
import json

from Cell import Cell
from SoundManager import SoundManager
from ui_components import create_sound_button, create_pitch_slider


class MusicTrackWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Track Window")

        self.bpm = 120  # Default BPM
        self.playing = False
        self.recording = False
        self.selected_sound = None
        self.selected_button = None
        self.grid_cells = []
        self.sound_colors = {}  # Dictionary to store colors for each sound
        self.cell_width = 50  # Width of each cell
        self.recorded_segments = []
        self.pitch_shifts = [0, 0, 0, 0]  # Pitch shifts for each row

        self.sound_manager = SoundManager()

        self.setup_ui()
        self.init_grid()
        self.animate()

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        self.top_frame = tk.Frame(self.main_frame, pady=10)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        self.setup_controls()
        self.setup_canvas()
        self.setup_sound_buttons()
        self.setup_pitch_controls()

    def setup_controls(self):
        tk.Label(self.top_frame, text="BPM").grid(row=0, column=0, padx=5)
        self.bpm_slider = tk.Scale(self.top_frame, from_=60, to=200, orient=tk.HORIZONTAL, command=self.update_bpm)
        self.bpm_slider.set(self.bpm)
        self.bpm_slider.grid(row=0, column=1, padx=5, sticky='ew')

        self.start_stop_button = tk.Button(self.top_frame, text="Start", command=self.toggle_playback)
        self.start_stop_button.grid(row=0, column=2, padx=5)

        self.rec_button = tk.Button(self.top_frame, text="Rec", command=self.toggle_recording)
        self.rec_button.grid(row=0, column=3, padx=5)

        self.add_column_button = tk.Button(self.top_frame, text="+", command=self.add_column)
        self.add_column_button.grid(row=0, column=4, padx=5)

        self.remove_column_button = tk.Button(self.top_frame, text="-", command=self.remove_column)
        self.remove_column_button.grid(row=0, column=5, padx=5)

    def setup_canvas(self):
        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, width=800, height=200, bg='white')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.config(xscrollcommand=self.scrollbar.set)

        self.line = self.canvas.create_line(0, 0, 0, 200, fill='red', width=2)
        self.position = 0

    def setup_sound_buttons(self):
        self.sound_frame = tk.Frame(self.main_frame, pady=10)
        self.sound_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.sound_buttons_frame = tk.Frame(self.sound_frame)
        self.sound_buttons_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.sound_manager.load_sounds("sound_directory")  # Update with your sound directory
        for i, (sound_file, sound_path) in enumerate(self.sound_manager.sounds.items()):
            create_sound_button(self.sound_buttons_frame, sound_file, sound_path, i, self.select_sound)

        self.pattern_frame = tk.Frame(self.sound_frame, pady=10)
        self.pattern_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.save_pattern_button = tk.Button(self.pattern_frame, text="Save Pattern", command=self.save_pattern)
        self.save_pattern_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.load_pattern_button = tk.Button(self.pattern_frame, text="Load Pattern", command=self.load_pattern)
        self.load_pattern_button.pack(side=tk.LEFT, padx=5, pady=5)

    def setup_pitch_controls(self):
        self.pitch_frame = tk.Frame(self.main_frame, pady=10)
        self.pitch_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.pitch_sliders = []
        for i in range(4):
            slider = create_pitch_slider(self.pitch_frame, f"Row {i + 1} Pitch", i, self.update_pitch)
            self.pitch_sliders.append(slider)

    def init_grid(self):
        self.track_length = 25  # Default length of track (number of cells)
        self.grid_cells = [[Cell() for _ in range(4)] for _ in range(self.track_length)]
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for col in range(self.track_length):
            for row in range(4):
                cell = self.grid_cells[col][row]
                cell.rect = self.canvas.create_rectangle(
                    col * self.cell_width, row * 50, (col + 1) * self.cell_width, (row + 1) * 50,
                    fill='white', outline='gray')
                if cell.sound:
                    color = self.sound_colors.get(cell.sound, 'yellow')
                    self.canvas.itemconfig(cell.rect, fill=color)
                self.canvas.tag_bind(cell.rect, '<Button-1>', lambda event, col=col, row=row: self.assign_sound_to_cell(col, row))
        self.line = self.canvas.create_line(0, 0, 0, 200, fill='red', width=2)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def update_bpm(self, value):
        self.bpm = int(value)

    def animate(self):
        if self.playing:
            self.position = (self.position + 1) % self.track_length
            self.update_canvas()
            self.play_sounds_at_position(self.position)
        self.root.after(int(60000 / self.bpm / 4), self.animate)

    def update_canvas(self):
        self.canvas.coords(self.line, self.position * self.cell_width, 0, self.position * self.cell_width, 200)
        self.canvas.update()

    def play_sounds_at_position(self, position):
        for row in range(4):
            cell = self.grid_cells[position][row]
            if cell.sound:
                self.sound_manager.play_sound(cell.sound)
                if self.recording:
                    sound_segment = AudioSegment.from_file(cell.sound)
                    shifted_sound = self.sound_manager.change_pitch(sound_segment, self.pitch_shifts[row])
                    self.recorded_segments.append(shifted_sound)

    def toggle_playback(self):
        self.playing = not self.playing
        self.start_stop_button.config(text="Stop" if self.playing else "Start")

    def toggle_recording(self):
        self.recording = not self.recording
        self.rec_button.config(text="Stop Rec" if self.recording else "Rec")
        if self.recording:
            self.recorded_segments = []
            self.blink_rec_button()

    def blink_rec_button(self):
        if self.recording:
            current_color = self.rec_button.cget("bg")
            next_color = "red" if current_color == "SystemButtonFace" else "SystemButtonFace"
            self.rec_button.config(bg=next_color)
            self.root.after(500, self.blink_rec_button)
        else:
            self.rec_button.config(bg="SystemButtonFace")

    def save_recording(self):
        if self.recorded_segments:
            full_recording = sum(self.recorded_segments)
            save_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                     filetypes=[("MP3 files", "*.mp3")],
                                                     initialdir=".",
                                                     title="Save Recording")
            if save_path:
                full_recording.export(save_path, format="mp3")
                messagebox.showinfo("Save Recording", f"Recording saved to {save_path}")

    def select_sound(self, sound_path, button):
        if self.selected_button:
            self.selected_button.config(bg=self.sound_colors[self.selected_sound])
        self.selected_sound = sound_path
        self.selected_button = button
        self.selected_button.config(bg='yellow')
        print(f"Selected sound: {sound_path}")

    def assign_sound_to_cell(self, col, row):
        cell = self.grid_cells[col][row]
        if cell.sound:
            cell.sound = None
            self.canvas.itemconfig(cell.rect, fill='white')
        else:
            cell.sound = self.selected_sound
            color = self.sound_colors[self.selected_sound]
            self.canvas.itemconfig(cell.rect, fill=color)
        print(f"Assigned {self.selected_sound} to cell ({col}, {row})")

    def add_column(self):
        new_column = [Cell() for _ in range(4)]
        self.grid_cells.append(new_column)
        self.track_length += 1
        self.draw_grid()

    def remove_column(self):
        if self.track_length > 1:
            self.grid_cells.pop()
            self.track_length -= 1
            self.draw_grid()
        else:
            messagebox.showwarning("Remove Column", "Cannot remove the last column.")

    def update_pitch(self, row, value):
        self.pitch_shifts[row] = int(value)

    def save_pattern(self):
        pattern = {'bpm': self.bpm, 'grid': [[cell.to_dict() for cell in column] for column in self.grid_cells], 'pitch_shifts': self.pitch_shifts}
        save_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json")],
                                                 initialdir=".",
                                                 title="Save Pattern")
        if save_path:
            with open(save_path, 'w') as f:
                json.dump(pattern, f)
            messagebox.showinfo("Save Pattern", f"Pattern saved to {save_path}")

    def load_pattern(self):
        load_path = filedialog.askopenfilename(defaultextension=".json",
                                               filetypes=[("JSON files", "*.json")],
                                               initialdir=".",
                                               title="Load Pattern")
        if load_path:
            with open(load_path, 'r') as f:
                pattern = json.load(f)
            self.bpm = pattern['bpm']
            self.bpm_slider.set(self.bpm)
            self.grid_cells = [[Cell.from_dict(cell_data) for cell_data in column] for column in pattern['grid']]
            self.pitch_shifts = pattern['pitch_shifts']
            for i in range(4):
                self.pitch_sliders[i].set(self.pitch_shifts[i])
            self.track_length = len(self.grid_cells)
            self.draw_grid()
            messagebox.showinfo("Load Pattern", f"Pattern loaded from {load_path}")
