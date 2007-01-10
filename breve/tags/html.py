from breve.flatten import flatten, register_flattener
from breve.tags import Proto, Tag, Namespace

#
# register common HTML elements
#
tag_names = [
    'a','abbr','acronym','address','applet','area',
    'b','base','basefont','bdo','big','blockquote', 'body','br','button',
    'caption','center','cite','code','col','colgroup',
    'dd','dfn','div','dl','dt',
    'em',
    'fieldset','font','form','frame','frameset',
    'h1','h2','h3','h4','h5','h6','head','hr','html',
    'i','iframe','img','input','ins','isindex',
    'kbd',
    'label','legend','li','link',
    'menu','meta',
    'noframes','noscript',
    'ol','optgroup','option',
    'p','param','pre',
    'q',
    's','samp','script','select','small','span','strike','strong','style','sub','sup',
    'table','tbody','td','textarea','tfoot','th','thead','title','tr','tt',
    'u','ul',
    'var'
]

class doctype ( object ):
    def __init__ ( self, type, dtd, validator ):
        self.type = type
        self.dtd = dtd
        self.validator = validator
        
    def __str__ ( self ):
        return ( '''<!DOCTYPE %s PUBLIC "%s" "%s">\n\n'''
                 % ( self.type, self.dtd, self.validator ) )

class xml ( str ): pass

class cdata ( str ):
    def __init__ ( self, children ):
        self.children = children
        
    def __str__ ( self ):
        return xml ( '<![CDATA[%s]]>' % self.children )
        
class inlineJS ( str ):
    def __init__ ( self, children ):
        self.children = children

    def __str__ ( self ):
        return '\n<script type="text/javascript">%s</script>' % cdata ( self.children )
        
class script ( Tag ):
    def __init__ ( self, **kwargs ):
        Tag.__init__ ( self, 'script' )
        self.attrs.update ( kwargs )
        self.children.append ( '' ) # IE requires </script> in all cases

tags = Namespace ( )
for t in tag_names:
    tags [ t ] = Proto ( t )

tags.update ( dict (
    doctype = doctype,
    xml = xml,
    inlineJS = inlineJS,
    script = script,
    cdata = cdata,
) )

