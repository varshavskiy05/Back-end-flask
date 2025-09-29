from flask import request, jsonify
from myapp.categories import bp
from myapp import models


@bp.route("/category", methods=["GET"])
def list_categories():
    return jsonify(list(models.categories.values()))


@bp.route("/category", methods=["POST"])
def create_category():
    data = request.get_json(force=True, silent=True)
    if not data or "name" not in data:
        return jsonify({"error": "Invalid input"}), 400
    category = models.create_category(data["name"])
    return jsonify(category), 201



@bp.route("/category", methods=["DELETE"])
def delete_category():
    data = request.json
    if not data or "id" not in data:
        return jsonify({"error": "Category id is required"}), 400
    cid = data["id"]
    if cid in models.categories:
        del models.categories[cid]
        return jsonify({"message": "Category deleted"})
    return jsonify({"error": "Category not found"}), 404
