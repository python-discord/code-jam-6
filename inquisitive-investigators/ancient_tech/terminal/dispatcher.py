import subprocess

from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty

from ..utils.utils import threaded


class Shell(EventDispatcher):
    __events__ = ('on_output', 'on_complete')
    process = ObjectProperty()

    @threaded
    def run_cmd(self, cmd, show_output=True, *args, **kwargs):
        """
        Runs a command inputted into the terminal
        on a separate thread.

        Dispatches the output during execution.
        """
        output = ''
        self.process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            shell=True
        )
        line_iter = iter(self.process.stdout.readline, b'')
        self.dispatch('on_output', '\n'.encode())
        
        for line in line_iter:
            output += line.decode()

            if show_output:
                self.dispatch('on_output', line)

        self.dispatch('on_output', '\n'.encode())
        self.dispatch('on_complete', output)

    @threaded
    def stop(self, *args, **kwargs):
        if self.process:
            self.process.kill()
