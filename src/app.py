import json
from flask import Flask, request
import dao
from db import db
import os

#SECRET_KEY = os.environ["SECRET_KEY"]

app = Flask(__name__)
db_filename = "plan.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# responses


def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code


def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

# Category


@app.route('/api/categories/')
def get_categories():
    return success_response(dao.get_all_categories())


@app.route('/api/categories/', methods=['POST'])
def create_category():
    body = json.loads(request.data)
    category = dao.create_category(name=body.get("name"))
    return success_response(category, 201)


@app.route('/api/categories/<int:c_id>/')
def get_category(c_id):
    c = dao.get_category_by_id(c_id)
    if c is None:
        return failure_response("Category not found!")
    return success_response(c)


@app.route('/api/categories/<int:c_id>/', methods=['DELETE'])
def delete_category(c_id):
    c = dao.delete_category_by_id(c_id)
    if c is None:
        return failure_response("Category not found!")
    return success_response(c)

# Transactions


@app.route('/api/users/<int:c_id>/transaction/', methods=['POST'])
def create_transaction(c_id):
    c = dao.get_user_by_id(c_id)
    if c is None:
        return failure_response("User not found!")
    body = json.loads(request.data)
    cost = body.get("cost")
    transaction = dao.create_transaction(
        body.get("title"),
        body.get("buy_date"),
        cost,
        c_id
    )
    dao.update_user_spent(c_id, cost)
    return success_response(transaction)

# User


@app.route('/api/users/', methods=['POST'])
def create_user():
    body = json.loads(request.data)
    user = dao.create_user(
        name=body.get("name"),
        limit=body.get("limit"),
        spent=body.get("spent")
    )
    return success_response(user, 201)


@app.route('/api/users/<int:user_id>/')
def get_user(user_id):
    u = dao.get_user_by_id(user_id)
    if u is None:
        return failure_response("User not found!")
    return success_response(u)


@app.route('/api/categories/<int:cat_id>/add/', methods=['POST'])
def add_to_category(cat_id):
    body = json.loads(request.data)
    c = dao.add_user_to_category(body.get("user_id"), cat_id)
    if c is None:
        return failure_response("User or Category not found!")
    return success_response(c, 201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
