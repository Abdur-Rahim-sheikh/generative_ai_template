class DomainException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class AlreadyExists(DomainException):
    def __init__(self, message: str = "This data already exists"):
        super().__init__(message=message)


class NotFound(DomainException):
    def __init__(self, message: str = "Id not Found"):
        super().__init__(message=message)


class InsufficientFunds(DomainException):
    def __init__(self, message: str = "Not enough coins in wallet"):
        super().__init__(message=message)
