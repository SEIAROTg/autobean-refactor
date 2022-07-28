import datetime
from typing import Type, TypeVar
from autobean_refactor.models import raw_models
from autobean_refactor.models.raw_models import price
from autobean_refactor.models.raw_models.price import PriceLabel
from . import internal

internal.token_model(PriceLabel)

_Self = TypeVar('_Self', bound='Price')


@internal.tree_model
class Price(price.Price):
    date = internal.required_date_property(price.Price.raw_date)
    currency = internal.required_string_property(price.Price.raw_currency)
    amount = price.Price.raw_amount

    @classmethod
    def from_value(
            cls: Type[_Self],
            date: datetime.date,
            currency: str,
            amount: raw_models.Amount,
    ) -> _Self:
        return cls.from_children(
            raw_models.Date.from_value(date),
            raw_models.Currency.from_value(currency),
            amount,
        )
