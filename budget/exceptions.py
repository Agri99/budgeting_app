class CategoryExistsError(Exception):
    """Raised when trying to create a category that already exists."""
    pass


class InsufficientFundsError(Exception):
    """Raised when a withdrawal or transfer is attempted without enough balance."""
    pass


