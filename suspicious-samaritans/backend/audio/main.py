from pydub import AudioSegment
from pydub import playback
import os


audiofile = os.path.abspath('./samples/drums.wav')
extension = audiofile[audiofile.rfind('.') + 1:]

clip = AudioSegment.from_file(audiofile, format=extension)
# raw_bytes = clip.raw_data
total_frames = clip.frame_count()

# MODIFY THIS
samples = clip.get_array_of_samples()


playback.play(clip)
