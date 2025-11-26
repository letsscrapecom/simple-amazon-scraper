from flask import Flask
from scraper.driver_manager import driver_manager
from routes import api
from config import Config

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)
    return app

if __name__ == '__main__':
    driver_manager.connect()
    
    app = create_app()

    app.run(host=Config.API_HOST, port=Config.API_PORT, debug=True, use_reloader=True)
