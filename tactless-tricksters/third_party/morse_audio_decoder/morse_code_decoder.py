from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave
import struct
import numpy as np

THRESHOLD = 300
chunk = 1024
FORMAT = pyaudio.paInt16
RATE = 48000
window = np.blackman(chunk)
FREQ = 700
HzVARIANCE = 20
ALLOWANCE = 3
WINDOW = 160

letter_to_morse = {
    "a": ".-", "b": "-...", "c": "-.-.",
    "d": "-..", "e": ".", "f": "..-.",
    "g": "--.", "h": "....", "i": "..",
    "j": ".---", "k": "-.-", "l": ".-..",
    "m": "--", "n": "-.", "o": "---",
    "p": ".--.", "q": "--.-", "r": ".-.",
    "s": "...", "t": "-", "u": "..-",
    "v": "...-", "w": ".--", "x": "-..-",
    "y": "-.--", "z": "--..", "1": ".----",
    "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----.", "0": "-----",
    " ": "/"}

class MorseCodeDecoder(object):
    def __int__(self):
        self.stop = False

    def is_silent(self, snd_data):
        "Returns 'True' if below the 'silent' threshold"
        return max(snd_data) < THRESHOLD


    def normalize(self, snd_data):
        "Average the volume out"
        # 32768 maximum /2
        MAXIMUM = 16384
        times = float(MAXIMUM) / max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i * times))
        return r


    def encode(self, list1):
        list1 = list1.split("0")
        # print(list1);
        listascii = ""
        counter = 0

        for i in range(len(list1)):
            if len(list1[i]) == 0:  # blank character adds 1
                counter += 1
            else:
                if counter < ALLOWANCE:
                    list1[i] += list1[i - counter - 1]
                    list1[i - counter - 1] = ""
                counter = 0

        # print(list1)

        for i in range(len(list1)):
            if len(list1[i]) >= 20 and len(list1[i]) < 50:  # 200-490 ms dah, throws values >50
                listascii += "-"
                counter = 0
            elif len(list1[i]) < 20 and len(list1[i]) > 5:  # 50-190ms is dit
                listascii += "."
                counter = 0
            elif len(list1[i]) == 0:  # blank character adds 1
                counter += 1
                if 40 < counter < 50 and len(list1[i + 1]) != 0:  # 370 ms blanks is letter space
                    listascii += " "
                    counter = 0
                elif counter == 80:  # 80 ms blanks is word space
                    listascii += "  "
                    counter = 0

        listascii = listascii.split(" ")
        # print(listascii)

        stringout = ""

        for i in range(len(listascii)):
            for letter, morse in letter_to_morse.items():
                if listascii[i] == morse:
                    stringout += letter
            if listascii[i] == "":
                stringout += " "

        if (stringout != " "):
            print(stringout)

        # print("record start")
        # record()

    def record(self):
        num_silent = 0
        snd_started = False
        oncount = 0
        offcount = 0
        status = 0
        timelist = ""

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=1,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=chunk)

        # r = array('h')
        print("started")
        self.stop = False
        while not self.stop:

            snd_data = stream.read(chunk, exception_on_overflow=False)

            if byteorder == 'big':
                snd_data.byteswap()

            # r.extend(snd_data)
            sample_width = p.get_sample_size(FORMAT)

            # find frequency of each chunk
            indata = np.array(wave.struct.unpack("%dh" % (chunk), snd_data)) * window

            # take fft and square each value
            fftData = abs(np.fft.rfft(indata)) ** 2

            # find the maximum
            which = fftData[1:].argmax() + 1
            silent = self.is_silent(indata)

            if silent:
                thefreq = 0
            elif which != len(fftData) - 1:
                y0, y1, y2 = np.log(fftData[which - 1:which + 2:])
                x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
                # find the frequency and output it
                thefreq = (which + x1) * RATE / chunk
            else:
                thefreq = which * RATE / chunk
            # print(thefreq)

            if thefreq > (FREQ - HzVARIANCE) and thefreq < (FREQ + HzVARIANCE):
                status = 1
                # print("1")
            else:
                status = 0
                # print("0")

            if status == 1:
                timelist += "1"
                num_silent = 0

            else:
                timelist += "0"
                num_silent += 1

            if num_silent > WINDOW and "1" in timelist:
                # print(timelist)
                # print("\n")
                # stream.stop_stream()
                # stream.close()
                self.encode(timelist)
                timelist = ""

            if num_silent > 1000:
                print("reset")
                num_silent = 0

        # print (timelist)
        print("ended")
        print(num_silent)
        p.terminate()

if __name__ == "__main__":
    mcd = MorseCodeDecoder()
    mcd.record()