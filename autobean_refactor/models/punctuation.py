from . import internal


@internal.token_model
class Newline(internal.SimpleDefaultRawTokenModel):
    RULE = '_NEWLINE'
    DEFAULT = '\n'


@internal.token_model
class Eol(internal.SimpleDefaultRawTokenModel):
    RULE = 'EOL'
    DEFAULT = ''


@internal.token_model
class Whitespace(internal.SimpleSingleValueRawTokenModel, internal.DefaultRawTokenModel):
    RULE = 'WHITESPACE'
    DEFAULT = ' '


@internal.token_model
class Comma(internal.SimpleDefaultRawTokenModel):
    RULE = '_COMMA'
    DEFAULT = ','


@internal.token_model
class Asterisk(internal.SimpleDefaultRawTokenModel):
    RULE = 'ASTERISK'
    DEFAULT = '*'
