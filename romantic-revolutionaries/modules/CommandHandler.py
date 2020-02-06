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
    def __init__(self, nav_control):
        super().__init__(method=nav_control.go, hotkeys=['go', 'move', 'head', 'walk', 'run',
                                                         'north', 'east', 'south', 'west',
                                                         'n', 'e', 's', 'w'])
        self.nav_control = nav_control
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

class Look(Command):
    def __init__(self, view_control):
        super().__init__(method=view_control.look, hotkeys=['look',
                                                         'north', 'east', 'south', 'west',
                                                         'n', 'e', 's', 'w'])
        self.view_control = view_control
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
        match = re.match(rf'({"|".join(self.hotkeys)})?( )?([a-zA-Z]+)?( )?(\d+)?', ' '.join(words))
        direction = None

        if match:
            if match.group(1) in list(self.directions.keys()):
                direction = self.directions[match.group(1)]
            elif match.group(3) in list(self.directions.keys()):
                direction = self.directions[match.group(3)]

        if direction:
            self.method(direction)
            return True


class CommandHandler:
    def __init__(self, app, **kwargs):
        self.callbacks = set()
        self.app = app
        self.nav_control = kwargs['nav_control']
        self.view_control = kwargs['view_control']

        self.commands = [Help(),
                         Move(self.nav_control),
                         Look(self.view_control)]

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
