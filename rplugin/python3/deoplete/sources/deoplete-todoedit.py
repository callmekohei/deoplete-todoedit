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

            bufferSubfolder = self.myFoo( r'\+\+\S+', '++' )
            return sorted( list( set( bufferSubfolder )) )

        elif last == '@':

            s = self.vim.eval('g:deoplete_todoedit_defaultContext')
            l = re.split('[" ",","]',s)
            defaultContext = list(filter(lambda x : x != '', l ))
            bufferContext = self.myFoo( r'@\S+' , '@' )
            return sorted( list( set( defaultContext + bufferContext )) )

        else:

            s = self.vim.eval("g:deoplete_todoedit_defaultFolder")
            l = re.split('[" ",","]',s)
            defaultFolder = list(filter(lambda x : x != '', l ))
            bufferFolder = self.myFoo( r'(?<!\+)\+(\w+|\d+)' , '+' )
            return sorted( list( set( defaultFolder + bufferFolder )) )

    def myFoo(self,regex,tag):

        s = '\n'.join( getlines( self.vim ) )
        l = re.findall( regex, s )
        return list( map(lambda x : x.replace( tag ,'') , l) )
