# Circumstantial Companions

![Chisel Preview](./preview.gif)

SMASH ROCK!  FASTER SWING = MORE ROCK SMASHED! This app is a pre-historically accurate
representation of Paleolithic technology.  Re-invent the wheel with this (rock)cutting-edge
simulation! A caveman workout routine guaranteed to give you chiseled slabs fast!

## Installation

1. Clone this repository.
2. `cd` into this directory.
3. `pip install -r requirements.txt kivy-garden`
4. `garden install navigationdrawer`

## Usage

1. `python -m main`

## Sources

```
assets
│
├───img
│   │   background.png
│   │   options_background.png
│   │   sign_border.png
│   │
│   ├───boulder
│   │       0.png
│   │       1.png
│   │       2.png
│   │       3.png
│   │       4.png
│   │
│   ├───burger
│   │       hover.png
│   │       normal.png
│   │       pressed.png
│   │
│   ├───button
│   │       hover.png
│   │       normal.png
│   │       pressed.png
│   │
│   ├───caveman
│   │       0.png
│   │       1.png
│   │       2.png
│   │       3.png
│   │
│   └───cursor
│           down.png
│           up.png
│
├───sounds
│       dig.wav
│
└───ttf
        han_wang_yan_kai.ttf
        keifont.ttf
        kirsty_rg.ttf
        zcool_kuaile_rg.ttf
```

### Images

- [`boulder/*.png`][boulder-dir] from [Pixabay][pixabay-url] are licensed under the [Pixabay License][pixabay-license-url].

- [`options_background.png`][img-dir], [`sign_border.png`][img-dir] and [`burger/*.png`][burger-dir] from [PureBDcraft ResourcePack][bdcraft-url] are licensed under their Terms of Use. The latter two are altered by [MusicOnline][musiconline-github].

- [`background.png`][img-dir], [`cursor/*.png`][cursor-dir] and [`caveman/*.png`][caveman-dir] are original works by [salt-die][salt-die-github].

- `button/*.png` are just a hundred pixels of the same color (of unknown [trademark][trademark-url]).

[boulder-dir]: ./assets/img/boulder
[sound-dir]: ./assests/sounds
[pixabay-url]: https://pixabay.com/
[pixabay-license-url]: https://pixabay.com/service/license/
[zapsplat-url]: https://www.zapsplat.com/
[zapsplat-license-url]: https://www.zapsplat.com/license-type/standard-license/

[img-dir]: ./assets/img
[burger-dir]: ./assets/img/burger
[bdcraft-url]: https://bdcraft.net/downloads/purebdcraft-minecraft/
[musiconline-github]: https://github.com/MusicOnline

[cursor-dir]: ./assets/img/cursor
[caveman-dir]: ./assets/img/caveman
[salt-die-github]: https://github.com/salt-die

[button-dir]: ./assets/img/button
[trademark-url]: https://en.wikipedia.org/wiki/Colour_trade_mark

### Sounds

- [`sounds/*.wav`][sound-dir] from [zapsplat][zapsplat-url] are under the [Zapsplat License][zapsplat-license-url].