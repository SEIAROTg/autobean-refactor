from lark import exceptions
import pytest
from autobean_refactor import models
from . import base


class TestLink(base.BaseTestModel):

    @pytest.mark.parametrize(
        'text,value', [
            ('foo:', 'foo'),
            ('foo-bar:', 'foo-bar'),
            ('foo_bar:' ,'foo_bar'),
        ],
    )
    def test_parse_success(self, text: str, value: str) -> None:
        token = self.parser.parse_token(text, models.MetaKey)
        assert token.raw_text == text
        assert token.value == value
        self.check_deepcopy_token(token)

    @pytest.mark.parametrize(
        'text', [
            'x',
            'foo',
            'foo :',
            '-foo:',
            'Foo:',
            'FOO:',
            '#foo:',
            '!foo:',
            '你好:',
            'foo-你好:',
        ],
    )
    def test_parse_failure(self, text: str) -> None:
        with pytest.raises(exceptions.UnexpectedInput):
            self.parser.parse_token(text, models.MetaKey)

    def test_set_raw_text(self) -> None:
        token = self.parser.parse_token('foo:', models.MetaKey)
        token.raw_text = 'bar:'
        assert token.raw_text == 'bar:'
        assert token.value == 'bar'

    def test_set_value(self) -> None:
        token = self.parser.parse_token('foo:', models.MetaKey)
        token.value = 'bar'
        assert token.value == 'bar'
        assert token.raw_text == 'bar:'
