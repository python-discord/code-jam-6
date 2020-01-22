from pydub import AudioSegment
from pydub import playback
from pydub import effects
from pydub import scipy_effects
from pydub.utils import db_to_float, get_min_max_value
from scipy.signal import savgol_filter, symiirorder1, wiener, butter, filtfilt
from scipy import ndimage
import random
import numpy as np
import array
import sys
import os
import pathlib
import math
import matplotlib
import matplotlib.pyplot as plt

np.set_printoptions(threshold=sys.maxsize)
dev_path = pathlib.Path(__file__).parent.absolute()


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


def band_pass_filter(audioclip: AudioSegment, cutoff=500) -> AudioSegment:
    """
    Yeah I just rewrapped the pydub's band_pass_filter. Fight me. 
    """

    audioclip = scipy_effects.low_pass_filter(audioclip, cutoff)
    audioclip = scipy_effects.high_pass_filter(audioclip, cutoff)
    
    return audioclip


def sine_filter(audioclip: AudioSegment, intensity=0, overlay_gain=10) -> AudioSegment:

    samples = audioclip.get_array_of_samples()
    audio_array = array.array(audioclip.array_type, samples)

    for i in range(1, int(audioclip.frame_count())):
        for j in range(audioclip.channels):
            # offset allows us to iterate theough the audio data by channel 

            offset = (i * audioclip.channels) + j
            stored_val = audio_array[offset]
            audio_array[offset] = int(math.sin(stored_val) * stored_val)

    static_clip = audioclip._spawn(data=audio_array)
    static_clip -= 20 + intensity

    mixed = audioclip.overlay(
        static_clip, 
        gain_during_overlay=overlay_gain
    )


    return mixed


def lofi_filter(audioclip: AudioSegment, cutoff=500) -> AudioSegment:
    """
    Yeah I just rewrapped the pydub's band_pass_filter. Fight me. 
    """

    audioclip = scipy_effects.low_pass_filter(audioclip, cutoff)
    audioclip = scipy_effects.high_pass_filter(audioclip, cutoff)
    
    return audioclip


def generate_pitch(hertz: int, length: int, channels=2, amplitude=500) -> AudioSegment:
    
    audioclip = AudioSegment(
        data=b'',
        sample_width=2,
        frame_rate=44100,
        channels=channels
    )

    audio_array = array.array('h', ([0] * (length * audioclip.frame_rate)))
    RPS = (audioclip.frame_rate / hertz) * channels

    for i in range(len(audio_array)):
        # sine_skew is the coefficent we multiply by to get the correct frequency 
        # of 440 hertz per second. We divide the regular period of 360 by the 
        # revolutions per second sine functions we want
        sine_skew = 360 / RPS

        # math.sin(math.radians(i)) creates a sine with a peroid of 2 pi (360 deg), which is multiplied
        # by the frequency we want
        audio_array[i] = int(amplitude * math.sin(math.radians(i) * sine_skew))
    

    return audioclip._spawn(data=audio_array)


def pitch_shift(audioclip: AudioSegment, hertz: int, amplitude=500) -> AudioSegment:
    
    audio_array = array.array('h', audioclip.get_array_of_samples())
    RPS = (audioclip.frame_rate / hertz) * audioclip.channels

    for i in range(len(audio_array)):
        # sine_skew is the coefficent we multiply by to get the correct frequency 
        # of 440 hertz per second. We divide the regular period of 360 by the 
        # revolutions per second sine functions we want
        sine_skew = 360 / RPS

        # math.sin(math.radians(i)) creates a sine with a peroid of 2 pi (360 deg), which is multiplied
        # by the frequency we want
        #print(int(100 * math.sin(math.radians(i) * sine_skew)))
        # print(int(audio_array[i] * math.sin(math.radians(i) * sine_skew)))
        audio_array[i] = int(audio_array[i] * math.sin(math.radians(i) * sine_skew))
    
    plt.plot([audio_array[i] for i in range(100000, 101000)])
    plt.show()

    return audioclip._spawn(data=audio_array)



def detuner(audioclip: AudioSegment, frequency: int) -> AudioSegment:

    samples = audioclip.get_array_of_samples()
    audio_array = array.array(audioclip.array_type, samples)

    frequency = (frequency * len(audioclip)) / audioclip.frame_rate

    for i in range(1, int(audioclip.frame_count())):
        for j in range(audioclip.channels):
            # offset allows us to iterate theough the audio data by channel 
            offset = (i * audioclip.channels) + j
            phaser_offset = math.sin((frequency) * math.radians(offset))

            stored_val = audio_array[offset]
            audio_array[offset] = int(phaser_offset * stored_val)


    plt.plot([audio_array[i] for i in range(100000, 101000)])
    plt.show()

    return audioclip._spawn(data=audio_array)



def phaser(audioclip: AudioSegment, frequency: int) -> AudioSegment:

    samples = audioclip.get_array_of_samples()
    audio_array = array.array(audioclip.array_type, samples)

    for i in range(1, int(audioclip.frame_count())):
        for j in range(audioclip.channels):
            # offset allows us to iterate theough the audio data by channel 
            offset = (i * audioclip.channels) + j
            phaser_offset = math.sin((1 / frequency) * math.radians(offset))

            stored_val = audio_array[offset]
            audio_array[offset] = int(phaser_offset * stored_val)


    plt.plot([audio_array[i] for i in range(100000, 101000)])
    plt.show()

    return audioclip._spawn(data=audio_array)


def compression_filter(audioclip: AudioSegment, cutoff: int) -> AudioSegment:
    """
    Yeah I just rewrapped the pydubs band_pass_filter. Fight me. 
    """
    # audioclip = audioclip.band_pass_filter(200, 500, order=3)

    sample_freq = audioclip.frame_rate
    samples = audioclip.get_array_of_samples()
    audio_array = array.array(audioclip.array_type, samples)

    freq_cutoff = cutoff
    normalizer = freq_cutoff / (sample_freq / 2)

    plt.plot([audio_array[i] for i in range(100000, 101000)])
    
    prev_val = [0] * audioclip.channels

    for i in range(1, int(audioclip.frame_count())):
        for j in range(audioclip.channels):
            # offset allows us to iterate theough the audio data by channel 
            offset = (i * audioclip.channels) + j
            if audio_array[offset] > 200:
                audio_array[offset] -= int(math.log(audio_array[offset]) * cutoff)
            if audio_array[offset] < -200:
                audio_array[offset] += int(math.log(-audio_array[offset]) * cutoff)

    plt.plot([audio_array[i] for i in range(100000, 101000)])
    plt.show()

    audioclip = audioclip._spawn(data=audio_array)
    
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



def main():
    file = AudioSegment.from_file("./assets/samples/nocture.wav")
    yay = pitch_shift(file, 666)
    playback.play(yay)
    

main()