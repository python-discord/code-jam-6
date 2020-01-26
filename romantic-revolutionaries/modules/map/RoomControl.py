class Room:
    def __init__(self):
        pass

    def intro_text(self):
        raise NotImplementedError()

    def adjacent_moves(self):
        pass

    def available_actions(self):
        pass


class StartingRoom(Room):
    def __init__(self, ):
        super().__init__()

    def intro_text(self):
        return """You find yourself in a cave with a flickering torch on the wall.
        You can make out four paths, each equally foreboding.
        """


class EmptyCavePath(Room):
    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """
