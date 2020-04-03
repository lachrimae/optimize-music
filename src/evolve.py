class Population(set):
    # Allows initialization by copy, initialization by set and initialization by class.
    def __init__(self, kind, score_function, mating_strategy, combination_method):
        self.combination_method = combination_method
        self.score_function = score_function
        if type(kind) == type:
            self.kind = kind
        elif type(kind) == Population:
            self = kind
        elif type(kind) == set:
            if len(set) == 0:
                raise ValueError("Cannot deduce kind from an empty set.")
            else:
                # Check that every element of the input has the same type
                inputKind = None
                firstLoop = True
                for elt in kind:
                    if firstLoop:
                        inputKind = type(elt)
                        firstLoop = False
                    else:
                        if type(elt) != inputKind:
                            raise ValueError("Cannot take mixed types as input")
                self = kind
                self.kind = inputKind

    def iterate(self) -> Population:
        return
