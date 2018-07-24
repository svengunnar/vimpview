let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

if !exists("g:vimpview_file_filter")
    let g:vimpview_file_filter = []
endif

pyx << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
from vimpview import *
init()
EOF


