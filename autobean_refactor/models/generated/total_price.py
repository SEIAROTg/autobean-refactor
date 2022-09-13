# DO NOT EDIT
# This file is automatically generated by autobean_refactor.modelgen.

import decimal
from typing import Optional, Type, TypeVar, final
from .. import base, internal
from ..currency import Currency
from ..number_expr import NumberExpr
from ..spacing import Whitespace

_Self = TypeVar('_Self', bound='TotalPrice')


@internal.token_model
class AtAt(internal.SimpleDefaultRawTokenModel):
    RULE = 'ATAT'
    DEFAULT = '@@'


@internal.tree_model
class TotalPrice(base.RawTreeModel, internal.SpacingAccessorsMixin):
    RULE = 'total_price'

    _label = internal.required_field[AtAt]()
    _number = internal.optional_left_field[NumberExpr](separators=(Whitespace.from_default(),))
    _currency = internal.optional_left_field[Currency](separators=(Whitespace.from_default(),))

    raw_number = internal.optional_node_property(_number)
    raw_currency = internal.optional_node_property(_currency)

    number = internal.optional_decimal_property(raw_number, NumberExpr)
    currency = internal.optional_string_property(raw_currency, Currency)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            label: AtAt,
            number: internal.Maybe[NumberExpr],
            currency: internal.Maybe[Currency],
    ):
        super().__init__(token_store)
        self._label = label
        self._number = number
        self._currency = currency

    @property
    def first_token(self) -> base.RawTokenModel:
        return self._label.first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return self._currency.last_token

    def clone(self: _Self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> _Self:
        return type(self)(
            token_store,
            self._label.clone(token_store, token_transformer),
            self._number.clone(token_store, token_transformer),
            self._currency.clone(token_store, token_transformer),
        )

    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._label = self._label.reattach(token_store, token_transformer)
        self._number = self._number.reattach(token_store, token_transformer)
        self._currency = self._currency.reattach(token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, TotalPrice)
            and self._label == other._label
            and self._number == other._number
            and self._currency == other._currency
        )

    @classmethod
    def from_children(
            cls: Type[_Self],
            number: Optional[NumberExpr],
            currency: Optional[Currency],
    ) -> _Self:
        label = AtAt.from_default()
        maybe_number = cls._number.create_maybe(number)
        maybe_currency = cls._currency.create_maybe(currency)
        tokens = [
            *label.detach(),
            *maybe_number.detach(),
            *maybe_currency.detach(),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        label.reattach(token_store)
        maybe_number.reattach(token_store)
        maybe_currency.reattach(token_store)
        return cls(token_store, label, maybe_number, maybe_currency)

    @classmethod
    def from_value(
            cls: Type[_Self],
            number: Optional[decimal.Decimal],
            currency: Optional[str],
    ) -> _Self:
        return cls.from_children(
            number=NumberExpr.from_value(number) if number is not None else None,
            currency=Currency.from_value(currency) if currency is not None else None,
        )

    def auto_claim_comments(self) -> None:
        self._currency.auto_claim_comments()
        self._number.auto_claim_comments()
