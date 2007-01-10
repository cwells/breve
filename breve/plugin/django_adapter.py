from breve import Template
from breve.tags import html
from django.http import HttpResponse

from django.conf import settings 
BREVE_ROOT = settings.BREVE_ROOT

class _loader ( object ):
    def __init__ ( self, root, breve_opts = None ):
        self.breve_opts = breve_opts or { }
        self.template_root = root

    def get_template ( self, template ):
        self.template_filename = template
        self.template_obj = Template ( tags = html.tags, root = self.template_root )
        return self
    
    def render ( self, vars = None ):
        self.vars = vars or { }
        return self.template_obj.render ( template = self.template_filename,
                                          vars = vars, **self.breve_opts )

loader = _loader ( root = BREVE_ROOT )

def render_to_response ( template, vars = None ):
    t = loader.get_template ( template )
    return HttpResponse ( t.render ( vars ) )

def render_to_string ( template, vars = None ):
    t = loader.get_template ( template )
    return t.render ( vars )
