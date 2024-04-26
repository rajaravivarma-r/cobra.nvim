import process

class Fzf:
    def __init__(self, executable="fzf"):
        self.executable = executable

    def filter(self, string):
        output = process.execute_and_get_output([self.executable, '--filter', string])
        return output.splitlines()
