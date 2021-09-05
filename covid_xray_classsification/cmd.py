from subprocess import run as __cmd__


class Runner:
    def __init__(self,
                 command=[]):
        self.command = command
    def run(self):
        result = __cmd__(self.command)
        if result.returncode != 0:
            raise Exception(f"Command execution returned non-zero exit status: {result.returncode}")
