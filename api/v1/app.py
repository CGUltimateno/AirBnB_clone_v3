#!/usr/bin/python3
""" Module for app.py """
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """ Closes storage """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ 404 error handler """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", default="0.0.0.0")
    port = getenv("HBNB_API_PORT", default="5000")
    app.run(host=host, port=port, threaded=True)
    