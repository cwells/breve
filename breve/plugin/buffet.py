import os
from breve import Template
from breve.tags import html

class BreveTemplatePlugin ( object ):
    """
    Breve Template Plugin for Pylons
    """
    extension = "b"

    def __init__ ( self, extra_vars_func = None, options = None ):
        if options is None:
            options = { }
        breve_opts = { 'doctype': Template.doctype, 'root': '.' }
        for k, v in options.iteritems ( ):
            if k.startswith ( 'breve.' ):
                breve_opts [ k [ len ( 'breve.' ): ] ] = v
                
        parts = breve_opts [ 'root' ].split ( '.' )
        breve_opts [ 'root' ] = os.path.join ( *parts )
        
        self.breve_opts = breve_opts
        self.get_extra_vars = extra_vars_func

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

        template_root = self.breve_opts.get ( 'root', '.' )
        template_path, template_filename = self.load_template ( template )
        if template_path.startswith ( template_root ):
            # this feels a bit hackish and brittle
            template_path = template_path [ len ( template_root ) + 1: ]

        template_obj = Template ( tags = html.tags, root = template_root )
        
        return template_obj.render ( template = os.path.join ( template_path, template_filename ),
                                     vars = vars,
                                     doctype = self.breve_opts [ 'doctype' ] )
    
