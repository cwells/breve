from breve.tags import Proto
from breve.flatten import flatten

class TestProto:
    p = Proto ( 'test' )
    
    def test_call ( self ):
        assert flatten ( self.p ( ) ) == '<test></test>' 

    def test_getattr ( self, attr = 'hello' ):
        assert flatten ( self.p [ attr ] ) == '<test>%s</test>' % attr

    def test_empty ( self ):
        assert flatten ( self.p ) == '<test />'

    def test_not_empty ( self ):
        assert flatten ( self.p [ 'hello' ] ) == '<test>hello</test>'

    def test_distinct ( self ):
        p = Proto ( 'test' )

        assert p is not self.p
        assert p ( ) is not self.p ( )
        assert p [ 'test' ] is not self.p [ 'test' ]

        assert self.p is self.p
        assert self.p ( ) is not self.p ( ) 
        assert self.p [ 'test' ] is not self.p [ 'test' ]

from breve.tags import html

class TestHtml:
    def test_empty_tags ( self ):
        for t in html.empty_tag_names:
            assert flatten ( html.tags [ t ] ) == '<%s />' % t
        for t in html.tag_names:
            assert flatten ( html.tags [ t ] ) == '<%s></%s>' % ( t, t )

    def test_cdata ( self ):
        assert flatten ( html.cdata ( 'test' ) ) == '<![CDATA[test]]>' 

    def test_empty_tags ( self ):
        for t in html.empty_tag_names:
            assert flatten ( html.tags [ t ] ) == '<%s />' % t
        for t in html.tag_names:
            assert flatten ( html.tags [ t ] ) == '<%s></%s>' % ( t, t )

class TestFlatteners:
    def test_unique_proto_str ( self ):
        ''' make sure str and Proto flatteners are different '''
        assert 
