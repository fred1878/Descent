from __future__ import annotations

import random
from typing import TYPE_CHECKING

import colour
import components.ai
from components.base_component import BaseComponent
from components.equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Item, Actor


class Equippable(BaseComponent):
    parent: Item

    def __init__(
            self,
            equipment_type: EquipmentType,
            melee_bonus: int = 0,
            ranged_bonus: int = 0,
            range_bonus: int = 0,
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
        self.range_bonus = range_bonus
        self.defense_bonus = defense_bonus
        self.magic_bonus = magic_bonus
        self.weapon_range = weapon_range
        self.required_melee = required_melee
        self.required_ranged = required_ranged
        self.required_defence = required_defence
        self.required_magic = required_magic

    def on_equip(self, user: Actor) -> None:
        pass

    def on_unequip(self, user: Actor) -> None:
        pass

    def on_pickup(self, user: Actor) -> None:
        pass

    def on_equipped_kill(self, user: Actor) -> None:
        pass

    def on_attack(self, user: Actor, target: Actor) -> None:
        pass

    def on_melee_hit(self, wearer: Actor, attacker: Actor) -> None:
        pass


class Dagger(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, melee_bonus=2, required_melee=1)


class FrenzyBlade(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, melee_bonus=2, required_melee=2)

    def on_attack(self, user: Actor, target: Actor) -> None:
        from components.ability import StatModifyingBuff
        frenzy = StatModifyingBuff("Frenzy", "Temporarily increases melee attack",
                                   has_turn_duration=True, turn_duration=5, melee_bonus=1)
        frenzy.add_buff(user)


class BronzeSword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, melee_bonus=4)


class BronzeMace(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, melee_bonus=3)

    def on_attack(self, user: Actor, target: Actor) -> None:
        stun_chance = random.randint(0, 9)
        if stun_chance > 7:  # 20%
            target.ai = components.ai.StunnedEnemy(target, target.ai, turns_remaining=random.randint(1, 3))


class IronSword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, melee_bonus=6, required_melee=3)


class SteelSword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, melee_bonus=8, required_melee=4)


class DarkSword(Equippable):
    def __init__(self):
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, melee_bonus=8, required_melee=6)

    def on_equip(self, user) -> None:
        user.attribute.change_corruption(10)

    def on_unequip(self, user) -> None:
        user.attribute.change_corruption(-10)


class VampiricBlade(Equippable):
    def __init__(self):
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, melee_bonus=8, required_melee=7)

    def on_equipped_kill(self, user) -> None:
        user.fighter.heal(2)
        if user is self.engine.player:
            self.engine.message_log.add_message("Your blade twists your mind and body", colour.red)
            self.engine.player.attribute.change_corruption(3, add_message=False)
            self.engine.player.attribute.change_insanity(2, add_message=False)


class Bloodthirster(Equippable):
    def __init__(self):
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, melee_bonus=5)
        self.kill_count = 0

    def on_equipped_kill(self, user) -> None:
        self.kill_count += 1
        if self.kill_count % 5 == 0:
            user.level.increase_max_hp(1)
            user.attribute.change_insanity(1)
        if self.kill_count % 15 == 0:
            self.melee_bonus += 1


class WoodenBow(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.RANGED_WEAPON, ranged_bonus=1, weapon_range=4)


class CompositeWoodenBow(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.RANGED_WEAPON, ranged_bonus=2, weapon_range=5, required_ranged=2)


class PiercingBow(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.RANGED_WEAPON, ranged_bonus=3, weapon_range=5, required_ranged=3)

    def on_attack(self, user: Actor, target: Actor) -> None:
        from components.ability import StatModifyingBuff
        armor_piercing = StatModifyingBuff("Armor down", "Temporarily decreases defence",
                                           has_turn_duration=True, turn_duration=10, defence_bonus=-1)
        armor_piercing.add_buff(user)


class UnstablePistol(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.RANGED_WEAPON, ranged_bonus=7, weapon_range=3, required_ranged=3)

    def on_attack(self, user: Actor, target: Actor) -> None:
        user.fighter.take_damage(random.randint(0, 3))
        stun_chance = random.randint(0, 9)
        if stun_chance > 5:  # 40%
            target.ai = components.ai.StunnedEnemy(target, target.ai, turns_remaining=random.randint(1, 3))


class WoodenWand(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, magic_bonus=3)


class GoldenWand(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, ranged_bonus=2, magic_bonus=6, weapon_range=3)


class CursedOrb(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, ranged_bonus=3, magic_bonus=12, weapon_range=2)

    def on_pickup(self, user) -> None:
        user.attribute.change_corruption(20, add_message=True)
        user.attribute.change_insanity(10, add_message=True)


class LeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1)


class BerserkerArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=2)

    def on_melee_hit(self, wearer: Actor, attacker: Actor) -> None:
        from components.ability import StatModifyingBuff
        berserker_rage = StatModifyingBuff("Berserker Rage", "Increase melee attack at the cost of defence",
                                           has_turn_duration=True, turn_duration=5, melee_bonus=1, defence_bonus=-1)
        berserker_rage.add_buff(wearer)


class SpikedLeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1)

    def on_melee_hit(self, wearer: Actor, attacker: Actor) -> None:
        if bool(random.getrandbits(1)):  # 50%
            self.engine.message_log.add_message(f"{attacker.name} was spiked for 2 damage", colour.red)
            attacker.fighter.take_damage(2)


class ChainMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=3)


class FlameMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=3)

    def on_melee_hit(self, wearer: Actor, attacker: Actor) -> None:
        self.engine.message_log.add_message(f"{attacker.name} was flamed for 3 damage", colour.red)
        attacker.fighter.take_damage(3)


class PlateMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=5)


class CursedLeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1)

    def on_pickup(self, user) -> None:
        user.level.change_gold(-69)
