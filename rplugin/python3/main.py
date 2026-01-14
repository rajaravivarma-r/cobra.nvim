from pathlib import Path

import pynvim

from text import Text
import tmux
import utils
import compare


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
        copy_line_number = False
        buffer_path = Path(self.nvim_helper.current_buffer_name())
        if any("rel" in a for a in args):
            copy_relative_path = True

        if any("line" in a for a in args):
            copy_line_number = True

        if copy_relative_path:
            current_path = Path(self.nvim.command_output("pwd"))
            buffer_path = buffer_path.relative_to(current_path)

        if copy_line_number:
            buffer_path = str(buffer_path) + f":{self.nvim_helper.current_cursor_row()}"
        pyperclip.copy(str(buffer_path))

    @pynvim.command("CaseToCamelCase", nargs="*")
    def convert_to_camel_case(self, args):
        """
        Converts 'hello_world' to helloWorld
        Used to convert between JSON and Ruby naming conventions
        """
        current_word = self.nvim_helper.get_current_word()
        text = Text(current_word)
        self.nvim_helper.replace_current_word(text.convert_to_camel_case())

    # TODO: Handle snake_case words
    # Right now it handles PascalCase words, quickly put together for an
    # usecase.
    @pynvim.command("CaseToConstant", nargs="*")
    def convert_to_constant(self, args):
        """
        Converts 'HelloWorld' to HELLO_WORLD
        """
        current_word = self.nvim_helper.get_current_word()
        text = Text(current_word)
        self.nvim_helper.replace_current_word(text.convert_to_constant_case())

    @pynvim.command("CaseToSnakeCase", nargs="*")
    def convert_to_snake_case(self, args):
        """
        Converts 'HelloWorld' or 'helloWorld' to hello_world
        """
        current_word = self.nvim_helper.get_current_word()
        text = Text(current_word)
        self.nvim_helper.replace_current_word(text.convert_to_snake_case())

    @pynvim.command("Compare", nargs="1", complete="customlist,CompareArguments", sync=True)
    def compare(self, args):
        """
        Compare lines across two splits in the current tabpage.

        Usage:
          :Compare show_common
          :Compare only_present_on_left
          :Compare only_present_on_right
        """
        action = args[0]
        try:
            if action == "show_common":
                compare.show_common(self.nvim)
                return

            if action == "only_present_on_left":
                compare.only_present_on_left(self.nvim)
                return

            if action == "only_present_on_right":
                compare.only_present_on_right(self.nvim)
                return
        except ValueError as e:
            return self.nvim.err_write(f"{e}\n")

        return self.nvim.err_write(
            "Compare: unknown action. Use one of: show_common, only_present_on_left, only_present_on_right\n"
        )

    @pynvim.function("PwfArguments", sync=True)
    def pwf_arguments(self, *args):
        # args will be a tuple of list like this (['line', 'Pwf line', 8],)
        # line - is the argument which is already entered
        # Pwf line - is the entire command line
        # 8 - is the position of the cursor
        return ["relative", "absolute", "line"]

    @pynvim.function("CompareArguments", sync=True)
    def compare_arguments(self, *args):
        return ["show_common", "only_present_on_left", "only_present_on_right"]
