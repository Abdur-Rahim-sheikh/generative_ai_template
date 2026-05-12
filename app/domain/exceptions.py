from fastapi import status


class DomainException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

        super().__init__(self.message)


class AlreadyExists(DomainException):
    def __init__(self, message: str = "This data already exists"):
        super().__init__(message=message, status_code=status.HTTP_409_CONFLICT)


class NotFound(DomainException):
    def __init__(self, message: str = "Id not Found"):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)


class InsufficientFunds(DomainException):
    def __init__(self, message: str = "Not enough coins in wallet"):
        super().__init__(message=message, status_code=status.HTTP_402_PAYMENT_REQUIRED)
