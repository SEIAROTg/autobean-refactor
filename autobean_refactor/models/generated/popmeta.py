# DO NOT EDIT
# This file is automatically generated by autobean_refactor.modelgen.

from typing import Optional, Type, TypeVar, final
from .. import base, internal
from ..block_comment import BlockComment
from ..inline_comment import InlineComment
from ..meta_key import MetaKey
from ..punctuation import Eol, Newline, Whitespace

_Self = TypeVar('_Self', bound='Popmeta')


@internal.token_model
class PopmetaLabel(internal.SimpleDefaultRawTokenModel):
    RULE = 'POPMETA'
    DEFAULT = 'popmeta'


@internal.tree_model
class Popmeta(base.RawTreeModel):
    RULE = 'popmeta'

    _leading_comment = internal.optional_right_field[BlockComment](separators=(Newline.from_default(),))
    _label = internal.required_field[PopmetaLabel]()
    _key = internal.required_field[MetaKey]()
    _inline_comment = internal.optional_left_field[InlineComment](separators=(Whitespace.from_default(),))
    _eol = internal.required_field[Eol]()
    _trailing_comment = internal.optional_left_field[BlockComment](separators=(Newline.from_default(),))

    raw_leading_comment = internal.optional_node_property(_leading_comment)
    raw_key = internal.required_node_property(_key)
    raw_inline_comment = internal.optional_node_property(_inline_comment)
    raw_trailing_comment = internal.optional_node_property(_trailing_comment)

    leading_comment = internal.optional_string_property(raw_leading_comment, BlockComment)
    key = internal.required_string_property(raw_key)
    inline_comment = internal.optional_string_property(raw_inline_comment, InlineComment)
    trailing_comment = internal.optional_string_property(raw_trailing_comment, BlockComment)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            leading_comment: internal.Maybe[BlockComment],
            label: PopmetaLabel,
            key: MetaKey,
            inline_comment: internal.Maybe[InlineComment],
            eol: Eol,
            trailing_comment: internal.Maybe[BlockComment],
    ):
        super().__init__(token_store)
        self._leading_comment = leading_comment
        self._label = label
        self._key = key
        self._inline_comment = inline_comment
        self._eol = eol
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
            self._label.clone(token_store, token_transformer),
            self._key.clone(token_store, token_transformer),
            self._inline_comment.clone(token_store, token_transformer),
            self._eol.clone(token_store, token_transformer),
            self._trailing_comment.clone(token_store, token_transformer),
        )

    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._leading_comment = self._leading_comment.reattach(token_store, token_transformer)
        self._label = self._label.reattach(token_store, token_transformer)
        self._key = self._key.reattach(token_store, token_transformer)
        self._inline_comment = self._inline_comment.reattach(token_store, token_transformer)
        self._eol = self._eol.reattach(token_store, token_transformer)
        self._trailing_comment = self._trailing_comment.reattach(token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, Popmeta)
            and self._leading_comment == other._leading_comment
            and self._label == other._label
            and self._key == other._key
            and self._inline_comment == other._inline_comment
            and self._eol == other._eol
            and self._trailing_comment == other._trailing_comment
        )

    @classmethod
    def from_children(
            cls: Type[_Self],
            key: MetaKey,
            *,
            leading_comment: Optional[BlockComment] = None,
            inline_comment: Optional[InlineComment] = None,
            trailing_comment: Optional[BlockComment] = None,
    ) -> _Self:
        maybe_leading_comment = cls._leading_comment.create_maybe(leading_comment)
        label = PopmetaLabel.from_default()
        maybe_inline_comment = cls._inline_comment.create_maybe(inline_comment)
        eol = Eol.from_default()
        maybe_trailing_comment = cls._trailing_comment.create_maybe(trailing_comment)
        tokens = [
            *maybe_leading_comment.detach(),
            *label.detach(),
            Whitespace.from_default(),
            *key.detach(),
            *maybe_inline_comment.detach(),
            *eol.detach(),
            *maybe_trailing_comment.detach(),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        maybe_leading_comment.reattach(token_store)
        label.reattach(token_store)
        key.reattach(token_store)
        maybe_inline_comment.reattach(token_store)
        eol.reattach(token_store)
        maybe_trailing_comment.reattach(token_store)
        return cls(token_store, maybe_leading_comment, label, key, maybe_inline_comment, eol, maybe_trailing_comment)

    @classmethod
    def from_value(
            cls: Type[_Self],
            key: str,
            *,
            leading_comment: Optional[str] = None,
            inline_comment: Optional[str] = None,
            trailing_comment: Optional[str] = None,
    ) -> _Self:
        return cls.from_children(
            leading_comment=BlockComment.from_value(leading_comment) if leading_comment is not None else None,
            key=MetaKey.from_value(key),
            inline_comment=InlineComment.from_value(inline_comment) if inline_comment is not None else None,
            trailing_comment=BlockComment.from_value(trailing_comment) if trailing_comment is not None else None,
        )
