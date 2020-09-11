from unittest import TestCase
from unittest.mock import patch

import argumentation
from argumentation import can_procedure
from world import read_expr
from world.logic_world import LogicWorld
from world.world_action import Action


class TestArgumentationLogicWorld(TestCase):
    @patch('argumentation.can_procedure.get_input', return_value='-30')
    def test_argumentation_logic_world(self, input):
        world = LogicWorld()
        create_actions(world)

        world.initial_model.add(read_expr('Mouldings'))
        world.initial_model.add(read_expr('SoftWood'))
        world.initial_model.add(read_expr('SeveralLayers'))

        world.defaults.append(read_expr('-WireBrush'))
        world.defaults.append(read_expr('-SoftWood'))
        world.defaults.append(read_expr('-WoodWrecked'))
        world.defaults.append(read_expr('-SeveralLayers'))

        world.logic_program.append(read_expr('BurnOff & -WoodWrecked -> NiceSurface'))
        world.logic_program.append(read_expr('Sanding & -SeveralLayers & -WoodWrecked -> NiceSurface'))
        world.logic_program.append(read_expr('FillerCompound & -WoodWrecked -> NiceSurface'))
        world.logic_program.append(read_expr('Repaint & NiceSurface -> NiceDoors'))
        world.logic_program.append(read_expr('WoodWrecked -> -NiceSurface'))
        world.logic_program.append(read_expr('BurnOff & Mouldings & -WireBrush -> ToughWork'))
        world.logic_program.append(read_expr('WireBrush & SoftWood -> WoodWrecked'))

        world.wanted_necessities[read_expr('ToughWork')] = -10
        world.wanted_necessities[read_expr('NiceDoors')] = 20

        can_procedure.start(world)

        plan_actions = [str(conflict.predicate) for conflict in argumentation.plan]

        assert len(argumentation.plan) == 7
        assert 'Repaint' == plan_actions[0]
        assert 'BurnOff' == plan_actions[1]
        assert 'WireBrush' == plan_actions[2]
        assert '-WireBrush' == plan_actions[3]
        assert '-BurnOff' == plan_actions[4]
        assert 'Sanding' == plan_actions[5]
        assert 'FillerCompound' == plan_actions[6]


def create_actions(world):
    effects_plus = [read_expr('Repaint')]
    action = Action('Repaint', [], effects_plus, [])
    world.actions.append(action)

    effects_plus = [read_expr('BurnOff')]
    action = Action('BurnOff', [], effects_plus, [])
    world.actions.append(action)

    effects_plus = [read_expr('WireBrush')]
    action = Action('WireBrush', [], effects_plus, [])
    world.actions.append(action)

    effects_plus = [read_expr('Sanding')]
    action = Action('Sanding', [], effects_plus, [])
    world.actions.append(action)

    effects_plus = [read_expr('FillerCompound')]
    action = Action('FillerCompound', [], effects_plus, [])
    world.actions.append(action)

    create_negative_actions(world)


def create_negative_actions(world):
    negative_actions = []

    for action in world.actions:
        negative_action = Action(str(action.predicate.negate()), action.effects_plus, action.effects_minus,
                                 action.effects_plus)
        negative_actions.append(negative_action)

    world.actions.extend(negative_actions)
