import collections
import spectrum
import log_additive

class Spectra(list):
    def __init__(self, spectra=None):
        if spectra is not None
            if type(spectra) is list and any([type(s) is not spectrum.Spectrum for s in spectra]):
                raise TypeError
            super().__init__(spectra)
        else:
            super().__init__()
        # The evil cache.
        # To be convinced of its evilness, look at interpolate_samples().
        # However, I expect this to be a single-process app so shared state is not the concern.
        self._as_samples = None

    def __setitem__(self, index : int, spect : spectrum.Spectrum):
        if not type(spect) is spectrum.Spectrum:
            raise TypeError
        self._as_samples = None
        super().__setitem__(index, spect)

    def calculate_samples(self):
        self._as_samples = [s.as_wave() for s in self]
        return self._as_samples
    
    def interpolate_samples(self, ratio : int, func):
        # ratio = 2 would put one sample in between every two original samples.
        # ratio = 3 would put two samples, etc.
        # func should implement the interface
        # of log_additive.interpolate(x1, x2, l) =~ l*x1 + (1-l)*x2.
        # It should share the property that func(x1, x2, 0) == x1 and func(x1, x2, 1) == x2.
        # TODO: Maybe write this interface into a class?
        s = self.calculate_samples()
        # Use list.pop() with deque.leftappend() to avoid the quadratic complexity of lift.append()
        interpolated_samples = collections.deque()
        for i in range(len(s) - 1):
            keyframe1 = s.pop()
            keyframe2 = s.pop()
            interpolated_samples.leftappend(keyframe1)
            middle_frames = list()
            for i in range(1, ratio):
                t = i / ratio
                new_sample = func(keyframe1, keyframe2, t)
                interpolated_samples.appendleft(new_sample)
            interpolated_samples.leftappend(keyframe2)
        return list(interpolated_samples)
