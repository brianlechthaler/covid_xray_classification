from subprocess import run as __cmd__


class Runner:
    def __init__(self,
                 command=[]):
        self.command = command