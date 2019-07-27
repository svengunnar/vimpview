
function! JOB_get_job_id(job)
	return matchstr(a:job, '\d\+')
endfunction

function! JOB_run_cmd(cmd)

	if !exists("g:JOB_cnt")
		let g:JOB_cnt = 0
		let g:JOB_name2job = {}
		let g:JOB_job2name = {}
	endif

	let name = "JOB_" . g:JOB_cnt
	let g:JOB_cnt = g:JOB_cnt + 1

	let job = job_start(['bash', '-c', a:cmd],
		\ {"err_cb": "JOB_handler",
		\ "out_io": "buffer",
		\ "err_io": "buffer",
		\ "err_name": name,
		\ "out_name": name,
		\ "out_modifiable": 0,
	 	\ "err_modifiable": 0,
		\ "close_cb": "JOB_close_handler"})
	let g:JOB_name2job[name] = job
	let g:JOB_job2name[JOB_get_job_id(job)] = name
endfunction
function! JOB_handler(channel, msg)
	let id = JOB_get_job_id(ch_getjob(a:channel))
	echom "ERR: " . g:JOB_job2name[id]
	let name =  g:JOB_job2name[id]
endfunction

function! JOB_clear_buffer(key)
	let job = g:JOB_name2job[a:key]
	let id = JOB_get_job_id(job)
	let name =  g:JOB_job2name[id]
	" Will cause JOB_close_handler to trigger
	call job_stop(job, "kill")
endfunction

function! JOB_close_handler(channel)
	if exists("g:JOB_job2name")
		let id = JOB_get_job_id(ch_getjob(a:channel))
		let name =  g:JOB_job2name[id]
		unlet g:JOB_job2name[id]
		unlet g:JOB_name2job[name]
	endif
endfunction

function! JOB_maybe_kill_job(name)
	let name = fnamemodify(a:name, ":t")
	if has_key(g:JOB_name2job, name)
		echom "KILL IT (" . name . ") WITH FIRE!"
		call JOB_clear_buffer(name)
	endif
endfunction

