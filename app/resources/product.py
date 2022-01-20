from flask_restful import Resource, marshal_with, marshal
from app.models import Product
from app.schemas import products_fields


class ProductList(Resource):

    @marshal_with(products_fields, envelope="products")
    def get(self):
        product = Product.query.all()
        return product

class ProductGet(Resource):
    def get(self, slug):
        product = Product.query.filter_by(slug=slug).first()
        if not product:
            return {"error": "Produto não encontrado"}, 400

        return marshal(product, products_fields, "product")