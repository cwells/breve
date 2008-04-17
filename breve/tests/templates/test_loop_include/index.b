html [
    head [ title [ v.title ] ],
    body [
        [ include ( 'include', vars = { 'count': _v } ) 
          for _v in range ( 3 ) ]
    ]
] 
