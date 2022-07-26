from typing import TypeVar, Type, final
from autobean_refactor.models.raw_models import punctuation
from . import base
from . import internal
from .currency import Currency
from .number_expr import NumberExpr

_Self = TypeVar('_Self', bound='Amount')


@internal.tree_model
class Amount(base.RawTreeModel):
    RULE = 'amount'

    @final
    def __init__(self, token_store: base.TokenStore, number: NumberExpr, currency: Currency):
        super().__init__(token_store)
        self._number = number
        self._currency = currency

    @property
    def first_token(self) -> base.RawTokenModel:
        return self._number.first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return self._currency

    _number = internal.field[NumberExpr]()
    _currency = internal.field[Currency]()
    raw_number = internal.required_node_property(_number)
    raw_currency = internal.required_node_property(_currency)

    def clone(self: _Self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> _Self:
        return type(self)(
            token_store,
            self._number.clone(token_store, token_transformer),
            token_transformer.transform(self._currency))
    
    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._number.reattach(token_store, token_transformer)
        self._currency = token_transformer.transform(self._currency)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, Amount)
            and self._number == other._number
            and self._currency == other._currency)

    @classmethod
    def from_children(cls: Type[_Self], number: NumberExpr, currency: Currency) -> _Self:
        token_store = base.TokenStore.from_tokens([
            *number.detach(),
            punctuation.Whitespace.from_default(),
            *currency.detach(),
        ])
        number.reattach(token_store)
        return cls(token_store, number, currency)
