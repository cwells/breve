html [
    head [
        title [ 'Flatteners and Renderers' ],
    ],

    body [
        h1 [ 'Custom Flatteners and Renderers' ],

        div [
            p [ '''We'll print today's date using a datetime object''' ], br,
            p [ '''Today is ''', today ]
        ],

        p [ '''And now for a custom renderer''' ], br,
        div ( render = example_renderer, data = today ) [ 'this will be replaced' ]
    ]
]
