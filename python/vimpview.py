from getfiles import get_files
import vim
import os.path
import json

class BufWrapper:
    def __init__(self, out):
        self.out = out
        self.first_append = True

    def append(self, value):
        if self.first_append:
            self.out[0] = value
            self.first_append = False
        else:
            self.out.append(value)

    def __getitem__(self, key):
        return self.out[key]

    def __setitem__(self, key, value):
        self.out[key] = value

    def empty(self):
        return self.first_append == True

def goto_window(w):
    vim.command("exe " + str(w.number) + " \"wincmd w\"")

def n_lead_white_spaces(s):
    return len(s) - len(s.lstrip())

def get_cursor_abs_path():
    # Find the absolute path of the file under the cursor
    z = 0
    row, _ = vim.current.window.cursor
    f = vim.current.buffer[row - z - 1]
    f_path = f.strip()
    i = n_lead_white_spaces(f)
    prev_i = i

    while True:

        if prev_i > i and "/" in f:
            f_path = os.path.join(f.strip(), f_path)
            prev_i = i

        if i == 0:
            break

        f = vim.current.buffer[row - z - 1]
        i = n_lead_white_spaces(f)
        z += 1
    return f_path

def init():
    vim.command('''
        function! OpenProjectView()
          pyx open_project_view()
        endfunction
            ''')

    vim.command('''
        function! OpenFile()
          pyx open_file()
        endfunction
            ''')

    vim.command('''
        function! PreQuit()
          pyx pre_quit()
        endfunction
            ''')

    vim.command('''
        function! CursorMoved()
          pyx cursor_moved()
        endfunction
            ''')

    vim.command("autocmd QuitPre * :call PreQuit()")

    proj_view_cmd = vim.bindeval("g:vimpview_open_project_view").decode("utf-8")
    vim.command("nnoremap " + proj_view_cmd + " :call OpenProjectView()<CR>")


def cursor_moved():
    print(get_cursor_abs_path())

def open_project_view():
    if "g:vimpview_idx" in vim.vars:
        vim.command("b " + str(vim.vars["g:vimpview_idx"]))
    else:
        vim.command("ene")

        t = BufWrapper(vim.current.buffer)

        projects = vim.bindeval("g:vimpview_projects").decode("utf-8")
        projects = json.loads(projects)

        root = get_files(projects, t)
        if t.empty():
            return

        vim.vars["g:vimpview_root_path"] = root
        # Create a new hidden buffer in the current window
        vim.command("setlocal ro")
        vim.command("setlocal hidden")
        vim.command("setlocal nomodifiable")
        vim.command("setlocal nonumber")

        # highlight current line
        vim.command("setlocal cursorline")
        vim.command("setlocal cursorline")
        vim.command("hi CursorLine term=bold cterm=bold guibg=Grey40")

        # Map current buffer <CR> to open file
        vim.command("nnoremap <buffer> <CR> :call OpenFile()<CR>")

        vim.vars["g:vimpview_idx"] = vim.current.buffer.number
        vim.command("autocmd CursorMoved <buffer> : call CursorMoved()")


def open_file():
    # Don't open directories
    if "/" in vim.current.line:
        return

    f_path = get_cursor_abs_path()

    # Open the file
    try:
        full_path = os.path.join(vim.vars["g:vimpview_root_path"].decode("utf-8"), f_path)
        vim.command("e " + os.path.relpath(full_path))
    except vim.error:
        return

def pre_quit():
    # clear the text in the buffer to avoid error msg
    if len(vim.windows) == 1:
        if "g:vimpview_idx" in vim.vars:
            idx = vim.vars["g:vimpview_idx"]
            vim.command("bdelete! " + str(idx))
            del vim.vars["g:vimpview_idx"]

