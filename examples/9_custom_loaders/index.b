html [
    head [
        title [ 'Custom loader' ]
    ],

    body [
        include ( 'frag' ),
        include ( 'frag1', loader = loaders.pathloader ),
        include ( 'frag2', loader = loaders.pathloader ),
	include ( 'a string', loader = loaders.stringloader )
    ]
]