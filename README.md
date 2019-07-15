# vimpview
vim plugin for browsing files.

Some or all of the following should be set:
`let g:vimpview_open_project_view="<Leader>o"` - open the current window for browsing files. Use `<CR>` to open buffer.
`let g:vimpview_open_buffers_view="<Leader>b"` - open the current window for browsing loaded buffers. Use <`CR`> to open buffer. Use `dd` to unload buffer.

Optional variable to define project roots and regex. Example: 

`let g:vimpview_projects=[['~/.vim/pack/plugins/start/vimpview/','.*\.vim$']]`

The default behavior is `[['.', '.*']]`
