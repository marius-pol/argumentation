from world import read_expr


class Action:
    def __init__(self, name, preconditions, effects_plus, effects_minus):
        self.__name = name
        self.__predicate = read_expr(self.__name)
        self.__preconditions = preconditions
        self.__effects_minus = effects_minus
        self.__effects_plus = effects_plus

    @property
    def name(self):
        return self.__name

    @property
    def predicate(self):
        return self.__predicate

    @property
    def preconditions(self):
        return self.__preconditions

    @property
    def effects_plus(self):
        return self.__effects_plus

    @property
    def effects_minus(self):
        return self.__effects_minus

    def __str__(self):
        return self.__name

    def __eq__(self, other):
        if isinstance(other, Action):
            return self.predicate == other.predicate
        return False

    def __hash__(self):
        return hash(self.name)
