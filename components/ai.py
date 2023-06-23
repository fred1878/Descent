from __future__ import annotations

from typing import List, Optional, Tuple, TYPE_CHECKING
import random
import numpy as np  # type: ignore
import tcod  # type: ignore
from actions import Action, BumpAction, MeleeAction, MovementAction, WaitAction, RangedAction

from entity import Actor


class BaseAI(Action):
    def perform(self) -> None:
        raise NotImplementedError()

    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        """Compute and return a path to the target position.

        If there is no valid path then returns an empty list.
        """
        # Copy the walkable array.
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            # Check that an enitiy blocks movement and the cost isn't zero (blocking.)
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # Add to the cost of a blocked position.
                # A lower number means more enemies will crowd behind each other in
                # hallways.  A higher number means enemies will take longer paths in
                # order to surround the player.
                cost[entity.x, entity.y] += 12

        # Create a graph from the cost array and pass that graph to a new pathfinder.
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))  # Start position.

        # Compute the path to the destination and remove the starting point.
        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]].
        return [(index[0], index[1]) for index in path]


class ShopAI(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []
        self.hostile = False

    def perform(self) -> None:
        if self.entity.fighter.hp < self.entity.fighter.max_hp:
            self.hostile = True
        if not self.hostile:
            return WaitAction(self.entity).perform()
        else:
            target = self.engine.player
            dx = target.x - self.entity.x
            dy = target.y - self.entity.y
            distance = max(abs(dx), abs(dy))  # distance to player

            if self.engine.game_map.visible[self.entity.x, self.entity.y]:
                if distance <= 1:
                    return MeleeAction(self.entity, dx, dy).perform()  # Will attack player when adjacent
                else:
                    self.path = self.get_path_to(target.x, target.y)
                    dest_x, dest_y = self.path.pop(0)
                    return MovementAction(self.entity, dest_x - self.entity.x, dest_y - self.entity.y).perform()

            return WaitAction(self.entity).perform()


class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # distance to player

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return MeleeAction(self.entity, dx, dy).perform()  # Will attack player when adjacent

            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(self.entity, dest_x - self.entity.x, dest_y - self.entity.y).perform()

        return WaitAction(self.entity).perform()


class HostileRangedEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # distance to player

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 3:
                return RangedAction(self.entity, (target.x, target.y)).perform()  # Will attack player when in range

            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(self.entity, dest_x - self.entity.x, dest_y - self.entity.y).perform()

        return WaitAction(self.entity).perform()


class MinionEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path_to_player: List[Tuple[int, int]] = []
        self.path_to_master: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx_player = target.x - self.entity.x
        dy_player = target.y - self.entity.y
        distance_to_player = max(abs(dx_player), abs(dy_player))  # distance to player

        nearest_master = Optional[Actor]
        master_list: List[Actor] = []

        for actor in self.entity.gamemap.actors:
            if -8 < actor.x - self.entity.x < 8 and -8 < actor.y - self.entity.y < 8 and actor.master:
                master_list.append(actor)

        if master_list:
            nearest_master = master_list[0]
            dx_master = nearest_master.x - self.entity.x
            dy_master = nearest_master.y - self.entity.y
            for master in master_list:
                distance = abs(master.x - self.entity.x) + abs(master.y - self.entity.y)
                if distance < abs(dx_master) + abs(dy_master):
                    nearest_master = master
            self.path_to_master = self.get_path_to(nearest_master.x, nearest_master.y)
        else:
            nearest_master = None

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance_to_player <= 1:
                return MeleeAction(self.entity, dx_player, dy_player).perform()  # Will attack player when adjacent

            self.path_to_player = self.get_path_to(target.x, target.y)

        if self.path_to_player:
            if nearest_master:
                dx_master = nearest_master.x - self.entity.x
                dy_master = nearest_master.y - self.entity.y
                distance_to_master = max(abs(dx_master), abs(dy_master))  # distance to master
                if distance_to_master <= 1:
                    dest_x, dest_y = self.path_to_player.pop(0)
                    return MovementAction(self.entity, dest_x - self.entity.x, dest_y - self.entity.y).perform()
                else:
                    dest_x, dest_y = self.path_to_master.pop(0)
                    return MovementAction(self.entity, dest_x - self.entity.x, dest_y - self.entity.y).perform()
            else:
                dest_x, dest_y = self.path_to_player.pop(0)
                return MovementAction(self.entity, dest_x - self.entity.x, dest_y - self.entity.y).perform()

        return WaitAction(self.entity).perform()


class ConfusedEnemy(BaseAI):
    """
    A confused enemy will stumble around aimlessly for a given number of turns, then revert back to its previous AI.
    If an actor occupies a tile it is randomly moving into, it will attack.
    """

    def __init__(
            self, entity: Actor,
            previous_ai: Optional[BaseAI],
            turns_remaining: int):
        super().__init__(entity)

        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def perform(
            self) -> None:  # Its possible the actor will just bump into the wall, wasting a turn. The actor will
        # either try to move or attack in the chosen random direction.
        if self.turns_remaining <= 0:  # Revert the AI back to the original state if the effect has run its course.
            self.engine.message_log.add_message(f"The {self.entity.name} is no longer confused.")
            self.entity.ai = self.previous_ai
        else:
            direction_x, direction_y = random.choice(  # Pick a random direction
                [
                    (-1, -1),  # Northwest
                    (0, -1),  # North
                    (1, -1),  # Northeast
                    (-1, 0),  # West
                    (1, 0),  # East
                    (-1, 1),  # Southwest
                    (0, 1),  # South
                    (1, 1),  # Southeast
                ]
            )
            self.turns_remaining -= 1
            return BumpAction(self.entity, direction_x, direction_y).perform()


class EvasiveEnemy(BaseAI):
    """
    An Evasive enemy will unpredictably move towards the player while evading side to side
    """

    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # distance to player

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return MeleeAction(self.entity, dx, dy).perform()  # Will attack player when adjacent

            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dodge = bool(random.getrandbits(1))
            if not dodge:
                dest_x, dest_y = self.path.pop(0)
                return MovementAction(self.entity, dest_x - self.entity.x, dest_y - self.entity.y).perform()
            if dodge:
                direction_x, direction_y = (0, 0)
                if abs(dx) > abs(dy):
                    if dx < 0:
                        direction_x, direction_y = random.choice(  # Pick a random direction
                            [
                                (-1, -1),  # Northwest
                                (-1, 1),  # Southwest
                            ]
                        )
                    elif dx > 0:
                        direction_x, direction_y = random.choice(  # Pick a random direction
                            [
                                (1, -1),  # Northeast
                                (1, 1),  # Southeast
                            ]
                        )
                elif abs(dx) < abs(dy):
                    if dy < 0:
                        direction_x, direction_y = random.choice(  # Pick a random direction
                            [
                                (-1, -1),  # Northwest
                                (1, -1),  # Northeast
                            ]
                        )
                    elif dy > 0:
                        direction_x, direction_y = random.choice(  # Pick a random direction
                            [
                                (-1, 1),  # Southwest
                                (1, 1),  # Southeast
                            ]
                        )
                elif abs(dx) == abs(dy):
                    if dx < 0 and dy < 0:
                        direction_x, direction_y = random.choice(  # Pick a random direction
                            [
                                (-1, 0),  # West
                                (0, 1),  # South
                            ]
                        )
                    if dx < 0 < dy:
                        direction_x, direction_y = random.choice(  # Pick a random direction
                            [
                                (1, 0),  # East
                                (0, 1),  # South
                            ]
                        )
                    if dx > 0 > dy:
                        direction_x, direction_y = random.choice(  # Pick a random direction
                            [
                                (0, -1),  # North
                                (-1, 0),  # West
                            ]
                        )
                    if dx > 0 and dy > 0:
                        direction_x, direction_y = random.choice(  # Pick a random direction
                            [
                                (0, -1),  # North
                                (1, 0),  # East
                            ]
                        )
                return BumpAction(self.entity, direction_x, direction_y).perform()

        return WaitAction(self.entity).perform()
