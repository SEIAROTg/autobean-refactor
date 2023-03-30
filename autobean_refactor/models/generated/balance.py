# DO NOT EDIT
# This file is automatically generated by autobean_refactor.modelgen.

import datetime
import decimal
from typing import Iterable, Iterator, Mapping, Optional, Self, final
from .. import base, internal, meta_item_internal
from ..account import Account
from ..block_comment import BlockComment
from ..currency import Currency
from ..date import Date
from ..inline_comment import InlineComment
from ..meta_item import MetaItem
from ..meta_value import MetaRawValue, MetaValue
from ..number_expr import NumberExpr
from ..punctuation import DedentMark, Eol
from ..spacing import Newline, Whitespace
from ..tolerance import Tolerance


@internal.token_model
class BalanceLabel(internal.SimpleDefaultRawTokenModel):
    RULE = 'BALANCE'
    DEFAULT = 'balance'


@internal.tree_model
class Balance(internal.SurroundingCommentsMixin, base.RawTreeModel, internal.SpacingAccessorsMixin):
    RULE = 'balance'

    indent_by = internal.data_field[str]()

    _date = internal.required_field[Date]()
    _label = internal.required_field[BalanceLabel]()
    _account = internal.required_field[Account]()
    _number = internal.required_field[NumberExpr]()
    _tolerance = internal.optional_left_field[Tolerance](separators=(Whitespace.from_default(),))
    _currency = internal.required_field[Currency]()
    _inline_comment = internal.optional_left_field[InlineComment](separators=(Whitespace.from_default(),))
    _eol = internal.required_field[Eol]()
    _meta = internal.repeated_field[MetaItem | BlockComment](separators=(Newline.from_default(),))
    _dedent_mark = internal.optional_left_field[DedentMark](separators=())

    @internal.custom_property
    def _leading_comment_pivot(self) -> base.RawTokenModel:
        return self._date.first_token

    @internal.custom_property
    def _tolerance_pivot(self) -> base.RawTokenModel:
        return self._number.last_token

    @internal.custom_property
    def _inline_comment_pivot(self) -> base.RawTokenModel:
        return self._currency.last_token

    @internal.custom_property
    def _dedent_mark_pivot(self) -> base.RawTokenModel:
        return self._meta.last_token or self._eol.last_token

    @internal.custom_property
    def _trailing_comment_pivot(self) -> base.RawTokenModel:
        return (self._dedent_mark and self._dedent_mark.last_token) or self._meta.last_token or self._eol.last_token

    raw_leading_comment = internal.optional_node_property(internal.SurroundingCommentsMixin._leading_comment, _leading_comment_pivot)
    raw_date = internal.required_node_property(_date)
    raw_account = internal.required_node_property(_account)
    raw_number = internal.required_node_property(_number)
    raw_tolerance = internal.optional_node_property(_tolerance, _tolerance_pivot)
    raw_currency = internal.required_node_property(_currency)
    raw_inline_comment = internal.optional_node_property(_inline_comment, _inline_comment_pivot)
    raw_meta_with_comments = internal.repeated_node_with_interleaving_comments_property(_meta)
    raw_meta = meta_item_internal.repeated_raw_meta_item_property(raw_meta_with_comments)
    raw_trailing_comment = internal.optional_node_property(internal.SurroundingCommentsMixin._trailing_comment, _trailing_comment_pivot)

    leading_comment = internal.optional_string_property(raw_leading_comment, BlockComment)
    date = internal.required_value_property(raw_date)
    account = internal.required_value_property(raw_account)
    number = internal.required_value_property(raw_number)
    tolerance = internal.optional_decimal_property(raw_tolerance, Tolerance)
    currency = internal.required_value_property(raw_currency)
    inline_comment = internal.optional_string_property(raw_inline_comment, InlineComment)
    meta = meta_item_internal.repeated_meta_item_property(raw_meta_with_comments, indent_by)
    trailing_comment = internal.optional_string_property(raw_trailing_comment, BlockComment)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            leading_comment: Optional[BlockComment],
            date: Date,
            label: BalanceLabel,
            account: Account,
            number: NumberExpr,
            tolerance: Optional[Tolerance],
            currency: Currency,
            inline_comment: Optional[InlineComment],
            eol: Eol,
            repeated_meta: internal.Repeated[MetaItem | BlockComment],
            dedent_mark: Optional[DedentMark],
            trailing_comment: Optional[BlockComment],
            *,
            indent_by: str = '    ',
    ):
        super().__init__(token_store)
        self._leading_comment = leading_comment
        self._date = date
        self._label = label
        self._account = account
        self._number = number
        self._tolerance = tolerance
        self._currency = currency
        self._inline_comment = inline_comment
        self._eol = eol
        self._meta = repeated_meta
        self._dedent_mark = dedent_mark
        self._trailing_comment = trailing_comment
        self.indent_by = indent_by

    @property
    def first_token(self) -> base.RawTokenModel:
        return (self._leading_comment and self._leading_comment.first_token) or self._date.first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return (self._trailing_comment and self._trailing_comment.last_token) or (self._dedent_mark and self._dedent_mark.last_token) or self._meta.last_token or self._eol.last_token

    def clone(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> Self:
        return type(self)(
            token_store,
            type(self)._leading_comment.clone(self._leading_comment, token_store, token_transformer),
            type(self)._date.clone(self._date, token_store, token_transformer),
            type(self)._label.clone(self._label, token_store, token_transformer),
            type(self)._account.clone(self._account, token_store, token_transformer),
            type(self)._number.clone(self._number, token_store, token_transformer),
            type(self)._tolerance.clone(self._tolerance, token_store, token_transformer),
            type(self)._currency.clone(self._currency, token_store, token_transformer),
            type(self)._inline_comment.clone(self._inline_comment, token_store, token_transformer),
            type(self)._eol.clone(self._eol, token_store, token_transformer),
            type(self)._meta.clone(self._meta, token_store, token_transformer),
            type(self)._dedent_mark.clone(self._dedent_mark, token_store, token_transformer),
            type(self)._trailing_comment.clone(self._trailing_comment, token_store, token_transformer),
            indent_by=self.indent_by,
        )

    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._leading_comment = type(self)._leading_comment.reattach(self._leading_comment, token_store, token_transformer)
        self._date = type(self)._date.reattach(self._date, token_store, token_transformer)
        self._label = type(self)._label.reattach(self._label, token_store, token_transformer)
        self._account = type(self)._account.reattach(self._account, token_store, token_transformer)
        self._number = type(self)._number.reattach(self._number, token_store, token_transformer)
        self._tolerance = type(self)._tolerance.reattach(self._tolerance, token_store, token_transformer)
        self._currency = type(self)._currency.reattach(self._currency, token_store, token_transformer)
        self._inline_comment = type(self)._inline_comment.reattach(self._inline_comment, token_store, token_transformer)
        self._eol = type(self)._eol.reattach(self._eol, token_store, token_transformer)
        self._meta = type(self)._meta.reattach(self._meta, token_store, token_transformer)
        self._dedent_mark = type(self)._dedent_mark.reattach(self._dedent_mark, token_store, token_transformer)
        self._trailing_comment = type(self)._trailing_comment.reattach(self._trailing_comment, token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, Balance)
            and self._leading_comment == other._leading_comment
            and self._date == other._date
            and self._label == other._label
            and self._account == other._account
            and self._number == other._number
            and self._tolerance == other._tolerance
            and self._currency == other._currency
            and self._inline_comment == other._inline_comment
            and self._eol == other._eol
            and self._meta == other._meta
            and self._dedent_mark == other._dedent_mark
            and self._trailing_comment == other._trailing_comment
            and self.indent_by == other.indent_by
        )

    @classmethod
    def from_children(
            cls,
            date: Date,
            account: Account,
            number: NumberExpr,
            tolerance: Optional[Tolerance],
            currency: Currency,
            *,
            leading_comment: Optional[BlockComment] = None,
            inline_comment: Optional[InlineComment] = None,
            meta: Iterable[MetaItem | BlockComment] = (),
            trailing_comment: Optional[BlockComment] = None,
            indent_by: str = '    ',
    ) -> Self:
        label = BalanceLabel.from_default()
        eol = Eol.from_default()
        repeated_meta = cls._meta.create_repeated(meta)
        dedent_mark = None
        tokens = [
            *cls._leading_comment.detach_with_separators(leading_comment),
            *date.detach(),
            Whitespace.from_default(),
            *label.detach(),
            Whitespace.from_default(),
            *account.detach(),
            Whitespace.from_default(),
            *number.detach(),
            *cls._tolerance.detach_with_separators(tolerance),
            Whitespace.from_default(),
            *currency.detach(),
            *cls._inline_comment.detach_with_separators(inline_comment),
            *eol.detach(),
            *cls._meta.detach_with_separators(repeated_meta),
            *cls._dedent_mark.detach_with_separators(dedent_mark),
            *cls._trailing_comment.detach_with_separators(trailing_comment),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        cls._leading_comment.reattach(leading_comment, token_store)
        cls._date.reattach(date, token_store)
        cls._label.reattach(label, token_store)
        cls._account.reattach(account, token_store)
        cls._number.reattach(number, token_store)
        cls._tolerance.reattach(tolerance, token_store)
        cls._currency.reattach(currency, token_store)
        cls._inline_comment.reattach(inline_comment, token_store)
        cls._eol.reattach(eol, token_store)
        cls._meta.reattach(repeated_meta, token_store)
        cls._dedent_mark.reattach(dedent_mark, token_store)
        cls._trailing_comment.reattach(trailing_comment, token_store)
        return cls(token_store, leading_comment, date, label, account, number, tolerance, currency, inline_comment, eol, repeated_meta, dedent_mark, trailing_comment, indent_by=indent_by)

    @classmethod
    def from_value(
            cls,
            date: datetime.date,
            account: str,
            number: decimal.Decimal,
            tolerance: Optional[decimal.Decimal],
            currency: str,
            *,
            leading_comment: Optional[str] = None,
            inline_comment: Optional[str] = None,
            meta: Optional[Mapping[str, MetaValue | MetaRawValue]] = None,
            trailing_comment: Optional[str] = None,
            indent_by: str = '    ',
    ) -> Self:
        return cls.from_children(
            leading_comment=BlockComment.from_value(leading_comment) if leading_comment is not None else None,
            date=Date.from_value(date),
            account=Account.from_value(account),
            number=NumberExpr.from_value(number),
            tolerance=Tolerance.from_value(tolerance) if tolerance is not None else None,
            currency=Currency.from_value(currency),
            inline_comment=InlineComment.from_value(inline_comment) if inline_comment is not None else None,
            meta=meta_item_internal.from_mapping(meta, indent=indent_by) if meta is not None else (),
            trailing_comment=BlockComment.from_value(trailing_comment) if trailing_comment is not None else None,
            indent_by=indent_by,
        )

    def auto_claim_comments(self) -> None:
        self.claim_leading_comment(ignore_if_already_claimed=True)
        self.claim_trailing_comment(ignore_if_already_claimed=True)
        type(self)._trailing_comment.auto_claim_comments(self._trailing_comment)
        self.raw_meta_with_comments.auto_claim_comments()
        type(self)._inline_comment.auto_claim_comments(self._inline_comment)
        type(self)._currency.auto_claim_comments(self._currency)
        type(self)._tolerance.auto_claim_comments(self._tolerance)
        type(self)._number.auto_claim_comments(self._number)
        type(self)._account.auto_claim_comments(self._account)
        type(self)._date.auto_claim_comments(self._date)
        type(self)._leading_comment.auto_claim_comments(self._leading_comment)

    def iter_children_formatted(self) -> Iterator[tuple[base.RawModel, bool]]:
        yield from type(self)._leading_comment.iter_children_formatted(self._leading_comment, False)
        yield from type(self)._date.iter_children_formatted(self._date, False)
        yield Whitespace.from_default(), False
        yield from type(self)._label.iter_children_formatted(self._label, False)
        yield Whitespace.from_default(), False
        yield from type(self)._account.iter_children_formatted(self._account, False)
        yield Whitespace.from_default(), False
        yield from type(self)._number.iter_children_formatted(self._number, False)
        yield from type(self)._tolerance.iter_children_formatted(self._tolerance, False)
        yield Whitespace.from_default(), False
        yield from type(self)._currency.iter_children_formatted(self._currency, False)
        yield from type(self)._inline_comment.iter_children_formatted(self._inline_comment, False)
        yield from type(self)._eol.iter_children_formatted(self._eol, False)
        yield from type(self)._meta.iter_children_formatted(self._meta, True)
        yield from type(self)._dedent_mark.iter_children_formatted(self._dedent_mark, False)
        yield from type(self)._trailing_comment.iter_children_formatted(self._trailing_comment, False)
