from typing import Generic, Type, TypeVar, final

from autobean_refactor.models.raw_models import punctuation, tag
from . import base
from . import internal

_Self = TypeVar('_Self', bound='_BasePushtag')
_SelfPushtag = TypeVar('_SelfPushtag', bound='Pushtag')
_SelfPoptag = TypeVar('_SelfPoptag', bound='Poptag')
_L = TypeVar('_L', 'PushtagLabel', 'PoptagLabel')


@internal.token_model
class PushtagLabel(internal.SimpleDefaultRawTokenModel):
    RULE = 'PUSHTAG'
    DEFAULT = 'pushtag'


@internal.token_model
class PoptagLabel(internal.SimpleDefaultRawTokenModel):
    RULE = 'POPTAG'
    DEFAULT = 'poptag'


class _BasePushtag(base.RawTreeModel, Generic[_L]):
    @final
    def __init__(self, token_store: base.TokenStore, label: _L, tag: tag.Tag):
        super().__init__(token_store)
        self._label = label
        self._tag = tag

    @property
    def first_token(self) -> base.RawTokenModel:
        return self._label

    @property
    def last_token(self) -> base.RawTokenModel:
        return self._tag

    _label = internal.field[_L]()
    _tag = internal.field[tag.Tag]()

    raw_tag = internal.required_node_property(_tag)

    def clone(self: _Self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> _Self:
        return type(self)(
            token_store,
            token_transformer.transform(self._label),
            token_transformer.transform(self._tag))
    
    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._label = token_transformer.transform(self._label)
        self._tag = token_transformer.transform(self._tag)


@internal.tree_model
class Pushtag(_BasePushtag[PushtagLabel]):
    RULE = 'pushtag'

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, Pushtag)
            and self._label == other._label
            and self._tag == other._tag)

    @classmethod
    def from_children(cls: Type[_SelfPushtag], tag: tag.Tag) -> _SelfPushtag:
        label = PushtagLabel.from_default()
        token_store = base.TokenStore.from_tokens([
            label,
            punctuation.Whitespace.from_default(),
            tag,
        ])
        return cls(token_store, label, tag)


@internal.tree_model
class Poptag(_BasePushtag[PoptagLabel]):
    RULE = 'poptag'

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, Poptag)
            and self._label == other._label
            and self._tag == other._tag)

    @classmethod
    def from_children(cls: Type[_SelfPoptag], tag: tag.Tag) -> _SelfPoptag:
        label = PoptagLabel.from_default()
        token_store = base.TokenStore.from_tokens([
            label,
            punctuation.Whitespace.from_default(),
            tag,
        ])
        return cls(token_store, label, tag)
