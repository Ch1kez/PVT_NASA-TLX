from flask import Flask, request, jsonify
from .database import SessionLocal
from .services import create_user, save_pvt_result

app = Flask(__name__)

@app.route("/users", methods=["POST"])
def add_user():
    db = SessionLocal()
    user_data = request.json
    user = create_user(db, user_data)
    return jsonify({"id": user.id, "name": user.name})

@app.route("/pvt", methods=["POST"])
def pvt_test():
    db = SessionLocal()
    pvt_data = request.json
    result = save_pvt_result(db, pvt_data)
    return jsonify({"reaction_time": result.reaction_time})
