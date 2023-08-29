from __future__ import annotations

import random
from typing import List, TYPE_CHECKING, Tuple

import game_map
from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor, Item


class Inventory(BaseComponent):
    parent: Actor

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: List[Item] = []

    def drop(self, item: Item) -> None:
        """
        Removes an item from the inventory and restores it to the game map, at the player's current location.
        """
        self.items.remove(item)
        item.place(self.parent.x, self.parent.y, self.gamemap)
        if self.parent is self.engine.player:
            self.engine.message_log.add_message(f"You dropped {item.name}.")
        else:
            self.engine.message_log.add_message(f"{self.parent.name} dropped {item.name}.")

    def scatter(self, item: Item) -> None:
        self.items.remove(item)
        x = self.parent.x
        y = self.parent.y
        drop_locations = (
            [
                (x + 1, y + 1),
                (x + 1, y),
                (x + 1, y - 1),
                (x, y + 1),
                (x, y - 1),
                (x - 1, y + 1),
                (x - 1, y),
                (x - 1, y - 1),
            ]
        )
        valid_locations = list(filter(lambda s: valid_drop_location(self.gamemap, s), drop_locations))

        drop_x, drop_y = random.choice(valid_locations)
        item.place(drop_x, drop_y, self.gamemap)

        if self.parent is self.engine.player:
            self.engine.message_log.add_message(f"You dropped {item.name}.")
        else:
            self.engine.message_log.add_message(f"{self.parent.name} dropped {item.name}.")


def valid_drop_location(dungeon: game_map.GameMap, xy: Tuple[int, int]) -> bool:
    x, y = xy
    return dungeon.tiles["walkable"][x, y]
