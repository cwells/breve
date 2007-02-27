html [
    preamble (
        xml_encoding = '''<?xml version="1.0" encoding="UTF-8"?>''',
        doctype = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">''',
    ),
    
    head [
        title [ 'Patterns' ]
    ],

    body [ 
         p [ '''=== Render a 3 column x 10 row table using patterns ===''' ],
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

         p [ '''=== Render a dictionary as a pattern ===''' ],
         ul ( render = mapping ( 'user' ), data = person ) [
             li ( pattern = 'firstname' ) [ 'First Name: ', curval ( 'user' ) ],
             li ( pattern = 'lastname' ) [ 'Last Name: ', curval ( 'user' ) ],
         ],

         p [ '''==== Render a list of dictionaries using patterns ===''' ],
         table ( render = sequence ( 'userlist' ), data = userlist ) [
             th [ 'First Name' ], th [ 'Last Name' ], th [ 'Projects' ],
             tr ( pattern = 'item', render = mapping ( 'user' ), class_ = 'odd-row' ) [
                 td ( pattern = 'firstname' ) [ curval ( 'user' ) ],
                 td ( pattern = 'lastname' ) [ curval ( 'user' ) ],
                 td ( pattern = 'projects' ) [ 
                     # one of the dictionary values is a list too...
                     ul ( render = sequence ( 'projects' ), data = curval ( 'user' ) ) [ 
                         li ( pattern = 'item' ) [ curval ( 'projects' ) ]
                     ]
                 ]
             ]
         ]
    ]
]
