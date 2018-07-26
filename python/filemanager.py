import subprocess
import os.path
import re

ind_per_lvl = "  "

def get_text(f, l_prev, out):
    l = f.split("/")
    ff = l.pop()

    start = 0

    if l_prev:
        for i in range(0, len(l_prev)):
            if i == len(l):
                break

            if l_prev[i] != l[i]:
                break

            start += 1

    extra_indent = ""
    z = 0
    for i in range(start, len(l)):
        extra_indent = ind_per_lvl * i
        out.append(extra_indent + l[i] + "/")
        z += 1

    out.append((start + z) * ind_per_lvl + ff)

    return l

def get_submodules(root):
    # Get the paths to the submodules
    try:
        subm = subprocess.check_output(["git", "--git-dir", os.path.join(root, ".git"), "config",
            "--file", os.path.join(root, ".gitmodules"), "--get-regexp",
            "path"]).decode("utf8")
    except:
        return []

    subm = re.compile("submodule.* ").split(subm)
    subm.pop(0)
    return list(map(lambda s: s.strip(), subm))


def process_root(root, rel_path, l_prev, out, regex):
    files = subprocess.check_output(["git", "--git-dir", os.path.join(root, ".git"), "ls-files",
        "-c", "--full-name"]).decode("utf-8")
    files = files.splitlines()
    subms = get_submodules(root)

    for f in files:

        if regex and f not in subms:
            m = re.compile(regex)
            full_path = os.path.join(rel_path, f)
            if not m.match(full_path):
                continue

        if f in subms:
            new_root = os.path.join(root, f)
            l_prev = process_root(new_root, os.path.join(rel_path, f), l_prev, out, regex)
        else:
            l_prev = get_text(os.path.join(rel_path, f), l_prev, out)

    return l_prev

def is_in_working_tree(print_error=False):
    try:
        out = subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"],
              stderr=subprocess.STDOUT).decode("utf-8")
        if "true" in out:
            return True
        else:
            return False
    except subprocess.CalledProcessError as e:
        if print_error:
            print(e.output)
        return False

def get_pview(out, regex):
    root = os.getcwd()

    orig_root = root

    if not is_in_working_tree(True):
        return None, None

    while is_in_working_tree():
        try:
            root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"],
                   stderr=subprocess.STDOUT).decode("utf-8")
        except subprocess.CalledProcessError as e:
            print(e.output)
            return None, None

        root = root.strip("\n")

        os.chdir(root)
        os.chdir("..")

    os.chdir(root)

    l_prev = []
    process_root(root, "", l_prev, out, regex)

    os.chdir(orig_root)

    return root

