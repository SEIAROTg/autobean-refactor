from . import internal


@internal.token_model
class Null(internal.SimpleDefaultRawTokenModel):
    """Contains literal `NULL`."""
    RULE = 'NULL'
    DEFAULT = 'NULL'
