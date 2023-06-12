from . import internal


@internal.token_model
class PostingFlag(internal.SimpleSingleValueRawTokenModel):
    """Posting flag (e.g. `!`)."""
    RULE = 'POSTING_FLAG'
