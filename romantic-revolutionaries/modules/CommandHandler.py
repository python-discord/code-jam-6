""" Command Control Module """

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


class Move(Command):
    def __init__(self, nav_control):
        super().__init__(method=nav_control.go, hotkeys=['go', 'move', 'head',
                                                            'walk', 'run', 'sprint'])
        self.nav_control = nav_control
        self.nav_control.subscribe(self.callback)
        self.directions = {
            'north': Directions.NORTH,
            'east': Directions.EAST,
            'south': Directions.SOUTH,
            'west': Directions.WEST
        }

    def parse(self, words):
        direction, distance = None, None
        try:
            direction = self.directions[words[1]]
        except KeyError:
            print('Invalid direction')
            return False

        try:
            distance = int(words[2])
        except IndexError:
            pass
        except ValueError:
            print('Invalid distance')
            return False

        self.method(direction, distance)
        return True

    def callback(self, direction, distance):
        for k, v in self.directions.items():
            if direction == v:
                direction = k
                break

        if distance > 1:
            self.app.add_text(f'You walk {direction} for {distance} spaces.')
        else:
            self.app.add_text(f'You walk {direction}.')


class Pickup(Command):
    def __init__(self, inventory_control):
        super().__init__(method=inventory_control.pickup, hotkeys=['pickup', 'grab', 'take'])
        self.inventory_control = inventory_control

    def parse(self, words):
        pass


class CommandHandler:
    def __init__(self, app, nav_control):
        self.callbacks = set()
        self.app = app
        self.nav_control = nav_control

        self.commands = [Help(), Move(self.nav_control)]

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

            if not valid_command:
                self.app.add_text(f"I don't know what you mean by [color=FF0000]{text}[/color].")
        except IndexError:
            pass
