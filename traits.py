from components.attribute import Trait


class Strong(Trait):
    def __init__(self):
        super().__init__("Strong")

    def trait_defence_bonus(self) -> int:
        return 20

