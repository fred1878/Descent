
To run `python main.py`

requires tcod

arrow keys + home,end,page_up,page_down OR numpad to move

5 or . to wait

esc to save and exit

to descend >

v to view history

, to pickup

i for inv

c for char screen

d for drop

ctrl+/ to look around

TODO: 

## The functionality

-tidy history\
-friendly NPCs\
-reusable/learnable spells\
-more random damage\
-environment effects --traps done\
-move actor,item,gameworld to own files\
-separate root, map, message, stats console\
-status bar has more info?\
-sort inventory\
-inspect items to see stats, description etc.\
-mouse driven menus\
-talk to the dead\
-have monsters with different FOV/multi layer FOV\
-random item descriptions? chat gipitty???\
-colours change as you DescentTM\
-key rebinding\

## Endgame stuff
-rexpaint graphics OR tcod graphical tiles\
-sound\
-compile binary playable builds\

### ongoing
-trait system --in progress\
-rework level system\
-rebalance\
-pack monster spawning/better spans in general --monsters can spawn minions\
-difficulty settings that can set params for items monsters etc --menu implemented\
-different AIs --in progress\

## The Ideas Guy

-corruption - items, scrolls and potions etc increase corruption\
-traits tied to corruption and separate\
-mutations\
-necromancer enemy and spell scroll\
-more monsters\
-more gruesome/twisted monsters\
-MOAR items inc magic items, explosives, potions, scrolls, ranged weapons, GUN, traps, rooms --traps done\
-"friendly" NPCs i.e patches type friendly\

### Done pile
-potion hotkey --done\
-move MainMenu to input_handlers --done\
-move main.py functionality to engine --done\
-add static rooms by floor --done\
-add to procgen ability to make rooms in room_factories --done\
-track kills --done\
-SAN meter --done\
-req stats for items --done\
-shopkeeper --done\
-monsters sometimes have gear --done\
-when monsters die they drop inventory --done\
