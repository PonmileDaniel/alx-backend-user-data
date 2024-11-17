#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Authetication class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method to check if auth is required"""
        if not path or not excluded_paths:
            return True

        print(f"Checking path: {path}, Excluded paths: {excluded_paths}")
        if path[-1] != "/":
            path += "/"

        for excluded_path in excluded_paths:
            if excluded_path.endswith("*") and path.startswith(excluded_path[:-1]):
                print(f"Path {path} matches excluded pattern {excluded_path}")
                return False
            if path == excluded_path:
                print(f"Path {path} is explicitly excluded")
                return False

        print(f"Path {path} requires authentication")
        return True


    # def authorization_header(self, request=None) -> str:
    #     """Method to get authorization header"""
    #     if request is None:
    #         return None
    #     return request.headers.get("Authorization")

    def authorization_header(self, request=None) -> str:
        """Get the Authorization header"""
        if request is None:
            print("No request object found")
            return None

        auth_header = request.headers.get("Authorization")
        print(f"Authorization Header: {auth_header}")
        return auth_header



    def current_user(self, request=None) -> TypeVar("User"):  # type: ignore
        """Method to get current user"""
        return None
