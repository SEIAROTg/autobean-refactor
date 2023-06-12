from . import internal


@internal.token_model
class Currency(internal.SimpleSingleValueRawTokenModel):
    """Currency (e.g. `USD`)."""
    RULE = 'CURRENCY'
