import copy
from typing import Tuple

import tcod  # type: ignore

import game_map
import entity_factories


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
                self.x1 <= other.x2
                and self.x2 >= other.x1
                and self.y1 <= other.y2
                and self.y2 >= other.y1
        )


class ShopRoom(RectangularRoom):
    def __init__(self, x: int, y: int, width: int, height: int, dungeon: game_map.GameMap):
        super().__init__(x, y, width, height)
        self.entities = dungeon.entities
        (x_shop, y_shop) = self.center
        shopkeeper = entity_factories.shopkeeper.spawn(dungeon, x_shop, y_shop)

        iron_sword = copy.deepcopy(entity_factories.iron_sword)
        chain_mail = copy.deepcopy(entity_factories.chain_mail)
        golden_wand = copy.deepcopy(entity_factories.golden_wand)

        iron_sword.parent = shopkeeper.inventory
        chain_mail.parent = shopkeeper.inventory
        golden_wand.parent = shopkeeper.inventory
        shopkeeper.inventory.items.append(iron_sword)
        shopkeeper.inventory.items.append(chain_mail)
        shopkeeper.inventory.items.append(golden_wand)

        steel_sword = copy.deepcopy(entity_factories.steel_sword)
        steel_sword.parent = shopkeeper.inventory
        shopkeeper.inventory.items.append(steel_sword)
        shopkeeper.equipment.toggle_equip(steel_sword, add_message=False)

