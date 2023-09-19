import tcod  # type: ignore

import colour

up_arrow = tcod.image.load("resources/uparrow.png")[:, :, :3]
down_arrow = tcod.image.load("resources/downarrow.png")[:, :, :3]
left_arrow = tcod.image.load("resources/leftarrow.png")[:, :, :3]
right_arrow = tcod.image.load("resources/rightarrow.png")[:, :, :3]
up_left_arrow = tcod.image.load("resources/upleftarrow.png")[:, :, :3]
up_right_arrow = tcod.image.load("resources/uprightarrow.png")[:, :, :3]
down_left_arrow = tcod.image.load("resources/downleftarrow.png")[:, :, :3]
down_right_arrow = tcod.image.load("resources/downrightarrow.png")[:, :, :3]
wait = tcod.image.load("resources/wait.png")[:, :, :3]


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
        self.movement_buttons_origin = (self.map_width, self.screen_height - 12)

    def render_movement_buttons(self, console: tcod.console.Console):
        # each arrow is 4x4 tiles
        x, y = self.movement_buttons_origin
        console.draw_semigraphics(up_left_arrow, x, y)
        console.draw_semigraphics(up_arrow, x + 4, y)
        console.draw_semigraphics(up_right_arrow, x + 8, y)
        console.draw_semigraphics(left_arrow, x, y + 4)
        console.draw_semigraphics(wait, x + 4, y + 4)
        console.draw_semigraphics(right_arrow, x + 8, y + 4)
        console.draw_semigraphics(down_left_arrow, x, y + 8)
        console.draw_semigraphics(down_arrow, x + 4, y + 8)
        console.draw_semigraphics(down_right_arrow, x + 8, y + 8)

    def render(self, console: tcod.console.Console):
        console.draw_rect(self.map_width, 0, self.screen_width - self.map_width, self.screen_height, ch=1,
                          bg=colour.white)
        self.render_movement_buttons(console)
