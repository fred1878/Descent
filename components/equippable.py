from __future__ import annotations

from typing import TYPE_CHECKING

import colour
from components.base_component import BaseComponent
from components.equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Item


class Equippable(BaseComponent):
    parent: Item

    def __init__(
            self,
            equipment_type: EquipmentType,
            melee_bonus: int = 0,
            ranged_bonus: int = 0,
            defense_bonus: int = 0,
            magic_bonus: int = 0,
            weapon_range: int = 0,
            required_melee: int = 0,
            required_ranged: int = 0,
            required_defence: int = 0,
            required_magic: int = 0,
    ):
        self.equipment_type = equipment_type
        self.melee_bonus = melee_bonus
        self.ranged_bonus = ranged_bonus
        self.equip_defense_bonus = defense_bonus
        self.magic_bonus = magic_bonus
        self.weapon_range = weapon_range
        self.required_melee = required_melee
        self.required_ranged = required_ranged
        self.required_defence = required_defence
        self.required_magic = required_magic

    def on_equip(self) -> None:
        pass

    def on_unequip(self) -> None:
        pass

    def on_pickup(self) -> None:
        pass

    def on_equipped_kill(self) -> None:
        pass


class Dagger(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, melee_bonus=2, required_melee=1)


class BronzeSword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, melee_bonus=4)


class IronSword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, melee_bonus=6, required_melee=3)


class SteelSword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, melee_bonus=8, required_melee=4)


class DarkSword(Equippable):
    def __init__(self):
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, melee_bonus=8)

    def on_equip(self) -> None:
        self.engine.player.level.change_gold(100)

    def on_unequip(self) -> None:
        self.engine.player.level.change_gold(-100)


class VampiricBlade(Equippable):
    def __init__(self):
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, melee_bonus=8)

    def on_equipped_kill(self) -> None:
        self.engine.message_log.add_message("Your blade twists your mind and body", colour.red)
        self.engine.player.attribute.change_corruption(3, add_message=False)
        self.engine.player.attribute.change_insanity(2, add_message=False)
        self.engine.player.fighter.heal(2)


class Bloodthirster(Equippable):
    def __init__(self):
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, melee_bonus=5)
        self.kill_count = 0

    def on_equipped_kill(self) -> None:
        self.kill_count += 1
        if self.kill_count % 5 == 0:
            self.engine.player.level.increase_max_hp(1)
            self.engine.player.attribute.change_insanity(1)


class WoodenBow(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.RANGED_WEAPON, ranged_bonus=1, weapon_range=4)


class CompositeWoodenBow(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.RANGED_WEAPON, ranged_bonus=2, weapon_range=5)


class WoodenWand(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, magic_bonus=3)


class GoldenWand(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, ranged_bonus=2, magic_bonus=6, weapon_range=3)


class CursedOrb(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, ranged_bonus=3, magic_bonus=12, weapon_range=2)

    def on_pickup(self) -> None:
        self.engine.player.attribute.change_corruption(20, add_message=True)
        self.engine.player.attribute.change_insanity(10, add_message=True)


class LeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1)


class ChainMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=3)


class PlateMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=5)


class CursedLeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1)

    def on_pickup(self) -> None:
        self.engine.player.level.change_gold(-69)
