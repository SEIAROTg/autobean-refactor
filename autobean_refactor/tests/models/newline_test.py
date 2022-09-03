from lark import exceptions
import pytest
from autobean_refactor import models
from .. import base


class TestNewline(base.BaseTestModel):

    @pytest.mark.parametrize(
        'text', [
            '\n',
            '\r\n',
            '\r\r\n',
        ],
    )
    def test_parse_success(self, text: str) -> None:
        token = self.parser.parse_token(text, models.Newline)
        assert token.raw_text == text
        self.check_deepcopy_token(token)

    @pytest.mark.parametrize(
        'text', [
            '\r',
            '\n ',
            '\n\r',
            '',
        ],
    )
    def test_parse_failure(self, text: str) -> None:
        with pytest.raises(exceptions.UnexpectedInput):
            self.parser.parse_token(text, models.Newline)
