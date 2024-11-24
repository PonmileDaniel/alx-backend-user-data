#!/usr/bin/env python3
"""
Create a SqlAlchemy model name user
"""

import bcrypt


def _hash_password(password: str) -> bytes:
        """
        Hash a password with bcrypt and return the hashed password"""
        if not isinstance(password, str):
            raise TypeError("Password must be a string.")
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password
