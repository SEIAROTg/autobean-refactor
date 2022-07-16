from lark import exceptions
import pytest
from autobean_refactor import parser as parser_lib
from autobean_refactor.models import raw_models


class TestTxn:

    def test_parse_success(self, parser: parser_lib.Parser) -> None:
        token = parser.parse_token('txn', raw_models.Txn)
        assert token.raw_text == 'txn'

    @pytest.mark.parametrize(
        'text', [
            '*',
            'TXN',
            'Txn',
            '',
        ],
    )
    def test_parse_failure(self, text: str, parser: parser_lib.Parser) -> None:
        with pytest.raises(exceptions.UnexpectedInput):
            parser.parse_token(text, raw_models.Txn)
