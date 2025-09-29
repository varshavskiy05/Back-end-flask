from flask import request, jsonify
from myapp.users import bp
from myapp import models


@bp.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = models.users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)


@bp.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = models.users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    models.users.delete(user_id)
    return jsonify({"message": "User deleted"}), 200


@bp.route("/user", methods=["POST"])
def create_user():
    data = request.get_json(force=True, silent=True)
    if not data or "name" not in data:
        return jsonify({"error": "Invalid input"}), 400
    user = models.create_user(data["name"])
    return jsonify(user), 201



@bp.route("/users", methods=["GET"])
def list_users():
    return jsonify(list(models.users.values()))
