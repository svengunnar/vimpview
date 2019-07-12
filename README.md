# vimpview
vim plugin for browsing files.

The following global variable must be set:
`let g:vimpview_open_project_view="<Leader>o"` - open/close the current window for browsing files

Optional variable to define project roots and regex. A valid json string.
`let g:vimpview_projects="[[\"~/.vim/pack/plugins/start/vimpview/\",\".*\.(py|vim)$\"]]`

# Requirements
* vim 8.x
