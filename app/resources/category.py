from flask_restful import Resource, marshal_with, marshal
from app.models import Category
from app.schemas import category_fields


class CategoryList(Resource):

    @marshal_with(category_fields, envelope="categories")
    def get(self):
        category = Category.query.all()
        return category

class CategoryGet(Resource):
    def get(self, slug):
        category = Category.query.filter_by(slug=slug).first()
        if not category:
            return {"error": "Categoria não encontrada"}, 400

        return marshal(category, category_fields, "category")

