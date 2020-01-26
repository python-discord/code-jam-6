# Enigma Communication
By: Amphibian Alchemists

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

The Enigma Machine from WWII is the most infamous encryption device of the era. Given a ciphered text from upper command, your job is to decipher the text and uncover some truths.

Table of Contents:
- Setup
- Short Tutorial: Gist of the game
- Full-Length Tutorial
- Settings
- Guides

---
### Setup
1. Clone or download this repository.
2. Create a virtual environment in your terminal (e.g. `virtualenv venv`).
3. Activate it (`source venv/bin/activate` or, on Windows, do `venv\Scripts\activate`. 
4. Go to the top directory where `requirements.txt` lives and `pip install -r requirements.txt`.
5. In terminal, run main.py by doing `python main.py` or `python3 main.py`

The current configuration is intended to be incorporated with the Discord Postal Service server. If you'd like to setup o=your own DPS in your city-based Discord server, there is another README that you can check out for instructions in the discord-postal-service directory.

---
### Short Tutorial: Gist of the game
Start a new game. You are given paper with instructions. Configure the rotors parallel with that of the paper. Configure the plug PAIRS (each pair of plugs is connected by one wire).

Once you have those configured, type whatever the ciphered text is. Autoinput is enabled.

Note: If you have autoinput off and mistype once, move the rotor that just rotated backwards and continue typing from where you messed up. Remember, Germans didn't have a backspace on a piece of paper like us with computers.

---
### Full-Length Tutorial
![](https://ietp-web-cdn-eandt-cache.azureedge.net/0/2/c/4/5/9/02c4592c9a481871f93b30cdb914d341e22f547b.jpg)

At the top are rotors which are configured by rotation, the middle is the lampboard which shows outputted characters, the middle is the input keyboard, and the bottom is the plugboard.

You will be configuring the rotors and plugboard where you can plug and unplug characters.

Every 24 hours, the Germans switched the rotors and plugboard settings according to a key distributed at the beginning of each month.

You are given these settings in order to decrypt the message. Your job is to configure the Enigma machine and produce logical, Anglicized/English text. Once you have configured the machine, using your keyboard, you can (randomly) type out the ciphered characters and will be magically typing out the outputted, logical characters if the machine is configured correctly.

When you create a new game, you are shown the Enigma machine.

- By pressing on a rotor, you will first be led to a new screen where you can rotate the rotor to its proper initial settings
- By pressing on the plugboard, you will be led to a new screen where you can drag-and-drop plugs to its proper initial place.

Once you have finished configuring both the plugboard and rotors, go to the main enigma machine and start randomly pressing keys. You can see which keys are being typed by the animations or you can press on the piece of paper at the top right to see the ciphered text.

The output characters when you type will be shown and automatically configured in another piece of paper. You can restart the game if you misconfigured the machine. __Remember, only start typing when you have finished configurations!__

---
### Settings
- Autoinput the next, correct ciphertext letter: On
- Musics: On
- Sound effects: On 

---
### Guides

You can learn more about the enigma machine here:
- https://en.wikipedia.org/wiki/Enigma_machine
- [In-depth YouTube guide and technical details](https://www.youtube.com/watch?v=GcI-YlFSGYo)

A diagram of the machine's internal functionality:
![](https://i.pinimg.com/originals/67/cc/c3/67ccc3a33d6fbbf4b2738e167b5cfa37.png)

---
### LICENSE
Apache 2.0 License

Authors: [Pancho](https://github.com/Franccisco), [YoomamaFTW](https://github.com/YoomamaFTW), [sloopoo](https://github.com/flextian)