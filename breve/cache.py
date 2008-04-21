from time import time

class Cache ( object ):
    __slots__ = [ 'ccache', 'scache', 'loader' ]
    def __init__ ( self ):
        self.ccache = { }
        self.scache = { }
       
    def compile ( self, template, root, loader ):
        uid, timestamp = loader.stat ( template, root )
        if uid in self.ccache:
            if timestamp == self.ccache [ uid ][ 'timestamp' ]:
                return self.ccache [ uid ][ 'bytecode' ]
        self.ccache [ uid ] = dict (
            timestamp = timestamp,
            bytecode = compile ( '(' + loader.load ( uid ) + ')', template, 'eval' )
        )
        return self.ccache [ uid ] [ 'bytecode' ]

    def get_fragment ( self, template, fragment, root ):
        uid, timestamp = loader.stat ( template, root )
        return self.ccache [ uid ][ 'bytecode' ]

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

