import pynvim
import re

from utils import logging


@pynvim.plugin
class FilesPlugin:
    def __init__(self, nvim):
        self.nvim = nvim

    # Call this command in any of the following ways
    # * Fopen spec/support/vcr_setup.rb:10:20
    # * Fopen spec/support/vcr_setup.rb:10
    # * Fopen spec/support/vcr_setup.rb
    @pynvim.command("Fopen", nargs="1")
    def open_file_with_line_and_column(self, file_path_with_line_and_column):
        file_path_with_line_and_column = file_path_with_line_and_column[0]
        logging.info(f"{file_path_with_line_and_column=}")
        file_path_line_no_col_no_regex = (
            r"(?P<file_path>[^:]*)(?::(?P<line_no>\d+))?(?::(?P<col_no>\d+))?"
        )
        match = re.search(
            file_path_line_no_col_no_regex, file_path_with_line_and_column
        )
        line_no = None
        col_no = None

        file_path = match.group("file_path")

        if not file_path:
            logging.warn(
                f"Cannnot detect file_path in {file_path_with_line_and_column}"
            )
            return

        if line_no_match := match.group("line_no"):
            line_no = int(line_no_match)

        if col_no_match := match.group("col_no"):
            col_no = int(col_no_match)

        self.nvim.command(f"e {file_path}")
        if line_no:
            self.nvim.command(str(line_no))
        if col_no:
            # Moving col_no times l puts the cursor on the 11th column, so
            # moving it one less
            self.nvim.command(f"normal {col_no - 1}l")
