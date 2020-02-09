import math
from spectrum import *
import scipy.io.wavfile as wavf
import numpy as np

def signum(x):
    return math.copysign(1,x)

def writeWav(fname, wav):
    maxLevel = max(list(map(lambda x: abs(x), wav)))
    wav = np.array(list(map(lambda x: x / maxLevel, wav)))
    # consult https://stackoverflow.com/questions/33213408/python-convert-an-array-to-wav
    wavf.write(fname, 44100, wav)
    # Success! After observing this, it has periodic zeros. Is the rest of the function periodic-ish? Better listen to it to find out!

def main():
    s1, s2 = Spectrum(), Spectrum()
    s1[880], s2[440] = 1.0, 1.0
    s3 = s1 + s2
    writeWav('440.wav', s1.as_wave())
    writeWav('880.wav', s2.as_wave())
    writeWav('sum.wav', s3.as_wave())

    s1Zeros = len(list(filter(lambda x: x == 0, s1)))
    s2Zeros = len(list(filter(lambda x: x == 0, s2)))
    if s1Zeros == s2Zeros:
        print('overlapping zeros')
    else:
        print('non-overlapping zeros')

if __name__ == '__main__':
    main()
