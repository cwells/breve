macro ( 'mymacro', lambda _args: 
    li [
        a ( href = _args.url ) [ _args.label ]
    ]
),

html [ 
    head [ 
        title [ 'Looping constructs and macros' ]
    ],

    body [
        span [ 'Using a macro to simplify a listcomp' ],
        ul [
            [ mymacro ( _args ) for _args in urls ]
        ],

        span [ 'Using tag multiplication' ],
        ul [
            li [ a ( href = "$url" ) [ "$label" ] ]
        ] * urls
    ]
]
