from filemanager import get_pview
import vim
import os.path

def goto_window(w):
    vim.command("exe " + str(w.number) + " \"wincmd w\"")

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
        t = []
        root = get_pview(t)
        if t == []:
            vim.command('''
                function! Run()
                  python print("Found no .git dir!")
                endfunction
                    ''')
            vim.command("nnoremap <leader>o :call Run()<CR>")
            return

        vim.vars["g:path"] = root
        # Create a new hidden buffer in the current window
        vim.command("ene")

        if t:
            vim.current.buffer[0] = t[0]

        for f in t[1:]:
            vim.current.buffer.append(f)

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

def open_file():
    # Don't open directories
    if "/" in vim.current.line:
        return

    # Find the absolute path of the file under the cursor
    z = 0
    row, _ = vim.current.window.cursor
    f = vim.current.buffer[row - z - 1]
    f_path = f.strip()
    i = len(f) - len(f.lstrip(' '))
    prev_i = i

    while True:

        if prev_i > i and "/" in f:
            f_path = os.path.join(f.strip(), f_path)
            prev_i = i

        if i == 0:
            break

        f = vim.current.buffer[row - z - 1]
        i = len(f) - len(f.lstrip(' '))
        z += 1

    # Open the file
    try:
        vim.command("e " + os.path.join(vim.vars["g:path"].decode("utf-8"), f_path))
    except vim.error:
        return

def pre_quit():
    # clear the text in the buffer to avoid error msg
    if len(vim.windows) == 1:
        if "g:b_idx" in vim.vars:
            idx = vim.vars["g:b_idx"]
            vim.command("bdelete! " + str(idx))
            del vim.vars["g:b_idx"]

