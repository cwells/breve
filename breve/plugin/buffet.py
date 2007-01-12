import os
from breve import Template
from breve.tags import html

class BreveTemplatePlugin ( object ):
    """
    Breve Template Plugin for Buffet-compatible frameworks
    Tested with TurboGears and Pylons
    """
    extension = "b"

    def __init__ ( self, extra_vars_func = None, options = None ):
        self.get_extra_vars = extra_vars_func
        self.options = options or { }
        self.breve_opts = None
        
    def get_config ( self, vars ):
        '''
        Different frameworks provide needed config info at different times
        and in different ways (notably TurboGears and Pylons), so I've wrapped
        up this messy code here.  It's sad and inefficient that we can't count
        on the config being passed at instantiation.  This should be fixed by
        having Buffet specify how this should be done and having the frameworks
        follow suit.
        '''
        breve_opts = {
            'root': '.',
            'namespace': '',
            'debug': False
        }        

        if 'std' in vars: # turbogears-specific
            cfg = vars [ 'std'] [ 'config' ]
            breve_opts [ 'root' ] = cfg ( 'breve.root', breve_opts [ 'root' ] )
            breve_opts [ 'namespace' ] = cfg ( 'breve.namespace', breve_opts [ 'namespace' ] )
            breve_opts [ 'debug' ] = cfg ( 'breve.debug', breve_opts [ 'debug' ] )
        else: # pylons-specific
            for k, v in self.options.iteritems ( ):
                if k.startswith ( 'breve.' ):
                    breve_opts [ k [ 6: ] ] = v

        parts = breve_opts [ 'root' ].split ( '.' )
        breve_opts [ 'root' ] = os.path.join ( *parts )        

        return breve_opts
        
    def load_template ( self, template_name ):
        """
        template_name == dotted.path.to.template (without .ext)
        """
        parts = template_name.split ( '.' )
        template_filename = parts.pop ( )
        template_path = ''
        if parts:
            template_path = os.path.join ( *parts )
        return template_path, template_filename

    def render ( self, info, format = "html", fragment = False, template = None ):
        """
        info == dict of variables to stick into the template namespace
        format == output format if applicable
        fragment == special rules about rendering part of a page
        template == dotted.path.to.template (without .ext)
        """
        vars = info

        # check to see if we were passed a function get extra vars
        if callable ( self.get_extra_vars ):
            vars.update ( self.get_extra_vars ( ) )
        
        if self.breve_opts is None:
            self.breve_opts = self.get_config ( vars )
        
        template_root = self.breve_opts [ 'root' ]
        template_path, template_filename = self.load_template ( template )
        if template_root and template_path.startswith ( template_root ):
            # this feels mildly brittle
            template_path = template_path [ len ( template_root ) + 1: ]

        # pylons-specific crap - this is broken and needs to be fixed in pylons
        format = vars.get ( 'format', format )

        if format == 'html':
            tag_defs = html
        else:
            # this seems weak (concerns about path). Should perhaps
            # find a better way, but getting only a string for format
            # makes it difficult to do too much
            tag_defs = __import__ ( format, { }, { } )

        self.breve_opts [ 'doctype' ] = self.breve_opts.get ( 'doctype', tag_defs.doctype )
        template_obj = Template ( tags = tag_defs.tags,
                                  xmlns = tag_defs.xmlns,
                                  **self.breve_opts )

        if fragment:
            return template_obj.render_partial ( os.path.join ( template_path, template_filename ),
                                                 vars = vars, **self.breve_opts )
        
        return template_obj.render ( os.path.join ( template_path, template_filename ),
                                     vars = vars, **self.breve_opts )

