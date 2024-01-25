# { "email": "user@example.com",
# "password": "mypassword"
# }

from flask import Blueprint, g, request, session, jsonify
from server.controllers import UserController

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@bp.route("/user", methods=["GET"])
def get_user():
    if g.user is not None:
        return g.user.as_dict()

    return jsonify(None)

@bp.route("/signup", methods=["POST"])
def signup():
    email = request.json.get("email")
    password = request.json.get("password")

    user = UserController.create_user(email=email, password=password)
    session["user_id"] = user.id

    return user.as_dict()


@bp.route("/signin", methods=["POST"])
def signin():
    email = request.json.get("email")
    password = request.json.get("password")

    user = UserController.authenticate_user(email, password)

    if not user:
        return {"message": "Incorrect email or password."}, 400

    session.permanent = True
    session["user_id"] = user.id
    
    print(session)

    return user.as_dict()


@bp.route("/signout", methods=["POST"])
def signout():
    session.clear()
    return {"message": "Successfully logged out."}
