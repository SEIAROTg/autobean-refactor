from lark import exceptions
import pytest
from autobean_refactor import parser as parser_lib
from autobean_refactor.models import raw_models
from . import conftest


class TestOption:

    @pytest.mark.parametrize(
        'text,key,value', [
            ('option "foo" "bar"', 'foo', 'bar'),
            ('option    "foo"    "multiple\nlines"', 'foo', 'multiple\nlines'),
        ],
    )
    def test_parse_success(self, text: str, key: str, value: str, parser: parser_lib.Parser) -> None:
        option = parser.parse(text, raw_models.Option)
        assert option.first_token.raw_text == 'option'
        assert option.raw_key.value == key
        assert option.raw_value.value == value
        assert option.last_token is option.raw_value

    @pytest.mark.parametrize(
        'text', [
            '    option "foo" "bar"',
            'option "foo"\n"bar"',
            'option "foo" "bar" "baz"',
            'option "foo"',
            'option ',
        ],
    )
    def test_parse_failure(self, text: str, parser: parser_lib.Parser) -> None:
        with pytest.raises(exceptions.UnexpectedInput):
            parser.parse(text, raw_models.Option)

    def test_set_raw_key(self, parser: parser_lib.Parser, print_model: conftest.PrintModel) -> None:
        option = parser.parse('option  "key"    "value"', raw_models.Option)
        option.raw_key = parser.parse_token('"new_key"', raw_models.EscapedString)
        assert print_model(option) == 'option  "new_key"    "value"'

    def test_set_raw_value(self, parser: parser_lib.Parser, print_model: conftest.PrintModel) -> None:
        option = parser.parse('option  "key"    "value"', raw_models.Option)
        option.raw_value = parser.parse_token('"new_value"', raw_models.EscapedString)
        assert print_model(option) == 'option  "key"    "new_value"'
