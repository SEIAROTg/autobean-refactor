import datetime
import decimal
from typing import Optional, Type, TypeVar
from autobean_refactor.models.raw_models import balance
from autobean_refactor.models.raw_models.balance import BalanceLabel, Tilde
from . import internal
from .account import Account
from .currency import Currency
from .date import Date
from .number_expr import NumberExpr

internal.token_model(Tilde)
internal.token_model(BalanceLabel)

_Self = TypeVar('_Self', bound='Balance')


@internal.tree_model
class Balance(balance.Balance):
    date = internal.required_date_property(balance.Balance.raw_date)
    account = internal.required_string_property(balance.Balance.raw_account)
    number = internal.required_number_expr_property(balance.Balance.raw_number)
    tolerance = internal.optional_number_expr_property(balance.Balance.raw_tolerance)
    currency = internal.required_string_property(balance.Balance.raw_currency)

    @classmethod
    def from_value(
            cls: Type[_Self],
            date: datetime.date,
            account: str,
            number: decimal.Decimal,
            tolerance: Optional[decimal.Decimal],
            currency: str,
    ) -> _Self:
        return cls.from_children(
            Date.from_value(date),
            Account.from_value(account),
            NumberExpr.from_value(number),
            NumberExpr.from_value(tolerance) if tolerance is not None else None,
            Currency.from_value(currency))
