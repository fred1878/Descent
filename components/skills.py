from components.ability import *
import actions


class TextSkill(Skill):
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


add_text = TextSkill("Conjure Text", "Add text to message log")


class PushSkill(Skill):
    def __init__(self, name, description, cost):
        super().__init__(name, description, cost)

    def use(self, action: actions.SkillAction) -> None:
        