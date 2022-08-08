# DO NOT EDIT
# This file is automatically generated by autobean_refactor.modelgen.

from typing import Optional, Type, TypeVar, final
from .. import base
from .. import internal
from ..meta_key import MetaKey
from ..meta_value import MetaRawValue
from ..punctuation import Whitespace

_Self = TypeVar('_Self', bound='Pushmeta')


@internal.token_model
class PushmetaLabel(internal.SimpleDefaultRawTokenModel):
    RULE = 'PUSHMETA'
    DEFAULT = 'pushmeta'


@internal.tree_model
class Pushmeta(base.RawTreeModel):
    RULE = 'pushmeta'

    _label = internal.required_field[PushmetaLabel]()
    _key = internal.required_field[MetaKey]()
    _value = internal.optional_field[MetaRawValue](separators=(Whitespace.from_default(),))

    raw_key = internal.required_node_property(_key)
    raw_value = internal.optional_node_property(_value)

    key = internal.required_string_property(raw_key)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            label: PushmetaLabel,
            key: MetaKey,
            value: internal.Maybe[MetaRawValue],
    ):
        super().__init__(token_store)
        self._label = label
        self._key = key
        self._value = value

    @property
    def first_token(self) -> base.RawTokenModel:
        return self._label.first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return self._value.last_token

    def clone(self: _Self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> _Self:
        return type(self)(
            token_store,
            self._label.clone(token_store, token_transformer),
            self._key.clone(token_store, token_transformer),
            self._value.clone(token_store, token_transformer),
        )
    
    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._label = self._label.reattach(token_store, token_transformer)
        self._key = self._key.reattach(token_store, token_transformer)
        self._value = self._value.reattach(token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, Pushmeta)
            and self._label == other._label
            and self._key == other._key
            and self._value == other._value
        )

    @classmethod
    def from_children(
            cls: Type[_Self],
            key: MetaKey,
            value: Optional[MetaRawValue],
    ) -> _Self:
        label = PushmetaLabel.from_default()
        maybe_value = internal.MaybeL[MetaRawValue].from_children(value, separators=cls._value.separators)
        tokens = [
            *label.detach(),
            Whitespace.from_default(),
            *key.detach(),
            *maybe_value.detach(),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        label.reattach(token_store)
        key.reattach(token_store)
        maybe_value.reattach(token_store)
        return cls(token_store, label, key, maybe_value)
