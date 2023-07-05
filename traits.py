from components.attribute import Trait


class StatModifyingTrait(Trait):
    def __init__(self,
                 melee_bonus: int = 0,
                 ranged_bonus: int = 0,
                 defence_bonus: int = 0,
                 magic_bonus: int = 0,
                 name: str = "stat modifying trait",
                 cost: int = 0
                 ):
        super().__init__(name, cost)
        self.melee_bonus = melee_bonus
        self.ranged_bonus = ranged_bonus
        self.defence_bonus = defence_bonus
        self.magic_bonus = magic_bonus

    @property
    def trait_melee_bonus(self) -> int:
        return self.melee_bonus

    @property
    def trait_ranged_bonus(self) -> int:
        return self.ranged_bonus

    @property
    def trait_defence_bonus(self) -> int:
        return self.defence_bonus

    @property
    def trait_magic_bonus(self) -> int:
        return self.magic_bonus


god_mode = StatModifyingTrait(
    melee_bonus=100,
    ranged_bonus=100,
    defence_bonus=100,
    magic_bonus=100,
    name="God Mode")
