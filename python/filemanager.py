import subprocess
import os.path

class FileManager:
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

    def __init__(self):

        # Find .git file
        self.root = None
        self.path = os.getcwd()
        git_file = ".git"
        while "/" != self.path:
            if os.path.isdir(os.path.join(self.path, git_file)):
                self.path = os.path.join(self.path, git_file)
                break
            self.path = os.path.dirname(self.path)

        if self.path == "/":
            return

        self.root = {"root" : ({}, [])}
        self.full_path = {}
        files = subprocess.check_output(["git", "--git-dir", self.path, "ls-files", "-c"])
        files = files.splitlines()

        for f in files:
            self.full_path[os.path.basename(f)] = f
            self.__add(f)

