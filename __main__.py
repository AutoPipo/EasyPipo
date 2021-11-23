# -*- coding: utf-8 -*-
from web.app import create_app

app = create_app()
app.run( 
    host = "0.0.0.0",
    port = 5002,
    debug = False,
    use_reloader=False
)