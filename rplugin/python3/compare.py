import re


def stable_unique(lines):
    seen = set()
    unique_lines = []
    for line in lines:
        if line in seen:
            continue
        seen.add(line)
        unique_lines.append(line)
    return unique_lines


def left_right_windows(nvim):
    windows = [
        w for w in nvim.current.tabpage.windows if w.buffer.options.get("buftype", "") == ""
    ]
    if len(windows) < 2:
        raise ValueError(
            "Compare requires at least two file-backed windows in the current tabpage"
        )

    win_info = []
    for window in windows:
        info = nvim.funcs.getwininfo(window.handle)[0]
        win_info.append((info.get("wincol", 0), info.get("winrow", 0), window))

    min_col = min(col for col, _row, _w in win_info)
    max_col = max(col for col, _row, _w in win_info)

    if min_col == max_col:
        win_info.sort(key=lambda x: (x[1], x[0]))
        return win_info[0][2], win_info[-1][2]

    left_win = min((t for t in win_info if t[0] == min_col), key=lambda x: x[1])[2]
    right_win = min((t for t in win_info if t[0] == max_col), key=lambda x: x[1])[2]
    return left_win, right_win


def split_lines(nvim):
    left_win, right_win = left_right_windows(nvim)
    left_lines = list(left_win.buffer[:])
    right_lines = list(right_win.buffer[:])
    return left_lines, right_lines


def open_compare_results(nvim, title, lines):
    nvim.command("botright new")
    buf = nvim.current.buffer
    buf.options["buftype"] = "nofile"
    buf.options["bufhidden"] = "wipe"
    buf.options["swapfile"] = False
    buf.options["buflisted"] = False
    buf.options["modifiable"] = True
    buf[:] = [title, ""] + (lines if lines else ["(none)"])
    buf.options["modifiable"] = False
    safe_title = re.sub(r"\s+", "_", title.strip()) or "results"
    buf_name = f"[Compare]_{safe_title}"
    nvim.command(f"file {nvim.funcs.fnameescape(buf_name)}")


def show_common(nvim):
    left_lines, right_lines = split_lines(nvim)
    right_set = set(right_lines)
    common = stable_unique([line for line in left_lines if line in right_set])
    open_compare_results(nvim, "Common lines", common)


def only_present_on_left(nvim):
    left_lines, right_lines = split_lines(nvim)
    right_set = set(right_lines)
    only_left = stable_unique([line for line in left_lines if line not in right_set])
    open_compare_results(nvim, "Only present on left", only_left)


def only_present_on_right(nvim):
    left_lines, right_lines = split_lines(nvim)
    left_set = set(left_lines)
    only_right = stable_unique([line for line in right_lines if line not in left_set])
    open_compare_results(nvim, "Only present on right", only_right)

