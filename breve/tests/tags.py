# -*- coding: utf-8 -*-
 
import doctest, unittest

from breve.tags.html import tags as T
from breve.tags.entities import entities as E
from breve.tags import macro, xml, test
from breve.flatten import flatten 
from breve.util import Namespace
from breve.tests.lib import my_name


class SerializationTestCase ( unittest.TestCase ):

    def test_tag_serialization ( self ):
        template = T.html [
            T.head [ T.title [ my_name ( ) ] ],
            T.body [ T.div [ 'okay' ] ]
        ]
        output = flatten ( template )
        self.assertEqual ( 
            output,
            u'<html><head><title>test_tag_serialization</title></head><body><div>okay</div></body></html>'
        )

    def test_unicode ( self ):
        template = T.html [
            T.head [ T.title [ my_name ( ) ] ],
            T.body [
                'Brev\xc3\xa9 converts plain strings', T.br,
                u'Brev\xe9 handles unicode strings', T.br,
                T.div [ "äåå? ▸ ", T.em [ "я не понимаю" ], "▸ 3 km²" ]
            ]
        ] 
        output = flatten ( template )
        self.assertEqual ( 
            output,
            u'<html><head><title>test_unicode</title></head><body>Brevé converts plain strings<br />Brevé handles unicode strings<br /><div>äåå? ▸ <em>я не понимаю</em>▸ 3 km²</div></body></html>'
        )

    def test_test ( self ):
        template = T.html [
            T.head [ T.title [ my_name ( ) ] ],
            T.body [
                test ( 1 == 1 ) and (
                    T.span [ 'This is displayed' ]
                ),
                test ( 1 == 0 ) and (
                    T.span [ 'This is not displayed' ]
                )
            ]
        ]
        output = flatten ( template )
        self.assertEqual (
            output,
            u'<html><head><title>test_test</title></head><body><span>This is displayed</span></body></html>'
        )

    def test_escaping ( self ):
        template = T.html [
            T.head [ T.title [ my_name ( ) ] ],
            T.body [
                T.div ( style = 'width: 400px;<should be &escaped&>' ) [
                    T.p ( class_ = 'foo' ) [ '&&&' ],
                    T.p [ 'Coffee', E.nbsp, E.amp, E.nbsp, 'cream' ],
                    xml ( '''<div>this should be <u>unescaped</u> &amp; unaltered.</div>''' )
                ]
            ]
        ]
        output = flatten ( template )
        self.assertEqual (
            output,
            u'<html><head><title>test_escaping</title></head><body><div style="width: 400px;&lt;should be &amp;escaped&amp;&gt;"><p class="foo">&amp;&amp;&amp;</p><p>Coffee&#160;&#38;&#160;cream</p><div>this should be <u>unescaped</u> &amp; unaltered.</div></div></body></html>'
        )

    def test_tag_multiplication ( self ):
        url_data = [
            dict ( url = 'http://www.google.com', label = 'Google' ),
            dict ( url = 'http://www.yahoo.com', label = 'Yahoo!' ),
            dict ( url = 'http://www.amazon.com', label = 'Amazon' )
        ]

        template = T.html [
            T.head [ T.title [ my_name ( ) ] ],
            T.body [
                T.ul [
                    T.li [ T.a ( href="$url" ) [ "$label" ] ] * url_data
                ]
            ]
        ]
        output = flatten ( template )
        self.assertEqual ( 
            output,
            u'<html><head><title>test_tag_multiplication</title></head><body><ul><li><a href="http://www.google.com">Google</a></li><li><a href="http://www.yahoo.com">Yahoo!</a></li><li><a href="http://www.amazon.com">Amazon</a></li></ul></body></html>'
        )

    def test_tag_multiplication_with_macro ( self ):
        url_data = [
            { 'url': 'http://www.google.com', 'label': 'Google', 'class': 'link' },
            { 'url': 'http://www.yahoo.com', 'label': 'Yahoo!', 'class': 'link' },
            { 'url': 'http://www.amazon.com', 'label': 'Amazon', 'class': 'link' }
        ]

        template = ( 
            macro ( 'test_macro', lambda url: 
                T.a ( href = url ) [ "$label" ]
            ),
            T.html [
                T.head [ T.title [ my_name ( ) ] ],
                T.body [
                    T.ul [ 
                        T.li ( class_="$class") [ test_macro ( "$url" ) ] * url_data 
                    ]
                ]
            ]
        )
        output = flatten ( template )
        self.assertEqual ( 
            output,
            u'<html><head><title>test_tag_multiplication_with_macro</title></head><body><ul><li class="link"><a href="http://www.google.com">Google</a></li><li class="link"><a href="http://www.yahoo.com">Yahoo!</a></li><li class="link"><a href="http://www.amazon.com">Amazon</a></li></ul></body></html>'
        )

class DOMTestCase ( unittest.TestCase ):

    def test_dom_traversal ( self ):
        template = T.html [
            T.head [ T.title [ my_name ( ) ] ],
            T.body [ T.div [ 'okay' ] ]
        ]

        traversal = [ ]
        def callback ( item, is_tag ):
            if is_tag:
                traversal.append ( item.name )
            else:
                traversal.append ( item )

        template.walk ( callback )
        output = ''.join ( traversal )
        self.assertEqual ( 
            output,
            u'htmlheadtitle%sbodydivokay' % my_name ( ),
        )
        

class CustomTagsTestCase ( unittest.TestCase ):

    def test_custom_tags ( self ):
        from breve.tests.sitemap import tags, xmlns
        T = Namespace ( tags )

        # test data
        loc = 'http://www.example.com/',
        lastmod = '2008-01-01',
        changefreq = 'monthly',
        priority = 0.8 

        template = T.urlset ( xmlns = xmlns ) [
            T.url [
                T.loc [ loc ],
                T.lastmod [ lastmod ],
                T.changefreq [ changefreq ],
                T.priority [ priority ]
            ]
        ]
        output = flatten ( template )

        self.assertEqual ( 
            output,
            u'<urlset xmlns="http://www.google.com/schemas/sitemap/0.84/sitemap.xsd"><url><loc>http://www.example.com/</loc><lastmod>2008-01-01</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url></urlset>'
        )


def suite ( ):
    suite = unittest.TestSuite ( )

    suite.addTest ( unittest.makeSuite ( SerializationTestCase, 'test' ) )
    suite.addTest ( unittest.makeSuite ( DOMTestCase, 'test' ) )
    suite.addTest ( unittest.makeSuite ( CustomTagsTestCase, 'test' ) )

    return suite

if __name__ == '__main__':
    unittest.main ( defaultTest = 'suite' )
