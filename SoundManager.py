import pygame
import os


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}

    def load_sounds(self, directory):
        try:
            for file_name in os.listdir(directory):
                if file_name.endswith('.wav') or file_name.endswith('.mp3'):
                    sound_path = os.path.join(directory, file_name)
                    self.sounds[file_name] = sound_path
        except Exception as e:
            print(f"Error loading sounds: {e}")

    def play_sound(self, sound_path):
        sound = pygame.mixer.Sound(sound_path)
        sound.play()

    def change_pitch(self, sound, semitones):
        return sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * (2.0 ** (semitones / 12.0)))
        }).set_frame_rate(sound.frame_rate)
