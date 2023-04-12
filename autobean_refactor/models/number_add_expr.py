import decimal
from typing import Any, Iterator, Optional, cast, final, TYPE_CHECKING
from typing_extensions import Self
from . import base
from . import internal
from .spacing import Whitespace
if TYPE_CHECKING:
    from .number_mul_expr import NumberMulExpr
else:
    NumberMulExpr = Any


@internal.token_model
class AddOp(internal.SimpleRawTokenModel):
    RULE = 'ADD_OP'


@internal.tree_model
class NumberAddExpr(base.RawTreeModel):
    RULE = 'number_add_expr'

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            operands: tuple[NumberMulExpr, ...],
            ops: tuple[AddOp, ...],
    ):
        super().__init__(token_store)
        self._raw_operands = operands
        self._raw_ops = ops

    @classmethod
    def from_parsed_children(cls, token_store: base.TokenStore, *children: Optional[base.RawModel]) -> Self:
        return cls(
            token_store,
            cast(tuple[NumberMulExpr, ...], children[::2]),
            cast(tuple[AddOp, ...], children[1::2]))

    @property
    def first_token(self) -> base.RawTokenModel:
        return self._raw_operands[0].first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return self._raw_operands[-1].last_token

    @property
    def raw_operands(self) -> tuple[NumberMulExpr, ...]:
        return self._raw_operands

    @property
    def raw_ops(self) -> tuple[AddOp, ...]:
        return self._raw_ops

    @property
    def value(self) -> decimal.Decimal:
        value = self._raw_operands[0].value
        for op, operand in zip(self._raw_ops, self._raw_operands[1:]):
            if op.raw_text == '+':
                value += operand.value
            elif op.raw_text == '-':
                value -= operand.value
            else:
                assert False
        return value

    def clone(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> Self:
        ops = tuple(op.clone(token_store, token_transformer) for op in self._raw_ops)
        operands = tuple(operand.clone(token_store, token_transformer) for operand in self._raw_operands)
        return type(self)(token_store, operands, ops)

    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._raw_ops = tuple(op.reattach(token_store, token_transformer) for op in self._raw_ops)
        self._raw_operands = tuple(operand.reattach(token_store, token_transformer) for operand in self._raw_operands)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, NumberAddExpr)
            and self._raw_operands == other._raw_operands
            and self._raw_ops == other._raw_ops)

    def auto_claim_comments(self) -> None:
        pass  # no block comments

    @classmethod
    def from_children(cls, operands: tuple[NumberMulExpr, ...], ops: tuple[AddOp, ...]) -> Self:
        tokens = []
        for operand, op in zip(operands, ops):
            tokens.extend(operand.detach())
            tokens.append(Whitespace.from_default())
            tokens.extend(op.detach())
            tokens.append(Whitespace.from_default())
        tokens.extend(operands[-1].detach())
        token_store = base.TokenStore.from_tokens(tokens)
        for operand in operands:
            operand.reattach(token_store)
        for op in ops:
            op.reattach(token_store)
        return cls(token_store, operands, ops)

    def iter_children_formatted(self) -> Iterator[tuple[base.RawModel, bool]]:
        for operand, op in zip(self._raw_operands, self._raw_ops):
            yield operand, False
            yield Whitespace.from_default(), False
            yield op, False
            yield Whitespace.from_default(), False
        yield self._raw_operands[-1], False
