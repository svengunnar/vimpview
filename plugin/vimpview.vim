function! OpenFile()
	 execute "e " . getline(".")
endfunction

function! SetupCurrentBuf()
	setlocal hidden
	setlocal nomodifiable
	setlocal nonumber
	" highlight current line
	setlocal cursorline
	hi CursorLine term=bold cterm=bold guibg=Grey40
	" Map current buffer <CR> to open file
	execute "nnoremap  <buffer> <CR> :call OpenFile()<CR>"
endfunction

function! CommonPath(proj_dir_path, root_dir_path)
	let i = 1
	let root_dir_path = a:root_dir_path
	while strlen(root_dir_path) >= strlen(a:proj_dir_path)
		if root_dir_path == a:proj_dir_path
			return 1
		endif
		let root_dir_path = fnamemodify(root_dir_path, ":h")
	endwhile
	return 0
endfunction

function! PopulateBuf()
	let n = 1
	let cur_proj = "."
	let regex = ".*"

	if exists("g:vimpview_projects")
		let l = g:vimpview_projects
		let root_dir_path = getcwd()
		for p in l
			let proj_dir_path = fnamemodify(p[0], ":p:h")
			if CommonPath(proj_dir_path, root_dir_path)
				if strlen(cur_proj) < strlen(proj_dir_path)
					let cur_proj = proj_dir_path
					let regex = p[1]
				endif
			endif
		endfor
	endif
	let lines = split(globpath(cur_proj, "**"), "\n")
	let n = 1
	let cur_proj_n = strlen(cur_proj)
	echom regex
	for line in lines
		let rel_line = line[cur_proj_n + 1:]
		if !empty(matchstr(rel_line, regex))
			call setline(n, rel_line)
			let n = n + 1
		endif
	endfor
endfunction

function! OpenVimPView()
	if exists("g:vimpview_bufnr")
		execute "b " . g:vimpview_bufnr
	else
		execute "ene"
		let g:vimpview_bufnr = bufnr("%")
		call PopulateBuf()
		call SetupCurrentBuf()
	endif
endfunction

function! PopulateBView()
	setlocal modifiable
	normal! dG
	let l = range(1, bufnr("$"))
	let i = 1
	for b in l
		if bufloaded(b) && bufname(b) != ""
			call setline(i, expand("#" . b . ":p"))
			let i = i + 1
		endif
	endfor
	setlocal nomodifiable
endfunction

function! CloseBuffer()
	setlocal modifiable
	let path = getline(".")
	execute "normal! dd"
	execute "bdelete! " . bufnr(path)
	setlocal nomodifiable
endfunction

function! OpenVimBView()
	if exists("g:vimbview_bufnr")
		execute "b " . g:vimbview_bufnr
		call PopulateBView()
	else
		execute "ene"
		let g:vimbview_bufnr = bufnr("%")
		call PopulateBView()
		call SetupCurrentBuf()
    		nnoremap <buffer> dd :call CloseBuffer()<CR>
	endif
endfunction

function! PreQuit()
    if exists("g:vimpview_bufnr")
	execute "bd! " . g:vimpview_bufnr
    endif
    if exists("g:vimbview_bufnr")
	execute "bd! " . g:vimbview_bufnr
    endif
endfunction

autocmd QuitPre * : call PreQuit()
if exists("g:vimpview_open_project_view")
	execute "nnoremap" . g:vimpview_open_project_view . " : call OpenVimPView()<CR>"
endif

if exists("g:vimpview_open_buffers_view")
	execute "nnoremap" . g:vimpview_open_buffers_view . " : call OpenVimBView()<CR>"
endif

