import sys, os
import difflib
from pprint import pprint

def diff ( actual, expected ):
    print "\n=" * 80
    print actual
    print "-" * 80
    d = difflib.Differ ( )
    result = d.compare ( actual.splitlines ( ), expected.splitlines ( ) ) 
    for l in result:
        if not l.startswith ( ' ' ):
            print l
    print "=\n" * 80

def log_output ( actual, expected ):
    ''' not used '''
    test_name = callers_name ( )
    file ( 'tmp/%s-actual.html' % test_name, 'w' ).write ( actual )
    file ( 'tmp/%s-expected.html' % test_name, 'w' ).write ( expected )    

def my_name ( ):
    return sys._getframe ( 1 ).f_code.co_name

def callers_name ( ):
    return sys._getframe ( 2 ).f_code.co_name

def caller ( ):
    return sys._getframe ( 2 )

def test_root ( ):
    return os.path.abspath ( os.path.dirname ( __file__ ) )

def template_root ( ):
    return os.path.join ( test_root ( ), 'templates', callers_name ( ) )

def expected_output ( ):
    return file ( os.path.join ( test_root ( ), 'output', '%s.html' % callers_name ( ) ) ).read ( ).strip ( )
