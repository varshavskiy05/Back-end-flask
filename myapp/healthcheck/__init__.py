from flask import Blueprint, jsonify

bp = Blueprint("healthcheck", __name__, url_prefix="/healthcheck")


@bp.route("/", methods=["GET"])
def healthcheck():
    return jsonify({"status": "ok"}), 200