# Dungeon Of The Silver Key
## A basic Lovecraft inspired text-based dungeon crawler written in Python

This is a project based and inspired in the original code of @Mili-NT and my reworking of that code. I intend to make a
version 2 of that game, but as there are intended a lot of changes, possibly the result is an entire new game.
This is an exercise in Object Oriented Programming.

It is not yet fully playable (depending on what stage of development is) as there is work to be done and some modifications
are continuously made. Yet, is still possible to play the old version (in "modified-old-code" branch). You need the 
[colorama](https://pypi.org/project/colorama/), [tabulate](https://pypi.org/project/tabulate/), and 
[pyfliget](https://github.com/pwaller/pyfiglet) modules in your virtual environment to run the game.  

There is still work to be done:

    * Plot
        - [ ] Add a story
        - [ ] Work in the prose (descriptions of rooms, enemies, objects, etc)
        - [ ] Make some things ambiguous so the player can fill the blanks with his imagination
        
    * Game Flow
        - [ ] Make the game feel more like old Interactive Fiction games
        - [ ] Add a sleep() between text lines so one is not flooded with text
        - [x] A "grab the left behind item in the room" function is missing
        - [x] The "view map" should show only the visited rooms
        
    * Map
        - [ ] The layout of the rooms
        - [ ] The placement of enemies
        - [ ] The placement of items
        - [ ] Adding puzzles and little notes
        - [ ] Maybe adding another "floor" in the dungeon
        
    * Rooms
        - [x] Insert the data in a json file
        - [ ] Add more data in the dictionaries 
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
