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

        # Create a variable to store the result of executing the specified command
        self.result = None

    def run(self,
            report_returncode_on_exception=True):
        """Run command specified at class instantiation. Takes no parameters, and does not return anything.

        Args:
            report_returncode_on_exception(bool): If set to True, exceptions from failed command will include their respective exit codes. (default False)"""

        # Run command, store results in self.result.
        self.result = __cmd__(self.command)
        # Check if the command executed successfully.
        if self.result.returncode != 0:
            # Don't report return code in exception.
            exception_text = f"Command execution returned non-zero exit status."
            # Check if we need to report return code in exception.
            if report_returncode_on_exception is True:
                # Report return code in exception.
                exception_text = f"Command execution returned non-zero exit status: {self.result.returncode}"
            # In case the command did not execute successfully, throw an error with the error code received.
            raise Exception(exception_text)
