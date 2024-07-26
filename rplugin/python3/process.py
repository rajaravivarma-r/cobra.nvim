import subprocess


def execute_command(command):
    subprocess.run(command)


def execute_and_get_output(command, as_string=True):
    output = subprocess.check_output(command)
    if as_string:
        output = output.decode("utf-8")

    return output
