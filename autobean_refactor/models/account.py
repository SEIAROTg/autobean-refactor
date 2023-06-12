from . import internal


@internal.token_model
class Account(internal.SimpleSingleValueRawTokenModel):
    """Account (e.g. `Assets:Foo`)."""
    RULE = 'ACCOUNT'
