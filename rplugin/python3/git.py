import process


def get_root_directory():
    return process.execute_and_get_output(
        ["git", "rev-parse", "--show-toplevel"]
    ).strip()
