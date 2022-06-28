from autobean_refactor import token_store as token_store_lib
from . import base
from . import escaped_string
from . import internal


@base.token_model
class OptionLabel(base.RawTokenModel):
    RULE = 'OPTION'


@base.tree_model
class Option(base.RawTreeModel):
    RULE = 'option'

    def __init__(
            self,
            token_store: token_store_lib.TokenStore,
            label: OptionLabel,
            key: escaped_string.EscapedString,
            value: escaped_string.EscapedString
    ):
        super().__init__(token_store)
        self._label = label
        self.raw_key = key
        self.raw_value = value

    @property
    def first_token(self) -> token_store_lib.Token:
        return self._label

    @property
    def last_token(self) -> token_store_lib.Token:
        return self.raw_value

    @internal.required_token_property
    def raw_key(self) -> escaped_string.EscapedString:
        pass

    @internal.required_token_property
    def raw_value(self) -> escaped_string.EscapedString:
        pass
