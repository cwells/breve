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
        to_compile = loader.load(uid)
        if to_compile[:1] == "#":
            # Skip lines that start with a comment, so that for example
            # encoding information is left intact. Putting a newline after
            # the opening bracket is also an option, but that makes the
            # line numbers in error messages off-by-one.
            i = -1
            while i < len(to_compile):
                i = to_compile.find("\n", i + 1)
                if i == -1:
                    break
                if to_compile[i + 1 : i + 2] != "#":
                    break
            if i >= 0:
                to_compile = to_compile[:i + 1] + \
                        "(" + to_compile[i + 1:] + "\n)"
        else:
            # The code starts immediately, no encoding information. So simply
            # put the container brackets in front and at the end. This will
            # not change the line number information in error messages.
            to_compile = "(" + to_compile + "\n)"
        self.ccache [ uid ] = dict (
            timestamp = timestamp,
            bytecode = compile ( to_compile, template, 'eval' )
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

