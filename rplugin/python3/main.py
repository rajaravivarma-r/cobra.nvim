from pathlib import Path
import re

import pynvim

from text import Text
import tmux
import utils


@pynvim.plugin
class CobraPlugin:
    def __init__(self, nvim):
        self.nvim = nvim
        self.nvim_helper = utils.NvimHelper(nvim)

    def _stable_unique(self, lines):
        seen = set()
        unique_lines = []
        for line in lines:
            if line in seen:
                continue
            seen.add(line)
            unique_lines.append(line)
        return unique_lines

    def _left_right_windows(self):
        windows = [
            w
            for w in self.nvim.current.tabpage.windows
            if w.buffer.options.get("buftype", "") == ""
        ]
        if len(windows) < 2:
            raise ValueError(
                "Compare requires at least two file-backed windows in the current tabpage"
            )

        win_info = []
        for window in windows:
            info = self.nvim.funcs.getwininfo(window.handle)[0]
            win_info.append(
                (info.get("wincol", 0), info.get("winrow", 0), window)
            )

        min_col = min(col for col, _row, _w in win_info)
        max_col = max(col for col, _row, _w in win_info)

        if min_col == max_col:
            win_info.sort(key=lambda x: (x[1], x[0]))
            return win_info[0][2], win_info[-1][2]

        left_win = min(
            (t for t in win_info if t[0] == min_col), key=lambda x: x[1]
        )[2]
        right_win = min(
            (t for t in win_info if t[0] == max_col), key=lambda x: x[1]
        )[2]
        return left_win, right_win

    def _split_lines(self):
        left_win, right_win = self._left_right_windows()
        left_lines = list(left_win.buffer[:])
        right_lines = list(right_win.buffer[:])
        return left_lines, right_lines

    def _open_compare_results(self, title, lines):
        self.nvim.command("botright new")
        buf = self.nvim.current.buffer
        buf.options["buftype"] = "nofile"
        buf.options["bufhidden"] = "wipe"
        buf.options["swapfile"] = False
        buf.options["buflisted"] = False
        buf.options["modifiable"] = True
        buf[:] = [title, ""] + (lines if lines else ["(none)"])
        buf.options["modifiable"] = False
        safe_title = re.sub(r"\s+", "_", title.strip()) or "results"
        buf_name = f"[Compare]_{safe_title}"
        self.nvim.command(f"file {self.nvim.funcs.fnameescape(buf_name)}")

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
            left_lines, right_lines = self._split_lines()
        except ValueError as e:
            return self.nvim.err_write(f"{e}\n")

        left_set = set(left_lines)
        right_set = set(right_lines)

        if action == "show_common":
            common = self._stable_unique([line for line in left_lines if line in right_set])
            self._open_compare_results("Common lines", common)
            return

        if action == "only_present_on_left":
            only_left = self._stable_unique(
                [line for line in left_lines if line not in right_set]
            )
            self._open_compare_results("Only present on left", only_left)
            return

        if action == "only_present_on_right":
            only_right = self._stable_unique(
                [line for line in right_lines if line not in left_set]
            )
            self._open_compare_results("Only present on right", only_right)
            return

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
