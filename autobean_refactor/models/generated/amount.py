# DO NOT EDIT
# This file is automatically generated by autobean_refactor.modelgen.

import decimal
from typing import Iterator, Type, TypeVar, final
from .. import base, internal
from ..currency import Currency
from ..number_expr import NumberExpr
from ..spacing import Whitespace

_Self = TypeVar('_Self', bound='Amount')


@internal.tree_model
class Amount(base.RawTreeModel, internal.SpacingAccessorsMixin):
    RULE = 'amount'
    INLINE = True

    _number = internal.required_field[NumberExpr]()
    _currency = internal.required_field[Currency]()

    raw_number = internal.required_node_property(_number)
    raw_currency = internal.required_node_property(_currency)

    number = internal.required_value_property(raw_number)
    currency = internal.required_value_property(raw_currency)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            number: NumberExpr,
            currency: Currency,
    ):
        super().__init__(token_store)
        self._number = number
        self._currency = currency

    @property
    def first_token(self) -> base.RawTokenModel:
        return self._number.first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return self._currency.last_token

    def clone(self: _Self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> _Self:
        return type(self)(
            token_store,
            type(self)._number.clone(self._number, token_store, token_transformer),
            type(self)._currency.clone(self._currency, token_store, token_transformer),
        )

    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._number = type(self)._number.reattach(self._number, token_store, token_transformer)
        self._currency = type(self)._currency.reattach(self._currency, token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, Amount)
            and self._number == other._number
            and self._currency == other._currency
        )

    @classmethod
    def from_children(
            cls: Type[_Self],
            number: NumberExpr,
            currency: Currency,
    ) -> _Self:
        tokens = [
            *number.detach(),
            Whitespace.from_default(),
            *currency.detach(),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        cls._number.reattach(number, token_store)
        cls._currency.reattach(currency, token_store)
        return cls(token_store, number, currency)

    @classmethod
    def from_value(
            cls: Type[_Self],
            number: decimal.Decimal,
            currency: str,
    ) -> _Self:
        return cls.from_children(
            number=NumberExpr.from_value(number),
            currency=Currency.from_value(currency),
        )

    def auto_claim_comments(self) -> None:
        type(self)._currency.auto_claim_comments(self._currency)
        type(self)._number.auto_claim_comments(self._number)

    def iter_children_formatted(self) -> Iterator[tuple[base.RawModel, bool]]:
        yield from type(self)._number.iter_children_formatted(self._number, False)
        yield Whitespace.from_default(), False
        yield from type(self)._currency.iter_children_formatted(self._currency, False)
