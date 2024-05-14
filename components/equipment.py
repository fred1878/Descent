from __future__ import annotations

from typing import Optional, TYPE_CHECKING, List

import colour
from components.base_component import BaseComponent
from components.equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Actor, Item


class Equipment(BaseComponent):
    parent: Actor

    def __init__(self, melee_weapon: Optional[Item] = None, ranged_weapon: Optional[Item] = None,
                 armor: Optional[Item] = None):
        self.melee_weapon = melee_weapon
        self.ranged_weapon = ranged_weapon
        self.armor = armor

    @property
    def equipped_items(self) -> List[Item]:
        items: List[Item] = []
        if self.melee_weapon is not None and self.melee_weapon.equippable is not None:
            items.append(self.melee_weapon)
        if self.ranged_weapon is not None and self.ranged_weapon.equippable is not None:
            items.append(self.ranged_weapon)
        if self.armor is not None and self.armor.equippable is not None:
            items.append(self.armor)
        return items

    @property
    def equip_defence_bonus(self) -> int:
        bonus = 0
        for item in self.equipped_items:
            bonus += item.equippable.defense_bonus
        return bonus

    @property
    def equip_melee_bonus(self) -> int:
        bonus = 0
        for item in self.equipped_items:
            bonus += item.equippable.melee_bonus
        return bonus

    @property
    def equip_ranged_bonus(self) -> int:
        bonus = 0
        for item in self.equipped_items:
            bonus += item.equippable.ranged_bonus
        return bonus

    @property
    def equip_magic_bonus(self) -> int:
        bonus = 0
        for item in self.equipped_items:
            bonus += item.equippable.magic_bonus
        return bonus

    @property
    def equip_range_bonus(self) -> int:
        bonus = 0
        for item in self.equipped_items:
            bonus += item.equippable.weapon_range
            bonus += item.equippable.range_bonus
        return bonus

    def item_is_equipped(self, item: Item) -> bool:
        return self.melee_weapon == item or self.armor == item or self.ranged_weapon == item

    def unequip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You remove the {item_name}.")

    def equip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You equip the {item_name}.")

    def equip_to_slot(self, slot: str, item: Item, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if current_item is not None:
            self.unequip_from_slot(slot, add_message)

        setattr(self, slot, item)

        if add_message:
            self.equip_message(item.name)

    def unequip_from_slot(self, slot: str, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if add_message:
            self.unequip_message(current_item.name)

        setattr(self, slot, None)

    def toggle_equip(self, equippable_item: Item, equipping_actor: Actor, add_message: bool = True) -> None:
        if equipping_actor.fighter.base_melee >= equippable_item.equippable.required_melee and \
                equipping_actor.fighter.base_ranged >= equippable_item.equippable.required_ranged and \
                equipping_actor.fighter.base_defense >= equippable_item.equippable.required_defence and \
                equipping_actor.fighter.magic >= equippable_item.equippable.required_magic:
            if equippable_item.equippable:
                if equippable_item.equippable.equipment_type == EquipmentType.MELEE_WEAPON:
                    slot = "melee_weapon"
                elif equippable_item.equippable.equipment_type == EquipmentType.RANGED_WEAPON:
                    slot = "ranged_weapon"
                elif equippable_item.equippable.equipment_type == EquipmentType.ARMOR:
                    slot = "armor"
                else:
                    raise NotImplementedError("Equipment class not implemented")

            if getattr(self, slot) == equippable_item:
                self.unequip_from_slot(slot, add_message)
                equippable_item.equippable.on_unequip(equipping_actor)
            else:
                self.equip_to_slot(slot, equippable_item, add_message)
                equippable_item.equippable.on_equip(equipping_actor)
        else:
            if equipping_actor is self.engine.player:
                self.engine.message_log.add_message("You do not have the stats to equip this item", colour.invalid)
            else:
                self.engine.message_log.add_message(f'{equipping_actor} does not have te stats to equip this item', colour.invalid)
