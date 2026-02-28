class BadRequest(Exception):
    pass


class RequestError(Exception):
    pass


class MissingScopeError(Exception):
    pass


class IncorrectTokenError(Exception):
    pass


class UnexpectedError(Exception):
    pass


class InvalidRequest(Exception):
    pass


class UnauthorizedClient(Exception):
    pass


class InvalidGrant(Exception):
    pass


class EmptyToken(Exception):
    pass