import os

class Cache:
    def __init__ ( self ):
        self.cache = { }

    def compile ( self, template ):
        timestamp = long ( os.stat ( template ).st_mtime )
        if template in self.cache and self.cache [ template ] [ 'timestamp' ] == timestamp:
            return self.cache [ template ] [ 'bytecode' ]

        self.cache [ template ] = dict (
            timestamp = timestamp,
            bytecode = compile ( file ( template, 'U' ).read ( ) + '\n', template, 'eval' )
        )
        return self.cache [ template ] [ 'bytecode' ]
                                                
        
