"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

class Persona:
    def __init__(self, nombre):
        self.nombre = nombre
    
    def saludar(self):
        return "Hola, " + self.nombre

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body), 200
_members = []

@app.route("/add_member", methods=["POST"])
def add_member():
    body = request.get_json()
    member = {
        "first_name": body["first_name"],
        "last_name": body["last_name"],
        "age": body["age"],
        "lucky_numbers": body["lucky_numbers"],
    }
    res = jackson_family.add_member(member)
    return jsonify(res), 201 

@app.route("/delete_member", methods=["DELETE"])
def delete_member():
    pass 

@app.route("/get_member", methods=["GET"])
def get_member():
    pass 

@app.route("/get_all_members", methods=["GET"])
def get_all_members():
    res = jackson_family.get_all_members()
    return jsonify(res), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
