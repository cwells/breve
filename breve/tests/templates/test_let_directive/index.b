let ( x = 1, y = 2 ),

html [
    head [ title [ v.title ] ],
    body [ 
        div [ v.message ],
        span [ x ], span [ y ]
    ]
]