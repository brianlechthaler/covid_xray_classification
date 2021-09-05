from subprocess import run as __cmd__


class Runner:
    """Simple command runner, designed to run a command with basic error handling.

    Args:
          command(list): List of strings that form a command and its arguments. (default [])
    """
    def __init__(self,
                 command=[]):
        # Store keyword parameters in self variables, then remove them from memory.
        self.command = command
        del command
        self.result = None
        del command

    def run(self):
        """Run command specified at class instantiation. Takes no parameters, and does not return anything."""
        # Run command, store results in self.result.
        self.result = __cmd__(self.command)
        # Check if the command executed successfully.
        if self.result.returncode != 0:
            # In case the command did not execute successfully, throw an error with the error code received.
            raise Exception(f"Command execution returned non-zero exit status: {self.result.returncode}")
