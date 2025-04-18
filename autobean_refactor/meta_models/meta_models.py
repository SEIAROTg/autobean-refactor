# pylance: disable
# type: ignore

from typing import Optional, Union
from .base import BlockCommentable, Inline, MetaModel, Floating, field

_META = field(
    separators=('Newline.from_default()',),
    indented=True,
    is_optional=True,
    is_keyword_only=True,
    default_value={},
    has_interleaving_comments=True)


# Auxiliary


class NumberUnaryExpr(MetaModel, Inline):
    """Unary number expression (e.g. `-42.00`)."""
    unary_op: 'UNARY_OP' = field(define_as='UnaryOp')
    operand: 'number_atom_expr' = field(has_circular_dep=True, separators=())


class NumberParenExpr(MetaModel, Inline):
    """Parentheses-enclosed number expression (e.g. `(42.00)`)."""
    _left_paren: 'LEFT_PAREN' = field(define_as='LeftParen')
    inner_expr: 'number_add_expr' = field(has_circular_dep=True, separators=())
    _right_paren: 'RIGHT_PAREN' = field(define_as='RightParen', separators=())


class NumberExpr(MetaModel, Inline):
    """Number expression."""
    number_add_expr: 'number_add_expr' = field(has_circular_dep=True)


class Amount(MetaModel, Inline):
    """Amount (e.g. `100.00 USD`)."""
    number: 'number_expr'
    currency: 'CURRENCY'


class Tolerance(MetaModel, Inline):
    """Tolerance (e.g. `~ 0.01`)."""
    _tilde: 'TILDE' = field(define_as='Tilde')
    number: 'number_expr'


class UnitPrice(MetaModel, Inline):
    """Unit price (e.g. `@ 10.00 USD`)."""
    _label: 'AT' = field(define_as='At')
    number: Optional['number_expr'] = field(floating=Floating.LEFT)
    currency: Optional['CURRENCY'] = field(floating=Floating.LEFT)


class TotalPrice(MetaModel, Inline):
    """Total price (e.g. `@@ 10.00 USD`)."""
    _label: 'ATAT' = field(define_as='AtAt')
    number: Optional['number_expr'] = field(floating=Floating.LEFT)
    currency: Optional['CURRENCY'] = field(floating=Floating.LEFT)


class CompoundAmount(MetaModel, Inline):
    """Compound amount (e.g. `1.00 # 10.00 USD`)."""
    number_per: Optional['number_expr'] = field(floating=Floating.RIGHT)
    _hash: 'HASH' = field(define_as='Hash')
    number_total: Optional['number_expr'] = field(floating=Floating.LEFT)
    currency: 'CURRENCY'


class UnitCost(MetaModel, Inline):
    """Unit cost (e.g. `{10.00 USD}`)."""
    _left_brace: 'LEFT_BRACE' = field(define_as='LeftBrace')
    components: list['cost_component'] = field(
        separators=('Comma.from_default()', 'Whitespace.from_default()'),
        separators_before=())
    _right_brace: 'RIGHT_BRACE' = field(define_as='RightBrace', separators=())


class TotalCost(MetaModel, Inline):
    """Total cost (e.g. `{{10.00 USD}}`)."""
    _dbl_left_brace: 'DBL_LEFT_BRACE' = field(define_as='DblLeftBrace')
    components: list['cost_component'] = field(
        separators=('Comma.from_default()', 'Whitespace.from_default()'),
        separators_before=())
    _dbl_right_brace: 'DBL_RIGHT_BRACE' = field(define_as='DblRightBrace', separators=())


class CostSpec(MetaModel, Inline):
    """Unit cost or total cost."""
    cost: Union['unit_cost', 'total_cost']


class Posting(MetaModel, BlockCommentable):
    """Posting (e.g. `Assets:Foo -10.00 USD`)."""
    indent: 'INDENT' = field(is_optional=True, is_keyword_only=True, default_value=' ' * 4)
    flag: Optional['POSTING_FLAG'] = field(floating=Floating.RIGHT, is_optional=True, is_keyword_only=True)
    account: 'ACCOUNT' = field(separators=())
    number: Optional['number_expr'] = field(floating=Floating.LEFT)
    currency: Optional['CURRENCY'] = field(floating=Floating.LEFT)
    cost: Optional['cost_spec'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    price: Optional[Union['unit_price', 'total_price']] = field(
        floating=Floating.LEFT, type_alias='PriceAnnotation', is_optional=True, is_keyword_only=True)
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())
    meta: list['meta_item'] = _META


class MetaItem(MetaModel, BlockCommentable):
    """Meta item (e.g. `foo: "bar"`)."""
    indent: 'INDENT' = field(is_optional=True, is_keyword_only=True, default_value=' ' * 4)
    key: 'META_KEY' = field(separators=())
    value: Optional['meta_value'] = field(floating=Floating.LEFT, type_alias='MetaRawValue')
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())


