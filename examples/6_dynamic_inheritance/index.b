html [
    head [
        title [ 'Dynamic Inheritance' ]
    ],

    body [
        h1 [ 'Dynamic Inheritance' ],
        p [ '''
            This example creates the slot name based on the value of 
            a variable passed into the template.  The unused override
            directive is simply discarded.
            ''' ],

        slot ( 'logged-%s' % [ 'out', 'in' ][ bool ( username ) ] )
    ]
]
