#!/usr/bin/python3
""" Module for places """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.place import Place
from models.city import City
from models.state import State
from models.user import User


@app_views.route('/cities/<city_id>/places',  strict_slashes=False)
def get_places(city_id):
    """ Retrieves the list of all Place objects """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    places_list = []
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)

def delete_place(place_id):
    """ Deletes a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)

def post_place(city_id):
    """ Creates a Place """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    user = storage.get(User, request.json['user_id'])
    if user is None:
        abort(404)
    place = Place(**request.get_json())
    place.city_id = city_id
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)

def update_place(place_id):
    """ Updates a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)

def search_place():
    """ Search for a place """
    if not request.json:
        abort(400, 'Not a JSON')
    states = request.get_json().get('states')
    cities = request.get_json().get('cities')
    amenities = request.get_json().get('amenities')
    places = []
    if not states and not cities and not amenities:
        places = storage.all(Place).values()
    else:
        if states:
            for state_id in states:
                state = storage.get(State, state_id)
                if state:
                    for city in state.cities:
                        places += city.places
        if cities:
            for city_id in cities:
                city = storage.get(City, city_id)
                if city:
                    places += city.places
        if amenities:
            for amenity_id in amenities:
                amenity = storage.get(Amenity, amenity_id)
                if amenity:
                    for place in storage.all(Place).values():
                        if amenity in place.amenities:
                            places.append(place)
    places_list = []
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)
