from pydub import AudioSegment
from pydub import playback
from pydub import scipy_effects
from scipy.signal import savgol_filter, symiirorder1, wiener
from scipy import ndimage
import random
import numpy as np
import array
import sys
import os

np.set_printoptions(threshold=sys.maxsize)
dev_path = os.getcwd()


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


def record_pop_filter(audioclip: AudioSegment, overlay_gain=0, effect_gain=0) -> AudioSegment:
    """
    Function to generate a static record-pop noise
    """

    effect_path = os.path.join(dev_path, "./assets/effects/static_3.wav")
    effectsclip = AudioSegment.from_file(effect_path)
    effectsclip += effect_gain

    mixed = audioclip.overlay(
        effectsclip, 
        loop=True, 
        gain_during_overlay=overlay_gain
    )

    return mixed


def bandpass_filter(audioclip: AudioSegment) -> AudioSegment:
    """
    Yeah I just rewrapped the pydubs band_pass_filter. Fight me. 
    """

    audioclip = audioclip.band_pass_filter(200, 500, order=3)
    return audioclip


def audio_medfilt_filter(audioclip: AudioSegment) -> AudioSegment:
    """
    This gives the audio a "compressed" quality
    """

    samples = audioclip.get_array_of_samples()
    audio_array = array.array(audioclip.array_type, samples)

    audio_array = ndimage.median_filter(audio_array, size=10, mode='wrap')

    mixed_array = array.array(audioclip.array_type, audio_array)
    mixed = audioclip._spawn(mixed_array)

    return mixed


def audio_spline_filter(audioclip: AudioSegment) -> AudioSegment:
    """
    This gives the audio a "compressed" quality
    """

    samples = audioclip.get_array_of_samples()
    audio_array = array.array(audioclip.array_type, samples)

    audio_array = wiener(audio_array)
    audio_array = audio_array.astype(int)
    print(audio_array[:1000])

    mixed_array = array.array(audioclip.array_type, audio_array)
    mixed = audioclip._spawn(mixed_array)

    return mixed


def main():
    file = AudioSegment.from_file("./assets/samples/nocture.wav")
    yay = record_pop_filter(bandpass_filter(file))
    playback.play(yay)

main()