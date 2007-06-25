preamble (
    encoding = 'ascii'
),


html [
    head [
        title [ 'Unicode' ]
    ],

    body [
        'Brev\xc3\xa9 converts plain strings', br,
        u'Brev\xe9 handles unicode strings'
    ]
] 
