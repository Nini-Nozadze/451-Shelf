from ext import *
from app import create_app
from routes import *



app = create_app()

app.run(host='0.0.0.0',)

if __name__ == "__main__":
    app.run(debug=True)

