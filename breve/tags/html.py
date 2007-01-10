from breve.flatten import flatten, register_flattener
from breve.tags import Proto, Tag, Namespace

#
# Despite what one might think, empty elements aren't really
# supported unless the HTTP Content-type header is text/xml
# and in fact the W3C recommends against such empty elements.
#
class HtmlProto ( str ):
    __slots__ = [ ]
    def __call__ ( self, **kw ):
        return Tag ( self )( **kw )
    
    def __getitem__ ( self, children ):
        return Tag ( self )[ children ]

def flatten_htmlproto ( p ):
    return '<%s></%s>' % ( p, p )

register_flattener ( HtmlProto, flatten_htmlproto )


#
# register common HTML elements
#
tag_names = [
    'a','abbr','acronym','address','applet',
    'b','bdo','big','blockquote', 'body','button',
    'caption','center','cite','code','colgroup',
    'dd','dfn','div','dl','dt',
    'em',
    'fieldset','font','form','frameset',
    'h1','h2','h3','h4','h5','h6','head','html',
    'i','iframe','ins',
    'kbd',
    'label','legend','li',
    'menu',
    'noframes','noscript',
    'ol','optgroup','option',
    'pre',
    'q',
    's','samp','select','small','span','strike','strong','style','sub','sup',
    'table','tbody','td','textarea','tfoot','th','thead','title','tr','tt',
    'u','ul',
    'var'
]

empty_tag_names = [
    'area', 'base', 'basefont', 'br', 'col', 'frame', 'hr',
    'img', 'input', 'isindex', 'link', 'meta', 'p', 'param'
]

class cdata ( str ):
    def __init__ ( self, children ):
        self.children = children
        
    def __str__ ( self ):
        return '<![CDATA[%s]]>' % self.children
        
class inlineJS ( str ):
    def __init__ ( self, children ):
        self.children = children

    def __str__ ( self ):
        return '\n<script type="text/javascript">%s</script>' % cdata ( self.children )
        
class Script ( Tag ):
    def __init__ ( self, *args, **kw ):
        Tag.__init__ ( self, 'script' )
        self.attrs.update ( kw )
    
class script ( Proto ):
    Class = Script
    
class Invisible ( Tag ):
    def __str__ ( self ):
        if self.render:
            self.children = [ ]
            t = self.render ( self, self.data )
        else:
            t = self
        if t.children:
            return ''.join ( [ flatten ( c ) for c in t.children ] )
        return ''
    
class invisible ( Proto ):
    Class = Invisible

class lorem_ipsum ( Tag ):
    ''' silliness ensues '''
    children = [
        'Lorem ipsum dolor sit amet, consectetuer adipiscing elit.',
        'In egestas nisl sit amet odio.',
        'Duis iaculis metus eu nulla.',
        'Donec venenatis sapien sed urna.',
        'Donec et felis ut elit elementum pellentesque.',
        'Praesent bibendum turpis semper lacus.'
    ]

    def __init__ ( self ):
        Tag.__init__ ( self, 'span' )
        

tags = Namespace ( )
for t in tag_names:
    tags [ t ] = HtmlProto ( t )

for t in empty_tag_names:
    tags [ t ] = Proto ( t )
    
tags.update ( dict (
    inlineJS = inlineJS,
    script = script ( 'script' ),
    cdata = cdata,
    invisible = invisible ( 'invisible' ),
    lorem_ipsum = lorem_ipsum,
) )

