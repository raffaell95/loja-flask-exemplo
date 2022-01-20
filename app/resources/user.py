from flask_restful import Resource, marshal
from app.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas import user_items_fields


class Orders(Resource):
    @jwt_required(optional=False)
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.get(current_user["id"])
        return marshal(user.items, user_items_fields)