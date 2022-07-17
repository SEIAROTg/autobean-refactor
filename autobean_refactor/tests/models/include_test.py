from lark import exceptions
import pytest
from autobean_refactor.models import easy_models
from autobean_refactor.models import raw_models
from . import base


class TestInclude(base.BaseTestModel):

    @pytest.mark.parametrize(
        'text,filename', [
            ('include "foo"', 'foo'),
            ('include    "multiple\nlines"', 'multiple\nlines'),
        ],
    )
    def test_parse_success(self, text: str, filename: str) -> None:
        include = self._parser.parse(text, raw_models.Include)
        assert include.first_token.raw_text == 'include'
        assert include.raw_filename.value == filename
        assert include.last_token is include.raw_filename

    @pytest.mark.parametrize(
        'text', [
            '    include "foo"',
            'include\n"foo"',
            'include "foo" "bar"',
            'include ',
        ],
    )
    def test_parse_failure(self, text: str) -> None:
        with pytest.raises(exceptions.UnexpectedInput):
            self._parser.parse(text, raw_models.Include)

    def test_set_raw_filename(self) -> None:
        include = self._parser.parse('include  "filename"', raw_models.Include)
        new_filename = self._parser.parse_token('"new_filename"', raw_models.EscapedString)
        include.raw_filename = new_filename
        assert include.raw_filename is new_filename
        assert self.print_model(include) == 'include  "new_filename"'

    def test_set_filename(self) -> None:
        include = self._parser.parse('include  "filename"', easy_models.Include)
        assert include.filename == 'filename'
        include.filename = 'new_filename'
        assert include.filename == 'new_filename'
        assert self.print_model(include) == 'include  "new_filename"'
