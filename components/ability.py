import copy

from components.base_component import *
from entity import Actor


class Skill(BaseComponent):
    from actions import SkillAction

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

    def use(self, action: SkillAction) -> None:
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
