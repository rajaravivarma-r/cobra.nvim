import process


class Fzf:
    def __init__(self, executable="fzf"):
        self.executable = executable

    def filter(self, filter_string, input_string):
        output = process.popen_and_get_output(
            [self.executable, "--filter", filter_string], input_string
        )
        return output.splitlines()
