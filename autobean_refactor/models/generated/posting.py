# DO NOT EDIT
# This file is automatically generated by autobean_refactor.modelgen.

import decimal
from typing import Iterable, Iterator, Mapping, Optional, Self, final
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


@internal.tree_model
class Posting(internal.SurroundingCommentsMixin, base.RawTreeModel, internal.SpacingAccessorsMixin):
    RULE = 'posting'

    indent_by = internal.data_field[str]()

    _indent = internal.required_field[Indent]()
    _flag = internal.optional_right_field[PostingFlag](separators=(Whitespace.from_default(),))
    _account = internal.required_field[Account]()
    _number = internal.optional_left_field[NumberExpr](separators=(Whitespace.from_default(),))
    _currency = internal.optional_left_field[Currency](separators=(Whitespace.from_default(),))
    _cost = internal.optional_left_field[CostSpec](separators=(Whitespace.from_default(),))
    _price = internal.optional_left_field[PriceAnnotation](separators=(Whitespace.from_default(),))
    _inline_comment = internal.optional_left_field[InlineComment](separators=(Whitespace.from_default(),))
    _eol = internal.required_field[Eol]()
    _meta = internal.repeated_field[MetaItem | BlockComment](separators=(Newline.from_default(),))

    @internal.custom_property
    def _leading_comment_pivot(self) -> base.RawTokenModel:
        return self._indent.first_token

    @internal.custom_property
    def _flag_pivot(self) -> base.RawTokenModel:
        return self._account.first_token

    @internal.custom_property
    def _number_pivot(self) -> base.RawTokenModel:
        return self._account.last_token

    @internal.custom_property
    def _currency_pivot(self) -> base.RawTokenModel:
        return (self._number and self._number.last_token) or self._account.last_token

    @internal.custom_property
    def _cost_pivot(self) -> base.RawTokenModel:
        return (self._currency and self._currency.last_token) or (self._number and self._number.last_token) or self._account.last_token

    @internal.custom_property
    def _price_pivot(self) -> base.RawTokenModel:
        return (self._cost and self._cost.last_token) or (self._currency and self._currency.last_token) or (self._number and self._number.last_token) or self._account.last_token

    @internal.custom_property
    def _inline_comment_pivot(self) -> base.RawTokenModel:
        return (self._price and self._price.last_token) or (self._cost and self._cost.last_token) or (self._currency and self._currency.last_token) or (self._number and self._number.last_token) or self._account.last_token

    @internal.custom_property
    def _trailing_comment_pivot(self) -> base.RawTokenModel:
        return self._meta.last_token or self._eol.last_token

    raw_leading_comment = internal.optional_node_property(internal.SurroundingCommentsMixin._leading_comment, _leading_comment_pivot)
    raw_indent = internal.required_node_property(_indent)
    raw_flag = internal.optional_node_property(_flag, _flag_pivot)
    raw_account = internal.required_node_property(_account)
    raw_number = internal.optional_node_property(_number, _number_pivot)
    raw_currency = internal.optional_node_property(_currency, _currency_pivot)
    raw_cost = internal.optional_node_property(_cost, _cost_pivot)
    raw_price = internal.optional_node_property(_price, _price_pivot)
    raw_inline_comment = internal.optional_node_property(_inline_comment, _inline_comment_pivot)
    raw_meta_with_comments = internal.repeated_node_with_interleaving_comments_property(_meta)
    raw_meta = meta_item_internal.repeated_raw_meta_item_property(raw_meta_with_comments)
    raw_trailing_comment = internal.optional_node_property(internal.SurroundingCommentsMixin._trailing_comment, _trailing_comment_pivot)

    leading_comment = internal.optional_indented_string_property(raw_leading_comment, BlockComment, raw_indent)
    indent = internal.required_value_property(raw_indent)
    flag = internal.optional_string_property(raw_flag, PostingFlag)
    account = internal.required_value_property(raw_account)
    number = internal.optional_decimal_property(raw_number, NumberExpr)
    currency = internal.optional_string_property(raw_currency, Currency)
    cost = raw_cost
    price = raw_price
    inline_comment = internal.optional_string_property(raw_inline_comment, InlineComment)
    meta = meta_item_internal.repeated_meta_item_property(raw_meta_with_comments, indent_by, raw_indent)
    trailing_comment = internal.optional_indented_string_property(raw_trailing_comment, BlockComment, raw_indent)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            leading_comment: Optional[BlockComment],
            indent: Indent,
            flag: Optional[PostingFlag],
            account: Account,
            number: Optional[NumberExpr],
            currency: Optional[Currency],
            cost: Optional[CostSpec],
            price: Optional[PriceAnnotation],
            inline_comment: Optional[InlineComment],
            eol: Eol,
            repeated_meta: internal.Repeated[MetaItem | BlockComment],
            trailing_comment: Optional[BlockComment],
            *,
            indent_by: str = '    ',
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
        self._meta = repeated_meta
        self._trailing_comment = trailing_comment
        self.indent_by = indent_by

    @property
    def first_token(self) -> base.RawTokenModel:
        return (self._leading_comment and self._leading_comment.first_token) or self._indent.first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return (self._trailing_comment and self._trailing_comment.last_token) or self._meta.last_token or self._eol.last_token

    def clone(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> Self:
        return type(self)(
            token_store,
            type(self)._leading_comment.clone(self._leading_comment, token_store, token_transformer),
            type(self)._indent.clone(self._indent, token_store, token_transformer),
            type(self)._flag.clone(self._flag, token_store, token_transformer),
            type(self)._account.clone(self._account, token_store, token_transformer),
            type(self)._number.clone(self._number, token_store, token_transformer),
            type(self)._currency.clone(self._currency, token_store, token_transformer),
            type(self)._cost.clone(self._cost, token_store, token_transformer),
            type(self)._price.clone(self._price, token_store, token_transformer),
            type(self)._inline_comment.clone(self._inline_comment, token_store, token_transformer),
            type(self)._eol.clone(self._eol, token_store, token_transformer),
            type(self)._meta.clone(self._meta, token_store, token_transformer),
            type(self)._trailing_comment.clone(self._trailing_comment, token_store, token_transformer),
            indent_by=self.indent_by,
        )

    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._leading_comment = type(self)._leading_comment.reattach(self._leading_comment, token_store, token_transformer)
        self._indent = type(self)._indent.reattach(self._indent, token_store, token_transformer)
        self._flag = type(self)._flag.reattach(self._flag, token_store, token_transformer)
        self._account = type(self)._account.reattach(self._account, token_store, token_transformer)
        self._number = type(self)._number.reattach(self._number, token_store, token_transformer)
        self._currency = type(self)._currency.reattach(self._currency, token_store, token_transformer)
        self._cost = type(self)._cost.reattach(self._cost, token_store, token_transformer)
        self._price = type(self)._price.reattach(self._price, token_store, token_transformer)
        self._inline_comment = type(self)._inline_comment.reattach(self._inline_comment, token_store, token_transformer)
        self._eol = type(self)._eol.reattach(self._eol, token_store, token_transformer)
        self._meta = type(self)._meta.reattach(self._meta, token_store, token_transformer)
        self._trailing_comment = type(self)._trailing_comment.reattach(self._trailing_comment, token_store, token_transformer)

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
            and self.indent_by == other.indent_by
        )

    @classmethod
    def from_children(
            cls,
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
            indent_by: str = '    ',
    ) -> Self:
        eol = Eol.from_default()
        repeated_meta = cls._meta.create_repeated(meta)
        tokens = [
            *cls._leading_comment.detach_with_separators(leading_comment),
            *indent.detach(),
            *cls._flag.detach_with_separators(flag),
            *account.detach(),
            *cls._number.detach_with_separators(number),
            *cls._currency.detach_with_separators(currency),
            *cls._cost.detach_with_separators(cost),
            *cls._price.detach_with_separators(price),
            *cls._inline_comment.detach_with_separators(inline_comment),
            *eol.detach(),
            *cls._meta.detach_with_separators(repeated_meta),
            *cls._trailing_comment.detach_with_separators(trailing_comment),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        cls._leading_comment.reattach(leading_comment, token_store)
        cls._indent.reattach(indent, token_store)
        cls._flag.reattach(flag, token_store)
        cls._account.reattach(account, token_store)
        cls._number.reattach(number, token_store)
        cls._currency.reattach(currency, token_store)
        cls._cost.reattach(cost, token_store)
        cls._price.reattach(price, token_store)
        cls._inline_comment.reattach(inline_comment, token_store)
        cls._eol.reattach(eol, token_store)
        cls._meta.reattach(repeated_meta, token_store)
        cls._trailing_comment.reattach(trailing_comment, token_store)
        return cls(token_store, leading_comment, indent, flag, account, number, currency, cost, price, inline_comment, eol, repeated_meta, trailing_comment, indent_by=indent_by)

    @classmethod
    def from_value(
            cls,
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
            indent_by: str = '    ',
    ) -> Self:
        return cls.from_children(
            leading_comment=BlockComment.from_value(leading_comment, indent=indent) if leading_comment is not None else None,
            indent=Indent.from_value(indent),
            flag=PostingFlag.from_value(flag) if flag is not None else None,
            account=Account.from_value(account),
            number=NumberExpr.from_value(number) if number is not None else None,
            currency=Currency.from_value(currency) if currency is not None else None,
            cost=cost,
            price=price,
            inline_comment=InlineComment.from_value(inline_comment) if inline_comment is not None else None,
            meta=meta_item_internal.from_mapping(meta, indent=indent + indent_by) if meta is not None else (),
            trailing_comment=BlockComment.from_value(trailing_comment, indent=indent) if trailing_comment is not None else None,
            indent_by=indent_by,
        )

    def auto_claim_comments(self) -> None:
        self.claim_leading_comment(ignore_if_already_claimed=True)
        self.claim_trailing_comment(ignore_if_already_claimed=True)
        type(self)._trailing_comment.auto_claim_comments(self._trailing_comment)
        self.raw_meta_with_comments.auto_claim_comments()
        type(self)._inline_comment.auto_claim_comments(self._inline_comment)
        type(self)._price.auto_claim_comments(self._price)
        type(self)._cost.auto_claim_comments(self._cost)
        type(self)._currency.auto_claim_comments(self._currency)
        type(self)._number.auto_claim_comments(self._number)
        type(self)._account.auto_claim_comments(self._account)
        type(self)._flag.auto_claim_comments(self._flag)
        type(self)._indent.auto_claim_comments(self._indent)
        type(self)._leading_comment.auto_claim_comments(self._leading_comment)

    def iter_children_formatted(self) -> Iterator[tuple[base.RawModel, bool]]:
        yield from type(self)._leading_comment.iter_children_formatted(self._leading_comment, False)
        yield from type(self)._indent.iter_children_formatted(self._indent, False)
        yield from type(self)._flag.iter_children_formatted(self._flag, False)
        yield from type(self)._account.iter_children_formatted(self._account, False)
        yield from type(self)._number.iter_children_formatted(self._number, False)
        yield from type(self)._currency.iter_children_formatted(self._currency, False)
        yield from type(self)._cost.iter_children_formatted(self._cost, False)
        yield from type(self)._price.iter_children_formatted(self._price, False)
        yield from type(self)._inline_comment.iter_children_formatted(self._inline_comment, False)
        yield from type(self)._eol.iter_children_formatted(self._eol, False)
        yield from type(self)._meta.iter_children_formatted(self._meta, True)
        yield from type(self)._trailing_comment.iter_children_formatted(self._trailing_comment, False)
