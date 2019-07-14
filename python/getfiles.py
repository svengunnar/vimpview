import os
import re

def common_path(a, b):
    common = os.path.commonpath([a, b])
    if a.endswith("/"):
        a = a[:-1]
    if b.endswith("/"):
        b = b[:-1]

    return a == b;

def get_files_priv(out, regex, root_dir = ".", lvl = 0):
    ind = "  "
    for root, _ , files in os.walk(root_dir):
        lvl = len(root.split("/")) - 2
        files = list(filter(lambda f: regex.match(f), files))
        if root != "." and len(files) > 0:
            out.append(ind*lvl + "{}/".format(os.path.basename(root)))
        
        for f in files:
            out.append(ind*(lvl + 1) + "{}".format(f))

def get_files(pr_l, out):
    root_dir = "."
    root_abs_path = os.path.abspath(".")
    if pr_l:
        for pr in pr_l:
            proj_dir = os.path.expanduser(pr[0])
            if common_path(proj_dir, root_abs_path):
                regex = re.compile(pr[1])
                os.chdir(proj_dir)
                get_files_priv(out, regex)
                os.chdir(root_abs_path)
                return proj_dir

    regex = re.compile(".*")
    get_files_priv(out, regex)
    return root_abs_path

if __name__== "__main__":
    out = []
    pr = [["~/.vim/pack/plugins/start/vimpview/", ".*\.(py|vim)$"]]
    get_files(pr, out)
    for o in out:
        print(o)
