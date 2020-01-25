""" Command Control Module """

import re

from modules.navigation.navcont import Directions

from kivy.app import App


class Command:
    def __init__(self, method, hotkeys):
        self.method = method
        self.hotkeys = hotkeys
        self.app = App.get_running_app()

    def __str__(self):
        return f"{self.hotkey}: {self.name}"


class Help(Command):
    def __init__(self):
        super().__init__(method=None, hotkeys=['help', '?', 'h'])

    def parse(self, text):
        self.app.add_text("""[color=00FFFF]Movement:[/color]
        [go/move/walk] [north/south/east/west] [distance]
        """)

        return True


class Move(Command):
    def __init__(self, nav_control, map_control):
        super().__init__(method=nav_control.go, hotkeys=['go', 'move', 'head', 'walk', 'run',
                                                         'north', 'east', 'south', 'west',
                                                         'n', 'e', 's', 'w'])
        self.nav_control = nav_control
        self.map_control = map_control
        self.map_control.subscribe(self.map_callback)
        self.directions = {
            'north': Directions.NORTH,
            'east': Directions.EAST,
            'south': Directions.SOUTH,
            'west': Directions.WEST,
            'n': Directions.NORTH,
            'e': Directions.EAST,
            's': Directions.SOUTH,
            'w': Directions.WEST
        }

    def parse(self, words):
        direction, distance = None, None
        match = re.match(rf'({"|".join(self.hotkeys)})?( )?([a-zA-Z]+)?( )?(\d+)?', ' '.join(words))

        if match:
            if match.group(1) in list(self.directions.keys()):
                direction = self.directions[match.group(1)]
            elif match.group(3) in list(self.directions.keys()):
                direction = self.directions[match.group(3)]
            if match.group(5) is not None:
                distance = int(match.group(5))
            else:
                distance = 1

        self.method(direction, distance)
        return True

    def map_callback(self, current_location, room, visible_block, did_bonk):
        if did_bonk:
            self.app.add_text("You walk directly into a wall and bonk your head.")
            return

        if room is not None:
            self.app.add_text(room.intro_text())

        next_path_text = "There are paths leading"
        if visible_block[0][1] != 0:
            next_path_text += ' North'
        if visible_block[1][0] != 0:
            next_path_text += ' West'
        if visible_block[1][2] != 0:
            next_path_text += ' East'
        if visible_block[2][1] != 0:
            next_path_text += ' South'

        next_path_text += '.'
        self.app.add_text(next_path_text)

        for _ in visible_block:
            print(_)
        print()


class CommandHandler:
    def __init__(self, app, **kwargs):
        self.callbacks = set()
        self.app = app
        self.nav_control = kwargs['nav_control']
        self.map_control = kwargs['map_control']

        self.commands = [Help(),
                         Move(self.nav_control, self.map_control)]

    def parse_command(self, text):
        if type(text) is not str:
            raise ValueError(f'Command is not a string: {text}')

        text = text.lower()
        words = text.split()

        valid_command = False
        try:
            for command in self.commands:
                if words[0] in command.hotkeys:
                    valid_command = command.parse(words)
                    if valid_command:
                        break

            if not valid_command:
                self.app.add_text(f"I don't know what you mean by [color=FF0000]{text}[/color].")
        except IndexError:
            pass
