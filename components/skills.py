import copy

import exceptions
import input_handlers
from tile_types import *
from actions import SkillAction, Action
from typing import Optional, Union

from components.base_component import BaseComponent
from entity import Actor

ActionOrHandler = Union[Action, "BaseEventHandler"]


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
        return SkillAction(user, self)

    def use(self, action: SkillAction) -> None:
        """Use this skill 'action' is the context for this activation."""
        raise NotImplementedError()


class TextSkill(Skill):
    def __init__(self,
                 name: str = "<unnamed skill>",
                 description: str = "<undescribed skill>",
                 cost: int = 0,
                 ):
        super().__init__(
            name, description, cost
        )

    def use(self, action: SkillAction) -> None:
        self.engine.message_log.add_message("used skill")


add_text_skill = TextSkill("Conjure Text", "Add text to message log")


class PushSkill(Skill):
    def __init__(self, name, description, cost):
        super().__init__(name, description, cost)

    def get_skill(self, action: SkillAction) -> input_handlers.SingleRangedAttackHandler:
        skill_user = self.parent
        self.engine.message_log.add_message("Select a target location.", colour.needs_target)
        return input_handlers.SingleRangedAttackHandler(self.engine,
                                                        callback=lambda xy: SkillAction(skill_user, self,
                                                                                        xy))

    def use(self, action: SkillAction) -> None:
        target = action.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to Target.")
        else:
            dx = self.parent.x - target.x
            dy = self.parent.y - target.y

            if abs(dx) > abs(dy):
                if dx > 0:
                    if self.engine.game_map.tiles[target.x - 1, target.y] == wall:
                        self.engine.message_log.add_message(f"{target.name} hit the wall and was dealt 1 damage")
                        target.fighter.take_damage(1)
                        target.x -= 1
                    else:
                        target.x -= 2
                else:
                    if self.engine.game_map.tiles[target.x + 1, target.y] == wall:
                        self.engine.message_log.add_message(f"{target.name} hit the wall and was dealt 1 damage")
                        target.fighter.take_damage(1)
                        target.x += 1
                    else:
                        target.x += 2
            elif abs(dx) < abs(dy):
                if dy > 0:
                    if self.engine.game_map.tiles[target.x, target.y - 1] == wall:
                        self.engine.message_log.add_message(f"{target.name} hit the wall and was dealt 1 damage")
                        target.fighter.take_damage(1)
                        target.y -= 1
                    else:
                        target.y -= 2
                else:
                    if self.engine.game_map.tiles[target.x, target.y + 1] == wall:
                        self.engine.message_log.add_message(f"{target.name} hit the wall and was dealt 1 damage")
                        target.fighter.take_damage(1)
                        target.y += 1
                    else:
                        target.y += 2
            else:
                if dx > 0:
                    if dy > 0:
                        if self.engine.game_map.tiles[target.x - 1, target.y - 1] == wall:
                            self.engine.message_log.add_message(f"{target.name} hit the wall and was dealt 1 damage")
                            target.fighter.take_damage(1)
                            target.x -= 1
                            target.y -= 1
                        else:
                            target.x -= 2
                            target.y -= 2
                    else:
                        if self.engine.game_map.tiles[target.x - 1, target.y + 1] == wall:
                            self.engine.message_log.add_message(f"{target.name} hit the wall and was dealt 1 damage")
                            target.fighter.take_damage(1)
                            target.x -= 1
                            target.y += 1
                        else:
                            target.x -= 2
                            target.y += 2

                else:
                    if dy > 0:
                        if self.engine.game_map.tiles[target.x + 1, target.y - 1] == wall:
                            self.engine.message_log.add_message(f"{target.name} hit the wall and was dealt 1 damage")
                            target.fighter.take_damage(1)
                            target.x += 1
                            target.y -= 1
                        else:
                            target.x += 2
                            target.y -= 2
                    else:
                        if self.engine.game_map.tiles[target.x + 1, target.y + 1] == wall:
                            self.engine.message_log.add_message(f"{target.name} hit the wall and was dealt 1 damage")
                            target.fighter.take_damage(1)
                            target.x += 1
                            target.y += 1
                        else:
                            target.x += 2
                            target.y += 2


push_skill = PushSkill("Push", "Push target away", 0)
