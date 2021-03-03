from argumentationcan.conflict import Conflict

computed_necessities = {}
plan = []


def get_computed_necessity(predicate):
    necessity = computed_necessities.get(predicate, 0)

    if necessity == 0:
        necessity = -computed_necessities.get(predicate.negate(), 0)

    return necessity


def set_computed_necessity(predicate, value):
    if get_computed_necessity(predicate) != 0:
        if predicate in computed_necessities:
            del computed_necessities[predicate]
        if predicate.negate() in computed_necessities:
            del computed_necessities[predicate.negate()]

    computed_necessities[predicate] = value
