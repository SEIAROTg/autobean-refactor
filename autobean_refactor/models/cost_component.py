from .date import Date
from .punctuation import Asterisk
from .escaped_string import EscapedString
from .currency import Currency
from .number_expr import NumberExpr
from .compound_amount import CompoundAmount

CostComponent = Date | Asterisk | EscapedString | Currency | NumberExpr | CompoundAmount
