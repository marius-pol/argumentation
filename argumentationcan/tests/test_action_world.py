from unittest import TestCase

import argumentationcan
from argumentationcan import procedure
from argumentationcan.world import read_expr
from argumentationcan.world.action_world import ActionWorld
from argumentationcan.world.world_action import Action


class TestArgumentationActionWorld(TestCase):
    def test_argumentation_action_world(self):
        world = ActionWorld()
        create_actions(world)

        world.model.add(read_expr('StateLowConsumption'))
        world.model.add(read_expr('StateHot'))
        world.model.add(read_expr('StateHotOutside'))

        world.wanted_necessities[read_expr('StateWarm')] = 1
        world.wanted_necessities[read_expr('StateLowConsumption')] = 2

        procedure.start(world)

        plan_actions = [str(conflict.predicate) for conflict in argumentationcan.plan]

        assert len(argumentationcan.plan) == 3
        assert 'SwitchCoolerOn' == plan_actions[0]
        assert 'SwitchCoolerOff' == plan_actions[1]
        assert 'CloseBlinds' == plan_actions[2]


def create_actions(world):
    preconditions = [read_expr('StateWarm'), read_expr('StateHotOutside'), read_expr('-StateWindowOpened')]
    effects_plus = [read_expr('StateHot'), read_expr('StateWindowOpened')]
    effects_minus = [read_expr('StateWarm')]
    action = Action('OpenWindow', preconditions, effects_plus, effects_minus)
    world.actions.append(action)

    preconditions = [read_expr('StateHot'), read_expr('-StateCoolerOn')]
    effects_plus = [read_expr('StateWarm'), read_expr('StateCoolerOn')]
    effects_minus = [read_expr('StateHot')]
    action = Action('SwitchCoolerOn', preconditions, effects_plus, effects_minus)
    world.actions.append(action)

    preconditions = []
    effects_plus = [read_expr('StateHighConsumption'), read_expr('StateCoolerOn')]
    effects_minus = [read_expr('StateLowConsumption')]
    action = Action('SwitchCoolerOn', preconditions, effects_plus, effects_minus)
    world.actions.append(action)

    preconditions = [read_expr('StateHot'), read_expr('-StateBlindsClosed')]
    effects_plus = [read_expr('StateWarm'), read_expr('StateBlindsClosed')]
    effects_minus = [read_expr('StateHot')]
    action = Action('CloseBlinds', preconditions, effects_plus, effects_minus)
    world.actions.append(action)

    preconditions = [read_expr('StateWarm'), read_expr('StateCoolerOn')]
    effects_plus = [read_expr('StateHot')]
    effects_minus = [read_expr('StateWarm')]
    action = Action('SwitchCoolerOff', preconditions, effects_plus, effects_minus)
    world.actions.append(action)

    preconditions = []
    effects_plus = [read_expr('StateLowConsumption')]
    effects_minus = [read_expr('StateCoolerOn'), read_expr('StateHighConsumption')]
    action = Action('SwitchCoolerOff', preconditions, effects_plus, effects_minus)
    world.actions.append(action)

    preconditions = [read_expr('StateCold'), read_expr('StateColdOutside'), read_expr('-StateHeaterOn')]
    effects_plus = [read_expr('StateWarm'), read_expr('StateHeaterOn')]
    effects_minus = [read_expr('StateCold')]
    action = Action('SwitchHeaterOn', preconditions, effects_plus, effects_minus)
    world.actions.append(action)

    preconditions = [read_expr('StateCold'), read_expr('StateWarmOutside'), read_expr('-StateWindowOpened')]
    effects_plus = [read_expr('StateWarm'), read_expr('StateWindowOpened')]
    effects_minus = [read_expr('StateCold')]
    action = Action('OpenWindow', preconditions, effects_plus, effects_minus)
    world.actions.append(action)
