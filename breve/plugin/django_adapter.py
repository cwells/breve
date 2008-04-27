import os
from breve import Template
from breve.tags import html
from django.http import HttpResponse
from django.template import Context, TemplateDoesNotExist
from django.utils.translation import gettext_lazy as _

from django.conf import settings 
BREVE_ROOT = settings.BREVE_ROOT

try:
    BREVE_OPTS = settings.BREVE_OPTS
except AttributeError:
    BREVE_OPTS = {}

def flatten_string ( obj ):
    return unicode ( obj ).encode ( settings.DEFAULT_CHARSET )

class _loader ( object ):
    def __init__ ( self, root, breve_opts = None ):
        self.breve_opts = breve_opts or { }
        self.root = root

    def get_template ( self, template ):
        return TemplateAdapter ( [ template ], root = self.root,
                                 breve_opts = self.breve_opts )

    def select_template ( self, template_list ):
        return TemplateAdapter ( template_list, root = self.root,
                                 breve_opts = self.breve_opts )

class TemplateAdapter ( object ):
    """
    Takes the root and a list of filenames of a breve templates in the
    constructor and returns an object that behaves as a
    django.templates.Template in the sense that the render (vars)
    method returns the rendered string. It tries the filenames in
    order and the first one for which a corresponding file exists is
    used. If none of the filenames matches, render raises
    django.template.TemplateDoesNotExist.
    """
    def __init__ ( self, names, root = BREVE_ROOT, breve_opts = { } ):
        self.template = Template ( tags = html.tags, root = root, **breve_opts )
        self.names = names
        self.breve_opts = breve_opts

    def render ( self, vars = None ):
        import os
        if vars == None:
            vars = { }
        elif isinstance ( vars, Context ):
            result = { }
            for d in [ d for d in vars ].__reversed__ ( ):
                result.update ( d )
            vars = result
        for name in self.names:
            try:                
                return flatten_string (
                    self.template.render (
                        template = name, vars = vars,
                        **self.breve_opts )
                )
            except OSError:
                pass
        if len ( self.names ) == 0:
            raise TemplateDoesNotExist ( _( "No templates given." ) )
        elif len ( self.names ) == 1:
            raise TemplateDoesNotExist (
                _( "The template %s does not exist." ) %
                os.path.join ( self.template.root, self.names [ 0 ] ) )
        else:
            raise TemplateDoesNotExist ( _( "None of the following templates exists: %s." ) %
                                         ", ".join ( [ os.path.join (self.template.root, name )
                                                       for name in self.names ] ) )


loader = _loader ( root = BREVE_ROOT, breve_opts = BREVE_OPTS )

def render_to_response(template, vars=None, **kwargs):
    t = loader.get_template(template)
    return HttpResponse(t.render(vars), **kwargs)

def render_to_string ( template, vars = None ):
    t = loader.get_template ( template )
    return flatten_string ( t.render ( vars ) )
