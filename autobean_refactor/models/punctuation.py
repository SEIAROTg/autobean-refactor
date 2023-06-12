from . import internal


@internal.token_model
class Eol(internal.SimpleDefaultRawTokenModel):
    """End of line. For internal use only."""
    RULE = 'EOL'
    DEFAULT = ''


@internal.token_model
class Indent(internal.SimpleSingleValueRawTokenModel, internal.DefaultRawTokenModel):
    """Contains spacing for indentation."""
    RULE = 'INDENT'
    DEFAULT = ' ' * 4


@internal.token_model
class DedentMark(internal.SimpleDefaultRawTokenModel):
    """Dedent mark. For internal use only."""
    RULE = 'DEDENT_MARK'
    DEFAULT = ''


@internal.token_model
class Comma(internal.SimpleDefaultRawTokenModel):
    """Contains literal `,`."""
    RULE = '_COMMA'
    DEFAULT = ','


@internal.token_model
class Asterisk(internal.SimpleDefaultRawTokenModel):
    """Contains literal `*`."""
    RULE = 'ASTERISK'
    DEFAULT = '*'
