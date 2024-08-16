from pathlib import Path

import itertools

import io

import logging

import wat

from contextlib import redirect_stdout, contextmanager

logging.basicConfig(
    level=logging.DEBUG, filename="/Users/rajaravivarma/vim.log", filemode="w"
)


class NvimHelper:
    def __init__(self, nvim):
        self.nvim = nvim

    def get_current_word(self):
        self.nvim.command('normal! "wyiw')
        return self.nvim.funcs.getreg("w")

    def replace_current_word(self, new_word):
        self.nvim.funcs.setreg("w", new_word)
        return self.nvim.command('normal! viw"wp')

    def current_buffer(self):
        return self.nvim.current.buffer.name

    def current_file_path_relative_to(self, parent_path: Path):
        current_buffer_path = Path(self.current_buffer())
        logging.info(f"{current_buffer_path=}")
        logging.info(f"{parent_path=}")
        return current_buffer_path.relative_to(parent_path)

    def current_cursor_row(self):
        return self.current_cursor_position()[0]

    def current_cursor_column(self):
        return self.current_cursor_position()[1]

    def current_cursor_position(self):
        return self.nvim.lua.vim.api.nvim_win_get_cursor(0)

    def exec_lua(self, lua_code, *args, **kwargs):
        return self.nvim.exec_lua(lua_code, *args, **kwargs)


def with_default_values(arr, default_arr):
    if len(arr) < len(default_arr):
        while len(arr) < len(default_arr):
            arr.append(default_arr[len(arr)])
    return arr


# Returns False if it is an empty list or checkes if `all` elements are True
def not_empty_and_all_true(arr):
    return bool(arr) and all(arr)


# Call the functions with the *args and **kwargs
def capture_output(func, *args, **kwargs):
    f = io.StringIO()
    with redirect_stdout(f):
        func(*args, **kwargs)
    return f.getvalue()


def wat_log(obj):
    logging.info(capture_output(wat.gray, obj))
