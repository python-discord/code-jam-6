# Kaleidoscopic Kings

## Installation

To get the project up and running is simple. Clone the repository and run `pipenv install`

If you are on Windows you will need to install additional Windows Kivy dependencies as per the [documentation](https://kivy.org/doc/stable/installation/installation-windows.html)

```
python -m pip install docutils pygments pypiwin32 kivy_deps.sdl2==0.1.* kivy_deps.glew==0.1.*
```

## What is it

Our project is broken down into two core parts - story engine and frontend.

Frontend display nicely the output of the backend and links frontend user interaction with backend varaibles.

Backend is completely modular and supports fully dynamic stories each having their own modular cards, states,
and assets.

There is also a very basic GUI editor which we were not able to fully complete due to deadline, we can say it's 
alpha.

## Game engine

Game stories are separated in folder and in those folders there is a strict directory layout.

It contains all game assets and game story data in json format. One can copy this folder,
change things inside of it manually and he'll get a complete new story experience complete with different assets
 and everything. This can be done easier with our editor but sadly it is in alpha and it was not completed fully.
 You can use it only if you are familiar with it since there was not enough time to add all options to it.

### Jurassic Greg

Current story pack we have created imagines you as Greg, a prehistoric man.
You were minding your own business rubbing two sticks together, and poof! you discovered fire. Whilst you 
didn't ask for this kind of evolution, you've got to live with it now, and with all the choices that come alongside being a robust modern man. 
For example, T-Rexes, should you kick them?


Throughout the game you'll be presented with a range of cards, you don't have to micromanage every little decision of 
life - just some of the little decisions. Whether to take a bath in the river, make a pterodactyl omelette, or whether 
maybe you *should* have kicked that T-Rex, you'll be responsible for ensuring the continuation of the great line of Greg.

Each choice you make will have two options, you need to decide whats best for Greg.

## Using it

### Playing the game
Playing the game is just about as simple as it  gets. You run the app, and you're presented with a choice. You make a choice,
rinse and repeat. 
![example screen](https://i.imgur.com/35j6Fmj.png "Playing the game")


### Making your own game

### Defining your own story
If you want to define your own story, or even if you just want to extend Greg's story, all you need to do is create json 
files to represent your events and choices using the alpha editor or editing them manually (as editor isn't fully complete).

### Customising your game
In order to customise the look and feel of your game, you'll need to create a folder for your game at the top level, which contains all the assets required. 
These necessary assets and the structure can be seen in Jurassic Greg's implementation in the game_data/caveman directory.

## The Team

* **[Charlie](https://github.com/CharlieADavies)** - *Team leader*
  * Charlie focused on getting the Kivy layout working. Finding assets, shifting things around by 5 pixels at a time. 
    Coming up with the overall look and feel for Jurassic Greg, as well as the customisable design.
* **[Braindead](https://github.com/albertopoljak)**
  * BrainDead was the MVP of the project, implementing practically the entire backend of the system, both the editor and the engine. 
    Taking general ideas from the whole team, providing plenty of his own, and turning them all into reality.
* **[Heagan](https://github.com/Heagan)**
  * Heagan was a key player in the idea and design phase, providing insight and research into the design and implementation git co
    of the eventual game, as well as implementing Animations for the front end of the app.
* **[GlowingRunes](https://github.com/glowingrunes)**
  * In addition to wireframing the layout, defining the style, and designing the first UI, GlowingRunes provided some 
    fantastic audio assets for the project, carrying the unique look and feel throughout the game.
* **soufianeh#4390** - MIA
