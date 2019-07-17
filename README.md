# vimpview
vim plugin for browsing files efficiently.

At least one of the following two points should be set for this plugin to do anything at all:
* `let g:vimpview_open_project_view="<Leader>o"` - open the current window for browsing files. Use `<CR>` to open buffer.
* `let g:vimpview_open_buffers_view="<Leader>b"` - open the current window for browsing loaded buffers. Use <`CR`> to open buffer. Use `dd` to unload buffer.

The following two points are completely optional:
* `let g:vimpview_projects=[['~/.vim/pack/plugins/start/vimpview/','.*\.vim$']]` - Optionally define project roots and regexes. The default behavior is `[['.', '.*']]`.
* `let g:vimpview_open_project_list="<Leader>l"` - A view for selecting project, does a `cd` into selected project. Only useful if the previous point is set.
