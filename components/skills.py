from components.ability import *
import actions


class TextTrait(Skill):
    def __init__(self,
                 name: str = "<unnamed skill>",
                 description: str = "<undescribed skill>",
                 cost: int = 0,
                 ):
        super().__init__(
            name, description, cost
        )

    def use(self, action: actions.SkillAction) -> None:
        self.engine.message_log.add_message("used skill")


add_text = TextTrait("Conjure Text", "Add text to message log")
