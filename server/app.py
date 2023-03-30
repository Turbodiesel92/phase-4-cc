#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request, abort
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'


class Pizzas(Resource):
    def get(self):

        pizza_dicts = [pizza.to_dict() for pizza in Pizza.query.all()]

        return make_response(
            jsonify(pizza_dicts),
            200
        )

api.add_resource(Pizzas, '/pizzas')

class Restaurants(Resource):
    def get(self):

        restaurant_dicts = [restaurant.to_dict() for restaurant in Restaurant.query.all()]

        return make_response(
            jsonify(restaurant_dicts),
            200
        )

api.add_resource(Restaurants, '/restaurants')


class RestaurantById(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()

        if not restaurant:
            return make_response({'error': "Restaurant not found"},404)

        restaurant_dict = restaurant.to_dict()

        return make_response(
            jsonify(restaurant_dict),
            200
        )

    def delete(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            abort(404, 'The Restaurant you are trying to delete was not found!')

        db.session.delete(restaurant)
        db.session.commit()

        response = make_response('', 204)

        return response

api.add_resource(RestaurantById, '/restaurants/<int:id>')


class RestaurantPizzas(Resource):
    def post(self):
        try:
            new_restaurant_pizza = RestaurantPizza(
                price=request.get_json()['price'],
                pizza_id=request.get_json()['pizza_id'],
                restaurant_id=request.get_json()['restaurant_id']
            )

            db.session.add(new_restaurant_pizza)
            db.session.commit()

            associated_pizza = Pizza.query.filter(Pizza.id == new_restaurant_pizza.pizza_id).first()
            associated_pizza_dict = associated_pizza.to_dict()

            return make_response(
                jsonify(associated_pizza_dict),
                201
            )
        except:
            return make_response(
                { 'error': ["Validation errors"] },
                400
            )

api.add_resource(RestaurantPizzas, '/restaurant_pizzas')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

