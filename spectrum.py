import numpy as np
from numpy import fft
import math

class Spectrum(list):
    BLUEPRINT = [0.0] * 44100

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
        shared_freqs = self.nonzero_freqs & other.nonzero_freqs
        unique_freqs = self.nonzero_freqs ^ other.nonzero_freqs
        shared_dict = {freq: self[freq] + other[freq] for freq in shared_freqs} 
        unique_dict = {freq: getEither(self, freq, other, freq) for freq in unique_freqs}
        output = Spectrum()
        for (freq, amp) in {**unique_dict, **shared_dict}.items():
            output[freq] = amp
        return output
    
    def __mul__(self, other):
        if type(other) == float:
            scalar = other
            new_freqs = {freq: self[freq] * val for freq in self.nonzero_freqs}
            output = Spectrum()
            for (freq, val) in new_freqs.items():
                output[freq] = val
            return output
        elif isinstance(other, Spectrum):
            if len(self.nonzero_freqs) > len(other.nonzero_freqs):
                s1 = other
                s2 = self
            else:
                s1 = self
                s2 = other
            return sum([s1[freq] * s2[freq] for freq in s1.nonzero_freqs])

    def as_wave(self):
        formattedForNumpy = np.asarray([0.0, *self], dtype=np.int16)
        return list(map(lambda x: x.real, fft.ifft(formattedForNumpy)))

    def __abs__(self, p):
        if p == float('inf'):
            return max(list(map(abs, self)))

        if p < 1:
            raise ValueError("The p-norm exists for p in [1, inf].")
        
        accum = 0.0
        for elt in self:
            accum += abs(elt)**p
        return accum**(1/p)

    def __abs__(self):
        return abs(self, 2)

# A Voice is a spectrum relative to a fundamental, which must remain at amplitude 1.0.
class Voice(Spectrum):
    def __init__(self):
        super().__init__()
        self[0] = 1.0
        
    def __setitem__(self, freq : int, amp : float):
        if freq == 0 and amp != 1.0:
            raise ValueError("The fundamental of a voice must remain at amplitude 1.0")
        super().__setitem__(freq, amp)
