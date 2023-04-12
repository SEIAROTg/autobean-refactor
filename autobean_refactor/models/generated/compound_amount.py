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
class Hash(internal.SimpleDefaultRawTokenModel):
    RULE = 'HASH'
    DEFAULT = '#'


@internal.tree_model
class CompoundAmount(base.RawTreeModel, internal.SpacingAccessorsMixin):
    RULE = 'compound_amount'
    INLINE = True

    _number_per = internal.optional_right_field[NumberExpr](separators=(Whitespace.from_default(),))
    _hash = internal.required_field[Hash]()
    _number_total = internal.optional_left_field[NumberExpr](separators=(Whitespace.from_default(),))
    _currency = internal.required_field[Currency]()

    @internal.custom_property
    def _number_per_pivot(self) -> base.RawTokenModel:
        return self._hash.first_token

    @internal.custom_property
    def _number_total_pivot(self) -> base.RawTokenModel:
        return self._hash.last_token

    raw_number_per = internal.optional_node_property(_number_per, _number_per_pivot)
    raw_number_total = internal.optional_node_property(_number_total, _number_total_pivot)
    raw_currency = internal.required_node_property(_currency)

    number_per = internal.optional_decimal_property(raw_number_per, NumberExpr)
    number_total = internal.optional_decimal_property(raw_number_total, NumberExpr)
    currency = internal.required_value_property(raw_currency)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            number_per: Optional[NumberExpr],
            hash: Hash,
            number_total: Optional[NumberExpr],
            currency: Currency,
    ):
        super().__init__(token_store)
        self._number_per = number_per
        self._hash = hash
        self._number_total = number_total
        self._currency = currency

    @property
    def first_token(self) -> base.RawTokenModel:
        return (self._number_per and self._number_per.first_token) or self._hash.first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return self._currency.last_token

    def clone(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> Self:
        return type(self)(
            token_store,
            type(self)._number_per.clone(self._number_per, token_store, token_transformer),
            type(self)._hash.clone(self._hash, token_store, token_transformer),
            type(self)._number_total.clone(self._number_total, token_store, token_transformer),
            type(self)._currency.clone(self._currency, token_store, token_transformer),
        )

    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._number_per = type(self)._number_per.reattach(self._number_per, token_store, token_transformer)
        self._hash = type(self)._hash.reattach(self._hash, token_store, token_transformer)
        self._number_total = type(self)._number_total.reattach(self._number_total, token_store, token_transformer)
        self._currency = type(self)._currency.reattach(self._currency, token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, CompoundAmount)
            and self._number_per == other._number_per
            and self._hash == other._hash
            and self._number_total == other._number_total
            and self._currency == other._currency
        )

    @classmethod
    def from_children(
            cls,
            number_per: Optional[NumberExpr],
            number_total: Optional[NumberExpr],
            currency: Currency,
    ) -> Self:
        hash = Hash.from_default()
        tokens = [
            *cls._number_per.detach_with_separators(number_per),
            *hash.detach(),
            *cls._number_total.detach_with_separators(number_total),
            Whitespace.from_default(),
            *currency.detach(),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        cls._number_per.reattach(number_per, token_store)
        cls._hash.reattach(hash, token_store)
        cls._number_total.reattach(number_total, token_store)
        cls._currency.reattach(currency, token_store)
        return cls(token_store, number_per, hash, number_total, currency)

    @classmethod
    def from_value(
            cls,
            number_per: Optional[decimal.Decimal],
            number_total: Optional[decimal.Decimal],
            currency: str,
    ) -> Self:
        return cls.from_children(
            number_per=NumberExpr.from_value(number_per) if number_per is not None else None,
            number_total=NumberExpr.from_value(number_total) if number_total is not None else None,
            currency=Currency.from_value(currency),
        )

    def auto_claim_comments(self) -> None:
        type(self)._currency.auto_claim_comments(self._currency)
        type(self)._number_total.auto_claim_comments(self._number_total)
        type(self)._number_per.auto_claim_comments(self._number_per)

    def iter_children_formatted(self) -> Iterator[tuple[base.RawModel, bool]]:
        yield from type(self)._number_per.iter_children_formatted(self._number_per, False)
        yield from type(self)._hash.iter_children_formatted(self._hash, False)
        yield from type(self)._number_total.iter_children_formatted(self._number_total, False)
        yield Whitespace.from_default(), False
        yield from type(self)._currency.iter_children_formatted(self._currency, False)
