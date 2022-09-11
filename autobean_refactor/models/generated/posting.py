# DO NOT EDIT
# This file is automatically generated by autobean_refactor.modelgen.

import decimal
from typing import Iterable, Mapping, Optional, Type, TypeVar, final
from .. import base, internal, meta_item_internal
from ..account import Account
from ..block_comment import BlockComment
from ..cost_spec import CostSpec
from ..currency import Currency
from ..inline_comment import InlineComment
from ..meta_item import MetaItem
from ..meta_value import MetaRawValue, MetaValue
from ..number_expr import NumberExpr
from ..posting_flag import PostingFlag
from ..punctuation import Eol, Indent
from ..spacing import Newline, Whitespace
from ..total_price import TotalPrice
from ..unit_price import UnitPrice

PriceAnnotation = TotalPrice | UnitPrice
_Self = TypeVar('_Self', bound='Posting')


@internal.tree_model
class Posting(internal.SurroundingCommentsMixin, base.RawTreeModel, internal.SpacingAccessorsMixin):
    RULE = 'posting'

    _indent = internal.required_field[Indent]()
    _flag = internal.optional_right_field[PostingFlag](separators=(Whitespace.from_default(),))
    _account = internal.required_field[Account]()
    _number = internal.optional_left_field[NumberExpr](separators=(Whitespace.from_default(),))
    _currency = internal.optional_left_field[Currency](separators=(Whitespace.from_default(),))
    _cost = internal.optional_left_field[CostSpec](separators=(Whitespace.from_default(),))
    _price = internal.optional_left_field[PriceAnnotation](separators=(Whitespace.from_default(),))
    _inline_comment = internal.optional_left_field[InlineComment](separators=(Whitespace.from_default(),))
    _eol = internal.required_field[Eol]()
    _meta = internal.repeated_field[MetaItem | BlockComment](separators=(Newline.from_default(),), default_indent='        ')

    raw_leading_comment = internal.optional_node_property(internal.SurroundingCommentsMixin._leading_comment)
    raw_indent = internal.required_node_property(_indent)
    raw_flag = internal.optional_node_property(_flag)
    raw_account = internal.required_node_property(_account)
    raw_number = internal.optional_node_property(_number)
    raw_currency = internal.optional_node_property(_currency)
    raw_cost = internal.optional_node_property(_cost)
    raw_price = internal.optional_node_property[PriceAnnotation](_price)
    raw_inline_comment = internal.optional_node_property(_inline_comment)
    raw_meta_with_comments = internal.repeated_node_with_interleaving_comments_property(_meta)
    raw_meta = meta_item_internal.repeated_raw_meta_item_property(raw_meta_with_comments)
    raw_trailing_comment = internal.optional_node_property(internal.SurroundingCommentsMixin._trailing_comment)

    leading_comment = internal.optional_indented_string_property(raw_leading_comment, BlockComment, raw_indent)
    indent = internal.required_value_property(raw_indent)
    flag = internal.optional_string_property(raw_flag, PostingFlag)
    account = internal.required_value_property(raw_account)
    number = internal.optional_decimal_property(raw_number, NumberExpr)
    currency = internal.optional_string_property(raw_currency, Currency)
    cost = raw_cost
    price = raw_price
    inline_comment = internal.optional_string_property(raw_inline_comment, InlineComment)
    meta = meta_item_internal.repeated_meta_item_property(raw_meta_with_comments)
    trailing_comment = internal.optional_indented_string_property(raw_trailing_comment, BlockComment, raw_indent)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            leading_comment: internal.Maybe[BlockComment],
            indent: Indent,
            flag: internal.Maybe[PostingFlag],
            account: Account,
            number: internal.Maybe[NumberExpr],
            currency: internal.Maybe[Currency],
            cost: internal.Maybe[CostSpec],
            price: internal.Maybe[PriceAnnotation],
            inline_comment: internal.Maybe[InlineComment],
            eol: Eol,
            meta: internal.Repeated[MetaItem | BlockComment],
            trailing_comment: internal.Maybe[BlockComment],
    ):
        super().__init__(token_store)
        self._leading_comment = leading_comment
        self._indent = indent
        self._flag = flag
        self._account = account
        self._number = number
        self._currency = currency
        self._cost = cost
        self._price = price
        self._inline_comment = inline_comment
        self._eol = eol
        self._meta = meta
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
            self._indent.clone(token_store, token_transformer),
            self._flag.clone(token_store, token_transformer),
            self._account.clone(token_store, token_transformer),
            self._number.clone(token_store, token_transformer),
            self._currency.clone(token_store, token_transformer),
            self._cost.clone(token_store, token_transformer),
            self._price.clone(token_store, token_transformer),
            self._inline_comment.clone(token_store, token_transformer),
            self._eol.clone(token_store, token_transformer),
            self._meta.clone(token_store, token_transformer),
            self._trailing_comment.clone(token_store, token_transformer),
        )

    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._leading_comment = self._leading_comment.reattach(token_store, token_transformer)
        self._indent = self._indent.reattach(token_store, token_transformer)
        self._flag = self._flag.reattach(token_store, token_transformer)
        self._account = self._account.reattach(token_store, token_transformer)
        self._number = self._number.reattach(token_store, token_transformer)
        self._currency = self._currency.reattach(token_store, token_transformer)
        self._cost = self._cost.reattach(token_store, token_transformer)
        self._price = self._price.reattach(token_store, token_transformer)
        self._inline_comment = self._inline_comment.reattach(token_store, token_transformer)
        self._eol = self._eol.reattach(token_store, token_transformer)
        self._meta = self._meta.reattach(token_store, token_transformer)
        self._trailing_comment = self._trailing_comment.reattach(token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, Posting)
            and self._leading_comment == other._leading_comment
            and self._indent == other._indent
            and self._flag == other._flag
            and self._account == other._account
            and self._number == other._number
            and self._currency == other._currency
            and self._cost == other._cost
            and self._price == other._price
            and self._inline_comment == other._inline_comment
            and self._eol == other._eol
            and self._meta == other._meta
            and self._trailing_comment == other._trailing_comment
        )

    @classmethod
    def from_children(
            cls: Type[_Self],
            account: Account,
            number: Optional[NumberExpr],
            currency: Optional[Currency],
            *,
            leading_comment: Optional[BlockComment] = None,
            indent: Indent,
            flag: Optional[PostingFlag] = None,
            cost: Optional[CostSpec] = None,
            price: Optional[PriceAnnotation] = None,
            inline_comment: Optional[InlineComment] = None,
            meta: Iterable[MetaItem | BlockComment] = (),
            trailing_comment: Optional[BlockComment] = None,
    ) -> _Self:
        maybe_leading_comment = cls._leading_comment.create_maybe(leading_comment)
        maybe_flag = cls._flag.create_maybe(flag)
        maybe_number = cls._number.create_maybe(number)
        maybe_currency = cls._currency.create_maybe(currency)
        maybe_cost = cls._cost.create_maybe(cost)
        maybe_price = cls._price.create_maybe(price)
        maybe_inline_comment = cls._inline_comment.create_maybe(inline_comment)
        eol = Eol.from_default()
        repeated_meta = cls._meta.create_repeated(meta)
        maybe_trailing_comment = cls._trailing_comment.create_maybe(trailing_comment)
        tokens = [
            *maybe_leading_comment.detach(),
            *indent.detach(),
            *maybe_flag.detach(),
            *account.detach(),
            *maybe_number.detach(),
            *maybe_currency.detach(),
            *maybe_cost.detach(),
            *maybe_price.detach(),
            *maybe_inline_comment.detach(),
            *eol.detach(),
            *repeated_meta.detach(),
            *maybe_trailing_comment.detach(),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        maybe_leading_comment.reattach(token_store)
        indent.reattach(token_store)
        maybe_flag.reattach(token_store)
        account.reattach(token_store)
        maybe_number.reattach(token_store)
        maybe_currency.reattach(token_store)
        maybe_cost.reattach(token_store)
        maybe_price.reattach(token_store)
        maybe_inline_comment.reattach(token_store)
        eol.reattach(token_store)
        repeated_meta.reattach(token_store)
        maybe_trailing_comment.reattach(token_store)
        return cls(token_store, maybe_leading_comment, indent, maybe_flag, account, maybe_number, maybe_currency, maybe_cost, maybe_price, maybe_inline_comment, eol, repeated_meta, maybe_trailing_comment)

    @classmethod
    def from_value(
            cls: Type[_Self],
            account: str,
            number: Optional[decimal.Decimal],
            currency: Optional[str],
            *,
            leading_comment: Optional[str] = None,
            indent: str = '    ',
            flag: Optional[str] = None,
            cost: Optional[CostSpec] = None,
            price: Optional[PriceAnnotation] = None,
            inline_comment: Optional[str] = None,
            meta: Optional[Mapping[str, MetaValue | MetaRawValue]] = None,
            trailing_comment: Optional[str] = None,
    ) -> _Self:
        return cls.from_children(
            leading_comment=BlockComment.from_value(leading_comment) if leading_comment is not None else None,
            indent=Indent.from_value(indent),
            flag=PostingFlag.from_value(flag) if flag is not None else None,
            account=Account.from_value(account),
            number=NumberExpr.from_value(number) if number is not None else None,
            currency=Currency.from_value(currency) if currency is not None else None,
            cost=cost,
            price=price,
            inline_comment=InlineComment.from_value(inline_comment) if inline_comment is not None else None,
            meta=meta_item_internal.from_mapping(meta) if meta is not None else (),
            trailing_comment=BlockComment.from_value(trailing_comment) if trailing_comment is not None else None,
        )
