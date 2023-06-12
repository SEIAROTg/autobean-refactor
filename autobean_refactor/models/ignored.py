from . import internal


@internal.token_model
class Ignored(internal.SimpleRawTokenModel):
    """Ignored line body (see `IgnoredLine`)."""
    RULE = 'IGNORED'
