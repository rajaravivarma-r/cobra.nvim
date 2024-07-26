from pathlib import Path

import pynvim

import git
import tmux
import utils

from fzf import Fzf

@pynvim.plugin
class RailsPlugin:
    def __init__(self, nvim):
        self.nvim = nvim
        self.nvim_helper = utils.NvimHelper(nvim)

    @pynvim.command("CRSpec", nargs="*", complete="customlist,CrspecAutocomplete")
    def run_rspec_in_tmux(self, args):
        """
        When called without any arguments, as in
        * CRSpec
        It will run the current spec file in the `default_tmux_pane` (specified in code)

        When called with arguments, that is, the target pane as the first argument
        and the spec file path relative to the git root directory as the second argument,
        it runs it appropriately

        No error conditions are handled right now, for example,
        * It does not check if the current file or the specified file are spec files
        * It does not check if the default tmux pane or the specified target panes
          are available
        Thus it will not fail gracefully
        """
        buffer_path = None
        if not args:
            buffer_path = str(
                self.nvim_helper.current_file_path_relative_to(
                    Path(git.get_root_directory())
                )
            )

        # To Specify the target pane see here https://github.com/tmux/tmux/wiki/Advanced-Use#command-targets
        # Use first pane of the second window as target, in the current session
        tmux_target_pane, target_spec_file = utils.with_default_values(
            args, [2.1, buffer_path]
        )
        tmux.run_command(f"bin/rspec {target_spec_file}", tmux_target_pane)

    @pynvim.function("CrspecAutocomplete", sync=True)
    def provide_autocomplete_list_for_crspec(self, func_args):
        arg_lead, command_line, cursor_position = func_args
        utils.logging.info(f"{arg_lead=}")
        utils.logging.info(f"{command_line=}")
        utils.logging.info(f"{cursor_position=}")

        stripped_command_line = command_line.strip()
        is_completing_target_pane = utils.not_empty_and_all_true(
            [v.isdigit() for v in arg_lead.split(".") if v]
        )
        if stripped_command_line == "CRSpec" or is_completing_target_pane:
            return tmux.get_window_index_and_pane_index_for_current_session()

        git_root_path = Path(git.get_root_directory())
        spec_files = [
            str(p.relative_to(git_root_path))
            for p in git_root_path.glob("spec/**/*_spec.rb")
        ]
        fzf = Fzf()
        filtered_files = fzf.filter(arg_lead, "\n".join(spec_files))
        utils.logging.info(f"\n{filtered_files=}\n")
        utils.logging.info(f"\n{arg_lead=}\n")
        return filtered_files
