class ValidationError(Exception):
    """Exception raised when form validation fails.

    Attributes:
        errors: mapping of field identifiers to error messages.
    """

    def __init__(self, errors: dict[str, str]):
        self.errors = errors
        super().__init__("Validation failed")
