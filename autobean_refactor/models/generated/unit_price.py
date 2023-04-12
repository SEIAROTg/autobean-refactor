# DO NOT EDIT
# This file is automatically generated by autobean_refactor.modelgen.

import decimal
from typing import Iterator, Optional, final
from typing_extensions import Self
from .. import base, internal
from ..currency import Currency
from ..number_expr import NumberExpr
from ..spacing import Whitespace


@internal.token_model
class At(internal.SimpleDefaultRawTokenModel):
    RULE = 'AT'
    DEFAULT = '@'


@internal.tree_model
class UnitPrice(base.RawTreeModel, internal.SpacingAccessorsMixin):
    RULE = 'unit_price'
    INLINE = True

    _label = internal.required_field[At]()
    _number = internal.optional_left_field[NumberExpr](separators=(Whitespace.from_default(),))
    _currency = internal.optional_left_field[Currency](separators=(Whitespace.from_default(),))

    @internal.custom_property
    def _number_pivot(self) -> base.RawTokenModel:
        return self._label.last_token

    @internal.custom_property
    def _currency_pivot(self) -> base.RawTokenModel:
        return (self._number and self._number.last_token) or self._label.last_token

    raw_number = internal.optional_node_property(_number, _number_pivot)
    raw_currency = internal.optional_node_property(_currency, _currency_pivot)

    number = internal.optional_decimal_property(raw_number, NumberExpr)
    currency = internal.optional_string_property(raw_currency, Currency)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            label: At,
            number: Optional[NumberExpr],
            currency: Optional[Currency],
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
        return (self._currency and self._currency.last_token) or (self._number and self._number.last_token) or self._label.last_token

    def clone(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> Self:
        return type(self)(
            token_store,
            type(self)._label.clone(self._label, token_store, token_transformer),
            type(self)._number.clone(self._number, token_store, token_transformer),
            type(self)._currency.clone(self._currency, token_store, token_transformer),
        )

    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._label = type(self)._label.reattach(self._label, token_store, token_transformer)
        self._number = type(self)._number.reattach(self._number, token_store, token_transformer)
        self._currency = type(self)._currency.reattach(self._currency, token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, UnitPrice)
            and self._label == other._label
            and self._number == other._number
            and self._currency == other._currency
        )

    @classmethod
    def from_children(
            cls,
            number: Optional[NumberExpr],
            currency: Optional[Currency],
    ) -> Self:
        label = At.from_default()
        tokens = [
            *label.detach(),
            *cls._number.detach_with_separators(number),
            *cls._currency.detach_with_separators(currency),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        cls._label.reattach(label, token_store)
        cls._number.reattach(number, token_store)
        cls._currency.reattach(currency, token_store)
        return cls(token_store, label, number, currency)

    @classmethod
    def from_value(
            cls,
            number: Optional[decimal.Decimal],
            currency: Optional[str],
    ) -> Self:
        return cls.from_children(
            number=NumberExpr.from_value(number) if number is not None else None,
            currency=Currency.from_value(currency) if currency is not None else None,
        )

    def auto_claim_comments(self) -> None:
        type(self)._currency.auto_claim_comments(self._currency)
        type(self)._number.auto_claim_comments(self._number)

    def iter_children_formatted(self) -> Iterator[tuple[base.RawModel, bool]]:
        yield from type(self)._label.iter_children_formatted(self._label, False)
        yield from type(self)._number.iter_children_formatted(self._number, False)
        yield from type(self)._currency.iter_children_formatted(self._currency, False)
