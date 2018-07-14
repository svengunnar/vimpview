from filemanager import FileManager
import vim
import os.path
import copy

def init():
    a = FileManager()
    text, full_path, git_path = a.get_result()
    if text == None:
        vim.command('''
            function! Run()
              python print("Found no .git dir!")
            endfunction
                ''')
        vim.command("nnoremap <leader>o :call Run()<CR>")
        return

    vim.vars["g:text"] = text
    vim.vars["g:full_path"] = full_path
    vim.vars["g:path"] = os.path.dirname(git_path)

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

    vim.command("autocmd QuitPre * :call PreQuit()")
    vim.command("nnoremap <leader>o :call OpenProjectView()<CR>")

def open_project_view():
    if "g:b_idx" in vim.vars:
        # Check if the window is already opened in some window
        # then we can just disregard this event.
        for w in vim.windows:
            if w.buffer.number == vim.vars["g:b_idx"]:
                print("project view already opened")
                return

        vim.command("vert sb" + str(vim.vars["g:b_idx"]))
        vim.current.window.width = 40
    else:
        vim.command("vnew")
        vim.current.window.width = 40
        t = vim.vars["g:text"]
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
    f = vim.current.line.strip()
    d = vim.vars["g:full_path"]

    if f not in d:
        return

    try:
        if len(vim.windows) > 1:
            vim.command("execute \"normal! \<c-w>b\"")
            vim.command("split " + os.path.join(vim.vars["g:path"], d[f]))
        else:
            win = vim.current.window
            vim.command("vsp " + os.path.join(vim.vars["g:path"], d[f]))
            vim.command("execute \"normal! \<C-W>r\"")
            win.width = 40
    except vim.error:
        return

def pre_quit():
    # clear the text in the buffer to avoid error msg
    if (len(vim.windows) == 1):
        if "g:b_idx" in vim.vars:
            idx = str(vim.vars["g:b_idx"])
            vim.command("bdelete! " + idx)
            del vim.vars["g:b_idx"]

