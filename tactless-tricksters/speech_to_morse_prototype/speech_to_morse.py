from typing import List

import numpy as np
import matplotlib.pyplot as plt
from pyaudio import PyAudio, paInt16
from scipy.io import wavfile
np.seterr(all='raise')
CHUNK = 4000
DATA_RATE = 400
RATE = 16000
NUM_BITS_PER_CHUNK = int(CHUNK/DATA_RATE)
NUM_BITS_PER_SEC = int(RATE/DATA_RATE)
NUM_CHANNELS = 1
active_threshold = 15

DOT_DURATION_THRESHOLD_MS = .08
DASH_DURATION_THRESHOLD_MS = .24
LETTER_END_DURATION_THRESHOLD_MS = .24
WORD_END_DURATION_THRESHOLD_MS = .56

DOT_DURATION_THRESHOLD_BIT = int(DATA_RATE*DOT_DURATION_THRESHOLD_MS/NUM_BITS_PER_CHUNK)
DASH_DURATION_THRESHOLD_BIT = int(DATA_RATE*DASH_DURATION_THRESHOLD_MS/NUM_BITS_PER_CHUNK)
LETTER_END_DURATION_THRESHOLD_BIT = int(DATA_RATE*LETTER_END_DURATION_THRESHOLD_MS/NUM_BITS_PER_CHUNK)
WORD_END_DURATION_THRESHOLD_BIT = int(DATA_RATE*WORD_END_DURATION_THRESHOLD_MS/NUM_BITS_PER_CHUNK)


class MorseSpeechToText:
    def __init__(self, debug=False, debug_plot=False):
        self.debug = debug
        self.debug_plot = debug_plot
        self.channels = NUM_CHANNELS
        self.pa = PyAudio()
        self.stream = self.pa.open(format=paInt16,
                                   channels=NUM_CHANNELS,
                                   rate=RATE,
                                   input=True,
                                   input_device_index=-1,
                                   frames_per_buffer=CHUNK)

    def run(self):
        try:
            old_buffer = np.array([])
            while True:
                data = np.frombuffer(self.stream.read(CHUNK), dtype=np.int16).astype(float)
                speech_activity_vec = np.concatenate((old_buffer, self.get_voice_activity(data)))
                morse_code, old_buffer = self.activity_to_morse(speech_activity_vec)
                if morse_code:
                    print(' '.join(morse_code), end=' ')
        finally:
            self.stream.close()
            self.pa.terminate()

    def run_wav(self, audio_path):
        fs, x = wavfile.read(audio_path)
        x = x.astype(float)
        old_buffer = np.array([])
        for i in range(0, len(x)-CHUNK, CHUNK):
            data = x[i:i+CHUNK]
            speech_activity_vec = np.concatenate((old_buffer, self.get_voice_activity(data)))
            morse_code, old_buffer = self.activity_to_morse(speech_activity_vec)
            if morse_code:
                print(''.join(morse_code), end='')

    def get_voice_activity(self, data):
        data_reshaped = data.reshape((NUM_BITS_PER_CHUNK, DATA_RATE))
        intensity = np.log(np.mean(data_reshaped ** 2, axis=1))
        speech_activity = (intensity > active_threshold).astype(int)
        if self.debug:
            print(f'max intensity: {max(intensity)}')
            print(f'min intensity: {min(intensity)}')
        if self. debug_plot:
            plt.plot(np.arange(len(data)) / RATE, (data-min(data))/(max(data)-min(data)))

        return speech_activity

    def activity_to_morse(self, active_vec):
        morse: List[str] = []
        # vector of indices where the signal went from 1/0 to 0/1
        onoffset_indices = np.concatenate(([0], np.where(np.diff(active_vec) != 0)[0]+1))
        # a vector of len of segment between on/offset
        segment_durations = np.diff(onoffset_indices)
        is_active_vec = active_vec[onoffset_indices]

        # for each segment of consecutive data value if the segment exceeds the duration threshold set morse value
        for seg_dur, is_active in zip(segment_durations, is_active_vec):
            if is_active:
                if seg_dur >= DASH_DURATION_THRESHOLD_BIT:
                    morse.append('-')
                else:
                    morse.append('.')
            else:
                if seg_dur >= WORD_END_DURATION_THRESHOLD_BIT:
                    morse.append(' ')
                elif seg_dur >= LETTER_END_DURATION_THRESHOLD_BIT:
                    morse.append(' ')
        # keep the last segment to be stitched to the next frame
        old_buffer = active_vec[onoffset_indices[-1]:]
        trunc_len = min(len(old_buffer), WORD_END_DURATION_THRESHOLD_BIT)
        old_buffer = old_buffer[-trunc_len:]

        if self.debug:
            print('speech activity vec: ' + str(active_vec))
            print('onoffset_indices: ' + str(onoffset_indices))
            print('segment_durations: ' + str(segment_durations))
            print('old buffer: ' + str(old_buffer))
        if self.debug_plot:
            plt.plot(np.arange(0, len(active_vec)) / 40, active_vec)
            plt.show()
        return morse, old_buffer


if __name__ == "__main__":
    ms = MorseSpeechToText(debug=False, debug_plot=False)
    # ms.run()
    ms.run_wav(r'morse_code_alphabet_16k.wav')
