# DO NOT EDIT
# This file is automatically generated by autobean_refactor.modelgen.

from typing import Iterable, Optional, Type, TypeVar, final
from .. import base, internal, meta_item_internal
from ..block_comment import BlockComment
from ..date import Date
from ..escaped_string import EscapedString
from ..inline_comment import InlineComment
from ..link import Link
from ..meta_item import MetaItem
from ..posting import Posting
from ..punctuation import DedentMark, Eol, IndentMark
from ..spacing import Newline, Whitespace
from ..tag import Tag
from ..transaction_flag import TransactionFlag

_Self = TypeVar('_Self', bound='Transaction')


@internal.tree_model
class Transaction(internal.SurroundingCommentsMixin, base.RawTreeModel, internal.SpacingAccessorsMixin):
    RULE = 'transaction'

    _date = internal.required_field[Date]()
    _flag = internal.required_field[TransactionFlag]()
    _string0 = internal.optional_left_field[EscapedString](separators=(Whitespace.from_default(),))
    _string1 = internal.optional_left_field[EscapedString](separators=(Whitespace.from_default(),))
    _string2 = internal.optional_left_field[EscapedString](separators=(Whitespace.from_default(),))
    _tags_links = internal.repeated_field[Link | Tag](separators=(Whitespace.from_default(),))
    _inline_comment = internal.optional_left_field[InlineComment](separators=(Whitespace.from_default(),))
    _eol = internal.required_field[Eol]()
    _indent_mark = internal.optional_left_field[IndentMark](separators=())
    _meta = internal.repeated_field[MetaItem](separators=(Newline.from_default(),), default_indent='    ')
    _postings = internal.repeated_field[Posting](separators=(Newline.from_default(),), default_indent='    ')
    _dedent_mark = internal.optional_left_field[DedentMark](separators=())

    raw_leading_comment = internal.optional_node_property(internal.SurroundingCommentsMixin._leading_comment)
    raw_date = internal.required_node_property(_date)
    raw_flag = internal.required_node_property(_flag)
    raw_string0 = internal.optional_node_property(_string0)
    raw_string1 = internal.optional_node_property(_string1)
    raw_string2 = internal.optional_node_property(_string2)
    raw_tags_links = internal.repeated_node_property(_tags_links)
    raw_inline_comment = internal.optional_node_property(_inline_comment)
    raw_meta = meta_item_internal.repeated_raw_meta_item_property(_meta)
    raw_postings = internal.repeated_node_property(_postings)
    raw_trailing_comment = internal.optional_node_property(internal.SurroundingCommentsMixin._trailing_comment)

    leading_comment = internal.optional_string_property(raw_leading_comment, BlockComment)
    date = internal.required_value_property(raw_date)
    flag = internal.required_value_property(raw_flag)
    string0 = internal.optional_string_property(raw_string0, EscapedString)
    string1 = internal.optional_string_property(raw_string1, EscapedString)
    string2 = internal.optional_string_property(raw_string2, EscapedString)
    inline_comment = internal.optional_string_property(raw_inline_comment, InlineComment)
    meta = meta_item_internal.repeated_meta_item_property(_meta)
    postings = raw_postings
    trailing_comment = internal.optional_string_property(raw_trailing_comment, BlockComment)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            leading_comment: internal.Maybe[BlockComment],
            date: Date,
            flag: TransactionFlag,
            string0: internal.Maybe[EscapedString],
            string1: internal.Maybe[EscapedString],
            string2: internal.Maybe[EscapedString],
            tags_links: internal.Repeated[Link | Tag],
            inline_comment: internal.Maybe[InlineComment],
            eol: Eol,
            indent_mark: internal.Maybe[IndentMark],
            meta: internal.Repeated[MetaItem],
            postings: internal.Repeated[Posting],
            dedent_mark: internal.Maybe[DedentMark],
            trailing_comment: internal.Maybe[BlockComment],
    ):
        super().__init__(token_store)
        self._leading_comment = leading_comment
        self._date = date
        self._flag = flag
        self._string0 = string0
        self._string1 = string1
        self._string2 = string2
        self._tags_links = tags_links
        self._inline_comment = inline_comment
        self._eol = eol
        self._indent_mark = indent_mark
        self._meta = meta
        self._postings = postings
        self._dedent_mark = dedent_mark
        self._trailing_comment = trailing_comment

    @property
    def first_token(self) -> base.RawTokenModel:
        return self._leading_comment.first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return self._trailing_comment.last_token

    def clone(self: _Self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> _Self:
        return type(self)(
            token_store,
            self._leading_comment.clone(token_store, token_transformer),
            self._date.clone(token_store, token_transformer),
            self._flag.clone(token_store, token_transformer),
            self._string0.clone(token_store, token_transformer),
            self._string1.clone(token_store, token_transformer),
            self._string2.clone(token_store, token_transformer),
            self._tags_links.clone(token_store, token_transformer),
            self._inline_comment.clone(token_store, token_transformer),
            self._eol.clone(token_store, token_transformer),
            self._indent_mark.clone(token_store, token_transformer),
            self._meta.clone(token_store, token_transformer),
            self._postings.clone(token_store, token_transformer),
            self._dedent_mark.clone(token_store, token_transformer),
            self._trailing_comment.clone(token_store, token_transformer),
        )

    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._leading_comment = self._leading_comment.reattach(token_store, token_transformer)
        self._date = self._date.reattach(token_store, token_transformer)
        self._flag = self._flag.reattach(token_store, token_transformer)
        self._string0 = self._string0.reattach(token_store, token_transformer)
        self._string1 = self._string1.reattach(token_store, token_transformer)
        self._string2 = self._string2.reattach(token_store, token_transformer)
        self._tags_links = self._tags_links.reattach(token_store, token_transformer)
        self._inline_comment = self._inline_comment.reattach(token_store, token_transformer)
        self._eol = self._eol.reattach(token_store, token_transformer)
        self._indent_mark = self._indent_mark.reattach(token_store, token_transformer)
        self._meta = self._meta.reattach(token_store, token_transformer)
        self._postings = self._postings.reattach(token_store, token_transformer)
        self._dedent_mark = self._dedent_mark.reattach(token_store, token_transformer)
        self._trailing_comment = self._trailing_comment.reattach(token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, Transaction)
            and self._leading_comment == other._leading_comment
            and self._date == other._date
            and self._flag == other._flag
            and self._string0 == other._string0
            and self._string1 == other._string1
            and self._string2 == other._string2
            and self._tags_links == other._tags_links
            and self._inline_comment == other._inline_comment
            and self._eol == other._eol
            and self._indent_mark == other._indent_mark
            and self._meta == other._meta
            and self._postings == other._postings
            and self._dedent_mark == other._dedent_mark
            and self._trailing_comment == other._trailing_comment
        )

    @classmethod
    def from_children(
            cls: Type[_Self],
            date: Date,
            flag: TransactionFlag,
            string0: Optional[EscapedString],
            string1: Optional[EscapedString],
            string2: Optional[EscapedString],
            postings: Iterable[Posting],
            *,
            leading_comment: Optional[BlockComment] = None,
            tags_links: Iterable[Link | Tag] = (),
            inline_comment: Optional[InlineComment] = None,
            meta: Iterable[MetaItem] = (),
            trailing_comment: Optional[BlockComment] = None,
    ) -> _Self:
        maybe_leading_comment = cls._leading_comment.create_maybe(leading_comment)
        maybe_string0 = cls._string0.create_maybe(string0)
        maybe_string1 = cls._string1.create_maybe(string1)
        maybe_string2 = cls._string2.create_maybe(string2)
        repeated_tags_links = cls._tags_links.create_repeated(tags_links)
        maybe_inline_comment = cls._inline_comment.create_maybe(inline_comment)
        eol = Eol.from_default()
        maybe_indent_mark = cls._indent_mark.create_maybe(None)
        repeated_meta = cls._meta.create_repeated(meta)
        repeated_postings = cls._postings.create_repeated(postings)
        maybe_dedent_mark = cls._dedent_mark.create_maybe(None)
        maybe_trailing_comment = cls._trailing_comment.create_maybe(trailing_comment)
        tokens = [
            *maybe_leading_comment.detach(),
            *date.detach(),
            Whitespace.from_default(),
            *flag.detach(),
            *maybe_string0.detach(),
            *maybe_string1.detach(),
            *maybe_string2.detach(),
            *repeated_tags_links.detach(),
            *maybe_inline_comment.detach(),
            *eol.detach(),
            *maybe_indent_mark.detach(),
            *repeated_meta.detach(),
            *repeated_postings.detach(),
            *maybe_dedent_mark.detach(),
            *maybe_trailing_comment.detach(),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        maybe_leading_comment.reattach(token_store)
        date.reattach(token_store)
        flag.reattach(token_store)
        maybe_string0.reattach(token_store)
        maybe_string1.reattach(token_store)
        maybe_string2.reattach(token_store)
        repeated_tags_links.reattach(token_store)
        maybe_inline_comment.reattach(token_store)
        eol.reattach(token_store)
        maybe_indent_mark.reattach(token_store)
        repeated_meta.reattach(token_store)
        repeated_postings.reattach(token_store)
        maybe_dedent_mark.reattach(token_store)
        maybe_trailing_comment.reattach(token_store)
        return cls(token_store, maybe_leading_comment, date, flag, maybe_string0, maybe_string1, maybe_string2, repeated_tags_links, maybe_inline_comment, eol, maybe_indent_mark, repeated_meta, repeated_postings, maybe_dedent_mark, maybe_trailing_comment)
