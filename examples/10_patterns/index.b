html [
    head [ 
        title [ 'Patterns' ]
    ],

    body [ 
         p [ '''Render a 3 column x 10 row table using patterns''' ],

         table ( render = sequence ( 'table-seq' ), data = mytable ) [
             invisible ( pattern = 'header', render = sequence ( 'row-seq' ) ) [
                 th ( pattern = 'item' ) [ curval ( 'row-seq' ) ], 
             ],

             tr ( pattern = 'item', render = sequence ( 'row-seq' ), class_ = 'even-row' ) [ 
                 td ( pattern = 'item' ) [ curval ( 'row-seq' ) ]
             ],
             tr ( pattern = 'item', render = sequence ( 'row-seq' ), class_ = 'odd-row' ) [ 
                 td ( pattern = 'item' ) [ curval ( 'row-seq' ) ]
             ],

             tr ( pattern = 'footer', render = sequence ( 'row-seq'), class_ = 'footer' ) [
                 td ( pattern = 'item' ) [ curval ( 'row-seq' ) ]
             ]
         ],

         p [ '''Render a list of dictionaries using patterns''' ],
         table ( render = sequence ( 'userlist' ), data = userlist ) [
             th [ 'firstname' ], th [ 'lastname' ],
             tr ( pattern = 'item', render = mapping ( 'user' ), class_ = 'even-row' ) [
                 td ( pattern = 'firstname' ) [ curval ( 'user' ) ],
                 td ( pattern = 'lastname' ) [ curval ( 'user' ) ],
             ],
             tr ( pattern = 'item', render = mapping ( 'user' ), class_ = 'odd-row' ) [
                 td ( pattern = 'firstname' ) [ curval ( 'user' ) ],
                 td ( pattern = 'lastname' ) [ curval ( 'user' ) ],
             ]

         ]
    ]
]
