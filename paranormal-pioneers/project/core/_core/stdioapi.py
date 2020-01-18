from .apibase import ApiBase
from project.core._core.vm import OSApiException, Terminal


class StdioApi(ApiBase):
    def terminal(self, uid: str) -> Terminal:
        return self.env.get_terminal(uid)
