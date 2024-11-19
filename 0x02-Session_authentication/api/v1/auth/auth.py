#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import request
from typing import List, TypeVar
import os


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
            if excluded_path.endswith("*") and \
                    path.startswith(excluded_path[:-1]):
                return False
            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        returns None - request
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar("User"):  # type: ignore
        """Method to get current user"""
        return None

    def session_cookie(self, request=None):
        """Function for cookies"""
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME')

        if session_name is None:
            return None
        return request.cookies.get(session_name, None)
