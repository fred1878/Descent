from __future__ import annotations
from typing import Callable, Optional, Tuple, TYPE_CHECKING, Union
import os
import tcod.event  # type: ignore
from tcod import libtcodpy
import actions
from actions import Action, BumpAction, WaitAction, PickupAction
import colour
import exceptions
import setup_game
import traceback
from difficulty_settings import DifficultySettings
from util import number_of_digits

if TYPE_CHECKING:
    from engine import Engine
    from entity import Item, Actor

MOVE_KEYS = {
    # Arrow keys.
    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, 1),
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (1, 0),
    tcod.event.KeySym.HOME: (-1, -1),
    tcod.event.KeySym.END: (-1, 1),
    tcod.event.KeySym.PAGEUP: (1, -1),
    tcod.event.KeySym.PAGEDOWN: (1, 1),
    # Numpad keys.
    tcod.event.KeySym.KP_1: (-1, 1),
    tcod.event.KeySym.KP_2: (0, 1),
    tcod.event.KeySym.KP_3: (1, 1),
    tcod.event.KeySym.KP_4: (-1, 0),
    tcod.event.KeySym.KP_6: (1, 0),
    tcod.event.KeySym.KP_7: (-1, -1),
    tcod.event.KeySym.KP_8: (0, -1),
    tcod.event.KeySym.KP_9: (1, -1),
}

WAIT_KEYS = {
    tcod.event.KeySym.PERIOD,
    tcod.event.KeySym.KP_5,
    tcod.event.KeySym.CLEAR,
}

CONFIRM_KEYS = {
    tcod.event.KeySym.RETURN,
    tcod.event.KeySym.KP_ENTER,
}

ActionOrHandler = Union[Action, "BaseEventHandler"]
"""An event handler return value which can trigger an action or switch active handlers.

If a handler is returned then it will become the active handler for future events.
If an action is returned it will be attempted and if it's valid then
MainGameEventHandler will become the active handler.
"""


class BaseEventHandler(tcod.event.EventDispatch[ActionOrHandler]):
    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        """Handle an event and return the next active event handler."""
        state = self.dispatch(event)
        if isinstance(state, BaseEventHandler):
            return state
        assert not isinstance(state, Action), f"{self!r} can not handle actions."
        return self

    def on_render(self, console: tcod.Console) -> None:
        raise NotImplementedError()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()


class MainMenu(BaseEventHandler):
    """Handle the main menu rendering and input."""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(setup_game.background_image, 0, 0)

        console.print(console.width // 2, console.height // 2 - 4, "DESCENT", fg=colour.menu_title,
                      alignment=libtcodpy.CENTER)
        console.print(console.width // 2, console.height - 2, "By fred1878", fg=colour.menu_title,
                      alignment=libtcodpy.CENTER)

        menu_width = 24
        for i, text in enumerate([" Play a [N]ew game", "[C]ontinue last game", "[O]ptions", "[Q]uit"]):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=colour.menu_text,
                bg=colour.black,
                alignment=libtcodpy.CENTER,
                bg_blend=libtcodpy.BKGND_ALPHA(64),
            )

    def ev_keydown(
            self, event: tcod.event.KeyDown
    ) -> Optional[BaseEventHandler]:
        if event.sym in (tcod.event.KeySym.q, tcod.event.KeySym.ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.KeySym.c:
            try:
                return MainGameEventHandler(setup_game.load_game("savegame.sav"))
            except FileNotFoundError:
                return PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.KeySym.n:
            return DifficultySelect(self.screen_width, self.screen_height)
        elif event.sym == tcod.event.KeySym.o:
            return OptionsMenu(self.screen_width, self.screen_height)

        return None


class OptionsMenu(BaseEventHandler):
    """Displays the options menu"""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

    def on_render(self, console: tcod.Console) -> None:
        console.draw_semigraphics(setup_game.background_image, 0, 0)
        console.print(console.width // 2, console.height // 2 - 4, "Options", fg=colour.menu_title,
                      alignment=libtcodpy.CENTER)
        menu_width = 8
        for i, text in enumerate(["[K]eybinds"]):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=colour.menu_text,
                bg=colour.black,
                alignment=libtcodpy.CENTER,
                bg_blend=libtcodpy.BKGND_ALPHA(64),
            )

    def ev_keydown(
            self, event: tcod.event.KeyDown
    ) -> Optional[BaseEventHandler]:
        if event.sym == tcod.event.KeySym.ESCAPE:
            raise SystemExit()
        elif event.sym == tcod.event.KeySym.k:
            return KeybindingsMenu(self.screen_width, self.screen_height)

        return None


