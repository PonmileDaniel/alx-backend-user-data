#!/usr/bin/env python3
"""
Encrypting password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password
    """
    hased = password.encode()
    hashed_password = bcrypt.hashpw(hased, bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate if the password matches the hased
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
