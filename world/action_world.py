from world import world_predicate, read_expr
from world.abstract_world import AbstractWorld


class ActionWorld(AbstractWorld):
    def __init__(self):
        super().__init__()

    def execute_action(self, action) -> bool:
        if not world_predicate.possible(self, action):
            return False

        new_actions = self.available_actions(str(action))

        for action in new_actions:
            if self.action_possible(action):
                self.model.difference_update(action.effects_minus)
                self.model.update(action.effects_plus)

        return True

    def abduction(self, predicate) -> []:
        possible_causes = [read_expr(action.name) for action in self.actions if
                           {predicate}.issubset(set(action.effects_plus))]

        return possible_causes
