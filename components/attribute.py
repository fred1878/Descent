import copy

from components.base_component import BaseComponent

from entity import Actor


class Trait(BaseComponent):
    parent: Actor

    def __init__(
            self,
            name: str = "<unnamed trait>",
            description: str = "<undescribed trait>",
            cost: int = 0,
            has_duration: bool = False,
            duration: int = 1
    ):
        self.cost = cost
        self.description = description
        self.name = name
        self.has_duration = has_duration
        self.duration = duration
        self.current_duration = duration

    def add_trait(self, entity: Actor):
        clone = copy.deepcopy(self)
        clone.parent = entity
        entity.attribute.traits.append(clone)

    def remove_trait(self):
        self.parent.attribute.traits.remove(self)

    def decrease_duration(self, amount: int = 1) -> bool:
        if self.has_duration:
            self.current_duration -= amount
            if self.current_duration <= 0:
                return False
        return True

    def refresh_duration(self):
        self.current_duration = self.duration


class Attribute(BaseComponent):
    parent: Actor

    def __init__(
            self,
            trait_list=None,
            insanity: int = 0,
            corruption: int = 0,
    ):
        self.traits = trait_list
        if trait_list is None:
            self.traits = []
        self.insanity = insanity
        self.corruption = corruption

    @property
    def trait_melee_bonus(self) -> int:
        bonus = 0
        for trait in self.traits:
            if hasattr(trait, "trait_melee_bonus"):
                bonus += trait.trait_melee_bonus
        return bonus

    @property
    def trait_ranged_bonus(self) -> int:
        bonus = 0
        for trait in self.traits:
            if hasattr(trait, "trait_ranged_bonus"):
                bonus += trait.trait_ranged_bonus
        return bonus

    @property
    def trait_defence_bonus(self) -> int:
        bonus = 0
        for trait in self.traits:
            if hasattr(trait, "trait_defence_bonus"):
                bonus += trait.trait_defence_bonus
        return bonus

    @property
    def trait_magic_bonus(self) -> int:
        bonus = 0
        for trait in self.traits:
            if hasattr(trait, "trait_magic_bonus"):
                bonus += trait.trait_magic_bonus
        return bonus

    def change_corruption(self, amount: int, add_message: bool = True) -> None:
        self.parent.attribute.corruption += amount
        if add_message:
            if amount > 0:
                self.engine.message_log.add_message("Your body festers!")
            elif amount < 0:
                self.engine.message_log.add_message("Your body is purified!")

    def change_insanity(self, amount: int, add_message: bool = True) -> None:
        self.parent.attribute.corruption += amount
        if add_message:
            if amount > 0:
                self.engine.message_log.add_message("The madness deppens!")
            elif amount < 0:
                self.engine.message_log.add_message("Your mind is clear!")
