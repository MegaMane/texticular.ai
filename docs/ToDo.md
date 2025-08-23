Feature 1 Player can move freely from room to room and get descriptions of all relevant things in current environment
Todo

    x Finish initialGameMap.json (port over rooms.json)
    x Load the game map with just rooms & exits
    x Create the Player Class
    x Test moving the player from room to room manually
    X Test player can move beteween open doors but not locked
    Test Player can examine objects
    Initialize Serialize/Deserialize items from Json
    Initialize Serialize/Deserialize rooms from Json
    Initialize Serialize/Deserialize player from Json
    Wire action funcs from Json


Feature 2 Player can pick up items store them in inventory and drop items

Player can view inventory

Containers player can take and put items from open containers
TODO
    put item in container
    item description concats adjectives
    encode/decode (player w inventory)
    Add all the items in 201 minus tv/phone to json

Feature 2.5 Room Descriptions now only include items/game objects that are visible to the player

XFeature 3 Player can unlock doors and containers with the correct key

Feature 4 Player can place and retrieve items from surfaces

 Trigger game events/interrupts or "cut scenes" and update game state as needed</li>

Feature 5 Player can use items and interact with objects in context-sensitive ways (Actions)
(meaning you can eat the cake but not the couch...but feel free to try)
   Test Wiring up Action function so that description can change based on player action room enter exit func

Feature 6 Player can interact with special items that change the game state (normal input)
phone keypad vending machine TV etc

 Implement shop (talking vending machine)
    use special context sensitive items * use phone/keypad/vending machine/magic medicine etc</li>
    implement magic eight ball (somewhat sentient object)

Feature 7 Player can Have conversations with other characters which puts the game into a different dialogue state with
options to pick from instead of free form typing

Implement Dialogue With NPCs
   Dialogue with npc can yield items
   or trigger other events depending on player choice

Purchase Items from "shops" or vendors which also puts the game into a different menu based interface similar to a dialogue


Feature 8 Implement Parser and Main Game Loop

 Implement Win and Game Over Conditions and allow player to restart

Feature 9 Implement Scoring System

Feature 10 Implement Save/Load System
    Save a game in progress, Load and Resume a Game
    Test saving and loading the game with the player in different rooms and descriptions changed

Feature 11 View a log of previous commands
Feature 12 Implement Hint System
Feature 12 Implement Flask/Web UI
Feature 13 Add Sound Effects and Splash Screens/visuals


ideas and other word vomit
---------------------------

	 * Implement Choices that are remembered in a PlayerChoices collection
     * equip special items {these don't count in inventory}
     * create a scoring and stat system

idea
Newspaper with phone number or some other story clue/puzzle piece embedded in it surrounded by current headlines
loaded from google news api scrapes each time program runs

https://thecleverprogrammer.com/2021/05/10/scrape-trending-news-using-python/
https://pypi.org/project/GoogleNews/