class KeybindingsMenu(BaseEventHandler):
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height


class DifficultySelect(BaseEventHandler):
    """Display select difficulty menu"""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

    def on_render(self, console: tcod.Console) -> None:
        console.draw_semigraphics(setup_game.background_image, 0, 0)
        console.print(console.width // 2, console.height // 2 - 4, "Select a difficulty", fg=colour.menu_title,
                      alignment=libtcodpy.CENTER)
        menu_width = 8
        for i, text in enumerate(["[E]asy", "[M]edium", "[H]ard"]):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=colour.menu_text,
                bg=colour.black,
                alignment=libtcodpy.CENTER,
                bg_blend=libtcodpy.BKGND_ALPHA(64),
            )

    def ev_keydown(
            self, event: tcod.event.KeyDown
    ) -> Optional[BaseEventHandler]:
        if event.sym == tcod.event.KeySym.ESCAPE:
            raise SystemExit()
        elif event.sym == tcod.event.KeySym.e:
            return MainGameEventHandler(setup_game.new_game(self.screen_width, self.screen_height,
                                                            DifficultySettings.EASY))
        elif event.sym == tcod.event.KeySym.m:
            return MainGameEventHandler(setup_game.new_game(self.screen_width, self.screen_height,
                                                            DifficultySettings.MEDIUM))
        elif event.sym == tcod.event.KeySym.h:
            return MainGameEventHandler(setup_game.new_game(self.screen_width, self.screen_height,
                                                            DifficultySettings.HARD))

        return None


class PopupMessage(BaseEventHandler):
    """Display a popup text window."""

    def __init__(self, parent_handler: BaseEventHandler, text: str):
        self.parent = parent_handler
        self.text = text

    def on_render(self, console: tcod.Console) -> None:
        """Render the parent and dim the result, then print the message on top."""
        self.parent.on_render(console)
        console.tiles_rgb["fg"] //= 8
        console.tiles_rgb["bg"] //= 8

        console.print(
            console.width // 2,
            console.height // 2,
            self.text,
            fg=colour.white,
            bg=colour.black,
            alignment=tcod.CENTER,
        )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[BaseEventHandler]:
        """Any key returns to the parent handler."""
        return self.parent


class EventHandler(BaseEventHandler):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        """Handle events for input handlers with an engine."""
        action_or_state = self.dispatch(event)
        if isinstance(action_or_state, BaseEventHandler):
            return action_or_state
        if self.handle_action(action_or_state):
            # A valid action was performed.
            if not self.engine.player.is_alive:
                # The player was killed sometime during or after the action.
                return GameOverEventHandler(self.engine)
            elif self.engine.player.level.requires_level_up:
                return LevelUpEventHandler(self.engine)
            return MainGameEventHandler(self.engine)  # Return to the main handler.
        return self

    def handle_action(self, action: Optional[Action]) -> bool:
        """Handle actions returned from event methods.

        Returns True if the action will advance a turn.
        """
        if action is None:
            return False

        try:
            action.perform()
        except exceptions.Impossible as exc:
            self.engine.message_log.add_message(exc.args[0], colour.impossible)
            return False  # Skip enemy turn on exceptions.

        self.engine.handle_enemy_turns()

        self.engine.handle_duration_events()

        self.engine.update_fov()
        return True

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = event.tile.x, event.tile.y

    def on_render(self, console: tcod.Console) -> None:
        self.engine.render(console)


