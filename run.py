import os
from core import create_app

app = create_app(os.getenv('APP_SETTINGS') or 'default')

if __name__ == '__main__': 
    app.run()
