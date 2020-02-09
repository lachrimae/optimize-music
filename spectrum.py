from numpy import fft
import math

class Spectrum(list):
    LENGTH_OF_PLAY = 2.0 # in seconds
    HERZ_INTERVAL = 0.5
    MAX_HERZ = 44100
    BLUEPRINT = [0.0] * math.floor((1 + (LENGTH_OF_PLAY * MAX_HERZ / HERZ_INTERVAL)))

    def __init__(self):
        super().__init__(self.BLUEPRINT)
        self.nonzero_freqs = set()

    def __setitem__(self, freq : int, amp : float):
        if type(freq) != int or type(amp) != float:
            raise TypeError("Frequencies are integers and amplitudes must be floats.")
        elif amp < 0:
            raise ValueError("Amplitudes must be nonzero.")
        if freq not in self.nonzero_freqs and amp != 0.0:
            self.nonzero_freqs.add(freq)
        elif amp == 0.0:
            self.nonzero_freqs.remove(freq)
        super().__setitem__(freq, amp)

    def __add__(self, other):
        def getEither(container1, key1, container2, key2):
            first = container1[key1]
            if first != 0:
                return first
            else:
                return container2[key2]
        shared_freqs = intersection(self.nonzero_freqs, other.nonzero_freqs)
        unique_keys = difference(union(self.nonzero_freqs, other.nonzero_freqs), shared_keys)
        shared_dict = {freq: self[freq] + other[freq] for freq in shared_freqs} 
        unique_dict = {freq: getEither(self, freq, other, freq) for freq in unique_freqs}
        output = Spectrum()
        for (freq, amp) in {**unique_dict, **shared_dict}.items():
            output[freq] = amp

    def __mul__(self, scalar : float):
        if type(scalar) != float:
            raise TypeError
        new_freqs = {freq: self[freq] * val for freq in self.nonzero_freqs}
        output = Spectrum()
        for (freq, val) in new_freqs.items():
            output[freq] = val
        return output

    def as_wave(self):
        formattedForNumpy = [0.0, *self]
        return list(map(lambda x: float(x), fft.ifft(formattedForNumpy)))

# A Voice is a spectrum relative to a fundamental, which must remain at amplitude 1.0.
class Voice(Spectrum):
    def __init__(self):
        super().__init__()
        self[0] = 1.0
        
    def __setitem__(self, freq : int, amp : float):
        if freq == 0 and amp != 1.0:
            raise ValueError("The fundamental of a voice must remain at amplitude 1.0")
        super().__setitem__(freq, amp)
