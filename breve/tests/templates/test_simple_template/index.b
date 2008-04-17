html [
    head [
        title [ v.title ],
        script ( type = 'text/javascript', src = '/js/phony.js' ),
        inlineJS ( '''
            function foo ( ) {
                alert ( 'hello, inlineJS!' );
            }
        ''' )
    ],

    body [
        h1 [ 'This is the basics.' ],

	comment ( '''
            This is an XML comment. It shows up in the final output. 
            Use Python-style comments if you don't want them to show
            up in the output.
        ''' ),

        div ( style = 'width: 400px;' ) [
            p ( style = 'font-weight: bold;' ) [ 
                'this list was generated using a Python listcomp' 
            ], 
            
            ul [ # generate an unordered list using a listcomp
                [ li [ 'item %d' % x ] for x in range ( 4 ) ]
            ],

            # print a variable
            p [ v.message ],
            
            # entities (like &amp;)
            p [ 'Coffee', E.nbsp, E.amp, E.nbsp, 'cream', E.copy, ' 2007, Cliff Wells' ]
        ]
    ]
]
