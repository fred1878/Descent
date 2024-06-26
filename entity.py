from __future__ import annotations

import copy
import math
import random
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING, Union, List


from components.level import Level
from components.equipment import Equipment
from gen_util import get_items_at_random
from render_order import RenderOrder
from util import get_max_value_for_floor

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.fighter import Fighter
    from components.consumable import Consumable
    from game_map import GameMap
    from components.inventory import Inventory
    from components.equippable import Equippable
    from components.attribute import Attribute
    from components.ability import Ability

T = TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    parent: Union[GameMap, Inventory]

    def __init__(
            self,
            parent: Optional[GameMap] = None,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            colour: Tuple[int, int, int] = (255, 255, 255),
            name: str = "unimplemented",
            blocks_movement: bool = False,
            render_order: RenderOrder = RenderOrder.CORPSE,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if parent:
            # If parent isn't provided now then it will be set later.
            self.parent = parent
            parent.entities.add(self)

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone

    def move(self, dx: int, dy: int) -> None:  # Move the entity
        self.x += dx
        self.y += dy

    def distance(self, x: int, y: int) -> float:
        """
        Return the distance between the current entity and the given (x, y) coordinate.
        """
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        """Place this entity at a new location.  Handles moving across GameMaps."""
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "parent"):  # Possibly uninitialized.
                if self.parent is self.gamemap:
                    self.gamemap.entities.remove(self)
            self.parent = gamemap
            gamemap.entities.add(self)


class Actor(Entity):
    def __init__(
            self,
            *,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            colour: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            ai_cls: Type[BaseAI],
            equipment: Equipment,
            fighter: Fighter,
            inventory: Inventory,
            level: Level,
            master: bool = False,
            attribute: Attribute,
            friendly: bool = False,
            ability: Ability
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            colour=colour,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )

        self.ai: Optional[BaseAI] = ai_cls(self)
        self.equipment: Equipment = equipment
        self.equipment.parent = self
        self.fighter = fighter
        self.fighter.parent = self

        self.inventory = inventory
        self.inventory.parent = self

        self.level = level
        self.level.parent = self

        self.master = master
        self.attribute = attribute
        self.attribute.parent = self
        self.friendly = friendly

        self.ability = ability
        self.ability.parent = self

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)


class Item(Entity):
    def __init__(
            self,
            *,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            colour: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            consumable: Optional[Consumable] = None,
            equippable: Optional[Equippable] = None,
            price: int = 0
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            colour=colour,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
        )

        self.consumable = consumable

        if self.consumable:
            self.consumable.parent = self

        self.equippable = equippable

        if self.equippable:
            self.equippable.parent = self

        self.price = price


class Chest(Entity):
    def __init__(
            self,
            *,
            x: int = 0,
            y: int = 0,
            char: str = "(",
            colour: Tuple[int, int, int] = (255, 255, 255),
            name: str = 'closed chest',
            opened: bool = False,
            opened_colour: Tuple[int, int, int] = (30, 30, 30),
            inventory: Inventory
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            colour=colour,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR
        )
        self.inventory = inventory
        self.inventory.parent = self
        self.opened = opened
        self.opened_colour = opened_colour

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of chest at the given location, fill it with items based on dungeon level"""
        from spawn_chances import max_chest_items_by_floor, chest_item_chances
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        number_of_items = random.randint(
            1, get_max_value_for_floor(max_chest_items_by_floor, clone.parent.engine.game_world.current_floor)
        )
        items: List[Item] = get_items_at_random(chest_item_chances, number_of_items, clone.parent.engine.game_world.current_floor)
        for item in items:
            self.inventory.items.append(item)

        gamemap.entities.add(clone)
        return clone

    def open_chest(self):
        self.opened = True
        self.blocks_movement = False
        self.colour = self.opened_colour
        self.name = 'opened chest'
        for item in self.inventory.items:
            self.inventory.scatter(item)
