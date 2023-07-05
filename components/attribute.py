from typing import TYPE_CHECKING, List

import numpy as np

from components.base_component import BaseComponent

from entity import Actor


class Trait(BaseComponent):
    parent: Actor

    def __init__(
            self,
            name: str = "<unnamed trait>",
            cost: int = 0
    ):
        self.cost = cost
        self.name = name


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
