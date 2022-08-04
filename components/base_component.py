from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
    from game_map import GameMap

class BaseComponent:
    parent: Entity  # This is the owning entity

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap # This makes it easier to reference the gamemap from the component

    @property
    def engine(self) -> Engine:
        return self.gamemap.engine # This makes it easier to reference the engine from the component