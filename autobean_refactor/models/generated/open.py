# DO NOT EDIT
# This file is automatically generated by autobean_refactor.modelgen.

from typing import Iterable, Optional, Type, TypeVar, final
from .. import base
from .. import internal
from ..account import Account
from ..currency import Currency
from ..date import Date
from ..escaped_string import EscapedString
from ..punctuation import Comma, Whitespace

_Self = TypeVar('_Self', bound='Open')


@internal.token_model
class OpenLabel(internal.SimpleDefaultRawTokenModel):
    RULE = 'OPEN'
    DEFAULT = 'open'


@internal.tree_model
class Open(base.RawTreeModel):
    RULE = 'open'

    _date = internal.required_field[Date]()
    _label = internal.required_field[OpenLabel]()
    _account = internal.required_field[Account]()
    _currencies = internal.repeated_field[Currency](separators=(Comma.from_default(), Whitespace.from_default()), separators_before=(Whitespace.from_default(),))
    _booking = internal.optional_field[EscapedString](separators=(Whitespace.from_default(),))

    raw_date = internal.required_node_property(_date)
    raw_account = internal.required_node_property(_account)
    raw_currencies = internal.repeated_node_property(_currencies)
    raw_booking = internal.optional_node_property(_booking)

    date = internal.required_date_property(raw_date)
    account = internal.required_string_property(raw_account)
    currencies = internal.repeated_string_property(raw_currencies, Currency)
    booking = internal.optional_string_property(raw_booking, EscapedString)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            date: Date,
            label: OpenLabel,
            account: Account,
            currencies: internal.Repeated[Currency],
            booking: internal.Maybe[EscapedString],
    ):
        super().__init__(token_store)
        self._date = date
        self._label = label
        self._account = account
        self._currencies = currencies
        self._booking = booking

    @property
    def first_token(self) -> base.RawTokenModel:
        return self._date.first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return self._booking.last_token

    def clone(self: _Self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> _Self:
        return type(self)(
            token_store,
            self._date.clone(token_store, token_transformer),
            self._label.clone(token_store, token_transformer),
            self._account.clone(token_store, token_transformer),
            self._currencies.clone(token_store, token_transformer),
            self._booking.clone(token_store, token_transformer),
        )
    
    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._date = self._date.reattach(token_store, token_transformer)
        self._label = self._label.reattach(token_store, token_transformer)
        self._account = self._account.reattach(token_store, token_transformer)
        self._currencies = self._currencies.reattach(token_store, token_transformer)
        self._booking = self._booking.reattach(token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, Open)
            and self._date == other._date
            and self._label == other._label
            and self._account == other._account
            and self._currencies == other._currencies
            and self._booking == other._booking
        )

    @classmethod
    def from_children(
            cls: Type[_Self],
            date: Date,
            account: Account,
            currencies: Iterable[Currency],
            booking: Optional[EscapedString],
    ) -> _Self:
        label = OpenLabel.from_default()
        repeated_currencies = internal.Repeated.from_children(currencies, separators=cls._currencies.separators, separators_before=cls._currencies.separators_before)
        maybe_booking = internal.MaybeL.from_children(booking, separators=cls._booking.separators)
        tokens = [
            *date.detach(),
            Whitespace.from_default(),
            *label.detach(),
            Whitespace.from_default(),
            *account.detach(),
            *repeated_currencies.detach(),
            *maybe_booking.detach(),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        date.reattach(token_store)
        label.reattach(token_store)
        account.reattach(token_store)
        repeated_currencies.reattach(token_store)
        maybe_booking.reattach(token_store)
        return cls(token_store, date, label, account, repeated_currencies, maybe_booking)