# Directives


class Include(MetaModel, BlockCommentable):
    """Include directive (e.g. `include "foo.bean"`)."""
    _label: 'INCLUDE' = field(define_as='IncludeLabel')
    filename: 'ESCAPED_STRING'
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())


class Option(MetaModel, BlockCommentable):
    """Option directive (e.g. `option "title" "foo"`)."""
    _label: 'OPTION' = field(define_as='OptionLabel')
    key: 'ESCAPED_STRING'
    value: 'ESCAPED_STRING'
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())


class Plugin(MetaModel, BlockCommentable):
    """Plugin directive (e.g. `plugin "foo"`)."""
    _label: 'PLUGIN' = field(define_as='PluginLabel')
    name: 'ESCAPED_STRING'
    config: Optional['ESCAPED_STRING'] = field(floating=Floating.LEFT, is_optional=True)
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())


class Popmeta(MetaModel, BlockCommentable):
    """Popmeta directive (e.g. `popmeta foo:`)."""
    _label: 'POPMETA' = field(define_as='PopmetaLabel')
    key: 'META_KEY'
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())


class Poptag(MetaModel, BlockCommentable):
    """Poptag directive (e.g. `poptag #foo`)."""
    _label: 'POPTAG' = field(define_as='PoptagLabel')
    tag: 'TAG'
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())


class Pushmeta(MetaModel, BlockCommentable):
    """Pushmeta directive (e.g. `pushmeta foo: "bar"`)."""
    _label: 'PUSHMETA' = field(define_as='PushmetaLabel')
    key: 'META_KEY'
    value: Optional['meta_value'] = field(floating=Floating.LEFT, type_alias='MetaRawValue')
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())


class Pushtag(MetaModel, BlockCommentable):
    """Pushtag directive (e.g. `pushtag #foo`)."""
    _label: 'PUSHTAG' = field(define_as='PushtagLabel')
    tag: 'TAG'
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())


class IgnoredLine(MetaModel, BlockCommentable):
    """Ignored line (e.g. `* title`).

    Lines starting with certain characters are ignored in beancount. This models captures those lines.
    """
    ignored: 'IGNORED'
    _eol: 'EOL' = field(separators=())


# Entries


class Balance(MetaModel, BlockCommentable):
    """Balance entry (e.g. `2000-01-01 balance Assets:Foo 100.00 USD`)."""
    date: 'DATE'
    _label: 'BALANCE' = field(define_as='BalanceLabel')
    account: 'ACCOUNT'
    number: 'number_expr'
    tolerance: Optional['tolerance'] = field(floating=Floating.LEFT)
    currency: 'CURRENCY'
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())
    meta: list['meta_item'] = _META
    _dedent_mark: Optional['DEDENT_MARK'] = field(floating=Floating.LEFT, separators=())


class Close(MetaModel, BlockCommentable):
    """Close entry (e.g. `2000-01-01 close Assets:Foo`)."""
    date: 'DATE'
    _label: 'CLOSE' = field(define_as='CloseLabel')
    account: 'ACCOUNT'
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())
    meta: list['meta_item'] = _META
    _dedent_mark: Optional['DEDENT_MARK'] = field(floating=Floating.LEFT, separators=())


class Commodity(MetaModel, BlockCommentable):
    """Commodity entry (e.g. `2000-01-01 commodity USD`)."""
    date: 'DATE'
    _label: 'COMMODITY' = field(define_as='CommodityLabel')
    currency: 'CURRENCY'
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())
    meta: list['meta_item'] = _META
    _dedent_mark: Optional['DEDENT_MARK'] = field(floating=Floating.LEFT, separators=())


class Event(MetaModel, BlockCommentable):
    """Event entry (e.g. `2000-01-01 event "foo" "bar"`)."""
    date: 'DATE'
    _label: 'EVENT' = field(define_as='EventLabel')
    type: 'ESCAPED_STRING'
    description: 'ESCAPED_STRING'
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())
    meta: list['meta_item'] = _META
    _dedent_mark: Optional['DEDENT_MARK'] = field(floating=Floating.LEFT, separators=())


class Pad(MetaModel, BlockCommentable):
    """Pad entry (e.g. `2000-01-01 pad Assets:Foo Equity:Opening-Balances`)."""
    date: 'DATE'
    _label: 'PAD' = field(define_as='PadLabel')
    account: 'ACCOUNT'
    source_account: 'ACCOUNT'
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())
    meta: list['meta_item'] = _META
    _dedent_mark: Optional['DEDENT_MARK'] = field(floating=Floating.LEFT, separators=())


class Price(MetaModel, BlockCommentable):
    """Price entry (e.g. `2000-01-01 price GBP 2.00 USD`)."""
    date: 'DATE'
    _label: 'PRICE' = field(define_as='PriceLabel')
    currency: 'CURRENCY'
    amount: 'amount'
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())
    meta: list['meta_item'] = _META
    _dedent_mark: Optional['DEDENT_MARK'] = field(floating=Floating.LEFT, separators=())


