from filemanager import get_pview
import vim
import os.path

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
        function! WinEnter()
          pyx win_enter()
        endfunction
            ''')

    vim.command("autocmd QuitPre * :call PreQuit()")
    vim.command("nnoremap <leader>o :call OpenProjectView()<CR>")

def open_project_view():
    if "g:b_idx" in vim.vars:
        for w in vim.windows:
            if w.buffer.number == vim.vars["g:b_idx"]:
                if w.number != vim.current.window.number:
                    old_buf = vim.current.window.buffer.number
                    goto_window(w)
                    vim.command("quit")
                    # Go back to the previous window
                    for w_old in vim.windows:
                        if w_old.buffer.number == old_buf:
                            goto_window(w_old)
                else:
                    goto_window(w)
                    vim.command("quit")

                return

        vim.command("b " + str(vim.vars["g:b_idx"]))
    else:
        vim.command("ene")

        t = BufWrapper(vim.current.buffer)

        regex = vim.bindeval("g:vimpview_filter").decode("utf-8")

        root = get_pview(t, regex)
        if t.empty():
            return

        vim.vars["g:root_path"] = root
        # Create a new hidden buffer in the current window

        vim.command("setlocal ro")
        vim.command("setlocal hidden")
        vim.command("setlocal nomodifiable")
        vim.command("setlocal nonumber")

        # highlight current line
        vim.command("setlocal cursorline")
        vim.command("color desert")
        vim.command("setlocal cursorline")
        vim.command("hi CursorLine term=bold cterm=bold guibg=Grey40")

        # Map current buffer <CR> to open file
        vim.command("nnoremap <buffer> <CR> :call OpenFile()<CR>")

        vim.vars["g:b_idx"] = vim.current.buffer.number

        # Cursor in the project view
        vim.command('''
            function! CursorMoved()
              pyx cursor_moved()
            endfunction
                ''')

        vim.command("autocmd CursorMoved <buffer="+str(vim.current.buffer.number)+"> :call CursorMoved()")

def open_file():
    # Don't open directories
    if "/" in vim.current.line:
        return

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

    # Open the file
    try:
        full_path = os.path.join(vim.vars["g:root_path"].decode("utf-8"), f_path)
        vim.command("e " + os.path.relpath(full_path))
    except vim.error:
        return

def pre_quit():
    # clear the text in the buffer to avoid error msg
    if len(vim.windows) == 1:
        if "g:b_idx" in vim.vars:
            idx = vim.vars["g:b_idx"]
            vim.command("bdelete! " + str(idx))
            del vim.vars["g:b_idx"]

def cursor_moved():
    # Move the cursor to point to the first character of the line
    row, _ = vim.current.window.cursor
    f = vim.current.buffer[row - 1]
    vim.current.window.cursor = (row, n_lead_white_spaces(f))

