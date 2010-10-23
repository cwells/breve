Brevé is a Python template engine that is designed to be clean and elegant with minimal syntax. Brevé was heavily inspired by Nevow Stan.

Like Stan (and unlike most Python template engines), Brevé is neither an XML parser nor PSP-style regex engine. Rather, Brevé templates are actual Python expressions. In popular parlance, Brevé is an internal DSL.

Unlike Stan, Brevé doesn't depend on Twisted or Nevow (it's a ground-up rewrite and has no external dependencies outside the Python Standard Library). Also Brevé is a full template engine, supporting concepts not found in Stan such as template inheritance, include files and simple conditionals. Brevé also drops support for a few Stan concepts that aren't strictly needed (e.g. patterns).

Brevé is relatively small, being around 300 lines of code for the engine proper, and around another 700 lines of code for the HTML entity and tag definitions.

Brevé supports the Buffet template engine API which means it works automatically with several frameworks, including Pylons, CherryPy and TurboGears. Brevé can also be used with Django, Tornado, or even standalone outside a framework.

A short example::

 html [
     head [
         title [ 'A Brevé Template' ]
     ],

     body [
         h1 [ 'Briefly, Brevé' ], br,
         div ( style = 'text-align: center;' ) [
             span [ '''
                 As you can see, Brevé maps very
                 directly to the final HTML output.
             ''' ]
         ]
     ]
 ]

