#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
import os
from api.v1.auth.auth import Auth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


auth = None
auth_type = getenv("Auth_TYPE", auth)
if auth_type == "auth":
    from api.v1.auth.auth import Auth

    auth = Auth()


@app.errorhandler(404)
def not_found(error) -> str:
    """Not found handler"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized request"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    For handling request forbidden
    """
    return jsonify({"error": "Forbidden"}), 403


# @app.before_request
# def authenticate_user():
#     """Filter requests before they rreach the view"""
#     if auth:
#         excluded_paths = [
#             "/api/v1/status/",
#             "/api/v1/unauthorized/",
#             "/api/v1/forbidden/",
#         ]
#         if auth.require_auth(request.path, excluded_paths):
#             if auth.authorization_header(request) is None:
#                 abort(401)
#             if auth.current_user(request) is None:
#                 abort(403)

@app.before_request
def authenticate_user():
    """Filter requests before they reach the view"""
    if auth:
        print(f"Request Path: {request.path}")
        excluded_paths = [
            "/api/v1/status/",
            "/api/v1/unauthorized/",
            "/api/v1/forbidden/",
        ]
        if auth.require_auth(request.path, excluded_paths):
            print(f"Path requires auth: {request.path}")
            if auth.authorization_header(request) is None:
                print("No Authorization header found")
                abort(401)  # Unauthorized
            if auth.current_user(request) is None:
                print("Current user not found")
                abort(403)  # Forbidden



if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
