from lark import exceptions
import pytest
from autobean_refactor import parser as parser_lib
from autobean_refactor.models import easy_models
from autobean_refactor.models import raw_models
from . import conftest


class TestPostingFlag:

    def _assert_raw_flag_type(self, raw_flag: raw_models.Asterisk | raw_models.Flag, text: str) -> None:
        if text == '*':
            assert isinstance(raw_flag, raw_models.Asterisk)
        else:
            assert isinstance(raw_flag, raw_models.Flag)

    @pytest.mark.parametrize(
        'text', [
            '*',
            '!',
            'T',
        ],
    )
    def test_parse_success(self, text: str, parser: parser_lib.Parser) -> None:
        flag = parser.parse(text, raw_models.PostingFlag)
        assert flag.raw_flag.raw_text == text
        assert flag.first_token is flag.raw_flag
        assert flag.last_token is flag.raw_flag

    @pytest.mark.parametrize(
        'text', [
            'txn',
            '**',
            '!!',
            'A'
        ],
    )
    def test_parse_failure(self, text: str, parser: parser_lib.Parser) -> None:
        with pytest.raises(exceptions.UnexpectedInput):
            parser.parse(text, raw_models.PostingFlag)

    def test_set_raw_flag(self, parser: parser_lib.Parser, print_model: conftest.PrintModel) -> None:
        flag = parser.parse('*', raw_models.PostingFlag)
        new_raw_flag = raw_models.Flag.from_raw_text('!')
        flag.raw_flag = new_raw_flag
        assert flag.raw_flag is new_raw_flag
        assert print_model(flag) == '!'

    @pytest.mark.parametrize(
        'text,new_text', [
            ('*', '!'),
            ('!', '*'),
        ],
    )
    def test_set_raw_text(self, text: str, new_text: str, parser: parser_lib.Parser, print_model: conftest.PrintModel) -> None:
        flag = parser.parse(text, easy_models.PostingFlag)
        assert flag.raw_text == text
        flag.raw_text = new_text
        assert flag.raw_text == new_text
        assert flag.raw_flag.raw_text == new_text
        self._assert_raw_flag_type(flag.raw_flag, new_text)
        assert print_model(flag) == new_text

    @pytest.mark.parametrize(
        'text,new_value', [
            ('*', '!'),
            ('!', '*'),
        ],
    )
    def test_set_value(self, text: str, new_value: str, parser: parser_lib.Parser, print_model: conftest.PrintModel) -> None:
        flag = parser.parse(text, easy_models.PostingFlag)
        assert flag.value == text
        flag.value = new_value
        assert flag.value == new_value
        assert flag.raw_flag.raw_text == new_value
        self._assert_raw_flag_type(flag.raw_flag, new_value)
        assert print_model(flag) == new_value
