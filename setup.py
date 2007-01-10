from setuptools import setup, find_packages

setup (
    name = 'Breve',
    version = '1.0.14',
    description = '''S-expression based template engine (similar to Nevow Stan)''',
    author = 'Cliff Wells',
    author_email = 'cliff@develix.com',
    url = 'http://www.develix.com/software/Breve',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Buffet',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
        
    install_requires = [ ],
    scripts = [ ],
    packages = find_packages ( ),
    zip_safe = True,
    entry_points = '''
        [python.templating.engines]
        breve = breve.plugin.buffet:BreveTemplatePlugin
    '''
)
    
