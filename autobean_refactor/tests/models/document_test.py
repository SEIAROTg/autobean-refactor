import datetime
from lark import exceptions
import pytest
from autobean_refactor.models import easy_models
from autobean_refactor.models import raw_models
from . import base


class TestDocument(base.BaseTestModel):

    @pytest.mark.parametrize(
        'text,date,account,filename', [
            ('2000-01-01 document Assets:Foo "path/to/foo"', datetime.date(2000, 1, 1), 'Assets:Foo', 'path/to/foo'),
            ('2000-01-01  document  Assets:Foo  "path/to/foo"', datetime.date(2000, 1, 1), 'Assets:Foo', 'path/to/foo'),
        ],
    )
    def test_parse_success(self, text: str, date: datetime.date, account: str, filename: str) -> None:
        document = self.easy_parser.parse(text, easy_models.Document)
        assert document.raw_date.value == date
        assert document.date == date
        assert document.raw_account.value == account
        assert document.account == account
        assert document.raw_filename.value == filename
        assert document.filename == filename
        self.check_deepcopy_tree(document)
        self.check_reattach_tree(document)

    @pytest.mark.parametrize(
        'text', [
            'document Assets:Foo "path/to/foo"',
            '2000-01-01 document Assets:Foo',
            '2000-01-01 document "path/to/foo"',
            '2000-01-01 document USD "path/to/foo"',
            '2000-01-01 document #tag "path/to/foo"',
        ],
    )
    def test_parse_failure(self, text: str) -> None:
        with pytest.raises(exceptions.UnexpectedInput):
            self.raw_parser.parse(text, raw_models.Document)

    def test_set_raw_date(self) -> None:
        document = self.raw_parser.parse('2000-01-01 document Assets:Foo "path/to/foo"', raw_models.Document)
        new_date = raw_models.Date.from_value(datetime.date(2012, 12, 12))
        document.raw_date = new_date
        assert document.raw_date is new_date
        assert self.print_model(document) == '2012-12-12 document Assets:Foo "path/to/foo"'

    def test_set_date(self) -> None:
        document = self.easy_parser.parse('2000-01-01  document Assets:Foo "path/to/foo"', easy_models.Document)
        assert document.date == datetime.date(2000, 1, 1)
        document.date = datetime.date(2012, 12, 12)
        assert document.date == datetime.date(2012, 12, 12)
        assert self.print_model(document) == '2012-12-12  document Assets:Foo "path/to/foo"'

    def test_set_raw_account(self) -> None:
        document = self.raw_parser.parse('2000-01-01 document  Assets:Foo  "path/to/foo"', raw_models.Document)
        new_account = raw_models.Account.from_value('Assets:Bar')
        document.raw_account = new_account
        assert document.raw_account is new_account
        assert self.print_model(document) == '2000-01-01 document  Assets:Bar  "path/to/foo"'

    def test_set_account(self) -> None:
        document = self.easy_parser.parse('2000-01-01 document  Assets:Foo  "path/to/foo"', easy_models.Document)
        assert document.account == 'Assets:Foo'
        document.account = 'Assets:Bar'
        assert document.account == 'Assets:Bar'
        assert self.print_model(document) == '2000-01-01 document  Assets:Bar  "path/to/foo"'

    def test_set_raw_filename(self) -> None:
        document = self.raw_parser.parse('2000-01-01 document Assets:Foo  "path/to/foo"', raw_models.Document)
        new_filename = raw_models.EscapedString.from_value('path/to/bar')
        document.raw_filename = new_filename
        assert document.raw_filename is new_filename
        assert self.print_model(document) == '2000-01-01 document Assets:Foo  "path/to/bar"'

    def test_set_filename(self) -> None:
        document = self.easy_parser.parse('2000-01-01 document Assets:Foo  "path/to/foo"', easy_models.Document)
        assert document.filename == 'path/to/foo'
        document.filename = 'path/to/bar'
        assert document.filename == 'path/to/bar'
        assert self.print_model(document) == '2000-01-01 document Assets:Foo  "path/to/bar"'

    def test_from_children(self) -> None:
        date = raw_models.Date.from_value(datetime.date(2000, 1, 1))
        account = raw_models.Account.from_value('Assets:Foo')
        filename = raw_models.EscapedString.from_value('path/to/foo')
        document = raw_models.Document.from_children(date, account, filename)
        assert document.raw_date is date
        assert document.raw_account is account
        assert document.raw_filename is filename
        assert self.print_model(document) == '2000-01-01 document Assets:Foo "path/to/foo"'
        self.check_consistency(document)

    def test_from_value(self) -> None:
        document = easy_models.Document.from_value(
            datetime.date(2000, 1, 1),
            'Assets:Foo',
            'path/to/foo')
        assert document.raw_date.value == datetime.date(2000, 1, 1)
        assert document.account == 'Assets:Foo'
        assert document.filename == 'path/to/foo'
        assert self.print_model(document) == '2000-01-01 document Assets:Foo "path/to/foo"'
        self.check_consistency(document)
        self.check_flavor_consistency(document)
