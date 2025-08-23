# Texticular (Interactive Fiction Engine)

**Synopsis**: Texticular started out as a project to implement a text adventure as a programming exercise but then evolved into something a little more complex. A reusable interactive fiction game engine driven off of Json config files. I wanted to make my game extensible and create a framework that could be built upon, but first and foremost I wanted to actually be able to finish the P.O.C. (The game the engine is named after "Texticular") and make it playable from beginning to end. Unfortunately I got a little overwhelmed and confused a few times along the way and never was able to finish my game. I need your help to take the game that's here as a basis for the finished product. But I'm open to refactoring and making necessary architecture changes to make something that is well designed and can be understood and extended in the future.

In the end what I want is a interactive fiction engine that is well documented and reasonably simple to understand how to use. I want a moderatly sophisticated command parser that works about as well as the classic infocom parsers or possibly has a few new tricks up it's sleeve. I want to add in some unique features like the ability to have autonomous npc's that can trigger some special context sensitive interactions when you talk with them or interact with them in certain ways to solve puzzles that progress the game. I want to have some dynamic conversations using graphs that lead to certain dialogue options that cause events to trigger in the game. I also want the game to start off as a command line or terminal based output with the ability to draw some ascii art or a simple ui made from text. However, I want the core logic and display logic to be separate enough that I could easily embed this application in a website or call it from an api and extend it to have things like sound and images later if I decide to go that route.

I'm going to layout the core functionality of Version 1.0 of the Engine Feature by Feature but not necessarily in the order they should be implemented in the section that follows 

## Features
-----------------

### The Player
-----------------------
 should be able to move from room to room in the environment and get descriptions of all the things that can be interacted with as well as examine individual objects. They should be able to pick up and drop items. Put items on top of things that are considered surfaces and pick them up. View and Manage their inventory, Open and close things like drawers or containers or other special objects.Unlock doors or other chests and special objects if they have the proper key. Initiate special context senstive interactions with special objects in the environement such as the vending machine or tv or telpehone that may trigger the game to enter a different state with a custom set of commands or ui ( Trigger game events/interrupts or "cut scenes" and update game state as needed). They should be able to Sit, Stand, and do a variety of other actions defined in the possible verbs of the game. The player should also be able to interact with other npc's in the game and have conversations with them, steal from them, potentially try to attack them or have other context sensitive interactions

### The Parser
-----------------------
The parser is really the heart of the game and the main method of taking in the player input on each turn tokenizing it and then those tokens are used to call the appropriate methods and perform actions to move the game state forward. Please read the document [ParserAlgorithm.md](ParserAlgorithm.md) and also drill down and read the links for "Benjamin Fan" and the code in my ./src/texticular/command_parser.py to get an idea for what I was going for.

Here is an excerpt from my README.md that has some info I had written in the past about the parser based on my reasearch

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

### NPCs and Conversations
-------------------------

I want to be able to kick off some interesting conversations with NPC's and trigger certain actions and game events such as the player receiving an item from an npc, a door unlocking or some kind of context sensitive action or event ocurring or things happening in other rooms etc. The game can also be lost in a conversation if things go wrong. Please use the dialogue system I was trying to implement as inspiration or a basis if possible. Look in src/texticular/dialogue (look at dialogue_graph.py and dialogue_test.py) and take a look at the [github](https://github.com/JonathanMurray/dialog-tree-py) repo that I got the original code from. 


### Shops and Vendors
------------------------------
 Implement shop (talking vending machine)
    use special context sensitive items * use phone/keypad/vending machine/magic medicine etc</li>
    implement magic eight ball (somewhat sentient object)


Purchase Items from "shops" or vendors which also puts the game into a different menu based interface similar to a dialogue



### The Game Loop
-----------------------

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

 Implement Win and Game Over Conditions and allow player to restart

### Json Config Files and Reusability/Customization
----------------------------------------------------
Currently I have several .json files stored in the data folder in the root of the application. If you need to rearrange those and put them somewhere else that's fine. But the idea was to be able to have another "user" of the application be able to follow a pattern like this to be able to create there own game map and story etc. If you have recommendations to make this system better or simplify it I'm open to suggestions.

