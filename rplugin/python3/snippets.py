import pynvim

from enum import Enum

from utils import logging, NvimHelper

from datetime_helper import get_current_timestamp


@pynvim.plugin
class SnippetsPlugin:
    class SnippetOptions(Enum):
        DATETIMESTAMP = "datetimestamp"

    def __init__(self, nvim):
        self.nvim = nvim
        self.nvim_helper = NvimHelper(nvim)

    # Call this command in any of the following ways
    # * Fopen spec/support/vcr_setup.rb:10:20
    # * Fopen spec/support/vcr_setup.rb:10
    # * Fopen spec/support/vcr_setup.rb
    @pynvim.command("Snippet", nargs="1", complete="customlist,SnippetAutocomplete")
    def insert_snippet(self, snippet_option):
        logging.info(f"{snippet_option=}")
        logging.info(dir(snippet_option))
        logging.info(type(snippet_option))

        value = self._snippet_value(snippet_option[0])
        if not value:
            self.nvim_helper.write_message(f"Snippet not supported: {snippet_option}")
            return

        logging.info(f"{value=}")

        self.nvim_helper.insert_after_cursor(value)

    @pynvim.function("SnippetAutocomplete", sync=True)
    def provide_autocomplete_list_for_snippets(self, func_args):
        arg_lead, command_line, cursor_position = func_args
        logging.info(f"{arg_lead=}")
        logging.info(f"{command_line=}")
        logging.info(f"{cursor_position=}")

        return [s.value for s in self.SnippetOptions]

    def _snippet_value(self, snippet_option):
        match snippet_option:
            case self.SnippetOptions.DATETIMESTAMP.value:
                return get_current_timestamp()
            case _:
                return None
