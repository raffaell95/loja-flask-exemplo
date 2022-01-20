from flask_restful import fields


category_fields = {
    "name": fields.String,
    "slug": fields.String
}

products_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "slug": fields.String,
    "price": fields.Float,
    "quantity": fields.Integer,
    "categories": fields.List(fields.Nested(category_fields))
}

items_fields = {
    "quantity": fields.Integer,
    "price": fields.Float
}

order_fields = {
    "reference_id": fields.String,
    "items": fields.Nested(items_fields),
    "status": fields.String
}

user_orders_fields = {
    "reference_id": fields.String,
    "status": fields.String
}

user_items_fields = {
    "quantity": fields.Integer,
    "price": fields.Float,
    "order": fields.Nested(user_orders_fields),
    "product": fields.Nested(products_fields)
}