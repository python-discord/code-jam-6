from .apibase import ApiBase
from project.core._core.vm import OSApiException, Terminal


class UserApi(ApiBase):
    def terminal(self, uid: str) -> Terminal:
        return self.env.get_terminal(uid)

    def add_terminal(self, uid: str, term: Terminal):
        self.env.add_terminal(uid, term)
