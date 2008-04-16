macro ( 'mymacro', lambda url, label: 
    li [
        a ( href = url ) [ label ]
    ]
),

html [ 
    head [ 
        title [ 'Looping constructs' ]
    ],

    body [
        span [ 'List comprehensions' ],
        ul [ [
            li [ a ( href = _u [ 'url' ] ) [ _u [ 'label' ] ] ]
            for _u in urls 
        ] ],

        span [ 'Using a macro to simplify a listcomp' ],
        ul [
            [ mymacro ( **_args ) for _args in urls ]
        ],

        span [ 'Using tag multiplication' ],
        ul [
            li [ a ( href = "$url" ) [ "$label" ] ]
        ] * urls
    ]
]
