from pathlib import Path
import re

import pynvim

import tmux
import utils


@pynvim.plugin
class CobraPlugin:
    def __init__(self, nvim):
        self.nvim = nvim
        self.nvim_helper = utils.NvimHelper(nvim)

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
    @pynvim.command("Pwf", nargs="*", complete="customlist,PwfArguments")
    def copy_current_filepath(self, args):
        import pyperclip

        copy_relative_path = False
        buffer_path = Path(self.nvim_helper.current_buffer())
        if any("rel" in a for a in args):
            copy_relative_path = True

        if copy_relative_path:
            current_path = Path(self.nvim.command_output("pwd"))
            buffer_path = buffer_path.relative_to(current_path)
        pyperclip.copy(str(buffer_path))

    @pynvim.command("CaseToCamelCase", nargs="*")
    def convert_to_camel_case(self, args):
        """
        Converts 'hello_world' to helloWorld
        Used to convert between JSON and Ruby naming conventions
        """
        current_word = self.nvim_helper.get_current_word()
        words = current_word.split("_")
        first_word = words.pop(0)
        capitalized_words = [first_word] + [w.capitalize() for w in words]
        self.nvim_helper.replace_current_word("".join(capitalized_words))

    # TODO: Handle snake_case words
    # Right now it handles PascalCase words, quickly put together for an
    # usecase.
    @pynvim.command("CaseToConstant", nargs="*")
    def convert_to_constant(self, args):
        """
        Converts 'HelloWorld' to HELLO_WORLD
        """
        current_word = self.nvim_helper.get_current_word()
        words = re.findall(r"[A-Z][a-z]+", current_word)
        constant_word = [w.upper() for w in words]
        self.nvim_helper.replace_current_word("_".join(constant_word))

    @pynvim.function("PwfArguments", sync=True)
    def pwf_arguments(self, *args):
        return ["relative", "absolute"]
