# vimpview
vim plugin for browsing files. The plugin tries to find the .git directory to identify a project. It also works with git submodules.

`let g:vimpview_open_project_view="<Leader>o"` - open/close the current window for browsing files
`<CR>` open selected file
`let g:vimpview_filter = '.*\.(py|vim)$'` in .vimrc will make the plugin only show .vim and .py files.
`let g:vimpview_projects="~/.vim/pack/plugins/start/vimpview/"` - separate with `:` to have more than one project.

# Requirements
* vim 8.x
