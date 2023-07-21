from __future__ import annotations

from typing import TYPE_CHECKING
from components.base_component import BaseComponent
from render_order import RenderOrder
import colour

if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    parent: Actor

    def __init__(self, hp: int, base_defense: int, base_melee: int = 0, base_ranged: int = 0, base_magic: int = 0):
        self.max_hp = hp
        self._hp = hp
        self.base_defense = base_defense
        self.base_melee = base_melee
        self.base_ranged = base_ranged
        self.base_magic = base_magic

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    @property
    def defense(self) -> int:
        return self.base_defense + self.defense_bonus

    @property
    def melee_power(self) -> int:
        return self.base_melee + self.melee_bonus

    @property
    def ranged_power(self) -> int:
        return self.base_ranged + self.ranged_bonus

    @property
    def magic(self) -> int:
        return self.base_magic + self.magic_bonus

    @property
    def defense_bonus(self) -> int:
        bonus = 0
        if self.parent.equipment:
            bonus += self.parent.equipment.equip_defence_bonus
        if self.parent.attribute:
            bonus += self.parent.attribute.trait_defence_bonus
        return bonus

    @property
    def melee_bonus(self) -> int:
        bonus = 0
        if self.parent.equipment:
            bonus += self.parent.equipment.equip_melee_bonus
        if self.parent.attribute:
            bonus += self.parent.attribute.trait_melee_bonus
        return bonus

    @property
    def ranged_bonus(self) -> int:
        bonus = 0
        if self.parent.equipment:
            bonus += self.parent.equipment.equip_ranged_bonus
        if self.parent.attribute:
            bonus += self.parent.attribute.trait_ranged_bonus
        return bonus

    @property
    def magic_bonus(self) -> int:
        bonus = 0
        if self.parent.equipment:
            bonus += self.parent.equipment.equip_magic_bonus
        if self.parent.attribute:
            bonus += self.parent.attribute.trait_magic_bonus
        return bonus

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount

    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "You have reached the end!"
            death_message_colour = colour.player_die
        else:
            death_message = f"{self.parent.name} is dead!"
            death_message_colour = colour.enemy_die
            for item in self.parent.inventory.items:
                self.parent.inventory.drop(item)

        self.parent.char = "%"
        self.parent.colour = (190, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_colour)
        self.engine.player.level.add_xp(self.parent.level.xp_given)
        self.engine.player.level.change_gold(self.parent.level.gold_given)
        self.engine.player.level.kill_count += 1
        for item in self.engine.player.inventory.items:
            if self.engine.player.equipment.item_is_equipped(item):
                item.equippable.on_equipped_kill()
