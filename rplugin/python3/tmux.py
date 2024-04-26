from enum import Enum

import process


class ControlKey(Enum):
    ENTER = "Enter"


def run_command(command, target_pane):
    send_keys(command, target_pane)
    send_keys(ControlKey.ENTER.value, target_pane)

def get_window_index_and_pane_index_for_current_session(separator='.'):
    command = ['tmux', 'list-panes', '-s', '-F', '#{window_index}.#{pane_index}']
    output = process.execute_and_get_output(command)
    return [line.strip() for line in output.strip().splitlines()]

def send_keys(text, target_pane):
    command = ["tmux", "send-keys", f"-t:{target_pane}", text]
    process.execute_command(command)
