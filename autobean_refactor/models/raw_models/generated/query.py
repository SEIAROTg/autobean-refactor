# DO NOT EDIT
# This file is automatically generated by autobean_refactor.modelgen.

from typing import Type, TypeVar, final
from .. import base
from .. import internal
from ..date import Date
from ..escaped_string import EscapedString
from ..punctuation import Whitespace

_Self = TypeVar('_Self', bound='Query')


class QueryLabel(internal.SimpleDefaultRawTokenModel):
    RULE = 'QUERY'
    DEFAULT = 'query'


class Query(base.RawTreeModel):
    RULE = 'query'

    _date = internal.required_field[Date]()
    _label = internal.required_field[QueryLabel]()
    _name = internal.required_field[EscapedString]()
    _query_string = internal.required_field[EscapedString]()

    raw_date = internal.required_node_property(_date)
    raw_name = internal.required_node_property(_name)
    raw_query_string = internal.required_node_property(_query_string)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            date: Date,
            label: QueryLabel,
            name: EscapedString,
            query_string: EscapedString,
    ):
        super().__init__(token_store)
        self._date = date
        self._label = label
        self._name = name
        self._query_string = query_string

    @property
    def first_token(self) -> base.RawTokenModel:
        return self._date.first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return self._query_string.last_token

    def clone(self: _Self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> _Self:
        return type(self)(
            token_store,
            self._date.clone(token_store, token_transformer),
            self._label.clone(token_store, token_transformer),
            self._name.clone(token_store, token_transformer),
            self._query_string.clone(token_store, token_transformer),
        )
    
    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._date = self._date.reattach(token_store, token_transformer)
        self._label = self._label.reattach(token_store, token_transformer)
        self._name = self._name.reattach(token_store, token_transformer)
        self._query_string = self._query_string.reattach(token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, Query)
            and self._date == other._date
            and self._label == other._label
            and self._name == other._name
            and self._query_string == other._query_string
        )

    @classmethod
    def from_children(
            cls: Type[_Self],
            date: Date,
            name: EscapedString,
            query_string: EscapedString,
    ) -> _Self:
        label = QueryLabel.from_default()
        tokens = [
            *date.detach(),
            Whitespace.from_default(),
            *label.detach(),
            Whitespace.from_default(),
            *name.detach(),
            Whitespace.from_default(),
            *query_string.detach(),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        date.reattach(token_store)
        label.reattach(token_store)
        name.reattach(token_store)
        query_string.reattach(token_store)
        return cls(token_store, date, label, name, query_string)
