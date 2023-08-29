import copy
import random
from typing import Tuple, List

import tcod  # type: ignore

import game_map
import entity_factories
import tile_types
from exceptions import Impossible


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int, dungeon: game_map.GameMap):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.dungeon = dungeon

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

    def random_tiles(self, count: int) -> List[Tuple[int, int]]:
        i = 0
        random_tile_list = []
        if count > (self.x1 + 1 - self.x2 - 1) * (self.y1 + 1 - self.y2 - 1):
            raise Impossible(str(self.__name__) + "cannot get " + str(count) + " random tiles as room too small")
        while i < count:
            x = random.randint(self.x1 + 1, self.x2 - 1)
            y = random.randint(self.y1 + 1, self.y2 - 1)
            xy = x, y
            if xy not in random_tile_list:
                random_tile_list.append(xy)
                i += 1
        return random_tile_list

    def setup_room(self) -> None:
        NotImplementedError()


class ShopRoom(RectangularRoom):
    def __init__(self, x: int, y: int, width: int, height: int, dungeon: game_map.GameMap):
        super().__init__(x, y, width, height, dungeon)

    def setup_room(self) -> None:
        self.dungeon.tiles[self.inner] = tile_types.floor
        (x_shop, y_shop) = self.center
        shopkeeper = entity_factories.shopkeeper.spawn(self.dungeon, x_shop, y_shop)

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
        shopkeeper.equipment.toggle_equip(steel_sword, shopkeeper, add_message=False)


class TrapRoom(RectangularRoom):
    def __init__(self, x: int, y: int, width: int, height: int, dungeon: game_map.GameMap):
        super().__init__(x, y, width, height, dungeon)

    def setup_room(self) -> None:
        self.dungeon.tiles[self.inner] = tile_types.floor
        random_trap_tiles = self.random_tiles(5)
        for tile in random_trap_tiles:
            self.dungeon.tiles[tile] = tile_types.trap


class ChestRoom(RectangularRoom):
    def __init__(self, x: int, y: int, width: int, height: int, dungeon: game_map.GameMap):
        super().__init__(x, y, width, height, dungeon)

    def setup_room(self) -> None:
        self.dungeon.tiles[self.inner] = tile_types.floor
        random_chest_tiles = self.random_tiles(1)
        for tile in random_chest_tiles:
            chest_x, chest_y = tile
            chest = entity_factories.chest.spawn(self.dungeon, chest_x, chest_y)
            small_health_potion_1 = copy.deepcopy(entity_factories.small_health_potion)
            small_health_potion_2 = copy.deepcopy(entity_factories.small_health_potion)
            small_health_potion_3 = copy.deepcopy(entity_factories.small_health_potion)
            chest.inventory.items.append(small_health_potion_1)
            chest.inventory.items.append(small_health_potion_2)
            chest.inventory.items.append(small_health_potion_3)
