# vimpview
vim plugin for browsing files. The plugin tries to find the .git directory to identify a project. It also works with git submodules.

`<leader>o` open/close the current window for browsing files

`<CR>` open selected file

`let g:vimpview_file_filter = ['.*\.py$', '.*\.vim$']` in .vimrc will make the plugin only show .vim and .py files. This
is directly fed into python's regex implementation.

# Pathogen
`git clone git@github.com:svengunnar/vimpview.git ~/.vim/bundle/vimpview`

# Requirements
* git
* vim 8.x