class AskUserEventHandler(EventHandler):
    """Handles user input for actions which require special input."""

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        """By default any key exits this input handler."""
        if event.sym in {
            tcod.event.KeySym.LSHIFT,
            tcod.event.KeySym.RSHIFT,
            tcod.event.KeySym.LCTRL,
            tcod.event.KeySym.RCTRL,
            tcod.event.KeySym.LALT,
            tcod.event.KeySym.RALT}:  # Ignore modifier keys.
            return None
        return self.on_exit()

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:
        """By default any mouse click exits this input handler."""
        return self.on_exit()

    def on_exit(self) -> Optional[ActionOrHandler]:
        """Called when the user is trying to exit or cancel an action.

        By default this returns to the main event handler.
        """
        return MainGameEventHandler(self.engine)


class CharacterScreenEventHandler(AskUserEventHandler):
    TITLE = "Character Information"

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)
        player = self.engine.player

        if player.x <= 30:
            x = 40
        else:
            x = 0

        y = 0

        width = len(self.TITLE) + 4

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=9,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        console.print(x=x + 1, y=y + 1, string=f"Level: {player.level.current_level}")
        console.print(x=x + 1, y=y + 2, string=f"XP: {player.level.current_xp}")
        console.print(x=x + 1, y=y + 3,
                      string=f"XP for next Level: {player.level.experience_to_next_level}", )

        console.print(x=x + 1, y=y + 4, string=f"Melee Attack: {player.fighter.melee_power}")
        console.print(x=x + 1, y=y + 5, string=f"Ranged Attack: {player.fighter.ranged_power}")
        console.print(x=x + 1, y=y + 6, string=f"Defense: {player.fighter.defense}")
        console.print(x=x + 1, y=y + 7, string=f"Magic: {player.fighter.magic}")


class TraitScreenEventHandler(AskUserEventHandler):
    TITLE = "Trait Information"

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)
        player = self.engine.player

        if player.x <= 30:
            x = 40
        else:
            x = 0

        y = 0

        width = len(self.TITLE) + 4
        traits = player.attribute.traits
        number_of_traits = len(traits)
        if len(traits) > 0:
            for i, trait in enumerate(traits):
                trait_length = len(trait.name) + len(trait.description) + 7
                if hasattr(trait, "max_duration"):
                    trait_length = len(trait.name) + len(trait.description) + \
                                   number_of_digits(trait.current_duration) + 10
                if trait_length > width:
                    width = trait_length

        height = number_of_traits + 2

        if height <= 3:
            height = 3

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=height,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        if len(traits) > 0:
            for i, trait in enumerate(traits):
                trait_string = f"({trait.name}) - {trait.description}"
                if hasattr(trait, "max_duration"):
                    trait_string = trait_string + f" ({trait.current_duration})"
                console.print(x + 1, y + i + 1, trait_string)
        else:
            console.print(x + 1, y + 1, "No Traits")


