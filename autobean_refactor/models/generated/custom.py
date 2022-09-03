# DO NOT EDIT
# This file is automatically generated by autobean_refactor.modelgen.

from typing import Iterable, Optional, Type, TypeVar, final
from .. import base, internal, meta_item_internal
from ..account import Account
from ..amount import Amount
from ..bool import Bool
from ..date import Date
from ..escaped_string import EscapedString
from ..inline_comment import InlineComment
from ..meta_item import MetaItem
from ..number_expr import NumberExpr
from ..punctuation import Eol, Newline, Whitespace

CustomRawValue = Account | Amount | Bool | Date | EscapedString | NumberExpr
_Self = TypeVar('_Self', bound='Custom')


@internal.token_model
class CustomLabel(internal.SimpleDefaultRawTokenModel):
    RULE = 'CUSTOM'
    DEFAULT = 'custom'


@internal.tree_model
class Custom(base.RawTreeModel):
    RULE = 'custom'

    _date = internal.required_field[Date]()
    _label = internal.required_field[CustomLabel]()
    _type = internal.required_field[EscapedString]()
    _values = internal.repeated_field[CustomRawValue](separators=(Whitespace.from_default(),))
    _inline_comment = internal.optional_left_field[InlineComment](separators=(Whitespace.from_default(),))
    _eol = internal.required_field[Eol]()
    _meta = internal.repeated_field[MetaItem](separators=(Newline.from_default(),), default_indent='    ')

    raw_date = internal.required_node_property(_date)
    raw_type = internal.required_node_property(_type)
    raw_values = internal.repeated_node_property(_values)
    raw_inline_comment = internal.optional_node_property(_inline_comment)
    raw_meta = meta_item_internal.repeated_raw_meta_item_property(_meta)

    date = internal.required_date_property(raw_date)
    type = internal.required_string_property(raw_type)
    inline_comment = internal.optional_string_property(raw_inline_comment, InlineComment)
    meta = meta_item_internal.repeated_meta_item_property(_meta)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            date: Date,
            label: CustomLabel,
            type: EscapedString,
            values: internal.Repeated[CustomRawValue],
            inline_comment: internal.Maybe[InlineComment],
            eol: Eol,
            meta: internal.Repeated[MetaItem],
    ):
        super().__init__(token_store)
        self._date = date
        self._label = label
        self._type = type
        self._values = values
        self._inline_comment = inline_comment
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
            self._type.clone(token_store, token_transformer),
            self._values.clone(token_store, token_transformer),
            self._inline_comment.clone(token_store, token_transformer),
            self._eol.clone(token_store, token_transformer),
            self._meta.clone(token_store, token_transformer),
        )

    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._date = self._date.reattach(token_store, token_transformer)
        self._label = self._label.reattach(token_store, token_transformer)
        self._type = self._type.reattach(token_store, token_transformer)
        self._values = self._values.reattach(token_store, token_transformer)
        self._inline_comment = self._inline_comment.reattach(token_store, token_transformer)
        self._eol = self._eol.reattach(token_store, token_transformer)
        self._meta = self._meta.reattach(token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, Custom)
            and self._date == other._date
            and self._label == other._label
            and self._type == other._type
            and self._values == other._values
            and self._inline_comment == other._inline_comment
            and self._eol == other._eol
            and self._meta == other._meta
        )

    @classmethod
    def from_children(
            cls: Type[_Self],
            date: Date,
            type: EscapedString,
            values: Iterable[CustomRawValue],
            *,
            inline_comment: Optional[InlineComment] = None,
            meta: Iterable[MetaItem] = (),
    ) -> _Self:
        label = CustomLabel.from_default()
        repeated_values = cls._values.create_repeated(values)
        maybe_inline_comment = cls._inline_comment.create_maybe(inline_comment)
        eol = Eol.from_default()
        repeated_meta = cls._meta.create_repeated(meta)
        tokens = [
            *date.detach(),
            Whitespace.from_default(),
            *label.detach(),
            Whitespace.from_default(),
            *type.detach(),
            *repeated_values.detach(),
            *maybe_inline_comment.detach(),
            *eol.detach(),
            *repeated_meta.detach(),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        date.reattach(token_store)
        label.reattach(token_store)
        type.reattach(token_store)
        repeated_values.reattach(token_store)
        maybe_inline_comment.reattach(token_store)
        eol.reattach(token_store)
        repeated_meta.reattach(token_store)
        return cls(token_store, date, label, type, repeated_values, maybe_inline_comment, eol, repeated_meta)