class Query(MetaModel, BlockCommentable):
    """Query entry (e.g. `2000-01-01 query "foo" "..."`)."""
    date: 'DATE'
    _label: 'QUERY' = field(define_as='QueryLabel')
    name: 'ESCAPED_STRING'
    query_string: 'ESCAPED_STRING'
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())
    meta: list['meta_item'] = _META
    _dedent_mark: Optional['DEDENT_MARK'] = field(floating=Floating.LEFT, separators=())


class Note(MetaModel, BlockCommentable):
    """Note entry (e.g. `2000-01-01 note Assets:Foo "foo"`)."""
    date: 'DATE'
    _label: 'NOTE' = field(define_as='NoteLabel')
    account: 'ACCOUNT'
    comment: 'ESCAPED_STRING'
    tags_links: list[Union['TAG', 'LINK']] = field(is_optional=True, is_keyword_only=True)
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())
    meta: list['meta_item'] = _META
    _dedent_mark: Optional['DEDENT_MARK'] = field(floating=Floating.LEFT, separators=())


class Document(MetaModel, BlockCommentable):
    """Document entry (e.g. `2000-01-01 balance Assets:Foo "foo.pdf"`)."""
    date: 'DATE'
    _label: 'DOCUMENT' = field(define_as='DocumentLabel')
    account: 'ACCOUNT'
    filename: 'ESCAPED_STRING'
    tags_links: list[Union['TAG', 'LINK']] = field(is_optional=True, is_keyword_only=True)
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())
    meta: list['meta_item'] = _META
    _dedent_mark: Optional['DEDENT_MARK'] = field(floating=Floating.LEFT, separators=())


class Open(MetaModel, BlockCommentable):
    """Open entry (e.g. `2000-01-01 open Assets:Foo`)."""
    date: 'DATE'
    _label: 'OPEN' = field(define_as='OpenLabel')
    account: 'ACCOUNT'
    currencies: list['CURRENCY'] = field(
        separators=('Comma.from_default()', 'Whitespace.from_default()'),
        separators_before=('Whitespace.from_default()',),
        is_optional=True)
    booking: Optional['ESCAPED_STRING'] = field(floating=Floating.LEFT, is_optional=True)
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())
    meta: list['meta_item'] = _META
    _dedent_mark: Optional['DEDENT_MARK'] = field(floating=Floating.LEFT, separators=())


class Custom(MetaModel, BlockCommentable):
    """Custom entry (e.g. `2000-01-01 custom "foo" "bar"`)."""
    date: 'DATE'
    _label: 'CUSTOM' = field(define_as='CustomLabel')
    type: 'ESCAPED_STRING'
    values: list[Union[
        'ESCAPED_STRING',
        'DATE',
        'BOOL',
        'amount',
        'number_expr',
        'ACCOUNT',
    ]] = field(type_alias='CustomRawValue')
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())
    meta: list['meta_item'] = _META
    _dedent_mark: Optional['DEDENT_MARK'] = field(floating=Floating.LEFT, separators=())


class Transaction(MetaModel, BlockCommentable):
    """Transaction entry (e.g. `2000-01-01 *`)."""
    date: 'DATE'
    flag: 'TRANSACTION_FLAG'
    string0: Optional['ESCAPED_STRING'] = field(floating=Floating.LEFT)
    string1: Optional['ESCAPED_STRING'] = field(floating=Floating.LEFT)
    string2: Optional['ESCAPED_STRING'] = field(floating=Floating.LEFT)
    tags_links: list[Union['TAG', 'LINK']] = field(is_optional=True, is_keyword_only=True)
    inline_comment: Optional['INLINE_COMMENT'] = field(floating=Floating.LEFT, is_optional=True, is_keyword_only=True)
    _eol: 'EOL' = field(separators=())
    meta: list['meta_item'] = _META
    postings: list['posting'] = field(
        separators=('Newline.from_default()',),
        indented=True,
        has_interleaving_comments=True)
    _dedent_mark: Optional['DEDENT_MARK'] = field(floating=Floating.LEFT, separators=())


# File


class File(MetaModel):
    """Contains everything in a file."""
    directives: list[Union[
        'option',
        'include',
        'plugin',
        'pushtag',
        'poptag',
        'pushmeta',
        'popmeta',
        'balance',
        'close',
        'commodity',
        'pad',
        'event',
        'query',
        'price',
        'note',
        'document',
        'open',
        'custom',
        'transaction',
        'ignored_line',
    ]] = field(
        type_alias='Directive',
        separators=('Newline.from_default()', 'Newline.from_default()'),
        separators_before=(),
        has_interleaving_comments=True,
    )
