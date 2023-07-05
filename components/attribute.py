from typing import TYPE_CHECKING

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


class Attribute(BaseComponent):
    parent: Actor

    def __init__(
            self,
            insanity: int = 0,
            corruption: int = 0,
            traits=None
    ):
        self.traits = traits
        if traits is None:
            self.traits = []
        self.insanity = insanity
        self.corruption = corruption

    @property
    def trait_defence_bonus(self) -> int:
        bonus = 0
        for trait in self.parent.attribute.traits:
            print(trait.name)
            if hasattr(trait, "trait_defence_bonus"):
                bonus += trait.trait_defence_bonus
        return bonus
