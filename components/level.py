from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor


class Level(BaseComponent):
    parent: Actor

    def __init__(
        self,
        current_level: int = 1,
        current_xp: int = 0,
        level_up_base: int = 100,
        level_up_factor: int = 160,
        xp_given: int = 0,
        current_gold: int = 0,
        gold_given: int = 0
    ):
        self.current_level = current_level
        self.current_xp = current_xp
        self.level_up_base = level_up_base
        self.level_up_factor = level_up_factor
        self.xp_given = xp_given
        self.current_gold = current_gold
        self.gold_given = gold_given
        self.kill_count = 0

    def change_gold(self, value: int) -> bool:
        if self.current_gold + value < 0:
            return False
        else:
            self.current_gold += value

    @property
    def experience_to_next_level(self) -> int:
        return self.level_up_base + self.current_level * self.level_up_factor

    @property
    def requires_level_up(self) -> bool:
        return self.current_xp > self.experience_to_next_level

    def add_xp(self, xp: int) -> None:
        if xp == 0 or self.level_up_base == 0:
            return

        self.current_xp += xp

        self.engine.message_log.add_message(f"You gain {xp} experience points.")

        if self.requires_level_up:
            self.engine.message_log.add_message(
                f"You advance to level {self.current_level + 1}!"
            )

    def increase_level(self) -> None:
        self.current_xp -= self.experience_to_next_level

        self.current_level += 1

    def increase_max_hp(self, amount: int = 20) -> None:
        self.parent.fighter.max_hp += amount
        self.parent.fighter.hp += amount

        self.engine.message_log.add_message("Your health improves!")

        self.increase_level()

    def increase_melee(self, amount: int = 1) -> None:
        self.parent.fighter.base_melee += amount

        self.engine.message_log.add_message("You feel stronger!")

        self.increase_level()

    def increase_ranged(self, amount: int = 1) -> None:
        self.parent.fighter.base_ranged += amount

        self.engine.message_log.add_message("You feel more aware!")

        self.increase_level()

    def increase_defense(self, amount: int = 1) -> None:
        self.parent.fighter.base_defense += amount

        self.engine.message_log.add_message("Your movements are getting swifter!")

        self.increase_level()

    def increase_magic(self, amount: int = 3) -> None:
        self.parent.fighter.base_magic += amount

        self.engine.message_log.add_message("You feel the power coursing through you!")

        self.increase_level()
