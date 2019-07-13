import os
import re

def get_files_priv(out, regex, root_dir = ".", lvl = 0):
    ind = "  "
    for root, _ , files in os.walk(root_dir):
        lvl = len(root.split("/")) - 1
        files = list(filter(lambda f: regex.match(f), files))

        if lvl != 0 and len(files) > 0:
            out.append(ind*(lvl - 1) + "{}/".format(os.path.basename(root)))

        for f in files:
            out.append(ind*lvl + "{}".format(f))

def get_files(pr_l, out):
    root_dir = "."
    root_abs_path = os.path.abspath(".")
    for pr in pr_l:
        proj_dir = os.path.expanduser(pr[0])
        common = os.path.commonpath([proj_dir, root_abs_path])
        if proj_dir.endswith("/"):
            proj_dir = proj_dir[:-1]
        if common.endswith("/"):
            common = common[:-1]

        if common == proj_dir:
            regex = re.compile(pr[1])
            os.chdir(proj_dir)
            get_files_priv(out, regex)
            os.chdir(root_abs_path)
            return proj_dir

    regex = re.compile(".*")
    get_files_rec(out, regex)
    return root_abs_path
