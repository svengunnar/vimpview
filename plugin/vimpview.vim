function! OpenPFile()
	execute "e ". fnamemodify(g:vimpview_cur_proj . "/" . getline(".") , ":~:.")
endfunction

function! OpenBFile()
	execute "e " . getline(".")
endfunction

function! SetupCurrentBuf()
	setlocal hidden
	setlocal nomodifiable
	setlocal nonumber
	setlocal cursorline
	setlocal buftype=nofile
	setlocal bufhidden=hide
	setlocal noswapfile
	setlocal nobuflisted
	hi CursorLine term=bold cterm=bold guibg=Grey40
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

function! PopulatePView()
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
	let lines = glob("`find " . cur_proj . " -type f -regextype egrep -regex \"" . regex . "\"`", 0, 1)
	let n = 1
	let cur_proj_n = strlen(cur_proj)
	for line in lines
		let rel_line = line[cur_proj_n + 1:]
		call setline(n, rel_line)
		let n = n + 1
	endfor

	let g:vimpview_cur_proj = fnamemodify(cur_proj, ":p:h")
	redraw | echo g:vimpview_cur_proj
endfunction

function! CursorMoved()
	redraw | echo g:vimpview_cur_proj
endfunction

function! OpenVimPView()
	if exists("g:vimpview_bufnr")
		execute "b " . g:vimpview_bufnr
	else
		execute "ene"
		let g:vimpview_bufnr = bufnr("%")
		call PopulatePView()
		call SetupCurrentBuf()
		autocmd CursorMoved <buffer> : call CursorMoved()
		execute "nnoremap  <buffer> <CR> :call OpenPFile()<CR>"
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
		execute "nnoremap  <buffer> <CR> :call OpenBFile()<CR>"
	endif
endfunction

function! OpenVimPList()
	execute "ene"
	call SetupCurrentBuf()
	let l = g:vimpview_projects
	let i = 1
	setlocal modifiable
	for p in l
		let proj_dir_path = fnamemodify(p[0], ":p:h")
		call setline(i, proj_dir_path)
		let i = i + 1
	endfor
	setlocal nomodifiable
	execute "nnoremap <buffer> <CR> : call ChangeProject()<CR>"
endfunction

function! ChangeProject()
	execute "cd " . getline(".")
	call PreQuit()
endfunction

function! CloseBuffer()
	setlocal modifiable
	let path = getline(".")
	execute "normal! dd"
	execute "bdelete! " . bufnr(path)
	setlocal nomodifiable
endfunction

function! PreQuit()
	if exists("g:vimpview_bufnr")
		unlet g:vimpview_bufnr
	endif
 	if exists("g:vimpview_cur_proj")
		unlet g:vimpview_cur_proj
	endif
	if exists("g:vimbview_bufnr")
		unlet g:vimbview_bufnr
	endif
endfunction

autocmd QuitPre * : call PreQuit()

if exists("g:vimpview_open_project_view")
	execute "nnoremap" . g:vimpview_open_project_view . " : call OpenVimPView()<CR>"
	if exists("g:vimpview_open_project_list") && exists("g:vimpview_projects")
		execute "nnoremap" . g:vimpview_open_project_list . " : call OpenVimPList()<CR>"
	endif
endif

if exists("g:vimpview_open_buffers_view")
	execute "nnoremap" . g:vimpview_open_buffers_view . " : call OpenVimBView()<CR>"
endif
