from lark import exceptions
import pytest
from autobean_refactor import parser as parser_lib
from autobean_refactor.models import raw_models


class TestAccount:

    @pytest.mark.parametrize(
        'text', [
            'Assets:Foo',
            'Assets:Foo:Bar',
            'Assets:X',
            'Assets:X银行',
            # This is an invalid beancount account name but does pass beancount lexer.
            # The validation happens in the parser here: https://github.com/beancount/beancount/blob/89bf061b60777be3ae050c5c44fef67d93029130/beancount/parser/grammar.py#L243.
            'Assets:银行',
        ],
    )
    def test_parse_success(self, text: str, parser: parser_lib.Parser) -> None:
        token = parser.parse_token(text, raw_models.Account)
        assert token.raw_text == text
        assert token.value == text

    @pytest.mark.parametrize(
        'text', [
            'Assets',
        ],
    )
    def test_parse_failure(self, text: str, parser: parser_lib.Parser) -> None:
        with pytest.raises(exceptions.UnexpectedInput):
            parser.parse_token(text, raw_models.Account)

    def test_set_raw_text(self, parser: parser_lib.Parser) -> None:
        token = parser.parse_token('Assets:Foo', raw_models.Account)
        token.raw_text = 'Liabilities:Foo'
        assert token.raw_text == 'Liabilities:Foo'
        assert token.value == 'Liabilities:Foo'

    def test_set_value(self, parser: parser_lib.Parser) -> None:
        token = parser.parse_token('Assets:Foo', raw_models.Account)
        token.value = 'Liabilities:Foo'
        assert token.value == 'Liabilities:Foo'
        assert token.raw_text == 'Liabilities:Foo'
