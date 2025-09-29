from flask import request, jsonify
from myapp.users import bp
from myapp import models
import datetime


@bp.route("/record/<int:record_id>", methods=["GET"])
def get_record(record_id):
    record = models.records.get(record_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404
    return jsonify(record)


@bp.route("/record/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    if record_id in models.records:
        del models.records[record_id]
        return jsonify({"message": "Record deleted"})
    return jsonify({"error": "Record not found"}), 404


@bp.route("/record", methods=["POST"])
def create_record():
    data = request.get_json(force=True, silent=True)
    if not data or "user_id" not in data or "category_id" not in data or "amount" not in data:
        return jsonify({"error": "user_id, category_id and amount are required"}), 400
    record = models.create_record(
        data["user_id"],
        data["category_id"],
        data["amount"]
    )
    return jsonify(record), 201


    rid = models.record_counter
    record = {
        "id": rid,
        "user_id": data["user_id"],
        "category_id": data["category_id"],
        "amount": data["amount"],
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    models.records[rid] = record
    models.record_counter += 1
    return jsonify(record)


@bp.route("/record", methods=["GET"])
def list_records():
    user_id = request.args.get("user_id", type=int)
    category_id = request.args.get("category_id", type=int)

    if not user_id and not category_id:
        return jsonify({"error": "user_id or category_id required"}), 400

    filtered = []
    for r in models.records.values():
        if user_id and category_id:
            if r["user_id"] == user_id and r["category_id"] == category_id:
                filtered.append(r)
        elif user_id and r["user_id"] == user_id:
            filtered.append(r)
        elif category_id and r["category_id"] == category_id:
            filtered.append(r)

    return jsonify(filtered)