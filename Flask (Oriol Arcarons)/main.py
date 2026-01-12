from flask import Flask
from src.api.routes import init_api_routes
from src.config.db import engine, Base

app = Flask(__name__) 

Base.metadata.create_all(engine)

init_api_routes(app) 

if __name__ == '__main__':
    app.run(debug=True) 