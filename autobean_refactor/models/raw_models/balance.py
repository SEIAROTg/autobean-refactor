from typing import Optional, TypeVar, Type, final
from autobean_refactor.models.raw_models import punctuation
from . import base
from . import internal
from .account import Account
from .currency import Currency
from .date import Date
from .number_expr import NumberExpr
from .tolerance import Tolerance

_Self = TypeVar('_Self', bound='Balance')


@internal.token_model
class BalanceLabel(internal.SimpleDefaultRawTokenModel):
    RULE = 'BALANCE'
    DEFAULT = 'balance'


@internal.tree_model
class Balance(base.RawTreeModel):
    RULE = 'balance'

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            date: Date,
            label: BalanceLabel,
            account: Account,
            number: NumberExpr,
            tolerance: internal.Maybe[Tolerance],
            currency: Currency,
    ):
        super().__init__(token_store)
        self._date = date
        self._label = label
        self._account = account
        self._number = number
        self._tolerance = tolerance
        self._currency = currency

    @property
    def first_token(self) -> base.RawTokenModel:
        return self._date

    @property
    def last_token(self) -> base.RawTokenModel:
        return self._currency

    _date = internal.required_field[Date]()
    _label = internal.required_field[BalanceLabel]()
    _account = internal.required_field[Account]()
    _number = internal.required_field[NumberExpr]()
    _tolerance = internal.optional_field[Tolerance](floating=internal.Floating.LEFT, separators=(punctuation.Whitespace.from_default(),))
    _currency = internal.required_field[Currency]()
  
    raw_date = internal.required_node_property(_date)
    raw_account = internal.required_node_property(_account)
    raw_number = internal.required_node_property(_number)
    raw_tolerance = internal.optional_node_property(_tolerance)
    raw_currency = internal.required_node_property(_currency)

    def clone(self: _Self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> _Self:
        return type(self)(
            token_store,
            self._date.clone(token_store, token_transformer),
            self._label.clone(token_store, token_transformer),
            self._account.clone(token_store, token_transformer),
            self._number.clone(token_store, token_transformer),
            self._tolerance.clone(token_store, token_transformer),
            self._currency.clone(token_store, token_transformer))
    
    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._date = self._date.reattach(token_store, token_transformer)
        self._label = self._label.reattach(token_store, token_transformer)
        self._account = self._account.reattach(token_store, token_transformer)
        self._number = self._number.reattach(token_store, token_transformer)
        self._tolerance = self._tolerance.reattach(token_store, token_transformer)
        self._currency = self._currency.reattach(token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, Balance)
            and self._date == other._date
            and self._account == other._account
            and self._number == other._number
            and self._tolerance == other._tolerance
            and self._currency == other._currency)

    @classmethod
    def from_children(
            cls: Type[_Self],
            date: Date,
            account: Account,
            number: NumberExpr,
            tolerance: Optional[Tolerance],
            currency: Currency,
    ) -> _Self:
        label = BalanceLabel.from_default()
        maybe_tolerance = internal.MaybeL.from_children(tolerance, separators=cls._tolerance.separators)
        tokens = [
            *date.detach(),
            punctuation.Whitespace.from_default(),
            label,
            punctuation.Whitespace.from_default(),
            *account.detach(),
            punctuation.Whitespace.from_default(),
            *number.detach(),
            *maybe_tolerance.detach(),
            punctuation.Whitespace.from_default(),
            *currency.detach(),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        number.reattach(token_store)
        maybe_tolerance.reattach(token_store)
        return cls(token_store, date, label, account, number, maybe_tolerance, currency)