class LevelUpEventHandler(AskUserEventHandler):
    TITLE = "Level Up"

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)
        player = self.engine.player

        if player.x <= 30:
            x = 40
        else:
            x = 0

        console.draw_frame(
            x=x,
            y=0,
            width=45,
            height=10,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        console.print(x=x + 1, y=1, string="Congratulations! You level up!")
        console.print(x=x + 1, y=2, string="Select an attribute to increase.")

        console.print(x=x + 1, y=4, string=f"a) Constitution (+20 HP, from {player.fighter.max_hp})")
        console.print(x=x + 1, y=5, string=f"b) Strength (+1 melee attack, from {player.fighter.base_melee})")
        console.print(x=x + 1, y=6, string=f"c) Perception (+1 ranged attack, from {player.fighter.base_ranged})")
        console.print(x=x + 1, y=7, string=f"d) Agility (+1 defense, from {player.fighter.base_defense})")
        console.print(x=x + 1, y=8, string=f"e) Magic (+3 magic, from {player.fighter.base_magic})")

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        player = self.engine.player
        key = event.sym
        index = key - tcod.event.KeySym.a

        if 0 <= index <= 4:
            if index == 0:
                player.level.increase_max_hp()
            elif index == 1:
                player.level.increase_melee()
            elif index == 2:
                player.level.increase_ranged()
            elif index == 3:
                player.level.increase_defense()
            else:
                player.level.increase_magic()
        else:
            self.engine.message_log.add_message("Invalid entry.", colour.invalid)

            return None

        return super().ev_keydown(event)

    def ev_mousebuttondown(
            self, event: tcod.event.MouseButtonDown
    ) -> Optional[ActionOrHandler]:
        """
        Don't allow the player to click to exit the menu, like normal.
        """
        return None


class InventoryEventHandler(AskUserEventHandler):
    """This handler lets the user select an item.

    What happens then depends on the subclass.
    """

    TITLE = "<missing title>"

    def on_render(self, console: tcod.Console) -> None:
        """Render an inventory menu, which displays the items in the inventory, and the letter to select them.
        Will move to a different position based on where the player is located, so the player can always see where
        they are.
        """
        super().on_render(console)
        player = self.engine.player
        number_of_items_in_inventory = len(player.inventory.items)

        height = number_of_items_in_inventory + 2

        if height <= 3:
            height = 3

        if player.x <= 30:
            x = 40
        else:
            x = 0

        y = 0

        width = len(self.TITLE) + 4

        for i, item in enumerate(player.inventory.items):
            item_width = len(item.name) + len(str(item.price)) + 9
            if item_width > width:
                width = item_width

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=height,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        if number_of_items_in_inventory > 0:
            for i, item in enumerate(player.inventory.items):
                item_key = chr(ord("a") + i)
                is_equipped = player.equipment.item_is_equipped(item)

                item_string = f"({item_key}) {item.name}"

                if is_equipped:
                    item_string = f"{item_string} (E)"

                console.print(x + 1, y + i + 1, item_string)
        else:
            console.print(x + 1, y + 1, "(Empty)")

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        player = self.engine.player
        key = event.sym
        index = key - tcod.event.KeySym.a

        if 0 <= index <= 26:
            try:
                selected_item = player.inventory.items[index]
            except IndexError:
                self.engine.message_log.add_message("Invalid entry.", colour.invalid)
                return None
            return self.on_item_selected(selected_item)
        return super().ev_keydown(event)

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        """Called when the user selects a valid item."""
        raise NotImplementedError()


class InventoryActivateHandler(InventoryEventHandler):
    """Handle using an inventory item."""

    TITLE = "Select an item to use"

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        """Return the action for the selected item."""
        if item.consumable:
            # Return the action for the selected item.
            return item.consumable.get_action(self.engine.player)
        elif item.equippable:
            return actions.EquipAction(self.engine.player, item)
        else:
            return None


class InventoryDropHandler(InventoryEventHandler):
    """Handle dropping an inventory item."""

    TITLE = "Select an item to drop"

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        """Drop this item."""
        return actions.DropItem(self.engine.player, item)


class ShopEventHandler(AskUserEventHandler):
    """This handler lets access the shop"""

    def __init__(self, engine: Engine, shopkeeper: Actor):
        super().__init__(engine)
        self.shopkeeper = shopkeeper

    TITLE = "Select an item to buy"

    def on_render(self, console: tcod.Console) -> None:
        """Render an shop menu, which displays the items in the shop, and the letter to select them.
        Will move to a different position based on where the player is located, so the player can always see where
        they are.
        """
        super().on_render(console)
        number_of_items_in_shop = len(self.shopkeeper.inventory.items)
        player = self.engine.player

        shop_menu_height = number_of_items_in_shop + 2

        if shop_menu_height <= 3:
            shop_menu_height = 3

        if player.x <= 30:
            x = 40
        else:
            x = 0
        y = 0

        shop_menu_width = len(self.TITLE) + 4

        for i, item in enumerate(self.shopkeeper.inventory.items):
            item_width = len(item.name) + len(str(item.price)) + 16
            if item_width > shop_menu_width:
                shop_menu_width = item_width

        console.draw_frame(
            x=x,
            y=y,
            width=shop_menu_width,
            height=shop_menu_height,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        if number_of_items_in_shop > 0:
            for i, item in enumerate(self.shopkeeper.inventory.items):
                item_key = chr(ord("a") + i)
                is_equipped = self.shopkeeper.equipment.item_is_equipped(item)

                item_string = f"({item_key}) {item.name} Cost:{item.price}"

                if is_equipped:
                    item_string = f"{item_string} (E)"

                console.print(x + 1, y + i + 1, item_string)
        else:
            console.print(x + 1, y + 1, "(Empty)")

        number_of_items_in_inventory = len(player.inventory.items)
        player_inventory_height = number_of_items_in_inventory + 2

        if player_inventory_height <= 3:
            player_inventory_height = 3

        if player.x <= 30:
            x = 70
        else:
            x = 30
        y = 0

        player_inventory_width = 0

        for i, item in enumerate(player.inventory.items):
            item_width = len(item.name) + len(str(item.price)) + 16
            if item_width > player_inventory_width:
                player_inventory_width = item_width

        console.draw_frame(
            x=x,
            y=y,
            width=player_inventory_width,
            height=player_inventory_height + 1,
            title="Sell Items",
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )
        console.print(x + 1, y + 1, "Hold SHIFT to sell items")
        if number_of_items_in_inventory > 0:
            for i, item in enumerate(player.inventory.items):
                item_key = chr(ord("a") + i)
                is_equipped = player.equipment.item_is_equipped(item)

                item_string = f"({item_key}) {item.name}"

                if is_equipped:
                    item_string = f"{item_string} (E)"

                console.print(x + 1, y + i + 2, item_string)
        else:
            console.print(x + 1, y + 1, "(Empty)")

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        player = self.engine.player
        key = event.sym
        index = key - tcod.event.KeySym.a
        modifier = event.mod

        if 0 <= index <= 26 and not modifier:
            try:
                selected_item = self.shopkeeper.inventory.items[index]
            except IndexError:
                self.engine.message_log.add_message("Invalid entry.", colour.invalid)
                return None
            return self.on_item_selected(selected_item)

        if 0 <= index <= 26 and modifier:
            try:
                selected_item = player.inventory.items[index]
            except IndexError:
                self.engine.message_log.add_message("Invalid entry.", colour.invalid)
                return None
            return self.on_item_selected(selected_item)
        return super().ev_keydown(event)

    def on_item_selected(self, item: Item) -> None:
        player = self.engine.player
        """Called when the user selects a valid item."""
        if item in self.shopkeeper.inventory.items:
            if item.price < player.level.current_gold and \
                    len(player.inventory.items) <= player.inventory.capacity:
                if self.shopkeeper.equipment.item_is_equipped(item):
                    self.shopkeeper.equipment.toggle_equip(item, self.shopkeeper, add_message=False)
                self.shopkeeper.inventory.items.remove(item)
                player.inventory.items.append(item)
                player.level.change_gold(-item.price)
                self.engine.message_log.add_message(f"You bought the {item.name} for {item.price} gold!", colour.gold)
            elif item.price > player.level.current_gold:
                raise exceptions.Impossible("You do not have enough gold")
            elif len(player.inventory.items) >= player.inventory.capacity:
                raise exceptions.Impossible("Your inventory is full.")
        elif item in player.inventory.items:
            if len(self.shopkeeper.inventory.items) >= self.shopkeeper.inventory.capacity:
                raise exceptions.Impossible("Shopkeeper inventory is full")
            else:
                if player.equipment.item_is_equipped(item):
                    player.equipment.toggle_equip(item, player, add_message=False)
                player.inventory.items.remove(item)
                self.shopkeeper.inventory.items.append(item)
                player.level.change_gold(item.price)
                self.engine.message_log.add_message(f"You sold the {item.name} for {item.price} gold!", colour.gold)


class SelectIndexHandler(AskUserEventHandler):
    """Handles asking the user for an index on the map."""

    def __init__(self, engine: Engine):
        """Sets the cursor to the player when this handler is constructed."""
        super().__init__(engine)
        player = self.engine.player
        engine.mouse_location = player.x, player.y

    def on_render(self, console: tcod.Console) -> None:
        """Highlight the tile under the cursor."""
        super().on_render(console)
        x, y = self.engine.mouse_location
        console.tiles_rgb["bg"][x, y] = colour.white
        console.tiles_rgb["fg"][x, y] = colour.black

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        """Check for key movement or confirmation keys."""
        key = event.sym
        if key in MOVE_KEYS:
            modifier = 1  # Holding modifier keys will speed up key movement.
            if event.mod & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
                modifier *= 5
            if event.mod & (tcod.event.KMOD_LCTRL | tcod.event.KMOD_RCTRL):
                modifier *= 10
            if event.mod & (tcod.event.KMOD_LALT | tcod.event.KMOD_RALT):
                modifier *= 20

            x, y = self.engine.mouse_location
            dx, dy = MOVE_KEYS[key]
            x += dx * modifier
            y += dy * modifier
            # Clamp the cursor index to the map size.
            x = max(0, min(x, self.engine.game_map.width - 1))
            y = max(0, min(y, self.engine.game_map.height - 1))
            self.engine.mouse_location = x, y
            return None
        elif key in CONFIRM_KEYS:
            return self.on_index_selected(*self.engine.mouse_location)
        return super().ev_keydown(event)

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[Action]:
        """Left click confirms a selection."""
        if self.engine.game_map.in_bounds(*event.tile):
            if event.button == 1:
                return self.on_index_selected(*event.tile)
        return super().ev_mousebuttondown(event)

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        """Called when an index is selected."""
        raise NotImplementedError()


class LookHandler(SelectIndexHandler):
    """Lets the player look around using the keyboard."""

    def on_index_selected(self, x: int, y: int) -> MainGameEventHandler:
        """Return to main handler."""
        return MainGameEventHandler(self.engine)


class TargetMeleeAttackHandler(SelectIndexHandler):

    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.player = self.engine.player
        engine.mouse_location = self.player.x, self.player.y

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        key = event.sym
        if key == tcod.event.KeySym.ESCAPE:
            return MainGameEventHandler(self.engine)
        if key in MOVE_KEYS:
            x, y = self.engine.mouse_location
            dx, dy = MOVE_KEYS[key]
            x += dx
            y += dy
            x = max(self.player.x - 1, min(x, self.player.x + 1))
            y = max(self.player.y - 1, min(y, self.player.y + 1))
            self.engine.mouse_location = x, y
            return None
        elif key in CONFIRM_KEYS:
            x, y = self.engine.mouse_location
            x = max(0, min(x, self.engine.game_map.width - 1))
            y = max(0, min(y, self.engine.game_map.height - 1))
            dx = x - self.player.x
            dy = y - self.player.y
            return actions.MeleeAction(self.player, dx, dy)

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        if self.player.x - 1 > x < self.player.x + 1 or self.player.y - 1 > y < self.player.y + 1:
            self.engine.message_log.add_message("Out of melee range")
        else:
            dx = x - self.player.x
            dy = y - self.player.y
            return actions.MeleeAction(self.player, dx, dy)


class SingleRangedAttackHandler(SelectIndexHandler):
    """Handles targeting a single enemy. Only the enemy selected will be affected."""

    def __init__(self, engine: Engine, callback: Callable[[Tuple[int, int]], Optional[Action]]):
        super().__init__(engine)

        self.callback = callback

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x, y))


