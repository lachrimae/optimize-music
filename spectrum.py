import numpy as np
from numpy import fft
import math

# A Spectrum() is essentially just a list()
class Spectrum(list):
    # Here we memoize the zeroed-out prototype for an empty Spectrum()
    BLUEPRINT = [0.0] * 44100

    def __init__(self):
        # TODO: write a copy constructor.
        super().__init__(self.BLUEPRINT)
        # We should expect most frequencies to be at zero amplitude most of the time.
        # The following variable keeps track of the "support" of our vector, and we can restrict
        # many calculations to just these frequencies.
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

    # Vector addition.
    def __add__(self, other):
        # getEither is a utility function for defining unique_dict later.
        def getEither(container1, key1, container2, key2):
            first = container1[key1]
            if first != 0:
                return first
            else:
                return container2[key2]
        shared_freqs = self.nonzero_freqs & other.nonzero_freqs
        unique_freqs = self.nonzero_freqs ^ other.nonzero_freqs
        # the keys of shared_dict and unique_dict will be added to create our output value.
        shared_dict = {freq: self[freq] + other[freq] for freq in shared_freqs} 
        unique_dict = {freq: getEither(self, freq, other, freq) for freq in unique_freqs}
        output = Spectrum()
        for (freq, amp) in {**unique_dict, **shared_dict}.items():
            output[freq] = amp
        return output
    
    # Supports scalar and inner products.
    def __mul__(self, other):
        # This is scalar multiplication.
        if type(other) == float:
            scalar = other
            new_freqs = {freq: self[freq] * val for freq in self.nonzero_freqs}
            output = Spectrum()
            for (freq, val) in new_freqs.items():
                output[freq] = val
            return output
        # This is the inner product associated with the 2-norm. 
        elif isinstance(other, Spectrum):
            # The order of operations matters if one Spectrum() has a much
            # larger support than the other.
            if len(self.nonzero_freqs) > len(other.nonzero_freqs):
                s1 = other
                s2 = self
            else:
                s1 = self
                s2 = other
            return sum([s1[freq] * s2[freq] for freq in s1.nonzero_freqs])

    def as_wave(self):
        # set the DC value at index 0 to 0.0
        formattedForNumpy = np.asarray([0.0, *self], dtype=np.int16)
        return list(map(lambda x: x.real, fft.ifft(formattedForNumpy)))

    # Define the general p-norm
    def __abs__(self, p):
        if p == float('inf'):
            return max(list(map(abs, self)))
        if p < 1:
            raise ValueError("The p-norm exists for p in [1, inf].")
        accum = 0.0
        for elt in self:
            accum += abs(elt)**p
        return accum**(1/p)

    # The default norm is the standard Euclidean norm, or 2-norm.
    # We can also think of this as the Hilbert space norm.
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
