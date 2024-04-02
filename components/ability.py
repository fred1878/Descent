import copy
from typing import Optional, Union

from components.base_component import *
import actions
from entity import Actor

ActionOrHandler = Union[actions.Action, "BaseEventHandler"]


class Skill(BaseComponent):
    parent: Actor

    def __init__(
            self,
            name: str = "<unnamed skill>",
            description: str = "<undescribed skill>",
            cost: int = 0,
    ):
        self.cost = cost
        self.description = description
        self.name = name

    def add_skill(self, entity: Actor) -> None:
        clone = copy.deepcopy(self)
        clone.parent = entity
        entity.ability.skills.append(clone)

    def get_skill(self, user: Actor) -> Optional[ActionOrHandler]:
        """Try to return the action for this skill."""
        return actions.SkillAction(user, self)

    def use(self, action: actions.SkillAction) -> None:
        """Use this skill 'action' is the context for this activation."""
        raise NotImplementedError()


class Ability(BaseComponent):
    parent: Actor

    def __init__(
            self,
            skills=None,
            skill_points: int = 0
    ):
        self.skills = skills
        if skills is None:
            self.skills = []
        self.skill_points = skill_points
