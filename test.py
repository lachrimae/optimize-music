import math
from spectrum import *
import scipy.io.wavfile as wavf
import numpy as np

def signum(x):
    return math.copysign(1,x)

def main():
    s1, s2 = Spectrum(), Spectrum()
    s1[880], s2[440] = 1.0, 1.0
    wav = s1.as_wave()
    for n in range(2, len(wav)):
        before2 = float(wav[n-2])
        before1 = float(wav[n-1])
        if abs(before1) < abs(before2) and abs(before1) < abs(wav[n]) and signum(before2) != signum(wav[n]):
            print(n)

    maxLevel = max(list(map(lambda x: abs(x), wav)))
    wav = np.array(list(map(lambda x: x / maxLevel, wav)))
    # consult https://stackoverflow.com/questions/33213408/python-convert-an-array-to-wav
    wavf.write('test.wav', 44100, wav)
    # Success! After observing this, it has periodic zeros. Is the rest of the function periodic-ish? Better listen to it to find out!

if __name__ == '__main__':
    main()
