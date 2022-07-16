from lark import exceptions
import pytest
from autobean_refactor import parser as parser_lib
from autobean_refactor.models import raw_models


class TestCurrency:

    @pytest.mark.parametrize(
        'text', [
            'USD',
            'AAPL',
            'NT.TO',
            'TLT_040921C144',
            '/6J',
            '/NQH21',
            '/NQH21_QNEG21C13100',
            'C345',
            # These are technically invalid currencies but it's difficult to reject them under contextual lexer.
            'TRUE',
            'FALSE',
            'NULL',
        ],
    )
    def test_parse_success(self, text: str, parser: parser_lib.Parser) -> None:
        token = parser.parse_token(text, raw_models.Currency)
        assert token.raw_text == text
        assert token.value == text

    @pytest.mark.parametrize(
        'text', [
            '/6.3',
            '/CAC_',
            'C_',
            'V',  # it is valid in v3 syntax
            'Asset',
        ],
    )
    def test_parse_failure(self, text: str, parser: parser_lib.Parser) -> None:
        with pytest.raises(exceptions.UnexpectedInput):
            parser.parse_token(text, raw_models.Currency)

    def test_set_raw_text(self, parser: parser_lib.Parser) -> None:
        token = parser.parse_token('USD', raw_models.Currency)
        token.raw_text = 'AAPL'
        assert token.raw_text == 'AAPL'
        assert token.value == 'AAPL'

    def test_set_value(self, parser: parser_lib.Parser) -> None:
        token = parser.parse_token('USD', raw_models.Currency)
        token.value = 'AAPL'
        assert token.value == 'AAPL'
        assert token.raw_text == 'AAPL'
