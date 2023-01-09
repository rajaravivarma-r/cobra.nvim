from pathlib import Path
import re

import pynvim


@pynvim.plugin
class CobraPlugin(object):
    def __init__(self, nvim):
        self.nvim = nvim

    # Requires `pyperclip` to be installed in the python instance used by neovim
    # Copies the current buffer's filepath.
    # It takes and argument to copy relative path of current buffer's filepath
    # with respect to the `pwd` of the vim instance.
    #
    # For example, given,
    # Absolute path of the file open in current buffer is
    # /Users/raja/.local/share/nvim/site/pack/packer/start/cobra.nvim/rplugin/python3/main.py
    # `:pwd` of vim instance is /Users/raja/.local/share/nvim/site/pack/packer/start/cobra.nvim/rplugin/python3
    #
    # Calling
    # :Pwf
    # copies '/Users/raja/.local/share/nvim/site/pack/packer/start/cobra.nvim/rplugin/python3/main.py' to the clipboard
    #
    # :Pwf rel
    # copies 'main.py' to the clipboard
    @pynvim.command("Pwf", nargs="*")
    def copy_current_filepath(self, args):
        import pyperclip

        copy_relative_path = False
        buffer_path = Path(self.nvim.current.buffer.name)
        if any("rel" in a for a in args):
            copy_relative_path = True

        if copy_relative_path:
            current_path = Path(self.nvim.command_output("pwd"))
            buffer_path = buffer_path.relative_to(current_path)
        pyperclip.copy(str(buffer_path))

    @pynvim.command("CaseToCamelCase", nargs="*")
    def convert_to_camel_case(self, args):
        current_word = self._current_word()
        words = current_word.split('_')
        first_word = words.pop(0)
        capitalized_words = [first_word] + [w.capitalize() for w in words]
        self._replace_current_word(''.join(capitalized_words))

    # TODO: Handle snake_case words
    # Right now it handles PascalCase words, quickly put together for an
    # usecase.
    @pynvim.command("CaseToConstant", nargs="*")
    def convert_to_constant(self, args):
        current_word = self._current_word()
        words = re.findall(r'[A-Z][a-z]+', current_word)
        constant_word = [w.upper() for w in words]
        self._replace_current_word('_'.join(constant_word))

    def _current_word(self):
        self.nvim.command('normal! "wyiw')
        return self.nvim.funcs.getreg('w')

    def _replace_current_word(self, new_word):
        self.nvim.funcs.setreg('w', new_word)
        return self.nvim.command('normal! viw"wp')
