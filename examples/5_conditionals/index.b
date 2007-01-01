html [
    head [
        title [ 'Conditionals' ]
    ],

    body [
        h1 [ 'Conditionals' ],

        switch ( username ) [
            case ( None ) [ span [ 'Not logged in' ] ],
            default [ 
                div [ 
                    span [ 'Welcome, ', username ],
                    ul [
                        [ li [ a ( href = l ) [ s ] ] 
                          for s, l in [ ( 'Menu 1', '/page1' ), 
                                        ( 'Menu 2', '/page2' ),
                                        ( 'Logout', '/logout' ) ] 
                        ]
                    ] 
                ] 
            ]
        ],

        br,
    ]
]