from __future__ import annotations
import lzma
import pickle
from typing import TYPE_CHECKING

import colour
import exceptions
import render_functions
from message_log import MessageLog
from side_bar import SideBar

from tcod.context import Context  # type: ignore
from tcod.console import Console  # type: ignore
from tcod.map import compute_fov  # type: ignore
import tcod  # type: ignore

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld


class Engine:
    game_map: GameMap
    game_world: GameWorld
    engine: Engine

    def __init__(self, player: Actor, screen_width: int, screen_height: int, map_width: int):
        self.player = player
        self.message_log = MessageLog()
        self.sidebar = SideBar(map_width, screen_width, screen_height)
        self.mouse_location = (0, 0)

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass

    def handle_duration_events(self) -> None:
        for entity in set(self.game_map.actors):
            for buff in entity.ability.buffs:
                if not buff.decrease_turn_duration():
                    buff.remove_buff()
            for trait in entity.attribute.traits:
                print(trait)
                if not trait.decrease_duration():
                    trait.remove_trait()

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = event.tile.x, event.tile.y

    def update_fov(self) -> None:  # Recompute the visible area based on the players point of view.
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y), radius=8)
        self.game_map.explored |= self.game_map.visible  # If a tile is "visible" it should be added to "explored".

    def render(self, console: Console) -> None:
        self.game_map.render(console)
        self.message_log.render(console=console, x=21, y=self.game_world.map_height + 2, width=40, height=7)
        self.sidebar.render(console)
        render_functions.render_bar(
            console=console, current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp, total_width=20, y=self.game_world.map_height + 2)
        render_functions.render_names_at_mouse_location(
            console=console, x=21, y=self.game_world.map_height + 1, engine=self)
        render_functions.render_insanity(
            console=console, insanity=self.player.attribute.insanity, location=(0, self.game_world.map_height + 4))
        render_functions.render_corruption(
            console=console, corruption=self.player.attribute.corruption, location=(0, self.game_world.map_height + 5))
        render_functions.render_dungeon_level(
            console=console, dungeon_level=self.game_world.current_floor, location=(0, self.game_world.map_height + 6))
        render_functions.render_gold(
            console=console, gold=self.player.level.current_gold, location=(0, self.game_world.map_height + 7))
        render_functions.render_kill_count(
            console=console, kill_count=self.player.level.kill_count, location=(0, self.game_world.map_height + 8))

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
