# -*- coding: utf-8 -*-

class UserDoesNotExist (Exception):
    """The user does not exist."""


class UserLoggedIn (Exception):
    "User logged in."



__all__ = [
    "UserDoesNotExist",
    "UserLoggedIn"
]
