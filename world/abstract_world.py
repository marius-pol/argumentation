from abc import ABC, abstractmethod

from nltk.sem.logic import NegatedExpression

from argumentation.conflict import Conflict
from world import world_predicate


class AbstractWorld(ABC):
    def __init__(self):
        self.__wanted_necessities = {}
        self.__model = set()

        self.__actions = []

    @property
    def wanted_necessities(self):
        return self.__wanted_necessities

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        self.__model = value

    @property
    def actions(self):
        return self.__actions

    def conflicts(self):
        conflicts = [Conflict(predicate, self.get_wanted_necessity(predicate)) for predicate in self.wanted_necessities]
        conflicts = [conflict for conflict in conflicts if world_predicate.conflicting(self, conflict.predicate)]
        conflicts = sorted(conflicts, key=lambda p: abs(self.get_wanted_necessity(p.predicate)), reverse=True)

        return conflicts

    def current_conflict(self):
        conflicts = self.conflicts()

        if len(conflicts) > 0:
            predicate = world_predicate.version_in_world(self, conflicts[0].predicate)
            necessity = self.get_wanted_necessity(predicate)

            return Conflict(predicate, necessity)
        return None

    def get_wanted_necessity(self, predicate):
        necessity = self.wanted_necessities.get(predicate, 0)

        if necessity == 0:
            necessity = -self.wanted_necessities.get(predicate.negate(), 0)

        return necessity

    @abstractmethod
    def abduction(self, predicate) -> []:
        pass

    @abstractmethod
    def execute_action(self, action) -> bool:
        pass

    def is_action(self, predicate):
        return str(predicate) in [action.name for action in self.actions]

    def available_actions(self, action_name):
        return [action for action in self.actions if action_name in action.name]

    def action_possible(self, action):
        return self.conditions_in_model(action.preconditions)

    def conditions_in_model(self, conditions):
        if conditions is None:
            return False

        not_in_model = True
        for condition in conditions:
            if not type(condition) is NegatedExpression and condition not in self.model:
                not_in_model = False

        return not_in_model
