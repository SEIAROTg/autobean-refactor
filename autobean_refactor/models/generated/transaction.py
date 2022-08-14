# DO NOT EDIT
# This file is automatically generated by autobean_refactor.modelgen.

from typing import Iterable, Optional, Type, TypeVar, final
from .. import base, internal, meta_item_internal
from ..date import Date
from ..escaped_string import EscapedString
from ..link import Link
from ..meta_item import MetaItem
from ..posting import Posting
from ..punctuation import Eol, Newline, Whitespace
from ..tag import Tag
from ..transaction_flag import TransactionFlag

_Self = TypeVar('_Self', bound='Transaction')


@internal.tree_model
class Transaction(base.RawTreeModel):
    RULE = 'transaction'

    _date = internal.required_field[Date]()
    _flag = internal.required_field[TransactionFlag]()
    _string0 = internal.optional_field[EscapedString](separators=(Whitespace.from_default(),))
    _string1 = internal.optional_field[EscapedString](separators=(Whitespace.from_default(),))
    _string2 = internal.optional_field[EscapedString](separators=(Whitespace.from_default(),))
    _tags_links = internal.repeated_field[Link | Tag](separators=(Whitespace.from_default(),))
    _eol = internal.required_field[Eol]()
    _meta = internal.repeated_field[MetaItem](separators=(Newline.from_default(), Whitespace.from_raw_text('    ')))
    _postings = internal.repeated_field[Posting](separators=(Newline.from_default(), Whitespace.from_raw_text('    ')))

    raw_date = internal.required_node_property(_date)
    raw_flag = internal.required_node_property(_flag)
    raw_string0 = internal.optional_node_property(_string0)
    raw_string1 = internal.optional_node_property(_string1)
    raw_string2 = internal.optional_node_property(_string2)
    raw_tags_links = internal.repeated_node_property(_tags_links)
    raw_meta = meta_item_internal.repeated_raw_meta_item_property(_meta)
    raw_postings = internal.repeated_node_property(_postings)

    date = internal.required_date_property(raw_date)
    flag = internal.required_string_property(raw_flag)
    string0 = internal.optional_string_property(raw_string0, EscapedString)
    string1 = internal.optional_string_property(raw_string1, EscapedString)
    string2 = internal.optional_string_property(raw_string2, EscapedString)
    meta = meta_item_internal.repeated_meta_item_property(_meta)
    postings = raw_postings

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            date: Date,
            flag: TransactionFlag,
            string0: internal.Maybe[EscapedString],
            string1: internal.Maybe[EscapedString],
            string2: internal.Maybe[EscapedString],
            tags_links: internal.Repeated[Link | Tag],
            eol: Eol,
            meta: internal.Repeated[MetaItem],
            postings: internal.Repeated[Posting],
    ):
        super().__init__(token_store)
        self._date = date
        self._flag = flag
        self._string0 = string0
        self._string1 = string1
        self._string2 = string2
        self._tags_links = tags_links
        self._eol = eol
        self._meta = meta
        self._postings = postings

    @property
    def first_token(self) -> base.RawTokenModel:
        return self._date.first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return self._postings.last_token

    def clone(self: _Self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> _Self:
        return type(self)(
            token_store,
            self._date.clone(token_store, token_transformer),
            self._flag.clone(token_store, token_transformer),
            self._string0.clone(token_store, token_transformer),
            self._string1.clone(token_store, token_transformer),
            self._string2.clone(token_store, token_transformer),
            self._tags_links.clone(token_store, token_transformer),
            self._eol.clone(token_store, token_transformer),
            self._meta.clone(token_store, token_transformer),
            self._postings.clone(token_store, token_transformer),
        )

    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._date = self._date.reattach(token_store, token_transformer)
        self._flag = self._flag.reattach(token_store, token_transformer)
        self._string0 = self._string0.reattach(token_store, token_transformer)
        self._string1 = self._string1.reattach(token_store, token_transformer)
        self._string2 = self._string2.reattach(token_store, token_transformer)
        self._tags_links = self._tags_links.reattach(token_store, token_transformer)
        self._eol = self._eol.reattach(token_store, token_transformer)
        self._meta = self._meta.reattach(token_store, token_transformer)
        self._postings = self._postings.reattach(token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, Transaction)
            and self._date == other._date
            and self._flag == other._flag
            and self._string0 == other._string0
            and self._string1 == other._string1
            and self._string2 == other._string2
            and self._tags_links == other._tags_links
            and self._eol == other._eol
            and self._meta == other._meta
            and self._postings == other._postings
        )

    @classmethod
    def from_children(
            cls: Type[_Self],
            date: Date,
            flag: TransactionFlag,
            string0: Optional[EscapedString],
            string1: Optional[EscapedString],
            string2: Optional[EscapedString],
            tags_links: Iterable[Link | Tag],
            meta: Iterable[MetaItem],
            postings: Iterable[Posting],
    ) -> _Self:
        maybe_string0 = internal.MaybeL.from_children(string0, separators=cls._string0.separators)
        maybe_string1 = internal.MaybeL.from_children(string1, separators=cls._string1.separators)
        maybe_string2 = internal.MaybeL.from_children(string2, separators=cls._string2.separators)
        repeated_tags_links = internal.Repeated.from_children(tags_links, separators=cls._tags_links.separators)
        eol = Eol.from_default()
        repeated_meta = internal.Repeated.from_children(meta, separators=cls._meta.separators)
        repeated_postings = internal.Repeated.from_children(postings, separators=cls._postings.separators)
        tokens = [
            *date.detach(),
            Whitespace.from_default(),
            *flag.detach(),
            *maybe_string0.detach(),
            *maybe_string1.detach(),
            *maybe_string2.detach(),
            *repeated_tags_links.detach(),
            *eol.detach(),
            *repeated_meta.detach(),
            *repeated_postings.detach(),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        date.reattach(token_store)
        flag.reattach(token_store)
        maybe_string0.reattach(token_store)
        maybe_string1.reattach(token_store)
        maybe_string2.reattach(token_store)
        repeated_tags_links.reattach(token_store)
        eol.reattach(token_store)
        repeated_meta.reattach(token_store)
        repeated_postings.reattach(token_store)
        return cls(token_store, date, flag, maybe_string0, maybe_string1, maybe_string2, repeated_tags_links, eol, repeated_meta, repeated_postings)
