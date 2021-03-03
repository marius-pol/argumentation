from nltk.sem.logic import NegatedExpression


def conflicting(world, predicate):
    return (realized(world, predicate) and world.get_wanted_necessity(predicate) < 0) or (
            not realized(world, predicate) and world.get_wanted_necessity(predicate) > 0)


def possible(world, predicate):
    return not realized(world, predicate.negate()) or world.is_action(predicate)


def version_in_world(world, predicate):
    predicate = positive_version(predicate)
    if not realized(world, predicate):
        predicate = predicate.negate()

    return predicate


def realized(world, expression):
    if type(expression) is NegatedExpression and expression.negate() not in world.model:
        return True

    return expression in world.model


def positive_version(expression):
    if type(expression) is NegatedExpression:
        return expression.negate()
    else:
        return expression
