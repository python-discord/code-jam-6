from pydub import AudioSegment
from pydub import playback
import os
import random
import array
from scipy import signal
from scipy.io.wavfile import read

audiofile = os.path.abspath('./assets/samples/drums.wav')
effect = os.path.abspath('./assets/effects/static_1.wav')

def load_file(path: str) -> AudioSegment:
    if '.' in path:
        extension = path[path.rfind('.') + 1:]
    clip = AudioSegment.from_file(path, format=extension)

<<<<<<< HEAD
clip = AudioSegment.from_file(audiofile, format=extension)
# raw_bytes = clip.raw_data
total_frames = clip.frame_count()

# MODIFY THIS
samples = clip.get_array_of_samples()
=======
    return clip


audio_clip = load_file(effect)
effect_clip = load_file(effect)

print(effect_clip.rms)

#MODIFY THIS
samples = effect_clip.get_array_of_samples()
print(type(samples))


"""
# now you have to convert back to an array.array
shifted_samples_array = array.array(effect_clip.array_type, samples)
>>>>>>> audio

new_sound = effect_clip._spawn(shifted_samples_array)

<<<<<<< HEAD
playback.play(clip)
=======
playback.play(new_sound)

"""
>>>>>>> audio