class AreaRangedAttackHandler(SelectIndexHandler):
    """Handles targeting an area within a given radius. Any entity within the area will be affected."""

    def __init__(
            self,
            engine: Engine,
            radius: int,
            callback: Callable[[Tuple[int, int]], Optional[Action]],
    ):
        super().__init__(engine)

        self.radius = radius
        self.callback = callback

    def on_render(self, console: tcod.Console) -> None:
        """Highlight the tile under the cursor."""
        super().on_render(console)

        x, y = self.engine.mouse_location

        # Draw a rectangle around the targeted area, so the player can see the affected tiles.
        console.draw_frame(
            x=x - self.radius - 1,
            y=y - self.radius - 1,
            width=self.radius ** 2,
            height=self.radius ** 2,
            fg=colour.red,
            clear=False,
        )

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x, y))


class MainGameEventHandler(EventHandler):

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        action: Optional[Action] = None

        key = event.sym
        modifier = event.mod

        player = self.engine.player

        if key == tcod.event.KeySym.PERIOD and modifier & (
                tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT
        ):
            return actions.TakeStairsAction(player)

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(player, dx, dy)
        elif key in WAIT_KEYS:
            action = WaitAction(player)

        elif key == tcod.event.KeySym.ESCAPE:
            raise SystemExit()
        elif key == tcod.event.KeySym.v:
            return HistoryViewer(self.engine)
        elif key == tcod.event.KeySym.COMMA:
            action = PickupAction(player)
        elif key == tcod.event.KeySym.i:
            return InventoryActivateHandler(self.engine)
        elif key == tcod.event.KeySym.d:
            return InventoryDropHandler(self.engine)
        elif key == tcod.event.KeySym.SLASH:
            return LookHandler(self.engine)
        elif key == tcod.event.KeySym.c:
            return CharacterScreenEventHandler(self.engine)
        elif key == tcod.event.KeySym.a:
            return TargetMeleeAttackHandler(self.engine)
        elif key == tcod.event.KeySym.s:
            return SingleRangedAttackHandler(
                self.engine, callback=lambda xy: actions.RangedAttackAction(self.engine.player, xy))
        elif key == tcod.event.KeySym.e:
            return SingleRangedAttackHandler(
                self.engine, callback=lambda xy: actions.ResurrectAction(self.engine.player, xy))
        elif key == tcod.event.KeySym.p:
            action = actions.find_quick_heal(self.engine.player)
        elif key == tcod.event.KeySym.t:
            return TraitScreenEventHandler(self.engine)
        elif key == tcod.event.KeySym.q:
            action = actions.DebugAction(self.engine.player)
        elif key == tcod.event.KeySym.w:
            action = actions.DebugAction2(self.engine.player)
        elif key == tcod.event.KeySym.z:
            nearest_shop = None
            closest_distance = 3
            for actor in self.engine.game_map.actors:
                if actor is not self.engine.player and self.engine.game_map.visible[actor.x, actor.y]:
                    distance = self.engine.player.distance(actor.x, actor.y)
                    if distance < closest_distance:
                        nearest_shop = actor
                        closest_distance = distance
            if nearest_shop is None:
                self.engine.message_log.add_message("No shop nearby", colour.invalid)
                return WaitAction(player)
            else:
                return ShopEventHandler(self.engine, nearest_shop)

        # No valid key was pressed
        return action


