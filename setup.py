import sys; sys.path.insert ( 0, '.' )
import breve

from setuptools import setup, find_packages

setup (
    name = 'Breve',
    version = breve.__version__,
    description = '''An s-expression style template engine.''',
    long_description = '''
        Breve is a Python template engine that is designed to be clean and elegant with
        minimal syntax.  Unlike most Python template engines, Breve is implemented as an
        `internal DSL`_ rather than a parser.

        Breve was heavily inspired by `Nevow Stan`_ and is, in fact, the successor to
        TurboStan (defunct), my earlier attempt to bring a Stan-like engine to TurboGears.

        Breve supports the Buffet_ template engine API which means it works
        automatically with several frameworks, including Pylons_, CherryPy_ and
        TurboGears_.  Breve also supports Django_.

        .. _Nevow Stan: http://divmod.org/trac/wiki/DivmodNevow
        .. _Buffet: http://projects.dowski.com/projects/buffet
        .. _TurboGears: http://www.turbogears.org
        .. _Pylons: http://www.pylonshq.com
        .. _CherryPy: http://www.cherrypy.org
        .. _Django: http://www.djangoproject.com
        .. _`internal DSL`: http://martinfowler.com/bliki/DomainSpecificLanguage.html
    ''',
    author = 'Cliff Wells',
    author_email = 'cliff@develix.com',
    url = 'http://breve.twisty-industries.com/',
    download_url = 'http://breve.twisty-industries.com/downloads/',
    classifiers = [
        'Development Status :: 5 - Production',
        'Environment :: Web Environment',
        'Environment :: Web Environment :: Buffet',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords = [ 'python.templating.engines' ],        
    install_requires = [ ],
    scripts = [ 'tools/soup2breve', 'tools/html2breve', 'tools/xsd2breve', 'tools/breve_server/breve_server' ],
    packages = find_packages ( ),
    zip_safe = True,
    entry_points = '''
        [python.templating.engines]
        breve = breve.plugin.buffet:BreveTemplatePlugin
    ''',
    test_suite = 'breve.tests.testsuite'
)
    
