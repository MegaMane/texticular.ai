# Texticular

A Game Written in Python Modeled After Classic Interactive Fiction or Text Adventures, with A relatively simple to use, reusable core engine 
that is config driven. Json files loaded to create rooms, items, characters, conversations etc.

Game Initialization
----------------------

The program starts by loading the game objects (rooms, items, containers, player etc.) into memory using the texticular.game_loader module

It does this by calling the function load_game_map() which takes in a parameter of a manifest.json file

This manifest.json file contains the pointers to the files that should be loaded into memory so objects are in the correct state

The default files are "newGameItems.json" and "newGameMap.json" The items and rooms are deserialized from json and game objects are constructed and put into a gamemap dictionary
at the moment this gamemap contains three major keys items, containers, and rooms

We also load the player from the game_loader by calling the "load_player" method (this needs work as it's currently just hard coded and needs to deserialize the player from json)


The last thing we do from the game_loader module As part of the game intialization is call a function to atach custom actions to items "wire_item_action_funcs" 

The way this works is:

Lastly before starting the main game loop we create an instance of the controller class





The Command Parser:
---------------------------


<p>A <b>Parser</b> is a software program that performs lexical analysis.  Lexical analysis is the process of separating a stream 
of characters into different words, which in computer science we call 'tokens' . When you read my answer you are 
performing the lexical operation of breaking the string of text at the space characters into multiple words.
</p>

<p>A <b>Parser</b> is part of a compiler that converts the statements in code into various categories of like key words,constants,
variable etc jus like identifying parts of speech in a sentence and produce token (each converted unit is called as a token )
</p>


<p>
A <b>Parser</b> goes one level further than the lexer and takes the tokens produced by the lexer and tries to determine if 
proper sentences have been formed.  Parsers work at the grammatical level, lexers work at the word level.
</p>

<p>A <b>Parser</b> defines rules of grammar for these tokens and determines whether these statements are semantically correct</p>

Parser example sentences:
------------------------
<p><i>Player should be able to type basic commands to interact with environment or move from room to room and 
navigate the map. Examples:</i></p>

Go North  
Go to the South  
Go To the Kitchen  
Hide under the Bed  
Pick up the green apple  
put the pocket change in the vending machine  
Use the vending machine  
Ask the Magic Eight ball a question  
open the drawer and put the pocket change inside  
put the pocket change in the drawer  
use the phone  
talk to Fred  
Attack the Cobra with the sword  
Put on the Scuba Suit  
Show the Chicken to Larry  
Pick up the Coins  
Buy the dog treats  
Take the Key  
Open the Drawer  

<p>The verbs or actions such as "Pick Up" or "Open" will be pre-defined by the engine.
The nouns or objects are defined at runtime in the games config files.
</p>


The Handler/Game Controller
---------------------------



The Main Game loop
-------------------

The basic game loop is this

Receive input as series of simple typed commands from the player
The Parser processes each of those commands and determines if they are valid (meaning they consist of at the very least a known verb, usually a direct object and optionally an indirect object)

If the command is valid it is passed off to the controller which:
	performs the actions
	triggers any events
	updates the clock

The results of the turn get sent back to the player as output

The main gameplay consists of navigating "rooms" which contain contextual actions that can be triggered as well as objects inside the rooms that also have their own set of contextual verb interactions.
There are also other characters that can be talked to which initializes a dialogue that may have side effects triggering other actions (such as making changes to a room, or yielding a new item that can be used)
The purpose of all this is to solve a puzzle. Navigating the rooms themselves to achieve some goal is the root of the gameplay. The simplest example of this being a lock and key puzzle. 
Their is also a simple currency and shop system that gets incorporated into the puzzle solving.


# Game Eelements

The UI
------

The initial UI is just console based and outputs text data. This may change in the future to use flask or Textual and/or  
include other elements/sub-divisions of the screen to show hp, inentory, current objectives etc.


The Player Character:
---------------------
Player should have an inventory that can be inspected
They Player has the following attributes
HP
HPoo
Sex
Age
Wearing

Rooms - The main building block of the game:
-------------------------------------------

Environment descriptions can change depending on where the player is in the game
How many times the room has been visited
Special events that may change the description of a room
Player state
Can Contain puzzles
Events (Discussed Below)
Rooms contain exits that may be locked (but can be unlocked with the proper key)

Items:
-------------------
Items can be simple or have slots that can contain other items (i.e. containers or other special cases)
Some items can be combined to form new items

containers can be locked and unlocked with the proper key

NPC's:
------------------
NPC's have their own inventory and can give items or items can potentially be stolen or looted under the right conditions

Dialogue:
--------------------

references : https://github.com/JonathanMurray/dialog-tree-py
Player should be able to talk to NPC's and trigger Dialogue scenes:
"Talk to hotel clerk" 
Triggers Dialogue Sequence:
Dialogue Sequences are special events that use directed graph where a player makes choices
similar to how you would in an rpg

Dialogue choices can trigger results (I.E. Get an item, Game over, Unlock a door, Get into a fight)


Events:
------------
Timed events or other external triggers can change the game environment 
NPC's, or Time running out/turns running out

Rooms can have events
Items can have events (I.E combining two items together, placing an item in a pedestal, taking an item etc. triggers an event)
Dialogue can Trigger an Event
Player Interactions with the environment can Trigger Events


Shops:
-------------
A Shop or bartering system where the currency can be defined in the config
I.E. pop caps instead of coins 
A shop interface where players buy and potentially sell items


Saving and Loading A Game:
--------------------------
Need to be able to save and load game and resume where you left off
Each class knows how to serialize and deserialize itself to json



Help:
--------------
To be defined....  But should look a little like/ be inspired by the "Play Some Interactive Fiction.pdf" in the
Reference/Documents folder.


# Important Classes


GameObject 
-----------

StoryItem
----------

Room  
--------

Player
--------

Parser
-------

Controller
----------


# About Actions