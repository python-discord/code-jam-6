from typing import IO, Optional, Dict
import configparser
import pathlib as pl


# TODO: Use an environment variable for the cfg paths
def _find_config_file(cfg_paths=('./vm.ini',)) -> IO:
    """find a config file for this instance of the VM"""
    for cfg_path in cfg_paths:
        cfg_file = pl.Path(cfg_path)
        if cfg_file.exists():
            return cfg_file.open('r')
    newline = '\n'
    raise NoConfigException(f"ERROR: could not find vm.ini, searched:\n{newline.join(cfg_paths)}")


class NoConfigException(Exception):
    pass


class OSApiException(Exception):
    pass


class Env:
    # TODO: add config validation/defaults
    def __init__(self, cfg_file: Optional[IO] = None):
        """create an environment, given a config file.
        If no config file is given, try to find one"""
        cfg = configparser.ConfigParser()
        if cfg_file:
            cfg.read(cfg_file)
        else:
            file = _find_config_file()
            cfg.read_file(file)
            file.close()
        oo = cfg['DEFAULT']

        self.fs_root: pl.Path = pl.Path(oo['fs_root'])
        self._terminals: Dict[str, Terminal] = {}

    def add_terminal(self, uid: str, term: "Terminal") -> None:
        self._terminals[uid] = term

    def get_terminal(self, uid: str) -> "Terminal":
        return self._terminals[uid]

    def get_users(self):
        yield from self._terminals.keys()


class Terminal:
    """override methods to create custom terminals"""
    # TODO: have terminals interface with the OS and observe their inputs
    @staticmethod
    def impl_ex(name, action):
        return OSApiException(f"Terminal '{name}' does not support operation '{action}'")

    def stdin(self) -> IO:
        """:return the standard input stream of this terminal"""
        raise Terminal.impl_ex(self.__name__, 'stdin')

    def stdout(self) -> IO:
        """:return the standard output stream of this terminal"""
        raise Terminal.impl_ex(self.__name__, 'stdout')
