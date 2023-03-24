from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from models import AlertModel
from schemas import AlertSchema
from sqlalchemy.exc import SQLAlchemyError
from db import db
from datetime import datetime


blp = Blueprint("Alerts", __name__, description="Operations on Alerts")


@blp.route("/alert/<int:alert_id>")
class Alert(MethodView):
    
    @blp.response(200, AlertSchema)
    def get(self, Alert_id):
        Alert = AlertModel.query.get_or_404(Alert_id)
        return Alert

    def delete(self, Alert_id):
        Alert = AlertModel.query.get_or_404(Alert_id)
        db.session.delete(Alert)
        db.commit()
        return {"message":"Alert deleted"}


@blp.route("/alert")
class AlertList(MethodView):
    @blp.response(200, AlertSchema(many=True))
    def get(self):
        return AlertModel.query.all()

    #@jwt_required(fresh=True)
    @blp.arguments(AlertSchema)
    @blp.response(201, AlertSchema)
    def post(self, Alert_data):
        
        Alert = AlertModel(**Alert_data)

        curr = datetime.now()
        Alert.timestamp = curr

        try:
            db.session.add(Alert)
            db.session.commit()
        except SQLAlchemyError as err:
            abort(500, message=f"An error occurred in processing - {err}")
        
        return "Placeholder"