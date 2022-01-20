from flask_restful import Resource, marshal, reqparse
from app.models import Product, Order, Item
from random import getrandbits
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas import order_fields
from app.extensions import db
import logging

class Create(Resource):

    @jwt_required(optional=False)
    def post(self):
        current_user = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument("product_id", type=int, required=True, help="product_id obrigatorio")
        parser.add_argument("quantity", type=int, required=True, help="quantity obrigatorio")
        args = parser.parse_args()

        product = Product.query.get(args.product_id)
        if not product:
            return {"error": "Produto não encontrado"}, 400

        if args.quantity > product.quantity:
            return {"error": "Não possuimos essa quantidade"}, 400

        try:
            order = Order()
            order.reference_id = f"FLS-{getrandbits(8)}"
            db.session.add(order)
            db.session.commit()

            item = Item()
            item.order_id = order.id
            item.product_id = product.id
            item.user_id = current_user["id"]
            item.quantity = args.quantity
            item.price = product.price * args.quantity
            db.session.add(item)
            db.session.commit()
            return marshal(order, order_fields, "order")
        except Exception as e:
            logging.critical(str(e))
            db.session.rollback()
            return {"error": "Não foi possivel criar o seu pedido"}, 500

class Pay(Resource):
    pass

class Notification(Resource):
    pass