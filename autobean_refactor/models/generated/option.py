# DO NOT EDIT
# This file is automatically generated by autobean_refactor.modelgen.

from typing import Iterator, Optional, Type, TypeVar, final
from .. import base, internal
from ..block_comment import BlockComment
from ..escaped_string import EscapedString
from ..inline_comment import InlineComment
from ..punctuation import Eol
from ..spacing import Newline, Whitespace

_Self = TypeVar('_Self', bound='Option')


@internal.token_model
class OptionLabel(internal.SimpleDefaultRawTokenModel):
    RULE = 'OPTION'
    DEFAULT = 'option'


@internal.tree_model
class Option(internal.SurroundingCommentsMixin, base.RawTreeModel, internal.SpacingAccessorsMixin):
    RULE = 'option'

    _label = internal.required_field[OptionLabel]()
    _key = internal.required_field[EscapedString]()
    _value = internal.required_field[EscapedString]()
    _inline_comment = internal.optional_left_field[InlineComment](separators=(Whitespace.from_default(),))
    _eol = internal.required_field[Eol]()

    @internal.custom_property
    def _leading_comment_pivot(self) -> base.RawTokenModel:
        return self._label.first_token

    @internal.custom_property
    def _inline_comment_pivot(self) -> base.RawTokenModel:
        return self._value.last_token

    @internal.custom_property
    def _trailing_comment_pivot(self) -> base.RawTokenModel:
        return self._eol.last_token

    raw_leading_comment = internal.optional_node_property(internal.SurroundingCommentsMixin._leading_comment, _leading_comment_pivot)
    raw_key = internal.required_node_property(_key)
    raw_value = internal.required_node_property(_value)
    raw_inline_comment = internal.optional_node_property(_inline_comment, _inline_comment_pivot)
    raw_trailing_comment = internal.optional_node_property(internal.SurroundingCommentsMixin._trailing_comment, _trailing_comment_pivot)

    leading_comment = internal.optional_string_property(raw_leading_comment, BlockComment)
    key = internal.required_value_property(raw_key)
    value = internal.required_value_property(raw_value)
    inline_comment = internal.optional_string_property(raw_inline_comment, InlineComment)
    trailing_comment = internal.optional_string_property(raw_trailing_comment, BlockComment)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            leading_comment: Optional[BlockComment],
            label: OptionLabel,
            key: EscapedString,
            value: EscapedString,
            inline_comment: Optional[InlineComment],
            eol: Eol,
            trailing_comment: Optional[BlockComment],
    ):
        super().__init__(token_store)
        self._leading_comment = leading_comment
        self._label = label
        self._key = key
        self._value = value
        self._inline_comment = inline_comment
        self._eol = eol
        self._trailing_comment = trailing_comment

    @property
    def first_token(self) -> base.RawTokenModel:
        return (self._leading_comment and self._leading_comment.first_token) or self._label.first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return (self._trailing_comment and self._trailing_comment.last_token) or self._eol.last_token

    def clone(self: _Self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> _Self:
        return type(self)(
            token_store,
            type(self)._leading_comment.clone(self._leading_comment, token_store, token_transformer),
            type(self)._label.clone(self._label, token_store, token_transformer),
            type(self)._key.clone(self._key, token_store, token_transformer),
            type(self)._value.clone(self._value, token_store, token_transformer),
            type(self)._inline_comment.clone(self._inline_comment, token_store, token_transformer),
            type(self)._eol.clone(self._eol, token_store, token_transformer),
            type(self)._trailing_comment.clone(self._trailing_comment, token_store, token_transformer),
        )

    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._leading_comment = type(self)._leading_comment.reattach(self._leading_comment, token_store, token_transformer)
        self._label = type(self)._label.reattach(self._label, token_store, token_transformer)
        self._key = type(self)._key.reattach(self._key, token_store, token_transformer)
        self._value = type(self)._value.reattach(self._value, token_store, token_transformer)
        self._inline_comment = type(self)._inline_comment.reattach(self._inline_comment, token_store, token_transformer)
        self._eol = type(self)._eol.reattach(self._eol, token_store, token_transformer)
        self._trailing_comment = type(self)._trailing_comment.reattach(self._trailing_comment, token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, Option)
            and self._leading_comment == other._leading_comment
            and self._label == other._label
            and self._key == other._key
            and self._value == other._value
            and self._inline_comment == other._inline_comment
            and self._eol == other._eol
            and self._trailing_comment == other._trailing_comment
        )

    @classmethod
    def from_children(
            cls: Type[_Self],
            key: EscapedString,
            value: EscapedString,
            *,
            leading_comment: Optional[BlockComment] = None,
            inline_comment: Optional[InlineComment] = None,
            trailing_comment: Optional[BlockComment] = None,
    ) -> _Self:
        label = OptionLabel.from_default()
        eol = Eol.from_default()
        tokens = [
            *cls._leading_comment.detach_with_separators(leading_comment),
            *label.detach(),
            Whitespace.from_default(),
            *key.detach(),
            Whitespace.from_default(),
            *value.detach(),
            *cls._inline_comment.detach_with_separators(inline_comment),
            *eol.detach(),
            *cls._trailing_comment.detach_with_separators(trailing_comment),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        cls._leading_comment.reattach(leading_comment, token_store)
        cls._label.reattach(label, token_store)
        cls._key.reattach(key, token_store)
        cls._value.reattach(value, token_store)
        cls._inline_comment.reattach(inline_comment, token_store)
        cls._eol.reattach(eol, token_store)
        cls._trailing_comment.reattach(trailing_comment, token_store)
        return cls(token_store, leading_comment, label, key, value, inline_comment, eol, trailing_comment)

    @classmethod
    def from_value(
            cls: Type[_Self],
            key: str,
            value: str,
            *,
            leading_comment: Optional[str] = None,
            inline_comment: Optional[str] = None,
            trailing_comment: Optional[str] = None,
    ) -> _Self:
        return cls.from_children(
            leading_comment=BlockComment.from_value(leading_comment) if leading_comment is not None else None,
            key=EscapedString.from_value(key),
            value=EscapedString.from_value(value),
            inline_comment=InlineComment.from_value(inline_comment) if inline_comment is not None else None,
            trailing_comment=BlockComment.from_value(trailing_comment) if trailing_comment is not None else None,
        )

    def auto_claim_comments(self) -> None:
        self.claim_leading_comment(ignore_if_already_claimed=True)
        self.claim_trailing_comment(ignore_if_already_claimed=True)
        type(self)._trailing_comment.auto_claim_comments(self._trailing_comment)
        type(self)._inline_comment.auto_claim_comments(self._inline_comment)
        type(self)._value.auto_claim_comments(self._value)
        type(self)._key.auto_claim_comments(self._key)
        type(self)._leading_comment.auto_claim_comments(self._leading_comment)

    def iter_children_formatted(self) -> Iterator[tuple[base.RawModel, bool]]:
        yield from type(self)._leading_comment.iter_children_formatted(self._leading_comment, False)
        yield from type(self)._label.iter_children_formatted(self._label, False)
        yield Whitespace.from_default(), False
        yield from type(self)._key.iter_children_formatted(self._key, False)
        yield Whitespace.from_default(), False
        yield from type(self)._value.iter_children_formatted(self._value, False)
        yield from type(self)._inline_comment.iter_children_formatted(self._inline_comment, False)
        yield from type(self)._eol.iter_children_formatted(self._eol, False)
        yield from type(self)._trailing_comment.iter_children_formatted(self._trailing_comment, False)
