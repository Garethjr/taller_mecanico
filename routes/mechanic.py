from flask import Blueprint, request, jsonify
from models.mechanic import Mechanic
from database import db

mechanic_bp = Blueprint("mechanic_bp", __name__)

@mechanic_bp.route("/api/Mechanic", methods=["GET"])
def get_mechanics():
    mechanics = Mechanic.query.all()
    return jsonify([m.serialize() for m in mechanics])

@mechanic_bp.route("/api/Mechanic", methods=["POST"])
def create_mechanic():
    data = request.json
    try:
        new_mechanic = Mechanic(
            name=data["name"],
            specialty=data.get("specialty"),
            phone=data.get("phone")
        )
        db.session.add(new_mechanic)
        db.session.commit()
        return jsonify(new_mechanic.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

