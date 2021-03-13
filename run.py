# -*- coding: utf-8 -*-

from __future__ import absolute_import
from web.app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run( 
            host = "127.0.0.1",  
            port =5000,
            debug = True,
        )
