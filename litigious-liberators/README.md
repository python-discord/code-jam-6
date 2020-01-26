# Resurgence 
### by Litigious Liberators


## Contents

- [Setting up your repo](#setting-up-your-repo)
- [Running the App](#running-the-app)
- [Using the App](#using-the-app)
- [Useful links](#useful-links)
- [License](#license)


### Setting up your repo

Clone this repo:

```bash
$ git clone git@github.com:duarteocarmo/code-jam-6.git
```

Create a virtualenv:

```bash
$ python -m venv <name_of_virtualenv>
```

Activate it:

```bash
$ . <name_of_virtualenv>/env/activate
```

Install dependencies

```bash
(env) $ cd litigious-liberators # navigate to our folder
(env) $ pip install -r requirements.txt # install normal requirements
(env) $ pip install -r requirements-dev.txt # install dev as well
```
## Running the App:
```bash
python main.py 
```
## Using the App
* Once you open the app, the game's backstory will be presented. You can __single-click__ to move to the next part of the story or __double-click__ to skip the entire story. 
* After that, you need to create your profile. Enter your name and answer few simple questions to determine your initial stats to move on to the next screen.
* Here you will be playing the actual game. You will be presented a scenario/individual where you have to press __right/left (keyboard)__ based on the choices displayed on the screen. To know more about the card, you can __click on the picture__.
* Your goal is to maximise all the three stats without any of them going empty. These stats might increase or decrease based on your choices

## Useful links


- **Code Jam Rules:** [https://pythondiscord.com/pages/code-jams/code-jam-6/rules/](https://pythondiscord.com/pages/code-jams/code-jam-6/rules/)

- **General Code Jam info:** [https://pythondiscord.com/pages/code-jams/code-jam-6/](https://pythondiscord.com/pages/code-jams/code-jam-6/)

- **Kivy:** [https://kivy.org/#home](https://kivy.org/#home)

## License

All projects will merged into our Code Jam repository, which uses the [MIT license](../LICENSE). Please make sure that if you add assets, the licenses of those assets are compatible with the MIT license.


There we go :) 
