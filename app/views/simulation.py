from flask import Blueprint, json, request, redirect, url_for

simulation_bp = Blueprint("simulation", __name__, url_prefix="/simulation/")


@simulation_bp.route("/")
def index():
    return json.jsonify({"msg": "hello there"})
