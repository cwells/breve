push ( temp = 'this is string 1' ),
push ( temp = 'this is string 2' ),

html [
    head [ title [ v.title ] ],
    body [
        div [ 
            v.message, 
            ' ', pop ( 'temp' ), 
            ' ', pop ( 'temp' ) 
       ]
    ]
]
