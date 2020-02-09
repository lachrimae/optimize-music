import math

def interpolate_abstract(f, x1, x2, l):
    return f(l*x2, (1-l)*x1)

def interpolate(x1, x2, l):
    return interpolate_abstract(lambda x: x, x1, x2, l)

def interpolate_decibels(x1, x2, l):
    return interpolate_abstract(add_decibels, x1, x2, l)

def log_add(x1, x2, coefficient, base, reference):
    relativePower = (x1 + x2) / reference
    return coefficient * math.log(relativePower, base)

def add_decibels(x1, x2):
    return log_add(x1, x2, 10.0, 2.0, 1e-12)

def add_decibels_under_ref(x1, x2, reference):
    return log_add(x1, x2, 10.0, 2.0, reference)
