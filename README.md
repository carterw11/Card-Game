# Card-Game
A card game made in python in 2021

## About the game
This is a turn based card game where the player uses a deck of spell cards to defeat enemies.

The player is first prompted to login or create an account, which is used to store different games and save their progress. Account usernames and passwords must be 6-10 characters, and passwords must contain at least 1 capital letter and special character.

### Example of login screen
![image](https://user-images.githubusercontent.com/59629473/204068365-172c368a-9d03-4b5f-8c5e-e55f90757634.png)

After logging into an account, the player can continue their game from the last time a battle ended. If the user is using a new account, they are prompted to choose a character. There are 3 choices, each with a different starting deck and character ability.

### Example of character select screen
![image](https://user-images.githubusercontent.com/59629473/204068345-1fd8bc97-7406-4cf1-bb16-45d10125bfdd.png)

The player has 2 resources, health and mana. Health is lost from enemy attacks, and can be gained back using cards that heal the player. If your health reaches zero, you lose the current battle. Mana is used to cast spell cards and use your character ability, and is regained every time your turn begins again.

Each turn, you are able to use cards, use your ability, view how to play, look at the card library, and end your turn. 

The how to play section gives an in depth explanation of how the game works, including how to understand and use cards, amd what enemies do.

The card library shows all types of cards in the game that can be acquired by the player.

Ending your turn allows the enemies to act, potentially dealing damage, or having other effects. After enemies have acted, the player's turn begins again.

### Example of game window
![image](https://user-images.githubusercontent.com/59629473/204068575-7df97341-827e-4172-af65-3097b6d94b44.png)

The bottom of the screen shows your cards, including their element, cost, damage, healing, as well as the end turn and ability buttons.

The middle of the screen shows your enemy/enemies, including their type, health, attack, defense, and weakness

After battles are completed, you gain experience, and are prompted to save your progress, exit, or continue to the next battle.

After gaining enough experience, you level up, giving you extra health, a choice of a new card to add to your deck, and additional mana every few levels. Leveling up also increases the difficulty, and occasionally quantity of enemies.

### Example of post game window
![image](https://user-images.githubusercontent.com/59629473/204068888-0dc0f477-db52-4965-a48d-2dffa24fbf41.png)

## How to run the game
To run the game, download all the files into the same directory, and have all the images under a foler called "images" in the same directory as the python file.

Make sure to install TKinter and Pillow.

Run the python file, create an account, and begin playing the game.

## Other notes
As a warning, the project uses a Pillow function called ANTIALIAS, which will be removed in Pillow version 10, and therefore likely will not work on that version.

There also seems to be an issue where card text dissappears when they are hovered over, which may be the cause of more recent TKinter or Pillow versions, as this was not an issue when this project was created.
