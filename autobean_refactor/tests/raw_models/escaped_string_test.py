from lark import exceptions
import pytest
from autobean_refactor import parser as parser_lib
from autobean_refactor.models import raw_models


class TestEscapedString:

    @pytest.mark.parametrize(
        'text,value', [
            ('""', ''),
            ('"foo"', 'foo'),
            ('"\'\'"', "''"),
            (r'"\""', '"'),
            (r'"你好"', '你好'),
            (r'"\u4f60\u597d"', '你好'),
            (r'"multiple\nlines"', 'multiple\nlines'),
            ('"multiple\nlines"', 'multiple\nlines'),
        ],
    )
    def test_parse_success(self, text: str, value: str, parser: parser_lib.Parser) -> None:
        token = parser.parse_token(text, raw_models.EscapedString)
        assert token.value == value
        assert token.raw_text == text

    @pytest.mark.parametrize(
        'text', [
            'foo',
            "'foo'",
            '"foo',
            'foo"',
            '"""',
            '',
        ],
    )
    def test_parse_failure(self, text: str, parser: parser_lib.Parser) -> None:
        with pytest.raises(exceptions.UnexpectedInput):
            parser.parse_token(text, raw_models.EscapedString)
