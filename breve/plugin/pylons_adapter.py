'''
Simple adapter for Pylons 0.9.7 and greater.  
Earlier versions of Pylons should use the Buffet adapter.
'''

from pylons.templating import pylons_globals
from breve import Template
from breve.tags.html import tags

def render ( template_name, tmpl_vars = None, loader = None, fragment = False ):
    if tmpl_vars is None:
        tmpl_vars = { }

    g = pylons_globals ( )
    tmpl_vars.update ( g )

    try:
        opts = g [ 'app_globals' ].breve_opts
    except AttributeError:
        opts = { }

    t = Template ( tags, **opts )
    return t.render ( template_name, vars = tmpl_vars, loader = loader, fragment = fragment )
