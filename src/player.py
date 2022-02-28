import os
import time
from threading import Thread
import pygame


class SynthPlayer(Thread):
    def __init__(self, sounds_path):
        Thread.__init__(self)
        self._chords_to_play = []
        self._chords_to_stop = []
        self.SOUND_FADE_MILLISECONDS = 0

        if "normal" in sounds_path:
            self.TONES = [-26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10,
             -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
             11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
        else:
            self.TONES = [-12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        self.sounds_path = sounds_path
        self._init_pygame()
        self.key_sounds = list(self._get_key_sounds())

    def run(self):
        while self.is_alive():
            for chord_index in self._chords_to_play:
                sound = self.key_sounds[chord_index]
                sound.stop()
                sound.play(fade_ms=50)

            for chord_index in self._chords_to_stop:
                sound = self.key_sounds[chord_index]
                sound.fadeout(700)
            time.sleep(0.05)

    def set_chords_to_play(self, chords):
        self._chords_to_play = chords

    def set_chords_to_stop(self, chords):
        self._chords_to_stop = chords

    def _get_key_sounds(self):
        sounds = []
        for tone in self.TONES:
            tone = str(tone)
            tone_path = os.path.join(self.sounds_path, tone+'.wav')
            sound = pygame.mixer.Sound(tone_path)
            sounds.append(sound)
        return sounds

    def _init_pygame(self):
        pygame.init()
        pygame.display.init()
        pygame.mixer.init(frequency=48000, size=32, channels=2)
