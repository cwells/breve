import os

class FileLoader ( object ):
    __slots__ = [ ]

    def stat ( self, template, root ):
        uid = os.path.join ( root, template )
        timestamp = long ( os.stat ( uid ).st_mtime )
        return uid, timestamp
    
    def load ( self, uid ):
        return unicode ( file ( uid, 'U' ).read ( ), 'utf-8' )
