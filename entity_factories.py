from components.ai import *
from components.fighter import Fighter
from entity import Actor, Item
from components.inventory import Inventory
from components import consumable, equippable
from components.level import Level
from components.equipment import Equipment
import colour

player = Actor(
    char="@",
    colour=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=10, base_power=2, base_magic=1),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=50),
)
# fren
shopkeeper = Actor(
    char="S",
    colour=(240, 210, 207),
    name="Shopkeeper",
    ai_cls=ShopAI,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=1, base_power=7, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=200),
)
# enemigos
minion = Actor(
    char="m",
    colour=(240, 210, 207),
    name="Minion",
    ai_cls=MinionEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=2, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=15),
)
master = Actor(
    char="M",
    colour=(240, 210, 207),
    name="Master",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=2, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=15),
    master=True,
)
kobold = Actor(
    char="k",
    colour=(240, 210, 207),
    name="Kobold",
    ai_cls=HostileRangedEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=3, base_defense=0, base_power=2, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=15),
)
hobbit = Actor(
    char="h",
    colour=colour.hobbit,
    name="Hobbit",
    ai_cls=EvasiveEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=6, base_defense=0, base_power=4, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=30),
)
orc = Actor(
    char="o",
    colour=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)
troll = Actor(
    char="T",
    colour=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=5, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)
reaper = Actor(
    char="D",
    colour=(20, 20, 20),
    name="Reaper",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=50, base_defense=3, base_power=9, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=500),
)
# items
small_health_potion = Item(
    char="!",
    colour=(127, 0, 255),
    name="Small Health Potion",
    consumable=consumable.HealingConsumable(amount=6),
)
health_potion = Item(
    char="!",
    colour=(0, 127, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=10),
)
lightning_scroll = Item(
    char="~",
    colour=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)
confusion_scroll = Item(
    char="~",
    colour=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll = Item(
    char="~",
    colour=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)
# equipment
dagger = Item(
    char="/",
    colour=(0, 191, 255),
    name="Dagger",
    equippable=equippable.Dagger()
)

bronze_sword = Item(
    char="/",
    colour=(205, 127, 50),
    name="Bronze Sword",
    equippable=equippable.BronzeSword()
)

iron_sword = Item(
    char="/",
    colour=(200, 200, 200),
    name="Iron Sword",
    equippable=equippable.IronSword()
)

wooden_wand = Item(
    char="\\",
    colour=(139, 69, 19),
    name="Wooden Wand",
    equippable=equippable.WoodenWand()
)

golden_wand = Item(
    char="\\",
    colour=colour.gold,
    name="Magic Wand",
    equippable=equippable.GoldenWand()
)

leather_armor = Item(
    char="[",
    colour=(139, 69, 19),
    name="Leather Armor",
    equippable=equippable.LeatherArmor(),
)

chain_mail = Item(
    char="[", colour=(192, 192, 192), name="Chain Mail", equippable=equippable.ChainMail()
)

plate_mail = Item(
    char="[", colour=(128, 128, 128), name="Plate Mail", equippable=equippable.PlateMail()
)
