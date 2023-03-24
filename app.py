import os
import secrets
from dotenv import dotenv_values

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db
from blocklist import BLOCKLIST
import models

from resources.alert import blp as AlertBlueprint


config = dotenv_values(".env")

# factory pattern
def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Webfire Alert REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URI", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    
    migrate = Migrate(app, db)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = config["secret"]
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"description": "The token has been revoked", "error": "token_revoked"}), 401


    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The token passed is not fresh", "error":"fresh_token_required"}), 401


    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The token has expired", "error": "token_expired"}), 401
    

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401


    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message": "No valid access token in request", "error": "authorization required"}), 401


    with app.app_context():
        db.create_all()

    api.register_blueprint(AlertBlueprint)

    return app









#
# docker run -p 5005:5000 rest-apis-flask-python

# runs a built image turning it into a volume. 
#docker run -dp 5000:5000 -w /app -v "C:\Users\Tyler\Desktop\FlaskRESTAPI/app" flask_practice

