from __future__ import annotations
import colour
import exceptions

from typing import Optional, Tuple, TYPE_CHECKING

import traits
from components.attribute import Trait
from render_order import RenderOrder
from tile_types import trap

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item, Chest


class Action:

    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.
        `self.engine` is the scope this action is being performed in.
        `self.entity` is the object performing the action.
        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class WaitAction(Action):
    def perform(self) -> None:
        pass


class TakeStairsAction(Action):
    def perform(self) -> None:
        """
        Take the stairs, if any exist at the entity's location.
        """
        if (self.entity.x, self.entity.y) == self.engine.game_map.downstairs_location:
            self.engine.game_world.generate_floor()
            self.engine.message_log.add_message("You descend the staircase.", colour.descend)
        else:
            raise exceptions.Impossible("There are no stairs here.")


class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""

    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("Your inventory is full.")

                self.engine.game_map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)
                if item.equippable:
                    item.equippable.on_pickup()

                self.engine.message_log.add_message(f"You picked up the {item.name}!")
                return

        raise exceptions.Impossible("There is nothing here to pick up.")


class ItemAction(Action):
    def __init__(self, entity: Actor, item: Item, target_xy: Optional[Tuple[int, int]] = None):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this action's destination."""
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        """Invoke the items ability, this action will be given to provide context."""
        if self.item.consumable:
            self.item.consumable.activate(self)


def find_quick_heal(player: Actor) -> ItemAction:
    for item in player.inventory.items:
        if item.name == "Health Potion" and (player.fighter.max_hp - player.fighter.hp) >= 10:
            return ItemAction(player, item)
        if item.name == "Small Health Potion" and (player.fighter.max_hp - player.fighter.hp) >= 6:
            return ItemAction(player, item)


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this action's destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    @property
    def target_chest(self) -> Optional[Chest]:
        """Return the actor at this action's destination."""
        return self.engine.game_map.get_chest_at_location(*self.dest_xy)

    @property
    def target_tile(self):
        dest_x, dest_y = self.dest_xy
        return self.engine.game_map.tiles[dest_x, dest_y]

    def perform(self) -> None:
        raise NotImplementedError()


class DebugAction(Action):
    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        pass


class DebugAction2(Action):
    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        traits.attack_down.add_trait(self.entity)
        print("debug action2")


class TargetAction(Action):
    def __init__(self, entity: Actor, target_xy: Tuple[int, int]):
        super().__init__(entity)
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this action's destination."""
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class DropItem(ItemAction):
    def perform(self) -> None:
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item, self.entity)
        self.entity.inventory.drop(self.item)


class EquipAction(Action):
    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity)

        self.item = item

    def perform(self) -> None:
        self.entity.equipment.toggle_equip(self.item, self.entity)


class RangedAttackAction(TargetAction):
    def __init__(self, entity: Actor, target_xy: Tuple[int, int]):
        super().__init__(entity, target_xy)

    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack.")

        damage = self.entity.fighter.ranged_power - target.fighter.defense

        attack_desc = f"{self.entity.name.capitalize()} shoots {target.name.capitalize()}"
        if self.entity is self.engine.player:
            attack_colour = colour.player_atk
        else:
            attack_colour = colour.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(f"{attack_desc} for {damage} hit points.", attack_colour)
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(f"{attack_desc} but does no damage.", colour.player_atk_no_damage)


class RangedBuffAction(TargetAction):
    def __init__(self, entity: Actor, target_xy: Tuple[int, int], trait: Trait):
        super().__init__(entity, target_xy)
        self.trait = trait

    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to target.")

        self.trait.add_trait(target)

        action_desc = f"{self.entity.name.capitalize()} casts " \
                      f"{self.trait.name.capitalize()} on {target.name.capitalize()}"
        if self.entity is self.engine.player:
            attack_colour = colour.player_atk
        else:
            attack_colour = colour.enemy_atk

        self.engine.message_log.add_message(action_desc, attack_colour)


class ResurrectAction(TargetAction):

    def __init__(self, entity: Actor, target_xy: Tuple[int, int]):
        super().__init__(entity, target_xy)

    @property
    def target_corpse(self) -> Optional[Actor]:
        """Return the corpse at this action's destination."""
        return self.engine.game_map.get_corpse_at_location(*self.target_xy)

    def perform(self) -> None:
        from components.ai import HostileEnemy
        from components.ai import AllyAI
        target = self.target_corpse
        if not target:
            raise exceptions.Impossible("Nothing to target.")
        if target.ai:
            raise exceptions.Impossible("Target is not dead")
        if self.entity == self.engine.player:
            target.ai = AllyAI(target)
            target.friendly = True
        else:
            target.ai = HostileEnemy(target)

        target.char = "z"
        target.render_order = RenderOrder.ACTOR
        target.blocks_movement = True
        target.level.xp_given = 0
        target.level.gold_given = 0
        if not target.name[:6] == "zombie":
            target.name = f"zombie of {target.name[11:]}"

        action_desc = f"{self.entity.name.capitalize()} revives {target.name.capitalize()}"

        self.engine.message_log.add_message(action_desc, colour.blood)


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack.")

        damage = self.entity.fighter.melee_power - target.fighter.defense

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name.capitalize()}"
        if self.entity is self.engine.player:
            attack_colour = colour.player_atk
        else:
            attack_colour = colour.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(f"{attack_desc} for {damage} hit points.", attack_colour)
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(f"{attack_desc} but does no damage.", colour.player_atk_no_damage)


class MovementAction(ActionWithDirection):

    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is blocked.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination is blocked by a tile.
            raise exceptions.Impossible("That way is blocked.")
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            # Destination is blocked by an entity.
            raise exceptions.Impossible("That way is blocked.")

        if self.target_tile == trap:
            if self.entity is self.engine.player:
                self.engine.message_log.add_message("You walked over a trap")
                self.engine.player.fighter.take_damage(5)

        self.entity.move(self.dx, self.dy)

        if self.entity is self.engine.player:
            print("x: " + str(self.entity.x) + " y: " + str(self.entity.y))


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            if self.target_actor.name == 'Shopkeeper' and self.target_actor.friendly \
                    and self.entity is self.engine.player:
                self.engine.message_log.add_message("Buy my stuff!", colour.gold)
            elif self.entity is self.engine.player and self.target_actor.friendly:
                return SwapLocationAction(self.entity, self.dx, self.dy).perform()
            else:
                return MeleeAction(self.entity, self.dx, self.dy).perform()
        if self.target_chest:
            if not self.target_chest.opened:
                print('opened chest')
                self.engine.message_log.add_message("You opened the chest")
                self.target_chest.open_chest()
            else:
                print('chest opened')
                return MovementAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()


class SwapLocationAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_tile == trap:
            if self.entity is self.engine.player:
                self.engine.message_log.add_message("You walked over a trap")
                self.engine.player.fighter.take_damage(5)
        self.target_actor.move(-self.dx, -self.dy)
        self.entity.move(self.dx, self.dy)
