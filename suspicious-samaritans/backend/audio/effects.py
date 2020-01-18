from pydub import AudioSegment
from pydub import playback
from scipy.signal import savgol_filter, symiirorder1
import random
import numpy as np
import array
import sys
import os

np.set_printoptions(threshold=sys.maxsize)


def static_filter(audioclip: AudioSegment, intensity: int) -> AudioSegment:
    """
    Overlays random noise over the given AudioSegment
    """

    samples = audioclip.get_array_of_samples()

    for i in range(len(samples)):
        samples[i] += random.randint(-intensity, +intensity)

    mixed_array = array.array(audioclip.array_type, samples)
    mixed = audioclip._spawn(mixed_array)

    return mixed


def record_pop(audioclip: AudioSegment, overlay_gain=0, effect_gain=0) -> AudioSegment:
    """
    Function to generate a static record-pop noise
    """

    effect_path = os.path.abspath("./assets/effects/static_3.wav")
    effectsclip = AudioSegment.from_file(effect_path)
    effectsclip += effect_gain

    mixed = audioclip.overlay(effectsclip, loop=True, gain_during_overlay=overlay_gain)

    return mixed


def audio_savgol_filter(audioclip: AudioSegment) -> AudioSegment:

    samples = audioclip.get_array_of_samples()
    audio_array = np.array(samples)

    audio_array = savgol_filter(audio_array, 69, 2)
    mixed = audioclip._spawn(audio_array.astype(int))

    return mixed


def audio_symiirorder1_filter(audioclip: AudioSegment, c0: float, z1: float) -> AudioSegment:

    samples = audioclip.get_array_of_samples()
    audio_array = np.array(samples)

    audio_array = symiirorder1(audio_array, c0, z1)
    mixed = audioclip._spawn(audio_array.astype(int))

    return mixed


def main():
    file = AudioSegment.from_file("./assets/samples/nocture.wav")
    playback.play(record_pop(file))
