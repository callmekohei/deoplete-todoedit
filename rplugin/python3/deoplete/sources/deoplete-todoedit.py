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
        context   = [ r'(@|@\S)' ]
        folder    = [ r'(\+|\+\S)' ]
        self.input_pattern = '|'.join( context + folder )

    def get_complete_position(self, context):
        m = re.search(r'\w*$', context['input'])
        return m.start() if m else -1

    def gather_candidates(self, context):

        if context['input'][0] == '@':

            return self.myContext()

        elif context['input'][0] == '+':

            if len(context['input']) == 1:
                return self.myFolder()
            else:
                if context['input'][1] == '+':
                    return self.mySubFolder()
                else:
                    return self.myFolder()
        else:
            pass

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
