from ._core import FsApi, UserApi, StdioApi
from ._core.vm import Env  # this will be redone in the future
from ._core import Terminal


class Api(FsApi, UserApi, StdioApi):
    pass


class SimpleBoot:
    def start(self) -> Api:
        return Api(Env())
