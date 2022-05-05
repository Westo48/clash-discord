class LoginError(Exception):
    """failed login"""
    pass


class AuthorizationError(Exception):
    """invalid token"""
    pass


class InvalidTagError(Exception):
    """invalid player tag"""
    pass


class ConflictError(Exception):
    """database conflict"""
    pass


class NotFoundError(Exception):
    """data not found"""
    pass
