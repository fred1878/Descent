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
            buffs=None,
            skill_points: int = 0
    ):
        self.skills = skills
        if skills is None:
            self.skills = []
        if buffs is None:
            self.buffs = []
        self.skill_points = skill_points

    @property
    def buff_melee_bonus(self) -> int:
        bonus = 0
        for buff in self.buffs:
            if hasattr(buff, "buff_melee_bonus"):
                bonus += buff.buff_melee_bonus
        return bonus

    @property
    def buff_ranged_bonus(self) -> int:
        bonus = 0
        for buff in self.buffs:
            if hasattr(buff, "buff_ranged_bonus"):
                bonus += buff.buff_ranged_bonus
        return bonus

    @property
    def buff_range_bonus(self) -> int:
        bonus = 0
        for buff in self.buffs:
            if hasattr(buff, "buff_range_bonus"):
                bonus += buff.buff_range_bonus
        return bonus

    @property
    def buff_defence_bonus(self) -> int:
        bonus = 0
        for buff in self.buffs:
            if hasattr(buff, "buff_defence_bonus"):
                bonus += buff.buff_defence_bonus
        return bonus

    @property
    def buff_magic_bonus(self) -> int:
        bonus = 0
        for buff in self.buffs:
            if hasattr(buff, "buff_magic_bonus"):
                bonus += buff.buff_magic_bonus
        return bonus


class Buff(BaseComponent):
    parent: Actor

    def __init__(
            self,
            name: str = "<unnamed buff>",
            description: str = "<undescribed buff>",
            has_turn_duration: bool = False,
            turn_duration: int = 1,
            has_hit_duration: bool = False,
            hit_duration: int = 1
    ):
        self.description = description
        self.name = name
        self.has_turn_duration = has_turn_duration
        self.has_hit_duration = has_hit_duration
        self.turn_duration = turn_duration
        self.hit_duration = hit_duration
        self.current_turn_duration = turn_duration
        self.current_hit_duration = hit_duration

    def add_buff(self, entity: Actor):
        clone = copy.deepcopy(self)
        clone.parent = entity
        entity.ability.buffs.append(clone)

    def remove_buff(self):
        self.parent.ability.buffs.remove(self)

    def decrease_hit_duration(self, amount: int = 1) -> bool:
        if self.has_hit_duration:
            self.current_hit_duration -= amount
            if self.current_hit_duration <= 0:
                return False
        return True

    def refresh_hit_duration(self):
        self.current_hit_duration = self.hit_duration

    def decrease_turn_duration(self, amount: int = 1) -> bool:
        if self.has_turn_duration:
            self.current_turn_duration -= amount
            if self.current_turn_duration <= 0:
                return False
        return True

    def refresh_turn_duration(self):
        self.current_turn_duration = self.turn_duration


class StatModifyingBuff(Buff):

    def __init__(self
                 , name: str = "stat modifying buff"
                 , description: str = "stat modifying buff descrition"
                 , has_turn_duration: bool = False
                 , turn_duration: int = 1
                 , has_hit_duration: bool = False
                 , hit_duration: int = 1
                 , melee_bonus: int = 0
                 , ranged_bonus: int = 0
                 , range_bonus: int = 0
                 , defence_bonus: int = 0
                 , magic_bonus: int = 0
                 ):
        super().__init__(name, description, has_turn_duration, turn_duration, has_hit_duration, hit_duration)
        self.melee_bonus = melee_bonus
        self.ranged_bonus = ranged_bonus
        self.range_bonus = range_bonus
        self.defence_bonus = defence_bonus
        self.magic_bonus = magic_bonus

    @property
    def buff_melee_bonus(self) -> int:
        return self.melee_bonus

    @property
    def buff_ranged_bonus(self) -> int:
        return self.ranged_bonus

    @property
    def buff_range_bonus(self) -> int:
        return self.range_bonus

    @property
    def buff_defence_bonus(self) -> int:
        return self.defence_bonus

    @property
    def buff_magic_bonus(self) -> int:
        return self.magic_bonus



