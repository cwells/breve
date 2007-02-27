from copy import deepcopy
from breve.tags import Tag
from breve.util import Curval

class sequence ( object ):
    def __init__ ( self, name ):
        self.name = name
        
    def __call__ ( self, tag, data ):
        def walk ( o, v ):
            if isinstance ( o, Tag ):
                for idx in range ( len ( o.children ) ):
                    c = o.children [ idx ]
                    if isinstance ( c, Curval ) and c.name == self.name:
                        o.children [ idx ] = v
                    elif isinstance ( c, Tag ):
                        c.data = v 
                        walk ( c, v )

        def process ( items, data ):
            output = [ ]
            if items:
                while data:
                    for i in items:
                        if not data:
                            break
                        if isinstance ( i, Curval ) and i.name == self.name:
                            output.append ( v )
                        elif isinstance ( i, Tag ):
                            itemtag = deepcopy ( i )
                            v = data.pop ( 0 )
                            itemtag.data = v
                            walk ( itemtag, v )
                            output.append ( itemtag )
                        else:
                            output.append ( itemtag )
            return output    
                
        if not data:
            return tag.clear ( )

        data = list ( data ) # coerce tuples

        items = [ ]
        header = None
        headers = [ ]
        footer = None
        footers = [ ]
        output = [ ]

        while tag.children:
            c = tag.children.pop ( )
            if isinstance ( c, Tag ) or isinstance ( c, Curval ):
                if c.pattern == 'header':
                    header = [ c ]
                    headers.append ( data.pop ( 0 ) )
                elif c.pattern == 'footer':
                    footer = [ c ]
                    footers.append ( data.pop ( -1 ) )
                elif c.pattern == 'item':
                    items.append ( c )
                elif c.pattern == 'value':
                    items.append ( c )
            else:
                items.append ( c )

        if header:
            output.extend ( process ( header, headers ) )
        if items:
            output.extend ( process ( items, data ) )
        if footer:
            output.extend ( process ( footer, footers ) )
        
        return tag [ output ]


class mapping ( object ):
    def __init__ ( self, name ):
        self.name = name
        
    def __call__ ( self, tag, data ):
        def walk ( o, v ):
            if isinstance ( o, Tag ):
                for idx in range ( len ( o.children ) ):
                    c = o.children [ idx ]
                    if isinstance ( c, Curval ) and c.name == self.name:
                        o.children [ idx ] = v
                    elif isinstance ( c, Tag ):
                        c.data = v 
                        walk ( c, v )

        if not data:
            return tag.clear ( )
        
        output = [ ]
        
        return tag [ output ]
