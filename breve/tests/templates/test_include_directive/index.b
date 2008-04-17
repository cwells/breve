html [
    head [ title [ 'Simple Includes' ] ],
    body [
        h1 [ 'Simple Includes' ],
        include ( 'include' ),

	h1 [ 'Includes with variables' ],
        [ include ( 'include-var', vars = dict ( _v = _v ) ) 
          for _v in range ( 3 ) ],

        h1 [ 'Includes can be nested' ],
        include ( 'include-nested' )
    ]
]
