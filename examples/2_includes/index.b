html [
    head [ title [ 'Simple Includes' ] ],
    body [
        h1 [ 'Simple Includes' ],

        ul [ [
            li [ include ( 'include' ) ] 
            for _i in range ( 3 )
        ] ]
    ]
]
