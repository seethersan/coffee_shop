import os
from flask import Flask, jsonify, request, abort, Response
from models import setup_db, Drink, Customer
from flask_cors import CORS
import json

from auth.auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route("/drinks", methods=["GET"])
    @requires_auth("get:drinks-detail")
    def get_drinks(jwt):
        drinks = Drink.query.all()
        drinks = [drink.get() for drink in drinks]

        return jsonify({"success": True, "drinks": drinks}), 200

    @app.route("/drinks", methods=["POST"])
    @requires_auth("post:drinks")
    def create_drink(jwt):
        body = request.get_json()
        title = body.get("title", None)
        recipe = body.get("recipe", None)
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()
        return jsonify({"success": True, "drinks": drink.get()}), 200

    @app.route("/drinks/<int:drink_id>", methods=["PATCH"])
    @requires_auth("patch:drinks")
    def update_drink(jwt, drink_id):
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if drink is None:
            abort(404)

        body = request.get_json()
        title = body.get("title", None)
        recipe = body.get("recipe", None)

        if title:
            drink.title = title

        if recipe:
            drink.recipe = json.dumps(recipe)

        drink.update()
        return jsonify({"success": True, "drinks": [drink.long()]}), 200

    @app.route("/drinks/<int:drink_id>", methods=["DELETE"])
    @requires_auth("delete:drinks")
    def delete_drink(jwt, drink_id):
        try:
            drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
            drink.delete()

            return jsonify({"success": True, "delete": drink_id}), 200
        except:
            abort(404)

    @app.route("/customers/<int:customer_id>", methods=["GET"])
    @requires_auth("get:customer")
    def get_customer(jwt, customer_id):
        customer = Customer.query.filter(Customer.id == customer_id).one_or_none()

        if customer is None:
            abort(404)

        return jsonify({"success": True, "customers": customer}), 200

    @app.route("/customers", methods=["GET"])
    @requires_auth("get:customers")
    def get_customers(jwt):
        customers = Customer.query.all()
        customers = [customer for customer in customers]

        return jsonify({"success": True, "customers": customers}), 200

    @app.route("/customers", methods=["POST"])
    @requires_auth("post:customers")
    def create_customer(jwt):
        body = request.get_json()
        name = body.get("name", None)
        address = body.get("address", None)
        customer = Customer(name=name, address=json.dumps(address))
        customer.insert()
        return jsonify({"success": True, "customers": customer}), 200

    @app.route("/customers/<int:customer_id>", methods=["PATCH"])
    @requires_auth("patch:customers")
    def update_customer(jwt, customer_id):
        customer = Customer.query.filter(Customer.id == customer_id).one_or_none()

        if customer is None:
            abort(404)

        body = request.get_json()
        name = body.get("name", None)
        address = body.get("address", None)

        if name:
            customer.name = name

        if address:
            customer.address = address

        customer.update()
        return jsonify({"success": True, "customers": [customer]}), 200

    @app.route("/customers/<int:customer_id>", methods=["DELETE"])
    @requires_auth("delete:customers")
    def delete_customer(jwt, customer_id):
        try:
            customer = Customer.query.filter(Customer.id == customer_id).one_or_none()
            customer.delete()

            return jsonify({"success": True, "delete": customer_id}), 200
        except:
            abort(404)

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}),
            400,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify(
                {"success": False, "error": 500, "message": "internal server error"}
            ),
            500,
        )

    @app.errorhandler(502)
    def service_unavailable(error):
        return (
            jsonify({"success": False, "error": 502, "message": "service unavailable"}),
            502,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(AuthError)
    def not_found(error):
        return jsonify({"success": False, "error": 401, "message": "unauthorized"}), 401

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
