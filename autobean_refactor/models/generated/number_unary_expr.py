# DO NOT EDIT
# This file is automatically generated by autobean_refactor.modelgen.

from typing import Iterator, TYPE_CHECKING, final
from typing_extensions import Self
from .. import base, internal
if TYPE_CHECKING:
  from ..number_atom_expr import NumberAtomExpr


@internal.token_model
class UnaryOp(internal.SimpleRawTokenModel):
    RULE = 'UNARY_OP'


@internal.tree_model
class NumberUnaryExpr(base.RawTreeModel, internal.SpacingAccessorsMixin):
    RULE = 'number_unary_expr'
    INLINE = True

    _unary_op = internal.required_field[UnaryOp]()
    _operand = internal.required_field['NumberAtomExpr']()

    raw_unary_op = internal.required_node_property(_unary_op)
    raw_operand = internal.required_node_property(_operand)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            unary_op: UnaryOp,
            operand: 'NumberAtomExpr',
    ):
        super().__init__(token_store)
        self._unary_op = unary_op
        self._operand = operand

    @property
    def first_token(self) -> base.RawTokenModel:
        return self._unary_op.first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return self._operand.last_token

    def clone(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> Self:
        return type(self)(
            token_store,
            type(self)._unary_op.clone(self._unary_op, token_store, token_transformer),
            type(self)._operand.clone(self._operand, token_store, token_transformer),
        )

    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._unary_op = type(self)._unary_op.reattach(self._unary_op, token_store, token_transformer)
        self._operand = type(self)._operand.reattach(self._operand, token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, NumberUnaryExpr)
            and self._unary_op == other._unary_op
            and self._operand == other._operand
        )

    @classmethod
    def from_children(
            cls,
            unary_op: UnaryOp,
            operand: 'NumberAtomExpr',
    ) -> Self:
        tokens = [
            *unary_op.detach(),
            *operand.detach(),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        cls._unary_op.reattach(unary_op, token_store)
        cls._operand.reattach(operand, token_store)
        return cls(token_store, unary_op, operand)

    def auto_claim_comments(self) -> None:
        type(self)._operand.auto_claim_comments(self._operand)
        type(self)._unary_op.auto_claim_comments(self._unary_op)

    def iter_children_formatted(self) -> Iterator[tuple[base.RawModel, bool]]:
        yield from type(self)._unary_op.iter_children_formatted(self._unary_op, False)
        yield from type(self)._operand.iter_children_formatted(self._operand, False)
