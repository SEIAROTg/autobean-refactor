import datetime
from typing import Type, TypeVar
from autobean_refactor.models.raw_models import pad
from autobean_refactor.models.raw_models.pad import PadLabel
from . import internal
from .account import Account
from .date import Date

internal.token_model(PadLabel)

_Self = TypeVar('_Self', bound='Pad')


@internal.tree_model
class Pad(pad.Pad):
    date = internal.required_date_property(pad.Pad.raw_date)
    account = internal.required_string_property(pad.Pad.raw_account)
    source_account = internal.required_string_property(pad.Pad.raw_source_account)

    @classmethod
    def from_value(cls: Type[_Self], date: datetime.date, account: str, source_account: str) -> _Self:
        return cls.from_children(
            Date.from_value(date),
            Account.from_value(account),
            Account.from_value(source_account))
