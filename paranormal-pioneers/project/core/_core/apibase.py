from .vm import Env


class ApiBase:
    def __init__(self, env: Env):
        self.env = env
