import datetime
from lark import exceptions
import pytest
from autobean_refactor import models
from .. import base


class TestClose(base.BaseTestModel):

    @pytest.mark.parametrize(
        'text,date,account', [
            ('2000-01-01 close Assets:Foo', datetime.date(2000, 1, 1), 'Assets:Foo'),
            ('2012-12-12  close  Assets:Bar', datetime.date(2012, 12, 12), 'Assets:Bar'),
        ],
    )
    def test_parse_success(
            self,
            text: str,
            date: datetime.date,
            account: str,
    ) -> None:
        close = self.parser.parse(text, models.Close)
        assert close.raw_date.value == date
        assert close.date == date
        assert close.raw_account.value == account
        assert close.account == account
        assert self.print_model(close) == text
        self.check_deepcopy_tree(close)
        self.check_reattach_tree(close)

    @pytest.mark.parametrize(
        'text', [
            '2000-01-01 cLose Assets:Foo',
            'close Assets:Foo',
            '2000-01-01 close',
        ],
    )
    def test_parse_failure(self, text: str) -> None:
        with pytest.raises(exceptions.UnexpectedInput):
            self.parser.parse(text, models.Close)

    def test_set_raw_date(self) -> None:
        close = self.parser.parse('2000-01-01  close Assets:Foo', models.Close)
        new_date = models.Date.from_value(datetime.date(2012, 12, 12))
        close.raw_date = new_date
        assert close.raw_date is new_date
        assert self.print_model(close) == '2012-12-12  close Assets:Foo'

    def test_set_date(self) -> None:
        close = self.parser.parse('2000-01-01  close Assets:Foo', models.Close)
        assert close.date == datetime.date(2000, 1, 1)
        close.date = datetime.date(2012, 12, 12)
        assert close.date == datetime.date(2012, 12, 12)
        assert self.print_model(close) == '2012-12-12  close Assets:Foo'

    def test_set_raw_account(self) -> None:
        close = self.parser.parse('2000-01-01  close Assets:Foo', models.Close)
        new_account = models.Account.from_value('Assets:Bar')
        close.raw_account = new_account
        assert close.raw_account is new_account
        assert self.print_model(close) == '2000-01-01  close Assets:Bar'

    def test_set_account(self) -> None:
        close = self.parser.parse('2000-01-01  close Assets:Foo', models.Close)
        assert close.account == 'Assets:Foo'
        close.account = 'Assets:Bar'
        assert close.account == 'Assets:Bar'
        assert self.print_model(close) == '2000-01-01  close Assets:Bar'

    def test_from_children(self) -> None:
        date = models.Date.from_value(datetime.date(2012, 12, 12))
        account = models.Account.from_value('Assets:Bar')
        close = models.Close.from_children(date, account)
        assert close.raw_date is date
        assert close.raw_account is account
        assert close.date == datetime.date(2012, 12, 12)
        assert close.account == 'Assets:Bar'
        assert self.print_model(close) == '2012-12-12 close Assets:Bar'

    def test_from_value(self) -> None:
        close = models.Close.from_value(datetime.date(2012, 12, 12), 'Assets:Bar')
        assert close.date == datetime.date(2012, 12, 12)
        assert close.account == 'Assets:Bar'
        assert self.print_model(close) == '2012-12-12 close Assets:Bar'