### Save and Load System
---------------------------------------------------
Save a game in progress, Load and Resume a Game. Possibly just serializng game state to json or xml to begin with.

### Other misc features...
------------------------------
1. Create a scoring and stat system, A Scoring System that with bonuses for special actions the player takes in the game that are clever or humorous and a display for the number of turns taken as well as the score and the poop meter. I want the Stat for the ascii poop meter to look like

```
HP (HAVE TO POOP!!!) [#############.....]
```

This would fill up after a certain amount of time (turns) pass and the player doesn't solve the puzzle or if certain key things trigger it to go up.

2. View a log of previous commands - A convenience and common expectation at the command line

3. Implement Hint System similar to what you would find in zork or hitchhikers guide to the galaxy or other infocom games

4. Add Sound Effects and Splash Screens/visuals

5. For Something even cooler Hook in AI generated voices to read the dialogue from the npcs

6. Implement Choices that are remembered in a PlayerChoices collection

7. equip special items these don't count in inventory and are mostly for fun or special interactions



## Project Guidelines
----------------
I know there is a lot here. We can break it down step by step and take the time needed to get it right. If you ever need clarificaiton on something or I have conflicting instructions or ideas that aren't quite making sense, just let me know and we will work it out.

Study my existing code and architecture including the "references/Documents/Texticular Hotel Map.pdf" to get an idea of How I was thinking to have chapter 1 laid out as well as "Documents/ToDo.md" and "Documents/story.md" and "README.md" at the root to get an idea of where I wanted the project to go and my thought process. Take this into consideration when planning the project. Try to use what you can without compromising quality or sound design. Don't be afraid to iterate on it or reorganize the project or refactor or restructure how things work in order to save my ego or not hurt my feelings. I would like to reuse the core of how I designed the application and the good parts if possible, but this is more of an excercise in seeing how we can work together to finish this project and realize it the way I originally pictured it even if it means a major rewrite. You have my blessing to reorganize the project as needed to produce the results we are after and even clean up unecessary or redundant files. Just put them in a "Cleanup" directory for me to preview.

Do Use the document [Learning Zil](./Documents/Learning_ZIL_Steven_Eric_Meretzky_1995.pdf) as inspiration for the project. I did. But do not be bound by the limitations of the time or try to mimic it exactly. Build something in the same spirit and hopefully in a similar direction to where I was headed if it makes sense, but not an exact clone.

Take some time and brainstorm and make a plan before we start coding. Iterate and try to think about what some good implementations and solutions would look like and write your ideas to a file called ClaudeProjectIdeas.md in the documents folder and lets discuss them before we start coding.

I want to impelement some nice touches like pops of color in the terminal or ascii art used for titles and decorations or even to create a ui of sorts. I'd like the game to look retro but polished with some nostalgia but not fully constrained by the actual limitation of the time

Please take the Story I have written so far in [Story.md](story.md) and try to flesh out and expand some of the missing descriptions and events using the style that it's written in to the best of your ability. Sarcasm, humor, swearing, poop jokes, all ok.

Please be dilligent about documenting the code both using google style doc strings and inline comments where appropriate as well as creating supplemental markdown and api docs as needed. I want the final product to be a pleasure to read through both the code and documenation and the api and game functionality to be well documented so it can be used as a learning tool for myself and others.

Keep in mind the modularity that I wanted with the design of the UI of the game itself. My next steps and intentions with this game are to create a fast api application or some sort of website driven by an api and possibly azure functions that can run this game.

If you can as we develop different features of this game, write a blog post  for each one that chronicles your development with code snippets and explanations of your thought process and store it in a subdirectory of the documents folder in the project.

write yourself unit test as you develop so that you can verify the functionality is working as expected and iterate on it if it isn't and so that I can run the test myself and confirm everything is working. For some of the more complex components it would be great to have a sandbox where I could play with the parser by itself or kick off a test conversation with an npc for example.

Thank you for your help and I look forward to working with you!



