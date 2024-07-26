import subprocess


def execute_command(command):
    subprocess.run(command)


def popen_and_get_output(command: list, stdin_input: str):
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = process.communicate(input=stdin_input.encode("utf-8"))

    # Decode to string
    return stdout.decode("utf-8")


def execute_and_get_output(command, as_string=True):
    output = subprocess.check_output(command)
    if as_string:
        output = output.decode("utf-8")

    return output
