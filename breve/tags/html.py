from breve.flatten import flatten, register_flattener
from breve.tags import Proto, Tag, Namespace, cdata, xml, flatten_tag, flatten_proto, custom_tag

xmlns = "http://www.w3.org/1999/xhtml"
doctype = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" 
              "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n'''

#
# Despite what one might think, empty elements aren't really
# supported unless the HTTP Content-type header is text/xml
# and in fact the W3C recommends against such empty elements.
#
class HtmlProto ( unicode ):
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
    'canvas', 'caption','center','cite','code','colgroup',
    'dd','dfn','div','dl','dt',
    'em',
    'fieldset','font','form','frameset',
    'h1','h2','h3','h4','h5','h6','head','html',
    'i','iframe','ins',
    'kbd',
    'label','legend','li',
    'menu',
    'nobr', 'noframes','noscript',
    'ol','optgroup',
    'pre',
    'q',
    's','samp','script', 'select','small','span','strike','strong','style','sub','sup',
    'table','tbody','td','textarea','tfoot','th','thead','title','tr','tt',
    'u','ul',
    'var'
]

empty_tag_names = [
    'area', 'base', 'basefont', 'br', 'col', 'frame', 'hr',
    'img', 'input', 'isindex', 'link', 'meta', 'p', 'param'
]
    
    
class inlineJS ( unicode ):
    def __init__ ( self, children ):
        self.children = children

def flatten_inlineJS ( o ):
    return u'\n<script type="text/javascript">\n//<![CDATA[%s\n//]]></script>\n' % o.children
register_flattener ( inlineJS, flatten_inlineJS )


# convenience tags

def flatten_checkbox ( o ):
    if o.attrs.get ( 'checked', False ):
        o.attrs [ 'checked' ] = 'checked'
    else:
        try:
            del o.attrs [ 'checked' ]
        except KeyError:
            pass
    return flatten_tag ( o )
checkbox = custom_tag ( 'input', 'checkbox', flatten_checkbox, attrs = { 'type': 'checkbox' } )

def flatten_option ( o ):
    if o.attrs.get ( 'selected', False ):
        o.attrs [ 'selected' ] = 'selected'
    else:
        try:
            del o.attrs [ 'selected' ]
        except KeyError:
            pass
    return flatten_tag ( o )
option = custom_tag ( 'option', flattener = flatten_option )

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
    checkbox = checkbox,
    option = option,
    inlineJS = inlineJS,
    lorem_ipsum = lorem_ipsum,
) )

# TAGS = Namespace ( )
# for t in tags:
#    TAGS [ t.upper ( ) ] = tags [ t ]

    