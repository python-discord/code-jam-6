"""Navigation Controller Module"""


class NavControl():
    """Control navigation requests.

        To subscribe pass your callback function to subscribe()
        Your callback function should accept a direction and a distance.

        If an invalid direction is passed in a ValueError will be raised.

        go() is the public function called to effect navigation.
        If go() is called without arguments, it will repeat the last
        direction and distance. If it is called without a distance it will
        repeat the last distance. And if it is called without a direction
        it will repeat the last direction. If you want to call with a distance
        but no direction, you must do so with named argument for your distance.
    """
    def __init__(self):
        self.callbacks=set()
        self.direction = 'N'
        self.distance = 1

    def subscribe(self, callback):
        self.callbacks.add(callback)

    def unsubscribe(self, callback):
        self.callbacks.remove(callback)

    def notify(self):
        for callback in self.callbacks:
            callback(self.direction, self.distance)

    def go(self, direction='*', distance=0):
        if direction != '*':
            direction = direction.upper()
            if direction not in "NSEW":
                raise(ValueError)

            self.direction = direction
        if distance != 0:
            self.distance = distance
        self.notify()
