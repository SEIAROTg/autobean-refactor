# DO NOT EDIT
# This file is automatically generated by autobean_refactor.modelgen.

import datetime
from typing import Iterable, Mapping, Optional, Type, TypeVar, final
from .. import base, internal, meta_item_internal
from ..date import Date
from ..escaped_string import EscapedString
from ..meta_item import MetaItem
from ..meta_value import MetaRawValue, MetaValue
from ..punctuation import Eol, Newline, Whitespace

_Self = TypeVar('_Self', bound='Query')


@internal.token_model
class QueryLabel(internal.SimpleDefaultRawTokenModel):
    RULE = 'QUERY'
    DEFAULT = 'query'


@internal.tree_model
class Query(base.RawTreeModel):
    RULE = 'query'

    _date = internal.required_field[Date]()
    _label = internal.required_field[QueryLabel]()
    _name = internal.required_field[EscapedString]()
    _query_string = internal.required_field[EscapedString]()
    _eol = internal.required_field[Eol]()
    _meta = internal.repeated_field[MetaItem](separators=(Newline.from_default(),), default_indent='    ')

    raw_date = internal.required_node_property(_date)
    raw_name = internal.required_node_property(_name)
    raw_query_string = internal.required_node_property(_query_string)
    raw_meta = meta_item_internal.repeated_raw_meta_item_property(_meta)

    date = internal.required_date_property(raw_date)
    name = internal.required_string_property(raw_name)
    query_string = internal.required_string_property(raw_query_string)
    meta = meta_item_internal.repeated_meta_item_property(_meta)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            date: Date,
            label: QueryLabel,
            name: EscapedString,
            query_string: EscapedString,
            eol: Eol,
            meta: internal.Repeated[MetaItem],
    ):
        super().__init__(token_store)
        self._date = date
        self._label = label
        self._name = name
        self._query_string = query_string
        self._eol = eol
        self._meta = meta

    @property
    def first_token(self) -> base.RawTokenModel:
        return self._date.first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return self._meta.last_token

    def clone(self: _Self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> _Self:
        return type(self)(
            token_store,
            self._date.clone(token_store, token_transformer),
            self._label.clone(token_store, token_transformer),
            self._name.clone(token_store, token_transformer),
            self._query_string.clone(token_store, token_transformer),
            self._eol.clone(token_store, token_transformer),
            self._meta.clone(token_store, token_transformer),
        )

    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._date = self._date.reattach(token_store, token_transformer)
        self._label = self._label.reattach(token_store, token_transformer)
        self._name = self._name.reattach(token_store, token_transformer)
        self._query_string = self._query_string.reattach(token_store, token_transformer)
        self._eol = self._eol.reattach(token_store, token_transformer)
        self._meta = self._meta.reattach(token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, Query)
            and self._date == other._date
            and self._label == other._label
            and self._name == other._name
            and self._query_string == other._query_string
            and self._eol == other._eol
            and self._meta == other._meta
        )

    @classmethod
    def from_children(
            cls: Type[_Self],
            date: Date,
            name: EscapedString,
            query_string: EscapedString,
            meta: Iterable[MetaItem] = (),
    ) -> _Self:
        label = QueryLabel.from_default()
        eol = Eol.from_default()
        repeated_meta = cls._meta.create_repeated(meta)
        tokens = [
            *date.detach(),
            Whitespace.from_default(),
            *label.detach(),
            Whitespace.from_default(),
            *name.detach(),
            Whitespace.from_default(),
            *query_string.detach(),
            *eol.detach(),
            *repeated_meta.detach(),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        date.reattach(token_store)
        label.reattach(token_store)
        name.reattach(token_store)
        query_string.reattach(token_store)
        eol.reattach(token_store)
        repeated_meta.reattach(token_store)
        return cls(token_store, date, label, name, query_string, eol, repeated_meta)

    @classmethod
    def from_value(
            cls: Type[_Self],
            date: datetime.date,
            name: str,
            query_string: str,
            *,
            meta: Optional[Mapping[str, MetaValue | MetaRawValue]] = None,
    ) -> _Self:
        return cls.from_children(
            Date.from_value(date),
            EscapedString.from_value(name),
            EscapedString.from_value(query_string),
            meta_item_internal.from_mapping(meta) if meta is not None else (),
        )
