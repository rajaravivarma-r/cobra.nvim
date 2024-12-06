from pathlib import Path

import itertools

import io

import logging

import wat

from contextlib import redirect_stdout, contextmanager

logging.basicConfig(
    level=logging.DEBUG, filename="/Users/rajaravivarma/vim.log", filemode="w"
)


class SimpleDelegator:
    def __init__(self, obj):
        self._wrapped_obj = obj

    def __getattr__(self, attr):
        if attr == "_wrapped_obj":
            return self._wrapped_obj
        return getattr(self._wrapped_obj, attr)

    def __setattr__(self, attr, value):
        if attr == "_wrapped_obj":
            super().__setattr__(attr, value)
        else:
            setattr(self._wrapped_obj, attr, value)

    def __delattr__(self, attr):
        if attr == "_wrapped_obj":
            raise AttributeError("Can't delete _wrapped_obj")
        delattr(self._wrapped_obj, attr)


class NvimHelper(SimpleDelegator):
    def __init__(self, nvim):
        super().__init__(nvim)
        self.nvim = nvim

    def get_current_word(self):
        self.nvim.command('normal! "wyiw')
        return self.nvim.funcs.getreg("w")

    def replace_current_word(self, new_word):
        self.nvim.funcs.setreg("w", new_word)
        return self.nvim.command('normal! viw"wp')

    def current_buffer_name(self):
        return self.nvim.current.buffer.name

    def current_file_path_relative_to(self, parent_path: Path):
        current_buffer_path = Path(self.current_buffer_name())
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

    def insert_after_cursor(self, text):
        return self.nvim.feedkeys(f"a{text}")

    def insert_at_cursor(self, text):
        return self.nvim.feedkeys(f"i{text}")

    def append_to_current_buffer(self, text):
        return self.nvim.current.buffer.append(text)

    def write_message(self, message):
        return self.nvim.out_write(f"{message}\n")


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
