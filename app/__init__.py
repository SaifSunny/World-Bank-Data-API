from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

load_dotenv()

def create_app():
    app = Flask(__name__)
    jwt = JWTManager(app)

    from app.api.routes import wb_blueprint
    app.register_blueprint(wb_blueprint, url_prefix='/v1/api')
    
    return app
