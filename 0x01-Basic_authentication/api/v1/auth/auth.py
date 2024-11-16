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

        if path[-1] != "/":
            path += "/"

        for excluded_path in excluded_paths:
            if excluded_path.endswith("*"):
                return False
            elif path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Method to get authorization header"""
        if request is None:
            return request.headers.get("Authorization", None)
        return None

    def current_user(self, request=None) -> TypeVar("User"):  # type: ignore
        """Method to get current user"""
        return None
