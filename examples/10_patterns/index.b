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

             tr ( pattern = 'item', render = sequence ( 'row-seq' ), class_ = 'odd-row' ) [ 
                 td ( pattern = 'item' ) [ curval ( 'row-seq' ) ]
             ],
             tr ( pattern = 'item', render = sequence ( 'row-seq' ), class_ = 'even-row' ) [ 
                 td ( pattern = 'item' ) [ curval ( 'row-seq' ) ]
             ],

             tr ( pattern = 'footer', render = sequence ( 'row-seq'), class_ = 'footer' ) [
                 td ( pattern = 'item' ) [ curval ( 'row-seq' ) ]
             ]
         ]
    ]
]