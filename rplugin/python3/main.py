from pathlib import Path

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
    def testcommand(self, args):
        import pyperclip

        copy_relative_path = False
        buffer_path = Path(self.nvim.current.buffer.name)
        if any("rel" in a for a in args):
            copy_relative_path = True

        if copy_relative_path:
            current_path = Path(self.nvim.command_output("pwd"))
            buffer_path = buffer_path.relative_to(current_path)
        pyperclip.copy(str(buffer_path))
