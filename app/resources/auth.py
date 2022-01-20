from flask_restful import Resource, reqparse
from flask import request
from app.extensions import db
from datetime import timedelta
from app.models import User
from flask_jwt_extended import create_access_token
import logging
from base64 import b64decode
from werkzeug.security import generate_password_hash, check_password_hash
from app.services.mail import send_mail
import secrets


class Login(Resource):
    def get(self):
        if not request.headers.get("Authorization"):
            return {"error": "Authorization não encontrado"}, 400

        basic, code = request.headers["Authorization"].split(" ")
        if not basic.lower() == "basic":
            return {"error": "autorização mal formatada"}, 400

        email, password = b64decode(code).decode().split(":")

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return {"error": "login e senha invalidos"}, 400

        token = create_access_token({"id": user.id}, expires_delta=timedelta(hours=3))

        return {"access_token": token}


class Register(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, help="O campo email é obrigatório")
        parser.add_argument(
            "password", required=True, help="O campo password é obrigatório"
        )
        args = parser.parse_args()

        user = User.query.filter_by(email=args.email).first()
        if user:
            return {"error": "email já registrado!"}, 400

        user = User()
        user.email = args.email
        user.password = generate_password_hash(args.password, salt_length=10)

        db.session.add(user)
        try:
            db.session.commit()
            send_mail("Bem vindo", user.email, "welcome", email=user.email)
            return {"message": "Usuário registrado com sucesso!"}, 201
        except Exception as e:
            db.session.rollback()
            logging.critical(str(e))
            return ({"error": "Não foi possivel fazer o registro do usuário"}, 500)


class ForgetPassword(Resource):
    def post(self):
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument("email", required=True, help="O campo email é Obrigatório")
        args = parser.parse_args()

        user = User.query.filter_by(email=args.email).first()
        if not user:
            return {"error": "dados não encontrados"}, 400

        password_temp = secrets.token_hex(8)
        user.password = generate_password_hash(password_temp)
        db.session.add(user)
        db.session.commit()

        send_mail("Recuperação de conta", user.email, "forget-password", password_temp=password_temp)
        return {"message": "E-mail enviado com sucesso!"}
