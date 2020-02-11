import math
from spectrum import *
import scipy.io.wavfile as wavf
import numpy as np
import wave

def signum(x):
    if x == 0.0:
        return 0.0
    return math.copysign(1, x)

def writeWav(fname, wav):
    maxLevel = max(list(map(lambda x: abs(x), wav)))
    wav = np.array(list(map(lambda x: x / maxLevel, wav)))
    # consult https://stackoverflow.com/questions/33213408/python-convert-an-array-to-wav
    wavf.write(fname, 44100, wav)

def main():
    s1, s2 = Spectrum(), Spectrum()
    s1[888], s2[440] = 1.0, 1.0
    s3 = s1 + s2
    writeWav('888.wav', s1.as_wave())
    writeWav('440.wav', s2.as_wave())
    writeWav('sum.wav', s3.as_wave())

    triangle_wave = Spectrum()
    # it must be the case that an empty Spectrum() added to another Spectrum() gives another empty spectrum.
    for n in range(1, 200):
        triangle_wave = triangle_wave + triangle(220, n)

    writeWav('triangle.wav', triangle_wave.as_wave())

def triangle(fundamental, overtoneNum):
    t = Spectrum()
    t[fundamental*overtoneNum] = 1.0 / float(overtoneNum)
    return t

if __name__ == '__main__':
    main()

