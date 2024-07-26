import pynvim

import git
import tmux
import utils


@pynvim.plugin
class RailsPlugin:
    def __init__(self, nvim):
        self.nvim = nvim
        self.nvim_helper = utils.NvimHelper(nvim)

    @pynvim.command("CRSpec", nargs="*")
    def run_rspec_in_tmux(self, args):
        """
        When called without any arguments, as in
        * CRSpec
        It will run the current spec file in the `default_tmux_pane` (specified in code)

        When called with arguments, that is, the target pane as the first argument
        and the spec file path relative to the git root directory as the second argument,
        it runs it appropriately

        No error conditions are handled right now, for example,
        * It does not check if the current file or the specifiec file are spec files
        * It does not check if the default tmux pane or the specified target panes
          are available
        Thus it will not fail gracefully
        """
        buffer_path = str(
            self.nvim_helper.current_file_path_relative_to(git.get_root_directory())
        )

        # To Specify the target pane see here https://github.com/tmux/tmux/wiki/Advanced-Use#command-targets
        # Use first pane of the second window as target, in the current session
        tmux_target_pane, target_spec_file = utils.with_default_values(
            args, [2.1, buffer_path]
        )
        tmux.run_command(f"bin/rspec {target_spec_file}", tmux_target_pane)
