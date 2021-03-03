import argumentationcan
from argumentationcan import Conflict

from argumentationcan.world import world_predicate


def solve_conflict(argumentation_world, conflict):
    print(('conflict on {0} with intensity {1}'.format(conflict.predicate, conflict.necessity)))

    if solution(argumentation_world, conflict):
        return True
    elif abduction(argumentation_world, conflict):
        return True
    elif not conflict.negation_phase:
        if negation(argumentation_world, conflict):
            return True
    elif revision(argumentation_world, conflict):
        return False
    else:
        give_up(conflict)
        return False


def start(argumentation_world):
    argumentationcan.plan = []
    argumentationcan.computed_necessities ={}

    conflict = argumentation_world.current_conflict()

    while conflict is not None:
        print('\n(Re)start procedure in argumentation_world {0}'.format(
            ' & '.join([str(p) for p in argumentation_world.model])))
        solve_conflict(argumentation_world, conflict)

        conflict = argumentation_world.current_conflict()

    print('\nno more conflicts')


def solution(argumentation_world, conflict):
    if conflict.necessity > 0:
        if argumentation_world.execute_action(conflict.predicate):
            print(('- solution {0} performed'.format(conflict.predicate)))
            argumentationcan.set_computed_necessity(conflict.predicate, conflict.necessity)

            argumentationcan.plan.append(conflict)

            return True

    return False


def abduction(argumentation_world, conflict):
    print(('abduction {0}'.format(conflict.predicate)))

    possible_causes = argumentation_world.abduction(conflict.predicate)
    mutable_causes = find_mutable_causes(possible_causes, conflict.necessity)

    for cause in mutable_causes:
        if solve_conflict(argumentation_world, Conflict(cause, conflict.necessity)):
            return True

    return False


def negation(argumentation_world, conflict):
    print(('negation {0}'.format(conflict.predicate.negate())))

    conflict.negation_phase = True

    return solve_conflict(argumentation_world, Conflict(conflict.predicate.negate(), -conflict.necessity, True))


def revision(argumentation_world, conflict):
    if conflict.predicate in argumentation_world.wanted_necessities \
            or conflict.predicate.negate() in argumentation_world.wanted_necessities:
        positive_version = world_predicate.positive_version(conflict.predicate)
        necessity = int(eval(get_input('? - revision - change necessity for {0}? current = {1}'.format(positive_version,
                                                                                                       argumentation_world.get_wanted_necessity(
                                                                                                           positive_version)))))

        argumentation_world.wanted_necessities.pop(conflict.predicate, None)
        argumentation_world.wanted_necessities.pop(conflict.predicate.negate(), None)
        argumentation_world.wanted_necessities[positive_version] = necessity

        return True

    return False


def give_up(conflict):
    print(('give up - predicate {0} stored with necessity {1}'.format(conflict.predicate, -conflict.necessity)))

    argumentationcan.set_computed_necessity(conflict.predicate, -conflict.necessity)


def find_mutable_causes(possible_causes, necessity):
    mutable_causes = []

    for possible_cause in possible_causes:
        if predicate_mutable(possible_cause, necessity):
            mutable_causes.append(possible_cause)

    return sorted(mutable_causes, key=lambda cause: abs(argumentationcan.get_computed_necessity(cause)))


def predicate_mutable(predicate, necessity):
    return necessity * argumentationcan.get_computed_necessity(predicate) <= 0 \
           and abs(argumentationcan.get_computed_necessity(predicate)) < abs(necessity)


def get_input(text):
    return input(text)
