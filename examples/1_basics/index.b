html [
    head [
        title [ 'Test 1' ],
        script ( type = 'text/javascript', src = '/js/phony.js' ),
        inlineJS ( '''
            function foo ( ) {
                alert ( 'hello, inlineJS!' );
            }
        ''' )
    ],

    body [
        h1 [ 'This is the basics.' ],

        div ( style = 'width: 400px;' ) [
            p ( style = 'font-weight: bold;' ) [ 
                'this list was generated using a Python listcomp' 
            ], 
            
            ul [ # generate an unordered list using a listcomp
                [ li [ 'item %d' % x ] for x in range ( 4 ) ]
            ],

            # print a variable
            p [ message ],
            
            # entities (like &amp;)
            p [ 'Coffee', E.nbsp, E.amp, E.nbsp, 'cream' ]
        ]
    ]
]
