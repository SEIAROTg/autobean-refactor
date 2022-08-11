import datetime
from lark import exceptions
import pytest
from autobean_refactor import models
from . import base


class TestCommodity(base.BaseTestModel):

    @pytest.mark.parametrize(
        'text,date,currency', [
            ('2000-01-01 commodity USD', datetime.date(2000, 1, 1), 'USD'),
            ('2012-12-12  commodity  EUR', datetime.date(2012, 12, 12), 'EUR'),
        ],
    )
    def test_parse_success(
            self,
            text: str,
            date: datetime.date,
            currency: str,
    ) -> None:
        commodity = self.parser.parse(text, models.Commodity)
        assert commodity.raw_date.value == date
        assert commodity.date == date
        assert commodity.raw_currency.value == currency
        assert commodity.currency == currency
        assert self.print_model(commodity) == text
        self.check_deepcopy_tree(commodity)
        self.check_reattach_tree(commodity)

    @pytest.mark.parametrize(
        'text', [
            '2000-01-01 commodIty USD',
            'commodity USD',
            '2000-01-01 commodity',
        ],
    )
    def test_parse_failure(self, text: str) -> None:
        with pytest.raises(exceptions.UnexpectedInput):
            self.parser.parse(text, models.Commodity)

    def test_set_raw_date(self) -> None:
        commodity = self.parser.parse('2000-01-01  commodity USD', models.Commodity)
        new_date = models.Date.from_value(datetime.date(2012, 12, 12))
        commodity.raw_date = new_date
        assert commodity.raw_date is new_date
        assert self.print_model(commodity) == '2012-12-12  commodity USD'

    def test_set_date(self) -> None:
        commodity = self.parser.parse('2000-01-01  commodity USD', models.Commodity)
        assert commodity.date == datetime.date(2000, 1, 1)
        commodity.date = datetime.date(2012, 12, 12)
        assert commodity.date == datetime.date(2012, 12, 12)
        assert self.print_model(commodity) == '2012-12-12  commodity USD'

    def test_set_raw_currency(self) -> None:
        commodity = self.parser.parse('2000-01-01  commodity USD', models.Commodity)
        new_currency = models.Currency.from_value('EUR')
        commodity.raw_currency = new_currency
        assert commodity.raw_currency is new_currency
        assert self.print_model(commodity) == '2000-01-01  commodity EUR'

    def test_set_currency(self) -> None:
        commodity = self.parser.parse('2000-01-01  commodity USD', models.Commodity)
        assert commodity.currency == 'USD'
        commodity.currency = 'EUR'
        assert commodity.currency == 'EUR'
        assert self.print_model(commodity) == '2000-01-01  commodity EUR'

    def test_from_children(self) -> None:
        date = models.Date.from_value(datetime.date(2012, 12, 12))
        currency = models.Currency.from_value('EUR')
        commodity = models.Commodity.from_children(date, currency)
        assert commodity.raw_date is date
        assert commodity.raw_currency is currency
        assert commodity.date == datetime.date(2012, 12, 12)
        assert commodity.currency == 'EUR'
        assert self.print_model(commodity) == '2012-12-12 commodity EUR'

    def test_from_value(self) -> None:
        commodity = models.Commodity.from_value(datetime.date(2012, 12, 12), 'EUR')
        assert commodity.date == datetime.date(2012, 12, 12)
        assert commodity.currency == 'EUR'
        assert self.print_model(commodity) == '2012-12-12 commodity EUR'
