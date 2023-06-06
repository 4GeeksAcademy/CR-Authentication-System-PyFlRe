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

# @api.route('/login', methods=['POST'])
# def login():
#     body = request.get_json ( force = True)
#     email = body['email']
#     password = hashlib.sha256(body['password'].encode("utf-8")).hexdigest()
#     print(password)
#     new_user = User(email = email, password = password)
#     db.session.add(new_user)
#     db.session.commit()
#     access_token = create_access_token(identity = email)
#     return jsonify(access_token = access_token)

@api.route('/hello', methods=["GET"])
@jwt_required()
def get_hello():
    email = get_jwt_identity()
    dictionary = {
        "message": "Hello World " + email
    }
    return jsonify(dictionary)