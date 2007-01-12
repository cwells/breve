# sitemap.py - example custom tag definition file

from breve.tags import Proto

xmlns = "http://www.google.com/schemas/sitemap/0.84/sitemap.xsd"
doctype = ""
tag_names = [ "changefreq", "lastmod", "loc", "priority", "url", "urlset" ]
tags = { }
for t in tag_names:
    tags [ t ] = Proto ( t )

        
