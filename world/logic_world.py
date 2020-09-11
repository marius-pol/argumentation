import re

import nltk

from world import world_predicate, read_expr
from world.abstract_world import AbstractWorld


class LogicWorld(AbstractWorld):

    def __init__(self):
        super().__init__()

        self.__initial_model = set()
        self.__defaults = []
        self.__logic_program = []
        self.__added_assumptions = []
        self.__retracted_assumptions = []
        self.__model_builder = nltk.inference.MaceCommand(None, [], max_models=50)

    @property
    def initial_model(self):
        return self.__initial_model

    @property
    def logic_program(self):
        return self.__logic_program

    @property
    def defaults(self):
        return self.__defaults

    def abduction(self, predicate) -> []:
        possible_causes = []

        for expression in self.__logic_program:
            if type(expression) is nltk.sem.logic.ImpExpression:
                if str(predicate) in [str(element) for element in self.get_atoms(expression.second)]:
                    for cause in self.get_atoms(expression.first):
                        cause_predicate = read_expr(cause)
                        if cause_predicate not in possible_causes:
                            possible_causes.append(cause_predicate)

        return possible_causes

    def get_atoms(self, expression):
        atoms = re.findall(r'([''-\w{2,}]+)', str(expression))

        if 'True' in atoms:
            atoms.remove('True')

        if '-' in atoms:
            atoms.remove('-')

        return atoms

    def execute_action(self, action) -> bool:
        if not world_predicate.possible(self, action):
            return False

        actions = self.available_actions(str(action))

        if len(actions) == 0:
            return False

        action_executed = False

        for action in actions:
            if self.execute_single_action(action):
                action_executed = True

        self.model = self.compute_model()

        return action_executed

    def execute_single_action(self, action):
        if set([precondition for precondition in action.preconditions]).issubset(set(self.model)):
            self.add_assumptions(action.effects_plus)
            self.retract_assumptions(action.effects_minus)

            return True

        return False

    def compute_model(self):
        self.reset_model_assumptions(True)
        self.__model_builder.build_model()

        if len(self.__model_builder.valuation) == 0:
            defaults_to_retract = []

            for default_assumption in self.__defaults:
                self.reset_model_assumptions()

                self.__model_builder.add_assumptions([default_assumption])
                self.__model_builder.build_model()

                if len(self.__model_builder.valuation) == 0:
                    defaults_to_retract.append(default_assumption)

            if len(defaults_to_retract) == 0:
                raise Exception('this should not happen')
            if len(defaults_to_retract) >= 1:
                self.reset_model_assumptions(True)
                self.__model_builder.retract_assumptions(defaults_to_retract)
                self.__model_builder.build_model()

        valuation = list(self.__model_builder.valuation.items())

        return {read_expr(key) for (key, value) in valuation if value}

    def reset_model_assumptions(self, with_defaults=False):
        del self.__model_builder.assumptions()[:]
        self.__model_builder.add_assumptions(self.__initial_model)
        self.__model_builder.add_assumptions(self.__logic_program)
        self.__model_builder.add_assumptions(self.__added_assumptions)
        self.__model_builder.retract_assumptions(self.__retracted_assumptions)

        if with_defaults:
            self.__model_builder.add_assumptions(self.__defaults)

    def add_assumptions(self, assumptions):
        for assumption in assumptions:
            if assumption.negate() in self.__added_assumptions:
                self.__added_assumptions.remove(assumption.negate())

        self.__added_assumptions.extend(assumptions)

    def retract_assumptions(self, assumptions):
        self.__retracted_assumptions.extend(assumptions)
