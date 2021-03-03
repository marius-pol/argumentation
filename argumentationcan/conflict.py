class Conflict:
    def __init__(self, predicate, necessity, negation_phase=False):
        self.__predicate = predicate
        self.__necessity = necessity
        self.__negation_phase = negation_phase

    @property
    def predicate(self):
        return self.__predicate

    @property
    def necessity(self):
        return self.__necessity

    @property
    def negation_phase(self):
        return self.__negation_phase

    @negation_phase.setter
    def negation_phase(self, value):
        self.__negation_phase = value

    def __str__(self):
        return '{0} ({1})'.format(self.__predicate, self.__necessity)
