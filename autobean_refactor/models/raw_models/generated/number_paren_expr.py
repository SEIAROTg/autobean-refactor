# DO NOT EDIT
# This file is automatically generated by autobean_refactor.modelgen.

from typing import TYPE_CHECKING, Type, TypeVar, final
from .. import base
from .. import internal
from ..punctuation import Whitespace
if TYPE_CHECKING:
  from ..number_expr import NumberAddExpr

_Self = TypeVar('_Self', bound='NumberParenExpr')


@internal.token_model
class LeftParen(internal.SimpleDefaultRawTokenModel):
    RULE = 'LEFT_PAREN'
    DEFAULT = '('


@internal.token_model
class RightParen(internal.SimpleDefaultRawTokenModel):
    RULE = 'RIGHT_PAREN'
    DEFAULT = ')'


@internal.tree_model
class NumberParenExpr(base.RawTreeModel):
    RULE = 'number_paren_expr'

    _left_paren = internal.required_field[LeftParen]()
    _inner_expr = internal.required_field['NumberAddExpr']()
    _right_paren = internal.required_field[RightParen]()

    raw_inner_expr = internal.required_node_property(_inner_expr)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            left_paren: LeftParen,
            inner_expr: 'NumberAddExpr',
            right_paren: RightParen,
    ):
        super().__init__(token_store)
        self._left_paren = left_paren
        self._inner_expr = inner_expr
        self._right_paren = right_paren

    @property
    def first_token(self) -> base.RawTokenModel:
        return self._left_paren.first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return self._right_paren.last_token

    def clone(self: _Self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> _Self:
        return type(self)(
            token_store,
            self._left_paren.clone(token_store, token_transformer),
            self._inner_expr.clone(token_store, token_transformer),
            self._right_paren.clone(token_store, token_transformer),
        )
    
    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._left_paren = self._left_paren.reattach(token_store, token_transformer)
        self._inner_expr = self._inner_expr.reattach(token_store, token_transformer)
        self._right_paren = self._right_paren.reattach(token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, NumberParenExpr)
            and self._left_paren == other._left_paren
            and self._inner_expr == other._inner_expr
            and self._right_paren == other._right_paren
        )

    @classmethod
    def from_children(
            cls: Type[_Self],
            inner_expr: 'NumberAddExpr',
    ) -> _Self:
        left_paren = LeftParen.from_default()
        right_paren = RightParen.from_default()
        tokens = [
            *left_paren.detach(),
            Whitespace.from_default(),
            *inner_expr.detach(),
            Whitespace.from_default(),
            *right_paren.detach(),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        left_paren.reattach(token_store)
        inner_expr.reattach(token_store)
        right_paren.reattach(token_store)
        return cls(token_store, left_paren, inner_expr, right_paren)
