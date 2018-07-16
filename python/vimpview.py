from filemanager import FileManager
import vim
import os.path


def goto_window(w):
    vim.command("exe " + str(w.number) + " \"wincmd w\"")

def init():
    vim.command('''
        function! OpenProjectView()
          python open_project_view()
        endfunction
            ''')

    vim.command('''
        function! OpenFile()
          python open_file()
        endfunction
            ''')

    vim.command('''
        function! PreQuit()
          python pre_quit()
        endfunction
            ''')

    vim.command('''
        function! WinEnter()
          python win_enter()
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
        t, full_path, git_path = FileManager().get_result()
        if t == None:
            vim.command('''
                function! Run()
                  python print("Found no .git dir!")
                endfunction
                    ''')
            vim.command("nnoremap <leader>o :call Run()<CR>")
            return

        vim.vars["g:full_path"] = full_path
        vim.vars["g:path"] = os.path.dirname(git_path)

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
    f = vim.current.line.decode("utf-8").strip()
    d = vim.vars["g:full_path"]

    if f not in d:
        return

    vim.command("e " + os.path.join(vim.vars["g:path"], d[f].decode("utf-8")))

def pre_quit():
    # clear the text in the buffer to avoid error msg
    if len(vim.windows) == 1:
        if "g:b_idx" in vim.vars:
            idx = vim.vars["g:b_idx"]
            vim.command("bdelete! " + str(idx))
            del vim.vars["g:b_idx"]

