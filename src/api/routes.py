from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
import hashlib
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


api = Blueprint('api', __name__)
       

@api.route('/token', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if email != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401
    
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

@api.route('/login', methods=['POST']) 
def login():
    data = request.json
    
    user = User.query.filter_by(email=data["email"], password=data["password"]).first()
    if not user:
        return jsonify({"msg": "Bad username or password"}), 401
    access_token=create_access_token(identity=user.email)
    
    return jsonify({"token": access_token, "user": user.serialize()})

@api.route("/register", methods=["POST"])
def register():
    data = request.json

    user = User.query.filter_by(email=data["email"]).first()
    if user:
        return jsonify({"msg": "User already exists."}), 401
    new_user = User(
        password=data["password"],
        email=data["email"],
    )
    db.session.add(new_user) 
    db.session.commit()

    return jsonify({"msg" : "Success or Whatever" })