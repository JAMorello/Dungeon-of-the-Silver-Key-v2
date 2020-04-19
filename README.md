# Dungeon Of The Silver Key
## A basic Lovecraft inspired text-based dungeon crawler written in Python

This is a project based in the original code of @Mili-NT. The objective was to structure it: reduce the huge amount of 
repetitive lines (from 4k went to 2k); make the code clean and easy to read and modify; make separate files that 
contains distinct functions, data, and info; implement classes (items, enemies, and player); correct some little 
mistakes (or that I think are mistakes, like items left behind disappearing, incongruous links between rooms, etc.). 

This work took me like 25 hours more or less, in the span of a week or so. I have added, improved, and modified some 
functions and stuff, but I think that the result (the functional game) is here is pretty close to what the original 
author intended. I hope I made some justice to his work.

This is the base code for the upcoming version 2 of the game.
There is still work to be done:
    * Plot:
        * Add a story
        * Work in the prose (descriptions of rooms, enemies, objects, etc)
        * Make some things ambiguous so the player can fill the blanks with his imagination
    * Game Flow:
        * Make the game feel more like old Interactive Fiction games
        * Add a sleep() between text lines so one is not flooded with text
        * A "grab the left behind item in the room" function is missing
        * The "view map" should show only the visited rooms
    * Map:
        * The layout of the rooms
        * The placement of enemies
        * The placement of items
        * Adding puzzles and little notes
        * Maybe adding another "floor" in the dungeon
    * Rooms:
        * Insert the data in a json file
        * Add more data in the dictionaries 
        * Reduce all the room scripts to only one
    * Player:
        * Add some classes (ej. classic ones like warrior, cleric, ranger)
        * Add at least one stat (damage) and rework the others
        * Make the sanity slipping more dangerous
        * Rework the spells and physical attacks
    * Enemies:
        * Check their stats and attacks
        * Make the miniboss feel more like so
        * Insert the data in a json file
    * Looting
        * Make the enemies drop more varied loot and adjust chances
    * Inventory:
        * Check what could possibly be changed
    * Items:
        * Add new items
        * Rework existing items (their values, descriptions, etc.)
        * Insert the data in a json file
    * Balance:
        * Check the combat balance between player and enemies
        * Make the final battle more long and dangerous (aka more epic)
     
*And perhaps much more!*

PD: Perhaps the version 2 will be in spanish, not in english

### README.md made by original creator(@Mili-NT) in 2019: 
This was my first actual project written in Python. I wrote it in January of this year when I knew next to nothing about classes, OOP, or basically anything beyond the basics of the language.

This project *DOES* reflect that. I have made no modifications (except making the inventory system functional) since I first wrote it.
It is poorly structured, strangely written, and has some formatting oddities in places. Nevertheless, it's fun to play and it reminds me how far i've come.

It's also STUPID long. Don't ever write code like this.

Side note: If you want to see how it was intended to look, run the .py version in pycharm, or anything that supports Figlet and colorama. The executable is black and white.

For anyone learning Python and attempting to make a text-based game like a few sources recommend:
* Feel free to use any portion of this code to help you along, especially the combat portions
* Don't give up and keep learning!
