import os
from breve import Template
from breve.tags import html
from urllib import splitquery

class BreveTemplatePlugin ( object ):
    """
    Breve Template Plugin for Buffet-compatible frameworks
    Tested with TurboGears and Pylons
    """
    extension = "b"
    tag_defs = { 'html' : html }
    
    def __init__ ( self, extra_vars_func = None, options = None ):
        self.get_extra_vars = extra_vars_func
        self.options = options or { }
        self.breve_opts = { }
        
    def get_config ( self, vars ):
        '''
        Different frameworks provide needed config info at different times
        and in different ways (notably TurboGears and Pylons), so I've wrapped
        up this messy code here.  It's sad and inefficient that we can't count
        on the config being passed at instantiation.  This should be fixed by
        having Buffet specify how this should be done and having the frameworks
        follow suit.
        
        Breve now allows a url-style syntax in the template name to bypass the
        brokenness in the various frameworks, e.g.:
            index?format=html&debug=1
        '''
        breve_opts = {
            'root': '.',
            'namespace': '',
            'debug': False,
            'tidy': False
        }        

        if 'std' in vars and 'config' in vars [ 'std' ]: # turbogears-specific hacks
            cfg = vars [ 'std'] [ 'config' ]
            breve_opts [ 'root' ] = cfg ( 'breve.root', breve_opts [ 'root' ] )
            breve_opts [ 'namespace' ] = cfg ( 'breve.namespace', breve_opts [ 'namespace' ] )
            breve_opts [ 'debug' ] = cfg ( 'breve.debug', breve_opts [ 'debug' ] )
            breve_opts [ 'tidy' ] = cfg ( 'breve.tidy', breve_opts [ 'tidy' ] )

        else: # pylons-specific
            for k, v in self.options.iteritems ( ):
                if k.startswith ( 'breve.' ):
                    breve_opts [ k [ 6: ] ] = v

        return breve_opts
        
    def load_template ( self, template_name ):
        """
        template_name == dotted.path.to.template (without .ext)
        @@ 1.1: Let's dump the dotted notation. It was a bad idea, the engine that
        inspired it (Kid) is probably dead, and it was always meaningless
        to everyone else anyway.  Also, let's support an extension as a synonym
        for "format", i.e. /blog/feed.rss would be the same as /blog/feed?format=rss
        """

        template, args = splitquery ( template_name )
        if args:
            args = dict ( [ a.split ( '=' )
                            for a in args.split ( '&' ) ] )
        else:
            args = { }
        parts = template.split ( '.' )
        template_filename = parts.pop ( )
        template_path = ''
        if parts:
            template_path = os.path.join ( *parts )
        return template_path, template_filename, args

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
            
        self.breve_opts.update ( self.get_config ( vars ) )
        template_path, template_filename, args = self.load_template ( template )
        # self.breve_opts.update ( args )

        template_root = self.breve_opts [ 'root' ]
        format = args.get ( 'format', format )

        if template_root and template_path.startswith ( template_root ):
            # this feels mildly brittle
            template_path = template_path [ len ( template_root ) + 1: ]

        if format not in self.tag_defs:
            # this seems weak (concerns about path). Should perhaps
            # find a better way, but getting only a string for format
            # makes it difficult to do too much
            self.tag_defs [ format ] = __import__ ( format, { }, { } )

        self.breve_opts [ 'doctype' ] = self.breve_opts.get ( 'doctype', self.tag_defs [ format ].doctype )
        template_obj = Template ( tags = self.tag_defs [ format ].tags,
                                  xmlns = self.tag_defs [ format ].xmlns,
                                  **self.breve_opts )

        if fragment:
            return template_obj.render_partial ( os.path.join ( template_path, template_filename ),
                                                 vars = vars, **self.breve_opts )
        
        return template_obj.render ( os.path.join ( template_path, template_filename ),
                                     vars = vars, **self.breve_opts )

