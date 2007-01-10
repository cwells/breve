import os
from breve import Template
from breve.tags import html

class BreveTemplatePlugin ( object ):
    """
    Breve Template Plugin for Pylons
    """
    extension = "b"

    def __init__ ( self, extra_vars_func = None, options = None ):
        self.get_extra_vars = extra_vars_func
        self.options = options or { }
        
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
            'doctype': Template.doctype,
            'root': '.',
            'namespace': Template.namespace
        }        

        if 'std' in vars: # turbogears-specific
            breve_opts ['root' ] = vars [ 'std'] [ 'config' ] ( 'breve.root', '.' )
            breve_opts ['doctype' ] = vars [ 'std'] [ 'config' ] ( 'breve.doctype', Template.doctype )
            breve_opts ['namespace' ] = vars [ 'std'] [ 'config' ] ( 'breve.namespace', Template.namespace )
        else: # pylons-specific
            for k, v in self.options.iteritems ( ):
                if k.startswith ( 'breve.' ):
                    breve_opts [ k [ len ( 'breve.' ): ] ] = v

        parts = breve_opts [ 'root' ].split ( '.' )
        breve_opts [ 'root' ] = os.path.join ( *parts )        
        
        return breve_opts
        
    def load_template ( self, template_name ):
        """
        template_name == dotted.path.to.template (without .ext)
        """
        parts = template_name.split ( '.' )
        template_filename = parts.pop ( )
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

        breve_opts = self.get_config ( vars )
        template_root = breve_opts [ 'root' ]
        
        template_path, template_filename = self.load_template ( template )
        if template_root and template_path.startswith ( template_root ):
            # this feels a bit hackish and brittle
            template_path = template_path [ len ( template_root ) + 1: ]

        template_obj = Template ( tags = html.tags, root = template_root )
        
        return template_obj.render ( template = os.path.join ( template_path, template_filename ),
                                     vars = vars, **breve_opts )
    
