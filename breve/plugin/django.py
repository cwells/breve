'''
We're going to support this basic idiom::

 from django.core import template, template_loader
 from django.utils.httpwrappers import HttpResponse
 def foo_view(request):
         t = template_loader.get_template('foo/foo_detail')
         c = template.Context({'foo': 'bar'})
         return HttpResponse(t.render(c))

When using Breve, this will become::

 from breve.plugins.django import template_loader
 from django.utils.httpwrappers import HttpResponse
 def foo_view ( request ):
     t = template_loader.get_template ( 'foo/foo_detail' )
     return HttpResponse ( t.render ( { 'foo': 'bar' } ) )

or the shorter idiom::

 from breve.plugins.django import render_to_response
 def foo_view ( request ):
     return render_to_response ( 'foo/foo_detail', { 'foo': 'bar' } )
'''

from breve import Template
from breve.tags import html
from django.utils.httpwrappers import HttpResponse
try:
    from django.conf.settings import BREVE_ROOT
except ImportError:
    BREVE_ROOT = '.'

class _template_loader ( object ):
    def __init__ ( self, root, breve_opts = None ):
        self.breve_opts = breve_opts or { }
        self.template_root = root

    def __call__ ( self, template ):
        self.template_filename = template
        return Template ( tags = html.tags, root = self.template_root )

    def render ( self, vars = None ):
        self.vars = vars or { }
        return template_obj.render ( template = self.template_filename,
                                     vars = vars, **self.breve_opts )

template_loader = _template_loader ( root = BREVE_ROOT )

def render_to_response ( template, vars = None ):
    t = template_loader.get_template ( template )
    return HttpResponse ( t.render ( vars ) )

def render_to_string ( template, vars = None ):
    t = template_loader.get_template ( template )
    return t.render ( vars )
