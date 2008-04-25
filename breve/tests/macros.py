# -*- coding: utf-8 -*-

import sys, os
import doctest, unittest

if __name__ == '__main__':
    # force import from source directory rather than site-packages
    sys.path.insert ( 0, os.path.abspath ( '../..' ) )
    import breve

from breve.tags.html import tags as T
from breve.tags.entities import entities as E
from breve.tags import macro, assign, xml, test, let
from breve.flatten import flatten 
from breve.util import Namespace
from breve.tests.lib import my_name


class MacrosTestCase ( unittest.TestCase ):

    def test_autotable_macro ( self ):
        '''test autotable macro'''

        data = [
            [ 'One', 'Two', 'Three', 'Four' ],
            range ( 0, 4 ),
            range ( 4, 8 ),
            range ( 8, 12 )
        ]

        template = (
            macro ( 'AutoTable', lambda data, header=False: (
                assign ( 'alts', [ 'even', 'odd' ] ),
                data and ( 
                    T.table ( class_='autotable' ) [
                        header and ( 
                            T.thead [ [ T.th [ _col ] for _col in data [ 0 ] ] ]
                        ),
                        T.tbody [
                            [ T.tr ( class_='row-%s' % alts [ _rx % 2 ] ) [ 
                                [ T.td ( class_='col-%s' % alts [ _cx % 2 ] ) [ _col ] 
                                  for _cx, _col in enumerate ( _row ) ]
                            ] for _rx, _row in enumerate ( data [ int ( header ): ] ) ]
                        ]
                    ]
                ) or ''
            ) ),

            T.html [
                T.head [ T.title [ my_name ( ) ] ],
                T.body [
                    AutoTable ( data, header=True )
                ]
            ]
        )
        output = flatten ( template )
        self.assertEqual (
            output,
            ( u'<html><head><title>test_autotable_macro</title></head>'
              u'<body><table class="autotable"><thead><th>One</th><th>Two</th><th>Three</th><th>Four</th></thead>'
              u'<tbody><tr class="row-even"><td class="col-even">0</td><td class="col-odd">1</td>'
              u'<td class="col-even">2</td><td class="col-odd">3</td></tr>'
              u'<tr class="row-odd"><td class="col-even">4</td><td class="col-odd">5</td><td class="col-even">6</td>'
              u'<td class="col-odd">7</td></tr>'
              u'<tr class="row-even"><td class="col-even">8</td><td class="col-odd">9</td>'
              u'<td class="col-even">10</td><td class="col-odd">11</td></tr></tbody>'
              u'</table></body></html>' )
        )

    def test_autolist_macro ( self ):
        '''test autolist macro'''
        
        data = [ "Item %s" % _i for _i in range ( 1,9 ) ]

        template = (
            macro ( 'AutoList', lambda data:
                data and ( 
                    T.ul ( class_='autolist' ) [
                        [ T.li [ _i ] for _i in data ]
                    ]
                ) or ''
            ),
            T.html [
                T.head [ T.title [ my_name ( ) ] ],
                T.body [ AutoList ( data ) ]
            ]
        )
        output = flatten ( template )
        self.assertEqual ( 
            output,
            ( u'<html><head><title>test_autolist_macro</title></head>'
              u'<body><ul class="autolist"><li>Item 1</li><li>Item 2</li>'
              u'<li>Item 3</li><li>Item 4</li><li>Item 5</li><li>Item 6</li>'
              u'<li>Item 7</li><li>Item 8</li></ul></body></html>' )
        )
        
    def test_autolist_macro ( self ):
        '''test autolist macro'''
        
        sublist1 = [ "List 1:%s" % _i for _i in range ( 3 ) ]
        sublist2 = [ "List 2:%s" % _i for _i in range ( 3, 6 ) ]
        sublist3 = [ "List 3:%s" % _i for _i in range ( 6, 9 ) ]
        sublist3.append ( sublist2 )

        data = [ 
            'Item A', 'Item B', 'Item C',
            sublist1, 
            'Item D', 'Item E', 'Item F',
            sublist3,
        ]
        template = (
            macro ( 'AutoList', lambda data, level=0:
                data and (
                    T.ul ( class_='autolist level-%s' % level ) [
                        [ T.li [
                              [ lambda _i, _j: _i, AutoList ]
                              [ isinstance ( _i, list ) ]( _i, level + 1 )
                          ]
                        for _i in data ]
                    ]
                ) or ''
            ),

            T.html [
                T.head [ T.title [ my_name ( ) ] ],
                T.body [ AutoList ( data ) ]
            ]
        )
        output = flatten ( template )
        self.assertEqual (
            output,
            ( u'<html><head><title>test_autolist_macro</title></head>'
              u'<body><ul class="autolist level-0"><li>Item A</li>'
              u'<li>Item B</li><li>Item C</li><li><ul class="autolist level-1">'
              u'<li>List 1:0</li><li>List 1:1</li><li>List 1:2</li></ul></li>'
              u'<li>Item D</li><li>Item E</li><li>Item F</li><li>'
              u'<ul class="autolist level-1"><li>List 3:6</li>'
              u'<li>List 3:7</li><li>List 3:8</li><li><ul class="autolist level-2">'
              u'<li>List 2:3</li><li>List 2:4</li><li>List 2:5</li></ul>'
              u'</li></ul></li></ul></body></html>' )
        )

    def test_toc_macro ( self ):
        '''test table-of-contents macro'''

        template = (
            assign ( 'TOC', [ ] ),
            macro ( 'TableOfContents', lambda matchtags, tag: (
                macro ( 'toc_search', lambda tag, is_tag:
                    tag.name in matchtags and (
                        TOC.append ( T.a ( href='#toc-%s' % tag.children [ 0 ] ) [ tag.children [ 0 ] ] ),
                        tag.attrs.update ( { 'class': 'chapter-%s' % tag.name } ),
                        tag.children.insert ( 0, T.a ( name='toc-%s' % tag.children [ 0 ] ) [ tag.name ] )
                    ) or True
                ),
                tag.walk ( toc_search, True )
            ) ),

            T.html [
                T.head [ T.title [ my_name ( ) ] ],
                T.body [ 
                    T.div ( id='TableOfContents' ) [ 
                        'Table of Contents', 
                        lambda: T.ul [ [ T.li [ _t ] for _t in TOC ] ]
                    ],
                    TableOfContents ( ( 'h1', 'h2', 'h3' ), T.div [
                        T.h1 [ 'Chapter 1' ],
                        T.div [ 'chapter 1 content' ],
                        T.h1 [ 'Chapter 2' ],
                        T.div [ 
                            'chapter 2 content',
                            T.h2 [ 'Chapter 2 subsection' ],
                            T.div [
                                'chapter 2 subsection content' 
                            ]
                        ]
                    ] )
                ]
            ]
        )

        actual = flatten ( template )
        # print actual


def suite ( ):
    suite = unittest.TestSuite ( )

    suite.addTest ( unittest.makeSuite ( MacrosTestCase, 'test' ) )

    return suite

if __name__ == '__main__':
    unittest.main ( defaultTest = 'suite' )
