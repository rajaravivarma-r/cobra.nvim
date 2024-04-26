from enum import Enum

import process


class ControlKey(Enum):
    ENTER = "Enter"


def run_command(command, target_pane):
    send_keys(command, target_pane)
    send_keys(ControlKey.ENTER.value, target_pane)


def send_keys(text, target_pane):
    command = ["tmux", "send-keys", f"-t:{target_pane}", text]
    process.execute_command(command)
