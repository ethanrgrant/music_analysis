import librosa
import numpy as np

class Song():

    def __init__(self, y, sr):
        self.y = y
        self.sr = sr
        self.s, self.log_S = self.calc_s()
        self.tuning = self.get_tuning()
        self.time = self.get_time()

    def calc_s(self):
        S = librosa.feature.melspectrogram(self.y, self.sr, n_mels=128)
        log_S = librosa.logamplitude(S, ref_power=np.max)
        return S, log_S

    def get_time(self):
        return librosa.core.get_duration(self.y, self.sr)

    def get_tuning(self):
        return librosa.core.estimate_tuning(self.y, self.sr)

    def print_output(self):
        print(self.tuning)
        print(self.time)