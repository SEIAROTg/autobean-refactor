from lark import exceptions
import pytest
from autobean_refactor.models import raw_models
from . import base


class TestIgnored(base.BaseTestModel):

    @pytest.mark.parametrize(
        'text', [
            '; foo',
            ';foo',
            '; 你好!'
            ';',
            '    ; foo',
            'option "" ""    ',
            'option "" "" ; xxx',
            '    \n',
        ],
    )
    def test_parse_success(self, text: str) -> None:
        file = self.raw_parser.parse(text, raw_models.File)
        self.check_deepcopy_tree(file)

    @pytest.mark.parametrize(
        'text', [
            '"; foo"',
            '    option "" ""',
        ],
    )
    def test_parse_failure(self, text: str) -> None:
        with pytest.raises(exceptions.UnexpectedInput):
            self.raw_parser.parse(text, raw_models.File)
