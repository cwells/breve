html [
    head [
        title [ 'Test All Breve Features' ],
        script ( type = 'text/javascript', src = '/js/phony.js' ),
        inlineJS ( '''
            function foo ( ) {
                alert ( 'hello, inlineJS!' );
            }
        ''' )
    ],

    body [
        h1 [ 'Testing it all together...' ],
        slot ( 'include-tests' ),
        # slot ( 'inheritance-tests' ),
    ]
]
