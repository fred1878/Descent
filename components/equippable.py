from __future__ import annotations

from typing import TYPE_CHECKING

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
            price: int = 0
    ):
        self.equipment_type = equipment_type
        self.melee_bonus = melee_bonus
        self.ranged_bonus = ranged_bonus
        self.defense_bonus = defense_bonus
        self.magic_bonus = magic_bonus
        self.weapon_range = weapon_range
        self.price = price


class Dagger(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, melee_bonus=2, price=20)


class BronzeSword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, melee_bonus=4, price=40)


class IronSword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, melee_bonus=6, price=100)


class WoodenBow(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.RANGED_WEAPON, ranged_bonus=1, weapon_range=4, price=20)


class WoodenWand(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, magic_bonus=3, price=20)


class GoldenWand(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, magic_bonus=6, price=50)


class LeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1, price=20)


class ChainMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=3, price=80)


class PlateMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=5, price=200)
