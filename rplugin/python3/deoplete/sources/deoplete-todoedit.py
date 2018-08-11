# ===========================================================================
#  FILE    : deoplete-todoedit.py
#  AUTHOR  : callmekohei <callmekohei at gmail.com>
#  License : MIT license
# ===========================================================================


import re
from .base import Base
from deoplete.util import getlines, expand

class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'todoedit'
        self.mark = '[todoedit]'
        self.filetypes = ['todoedit']

        # input pattern
        context    = [ r'^@|(?<=\s)@' ]
        folder     = [ r'^\+|(?<=\s)\+' ]
        subfolder  = [ r'^\+\+|(?<=\s)\+\+' ]
        self.input_pattern = '|'.join( context + folder + subfolder )

    def get_complete_position(self, context):
        m = re.search(r'\w*$', context['input'])
        return m.start() if m else -1

    def gather_candidates(self, context):

        last = context['input'].split(' ')[-1]
        if len(last) == 2 :
            return self.mySubFolder()
        elif last == '@':
            return self.myContext()
        else:
            return self.myFolder()

    def mySubFolder(self):

        s = '\n'.join( getlines( self.vim ) )
        l = re.findall( r'\+\+\S+', s )
        bufferContexts = list( map(lambda x : x.replace('++','') , l) )

        return sorted( list( set( bufferContexts )) )

    def myFolder(self):

        tmp = self.vim.eval("g:deoplete_todoedit_defaultFolder")
        tmp = re.split('[" ",","]',tmp)
        defaultFolder = list(filter(lambda x : x != '', tmp ))

        s = '\n'.join( getlines( self.vim ) )
        l = re.findall( r'(?<!\+)\+(\w+|\d+)' , s )
        bufferFolder = list( map(lambda x : x.replace('+','') , l) )

        return sorted( list( set( defaultFolder + bufferFolder )) )

    def myContext(self):

        tmp = self.vim.eval('g:deoplete_todoedit_defaultContext')
        tmp = re.split('[" ",","]',tmp)
        defaultContext = list(filter(lambda x : x != '', tmp ))

        s = '\n'.join( getlines( self.vim ) )
        l = re.findall( r'@\S+', s )
        bufferContext = list( map(lambda x : x.replace('@','') , l) )

        return sorted( list( set( defaultContext + bufferContext )) )
