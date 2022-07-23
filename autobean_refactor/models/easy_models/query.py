import datetime
from typing import Type, TypeVar
from autobean_refactor.models.raw_models import query
from autobean_refactor.models.raw_models.query import QueryLabel
from . import internal
from .escaped_string import EscapedString
from .date import Date

internal.token_model(QueryLabel)

_Self = TypeVar('_Self', bound='Query')


@internal.tree_model
class Query(query.Query):
    date = internal.required_date_property(query.Query.raw_date)
    name = internal.required_string_property(query.Query.raw_name)
    query_string = internal.required_string_property(query.Query.raw_query_string)

    @classmethod
    def from_value(cls: Type[_Self], date: datetime.date, name: str, query_string: str) -> _Self:
        return cls.from_children(
            Date.from_value(date),
            EscapedString.from_value(name),
            EscapedString.from_value(query_string))
