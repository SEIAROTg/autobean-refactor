# DO NOT EDIT
# This file is automatically generated by autobean_refactor.modelgen.

from typing import Iterator, Self, TYPE_CHECKING, final
from .. import base, internal
if TYPE_CHECKING:
  from ..number_add_expr import NumberAddExpr


@internal.tree_model
class NumberExpr(base.RawTreeModel, internal.SpacingAccessorsMixin):
    RULE = 'number_expr'
    INLINE = True

    _number_add_expr = internal.required_field['NumberAddExpr']()

    raw_number_add_expr = internal.required_node_property(_number_add_expr)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            number_add_expr: 'NumberAddExpr',
    ):
        super().__init__(token_store)
        self._number_add_expr = number_add_expr

    @property
    def first_token(self) -> base.RawTokenModel:
        return self._number_add_expr.first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return self._number_add_expr.last_token

    def clone(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> Self:
        return type(self)(
            token_store,
            type(self)._number_add_expr.clone(self._number_add_expr, token_store, token_transformer),
        )

    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._number_add_expr = type(self)._number_add_expr.reattach(self._number_add_expr, token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, NumberExpr)
            and self._number_add_expr == other._number_add_expr
        )

    @classmethod
    def from_children(
            cls,
            number_add_expr: 'NumberAddExpr',
    ) -> Self:
        tokens = [
            *number_add_expr.detach(),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        cls._number_add_expr.reattach(number_add_expr, token_store)
        return cls(token_store, number_add_expr)

    def auto_claim_comments(self) -> None:
        type(self)._number_add_expr.auto_claim_comments(self._number_add_expr)

    def iter_children_formatted(self) -> Iterator[tuple[base.RawModel, bool]]:
        yield from type(self)._number_add_expr.iter_children_formatted(self._number_add_expr, False)
