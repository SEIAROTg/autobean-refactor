from autobean_refactor import token_store as token_store_lib
from . import base
from . import escaped_string


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
        self._key = key
        self._value = value

    @property
    def first_token(self) -> token_store_lib.Token:
        return self._label

    @property
    def last_token(self) -> token_store_lib.Token:
        return self._value

    @property
    def raw_key(self) -> escaped_string.EscapedString:
        return self._key

    @raw_key.setter
    def raw_key(self, key: escaped_string.EscapedString) -> None:
        self._token_store.replace(self._key, key)
        self._key = key

    @property
    def raw_value(self) -> escaped_string.EscapedString:
        return self._value
    
    @raw_value.setter
    def raw_value(self, value: escaped_string.EscapedString) -> None:
        self._token_store.replace(self._value, value)
        self._value = value
