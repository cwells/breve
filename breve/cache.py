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
            bytecode = compile ( file ( template, 'U' ).read ( ) + '\n', template, 'eval' )
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
        
def memoize ( f ):
    return Memoize ( f )

class Memoize ( object ):
    __slots__ = [ 'cache', 'fn', 'instance', 'expires' ]
    def __init__ ( self, fn ):
        self.cache = { }
        self.fn = fn

    def __get__ ( self, instance, cls=None ):
        self.instance = instance
        return self

    def __call__ ( self, *args ):
        if self.cache.has_key ( args ):
            return self.cache [ args ]
        else:
            object = self.cache [ args ] = self.fn ( self.instance, *args )
        return object
