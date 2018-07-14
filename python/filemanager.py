import subprocess
import os.path
import re

class FileManager:

    def get_submodules(self, git_dir):
        # Get the paths to the submodules
        try:
            subm = subprocess.check_output(["git", "--git-dir", git_dir, "config",
                "--file", os.path.join(os.path.dirname(git_dir), ".gitmodules"), "--get-regexp",  "path"])
        except:
            return []

        subm = re.compile("submodule.* ").split(subm)
        subm.pop(0)
        return map(lambda s: s.strip(), subm)

    def __add_rec(self, l, d, last_key):
        key = l.pop(0)

        if not l:
            d[last_key][1].append(key)
        else:
            if key not in d[last_key][0]:
                d[last_key][0][key] = ({}, [])

            self.__add_rec(l, d[last_key][0], key)

    def __add(self, f):
        l = []
        while f != '':
            l.append(os.path.basename(f))
            f = os.path.dirname(f)

        l = l[::-1]
        self.__add_rec(l, self.root, "root")

    def __gen_text_rec(self, d, l, indent):
        for f in d[1]:
            l.append(indent + f)

        for key in d[0]:
            l.append(indent + key + "/")
            self.__gen_text_rec(d[0][key], l, indent + " ")

    def get_result(self):
        if  self.root == None:
            return (None, None, None)

        l = []
        self.__gen_text_rec(self.root["root"], l, ""),
        return (l, self.full_path, self.path)

    def setup_dir(self, rel_root_subm_dir = ""):
        # Get files for root
        cur_root_dir = os.path.join(os.path.dirname(self.path), rel_root_subm_dir)
        files = subprocess.check_output(["git", "--git-dir", os.path.join(cur_root_dir, ".git"), "ls-files", "-c"])
        files = files.splitlines()

        subms = self.get_submodules(cur_root_dir)
        for f in files:
            if f in subms:
                self.setup_dir(os.path.join(rel_root_subm_dir, f))
            else:
                # find absolute path to f
                abs_path = os.path.join(cur_root_dir, f)
                self.full_path[os.path.basename(f)] = abs_path
                # Add the file to the dict
                self.__add(os.path.join(rel_root_subm_dir, f))

    def __init__(self):
        # Find .git file
        self.root = None
        self.path = os.getcwd()
        while "/" != self.path:
            if os.path.isdir(os.path.join(self.path, ".git")):
                self.path = os.path.join(self.path, ".git")
                break
            self.path = os.path.dirname(self.path)

        if self.path == "/":
            return

        self.root = {"root" : ({}, [])}
        self.full_path = {}

        self.setup_dir()

