from pathlib import Path

import itertools

import logging

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

    def current_file_path_relative_to(self, parent_path):
        current_buffer_path = Path(self.current_buffer())
        logging.info(f"{current_buffer_path=}")
        parent_path = Path(parent_path.strip()).absolute()
        logging.info(f"{parent_path=}")
        return current_buffer_path.relative_to(parent_path)


def with_default_values(arr, default_arr):
    if len(arr) < len(default_arr):
        while len(arr) < len(default_arr):
            arr.append(default_arr[len(arr)])
    return arr
