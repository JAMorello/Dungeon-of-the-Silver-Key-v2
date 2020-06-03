# Dungeon Of The Silver Key
## A basic Lovecraft inspired text-based dungeon crawler written in Python

![Nyarlathothep by jason engle](/data/banner002.jpg)

> *“There are twists of time and space, of vision and reality, which only a dreamer can divine; 
> and from what I know of Carter I think he has merely found a way to traverse these mazes.”*
> **"The Silver Key" of H.P. Lovecraft**

This is a project based and inspired in the original code of  [@Mili-NT](https://github.com/Mili-NT/Dungeon-Of-The-Silver-Key) 
and my reworking of that code. I intend to make a version 2 of that game, but as there are intended a lot of changes, 
possibly the result is an entire new game. This is an exercise in Object Oriented Programming. Also, in 
"Research on Interactive Fiction.txt" you can see some notes and links of my research on IF for this project 
(for now, there is not a lot of that implemented, hopefully in the future I´ll do it!).

Table of Contents
=================

  * [How to run the game](#how-to-run-the-game)
  * [How to play](#how-to-play)
  * [There is still work to be done](#there-is-still-work-to-be-done)

### How to run the game:

Depending on what stage of development is, perhaps you can´t play the game with the latest addition as there is work to 
be done and some modifications are continuously made (it´s more probable that I have a separated branch with the changes
that makes the game unusable).
 
Nonetheless, you can download the files from 'master-v2' branch (last update: 15/05/2020) and play with the latest 
available executable (uploaded: 10/05/2020). Make sure it is in same directory as the "data" folder.

Or you can try your luck and use all the files of the project (the newest from the 'master-v2' branch or the base game 
from "modified-old-code" branch, or even the old version of @Mili-NT in 'old-game-code') to run the game (through 
"start.py") in your local Python environment. If you are going to do the latter, don´t forget to install the 
requirements.txt! You need the [colorama](https://pypi.org/project/colorama/), [tabulate](https://pypi.org/project/tabulate/)
, and [pyfliget](https://github.com/pwaller/pyfiglet) modules in your virtual environment to run the game.  

### How to play:

The game operates similar to other text adventures or interactive fiction games.  
There is a command prompt and some common commands that you can type. 
The off-combat interpreter is very rudimentary and understands very simplistic english commands. 
The game is not exhaustive or comprehensive, so there might be some misunderstanding by the interpreter.

   - move <?>    //    Travel to the north, south, west or east (also works: n, s, w, e)

   - look <?>    //    You can look at the room, available doors, map and inventory

   - take <?>    //    Picks up an item
    
   - use <?>     //    Uses an item (only potions)
    
* While seeing inventory you can inspect closely an item by typing the name (for now, case sensitive)
* While in combat, a list of possible combat moves is showed to you and you move write the complete name of the move of your choice.

### There is still work to be done:

    * Plot
        - [ ] Add a story
        - [ ] Work in the prose (descriptions of rooms, enemies, objects, etc)
        - [ ] Make some things ambiguous so the player can fill the blanks with his imagination
    
    * Parser:
        - [x] Make a rudimentary parser
        - [ ] Work a bit in the parser (look at object/monster/near room, drop object, see user stats, etc)
        - [ ] Add use of some spells outside of combat
        - [ ] Make the parser a bit more sofisticaded (implement prepositions)
        - [ ] ???
    
    * Game Flow
        - [x] Add a sleep() between some functions so one is not flooded with text
        - [x] A "grab the left behind item in the room" function is missing
        - [x] The "view map" should show only the visited rooms
        - [ ] Implement off combat use of spells
        - [ ] do_look(): in general ("look"); to object, to room, to direction (cleaner())
        - [ ] do_examine(): ("examine") "Examine what?"; with obj, do_look(). ¿What if more info?
        
    * Map
        - [ ] Review layout of the rooms
        - [ ] Review placement of enemies
        - [ ] Review placement of items
        - [ ] Adding puzzles and little notes
        - [ ] Maybe adding another "floor" in the dungeon (or an "exterior" previous to enter the dungeon)
        
    * Rooms
        - [x] Insert the data in a json file
        - [x] Reduce all the room scripts to only one
        - [ ] get_near_room_description() --> In current room (more complex dict) or from dumped .json (only one line, but how?)
        - [ ] Add more data in the dictionaries (what data? near_room_description, i.e??)
        
    * Player
        - [x] Implement properties and setters to the class
        - [x] Add as class variables the max_stats, attacks, and score
        - [x] Put all the moves (i.e. the pyshical and spell moves) to a .json file
        - [ ] Add some classes (ej. classic ones like warrior, cleric, ranger)
        - [ ] Add at least one stat (ej. damage) and rework the others
        - [ ] Make the sanity slipping more dangerous
        - [ ] Rework the spells and physical attacks
        
    * Enemies
        - [x] Insert the data in a json file
        - [ ] Check their stats and attacks
        - [ ] Make the miniboss feel more like so
        
    * Looting
        - [ ] Make the enemies drop more varied loot and adjust chances
        
    * Inventory
        - [x] Do not show if it is empty
        - [ ] look_at()
        - [ ] pick_up() --> a "movable or not" is missing; also, if person or not; if there isn´t any, "There isn´t any %"; success message
        - drop() --> implement; nothing to drop, "You don´t have any %"; success message

    * Items
        - [x] Insert the data in a json file
        - [ ] Add new items
        - [ ] Rework existing items (their values, descriptions, etc.)
    
    * Combat
        - [x] Merge all the player moves functions in a single one
        - [ ] Check the combat balance between player and enemies
        - [ ] Make the final battle more long and dangerous (aka more epic)
     
*And perhaps much more!*
