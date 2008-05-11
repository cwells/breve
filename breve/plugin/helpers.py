from breve import Template
from breve.tags.html import tags

def render_decorator ( template, **template_kw ):
    '''
    decorator for turning a dict and a breve 
    template into flattened output
    '''
    def _template ( f ):
        def _render ( *args, **kw ):
            t = Template ( tags, **template_kw )
            values = f ( *args, **kw )
            return t.render ( template, values )
        return _render
    return _template

def render_middleware ( environ, start_response ):
    ''' soon! '''
    return



