if exists('g:loaded_deoplete_todoedit')
  finish
endif
let g:loaded_deoplete_todoedit = 1

if !exists("g:deoplete_todoedit_defaultFolder")
  let g:deoplete_todoedit_defaultFolder = ''
endif

if !exists("g:deoplete_todoedit_defaultContext")
  let g:deoplete_todoedit_defaultContext = ''
endif
