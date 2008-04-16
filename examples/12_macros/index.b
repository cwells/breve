evaluate ( 'macros' ),

html [
    head [ 
        title [ 'Macros' ]
    ],

    body [
        div [ list_macro ( urls ) ],
        include_macro ( 'include' ),
        include ( 'include2' )
    ]
]
