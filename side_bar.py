import tcod  # type: ignore

import colour

arrow_keys = tcod.image.load("resources/arrowkeys3.png")[:, :, :3]


class SideBar:
    def __init__(
            self
            , map_width: int
            , screen_width: int
            , screen_height: int
    ):
        self.map_width = map_width
        self.screen_width = screen_width
        self.screen_height = screen_height

    def render_movement_buttons(self, console: tcod.console.Console):
        console.draw_semigraphics(arrow_keys, self.map_width, self.screen_height - 16)

    def render(self, console: tcod.console.Console):
        console.draw_rect(self.map_width, 0, self.screen_width - self.map_width, self.screen_height, ch=1, bg=colour.white)
        self.render_movement_buttons(console)