def on_quit() -> None:
    """Handle exiting out of a finished game."""
    if os.path.exists("savegame.sav"):
        os.remove("savegame.sav")  # Deletes the active save file.
    raise exceptions.QuitWithoutSaving()  # Avoid saving a finished game.


class GameOverEventHandler(EventHandler):

    def ev_quit(self, event: tcod.event.Quit) -> None:
        on_quit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        if event.sym == tcod.event.KeySym.ESCAPE:
            on_quit()


CURSOR_Y_KEYS = {
    tcod.event.KeySym.UP: -1,
    tcod.event.KeySym.DOWN: 1,
    tcod.event.KeySym.PAGEUP: -20,
    tcod.event.KeySym.PAGEDOWN: 20,
}


class HistoryViewer(EventHandler):
    """Print the history on a larger window which can be navigated."""

    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length - 1

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)  # Draw the main state as the background.

        log_console = tcod.Console(console.width - 6, console.height - 6)

        # Draw a frame with a custom banner title.
        log_console.draw_frame(0, 0, log_console.width, log_console.height)
        log_console.print_box(
            0, 0, log_console.width, 1, "┤Message history├", alignment=tcod.CENTER
        )

        # Render the message log using the cursor parameter.
        self.engine.message_log.render_messages(
            log_console,
            1,
            1,
            log_console.width - 2,
            log_console.height - 2,
            self.engine.message_log.messages[: self.cursor + 1],
        )
        log_console.blit(console, 3, 3)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[MainGameEventHandler]:
        # Fancy conditional movement to make it feel right.
        if event.sym in CURSOR_Y_KEYS:
            adjust = CURSOR_Y_KEYS[event.sym]
            if adjust < 0 and self.cursor == 0:
                # Only move from the top to the bottom when you're on the edge.
                self.cursor = self.log_length - 1
            elif adjust > 0 and self.cursor == self.log_length - 1:
                # Same with bottom to top movement.
                self.cursor = 0
            else:
                # Otherwise move while staying clamped to the bounds of the history log.
                self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))
        elif event.sym == tcod.event.KeySym.HOME:
            self.cursor = 0  # Move directly to the top message.
        elif event.sym == tcod.event.KeySym.END:
            self.cursor = self.log_length - 1  # Move directly to the last message.
        else:  # Any other key moves back to the main game state.
            return MainGameEventHandler(self.engine)
        return None
