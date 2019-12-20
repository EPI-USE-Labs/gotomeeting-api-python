class HTTPError(Exception):
    pass


class HTTPError400(HTTPError):
    pass


class HTTPError403(HTTPError):
    pass


class HTTPError404(HTTPError):
    pass


class HTTPError409(HTTPError):
    pass


class HTTPError500(HTTPError):
    pass


class HTTPError502(HTTPError):
    pass


class UserNotFoundError(Exception):
    pass


class GroupNotFoundError(Exception):
    pass


class CredentialError(Exception):
    pass


class InvalidFilterError(Exception):
    pass


class UserExistsError(Exception):
    pass


class EmptyUpdateParametersError(Exception):
    pass
