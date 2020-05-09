# Dungeon Of The Silver Key
## A basic Lovecraft inspired text-based dungeon crawler written in Python

> *“There are twists of time and space, of vision and reality, which only a dreamer can divine; 
> and from what I know of Carter I think he has merely found a way to traverse these mazes.”*
> **"The Silver Key" of H.P. Lovecraft**

This is a project based and inspired in the original code of @Mili-NT and my reworking of that code. I intend to make a
version 2 of that game, but as there are intended a lot of changes, possibly the result is an entire new game.
This is an exercise in Object Oriented Programming. Also, in "Research on Interactive Fiction.txt" you can see some notes
and links of my research on IF for this project (for now, there is not a lot of that implemented, hopefully in the future
I´ll do it!)

### How to run the game:

Depending on what stage of development is, perhaps you can´t play the game with the latest addition as there is work to
 be done and some modifications are continuously made. You can download the latest available exe or the files 
 (the newest from the 'master-v2' branch or the base game from "modified-old-code" branch, or even the old version in 
 'old-game-code') to run in your local Python environment. If you are going to do the latter, don´t forget to install 
 the requirements.txt! You need the [colorama](https://pypi.org/project/colorama/), [tabulate](https://pypi.org/project/tabulate/), and 
[pyfliget](https://github.com/pwaller/pyfiglet) modules in your virtual environment to run the game.  


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
        - [ ] Make the parser a bit more sofisticaded (implement prepositions)
        - [ ] ???
    
    * Game Flow
        - [x] Add a sleep() between some functions so one is not flooded with text
        - [x] A "grab the left behind item in the room" function is missing
        - [ ] A "drop item" is missing
        - [x] The "view map" should show only the visited rooms
        
    * Map
        - [ ] Review layout of the rooms
        - [ ] Review placement of enemies
        - [ ] Review placement of items
        - [ ] Adding puzzles and little notes
        - [ ] Maybe adding another "floor" in the dungeon (or an "exterior" previous to enter the dungeon)
        
    * Rooms
        - [x] Insert the data in a json file
        - [ ] Add more data in the dictionaries (what data? near_room_description, i.e??)
        - [x] Reduce all the room scripts to only one
        
    * Player
        - [ ] Add some classes (ej. classic ones like warrior, cleric, ranger)
        - [ ] Add at least one stat (ej. damage) and rework the others
        - [ ] Make the sanity slipping more dangerous
        - [ ] Rework the spells and physical attacks
        
    * Enemies
        - [ ] Check their stats and attacks
        - [ ] Make the miniboss feel more like so
        - [x] Insert the data in a json file
        
    * Looting
        - [ ] Make the enemies drop more varied loot and adjust chances
        
    * Inventory
        - [ ] Check what could possibly be changed
        
    * Items
        - [ ] Add new items
        - [ ] Rework existing items (their values, descriptions, etc.)
        - [x] Insert the data in a json file
        
    * Balance
        - [ ] Check the combat balance between player and enemies
        - [ ] Make the final battle more long and dangerous (aka more epic)
     
*And perhaps much more!*
