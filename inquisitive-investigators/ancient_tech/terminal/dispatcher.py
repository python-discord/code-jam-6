import subprocess
from os import chdir, getcwd
from pathlib import Path
from typing import Any, List

from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty

from ..utils.utils import threaded


class Shell(EventDispatcher):
    __events__ = ('on_output', 'on_cwd_change', 'on_complete')
    process = ObjectProperty()

    @threaded
    def run_cmd(
        self, cmd: List[str], 
        show_output: bool = True, 
        *args: Any, **kwargs: Any
        ) -> None:
        """
        Runs a command inputted into the terminal
        on a separate thread.

        Dispatches the output during execution.
        """
        if cmd[0] == 'cd' and len(cmd) >= 2:
            try:
                chdir(cmd[1])
            except FileNotFoundError:
                self.dispatch('on_output', b'\nThe system cannot find the path specified.')
            else:
                self.dispatch('on_cwd_change', getcwd())
        
        else:
            self.process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                shell=True,
            )

            self.dispatch('on_output', b'\n')
            line_iter = iter(self.process.stdout.readline, b'')
            
            if show_output:
                for line in line_iter:  
                    self.dispatch('on_output', line)

        self.dispatch('on_output', b'\n')
        self.dispatch('on_complete')

    @threaded
    def stop(self, *args: Any, **kwargs: Any) -> None:
        if self.process:
            self.process.kill()
