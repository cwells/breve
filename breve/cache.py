import os
from time import time
 
class Cache ( object ):
    __slots__ = [ 'ccache', 'scache' ]
    def __init__ ( self ):
        self.ccache = { }
        self.scache = { }
        
    def compile ( self, template ):
        timestamp = long ( os.stat ( template ).st_mtime )
        if template in self.ccache and self.ccache [ template ] [ 'timestamp' ] == timestamp:
            return self.ccache [ template ] [ 'bytecode' ]

        self.ccache [ template ] = dict (
            timestamp = timestamp,
            bytecode = compile ( file ( template, 'U' ).read ( ), template, 'eval' )
        )
        return self.ccache [ template ] [ 'bytecode' ]

    def memoize ( self, id, timeout, f, *args, **kw ):
        t = time ( )
        if id not in self.scache:
            self.scache [ id ] = {
                'timestamp': t,
                'string': f ( *args, **kw )
            }
        elif ( t - self.scache [ id ] [ 'timestamp' ] ) > timeout:
            self.scache [ id ] = {
                'timestamp': t,
                'string': f ( *args, **kw )
            }
            
        return self.scache [ id ] [ 'string' ]
