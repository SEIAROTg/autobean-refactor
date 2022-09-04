import datetime
from typing import Optional
import pytest
from autobean_refactor import models
from .. import base


_CLOSE_LEADING = '''\
; foo
; bar
2000-01-01 close Assets:Foo ; baz\
'''
_CLOSE_TRAILING = '''\
2000-01-01 close Assets:Foo ; baz
; qux
; quxx\
'''
_CLOSE_BOTH = '''\
; foo
; bar
2000-01-01 close Assets:Foo ; baz
; qux
; quxx\
'''
_CLOSE_NEITHER = '''\
2000-01-01 close Assets:Foo ; baz\
'''
_SET_TESTCASES = [
    (None, None, _CLOSE_NEITHER),
    ('foo\nbar', None, _CLOSE_LEADING),
    (None, 'qux\nquxx', _CLOSE_TRAILING),
    ('foo\nbar', 'qux\nquxx', _CLOSE_BOTH),
]


class TestSurroundingComment(base.BaseTestModel):

    @pytest.mark.parametrize(
        'leading_comment,trailing_comment,expected_text', _SET_TESTCASES,
    )
    def test_set_raw_comment(self, leading_comment: Optional[str], trailing_comment: Optional[str], expected_text: str) -> None:
        model = self.parser.parse(_CLOSE_NEITHER, models.Close)
        raw_leading_comment = models.BlockComment.from_value(leading_comment) if leading_comment else None
        model.raw_leading_comment = raw_leading_comment
        assert model.raw_leading_comment is raw_leading_comment
        raw_trailing_comment = models.BlockComment.from_value(trailing_comment) if trailing_comment else None
        model.raw_trailing_comment = raw_trailing_comment
        assert model.raw_trailing_comment is raw_trailing_comment
        assert self.print_model(model) == expected_text
        self.check_deepcopy_tree(model)

    @pytest.mark.parametrize(
        'leading_comment,trailing_comment,expected_text', _SET_TESTCASES,
    )
    def test_set_comment(self, leading_comment: Optional[str], trailing_comment: Optional[str], expected_text: str) -> None:
        close = self.parser.parse(_CLOSE_NEITHER, models.Close)
        close.leading_comment = leading_comment
        assert close.leading_comment == leading_comment
        close.trailing_comment = trailing_comment
        assert close.trailing_comment == trailing_comment
        assert self.print_model(close) == expected_text
        self.check_deepcopy_tree(close)

    @pytest.mark.parametrize(
        'leading_comment,trailing_comment,expected_text', _SET_TESTCASES,
    )
    def test_from_children(self, leading_comment: Optional[str], trailing_comment: Optional[str], expected_text: str) -> None:
        date = models.Date.from_value(datetime.date(2000, 1, 1))
        account = models.Account.from_value('Assets:Foo')
        inline_comment = models.InlineComment.from_value('baz')
        raw_leading_comment = models.BlockComment.from_value(leading_comment) if leading_comment else None
        raw_trailing_comment = models.BlockComment.from_value(trailing_comment) if trailing_comment else None
        close = models.Close.from_children(
            date,
            account,
            inline_comment=inline_comment,
            leading_comment=raw_leading_comment,
            trailing_comment=raw_trailing_comment)
        assert close.raw_leading_comment is raw_leading_comment
        assert close.raw_trailing_comment is raw_trailing_comment
        assert self.print_model(close) == expected_text
        self.check_deepcopy_tree(close)

    @pytest.mark.parametrize(
        'leading_comment,trailing_comment,expected_text', _SET_TESTCASES,
    )
    def test_from_value(self, leading_comment: Optional[str], trailing_comment: Optional[str], expected_text: str) -> None:
        close = models.Close.from_value(
            datetime.date(2000, 1, 1),
            'Assets:Foo',
            inline_comment='baz',
            leading_comment=leading_comment,
            trailing_comment=trailing_comment)
        assert close.leading_comment == leading_comment
        assert close.trailing_comment == trailing_comment
        assert self.print_model(close) == expected_text
        self.check_deepcopy_tree(close)
