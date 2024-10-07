#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

# Initialize migration and db
migrate = Migrate(app, db)
db.init_app(app)

# Initialize Flask-RESTful API
api = Api(app)

# Plants resource to handle GET (list all plants) and POST (add new plant)
class Plants(Resource):
    def get(self):
        # Fetch all plants and serialize them using to_dict()
        plants = Plant.query.all()
        plant_list = [plant.to_dict() for plant in plants]
        return make_response(jsonify(plant_list), 200)

    def post(self):
        # Retrieve data from the request
        data = request.get_json()
        try:
            # Validate that all required fields are present in the request body
            if not all(key in data for key in ('name', 'image', 'price')):
                return make_response(jsonify({"error": "Missing required fields"}), 400)
            
            # Create a new plant record
            new_plant = Plant(name=data['name'], image=data['image'], price=data['price'])

            # Add to the database
            db.session.add(new_plant)
            db.session.commit()

            # Return the newly created plant serialized with to_dict()
            return make_response(jsonify(new_plant.to_dict()), 201)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

# PlantByID resource to handle GET for individual plants by id
class PlantByID(Resource):
    def get(self, id):
        # Use session.get() instead of query.get()
        plant = db.session.get(Plant, id)
        if plant is None:
            return {"error": "Plant not found"}, 404
        return make_response(jsonify(plant.to_dict()), 200)
    
# Add resources to API with specified endpoints
api.add_resource(Plants, '/plants')  # Index and Create routes
api.add_resource(PlantByID, '/plants/<int:id>')  # Show route

if __name__ == '__main__':
    app.run(port=5555, debug=True)
