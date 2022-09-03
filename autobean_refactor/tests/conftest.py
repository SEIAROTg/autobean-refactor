import pytest
from autobean_refactor import parser as parser_lib
from autobean_refactor import models


@pytest.fixture(scope='package')
def parser() -> parser_lib.Parser:
    return parser_lib.Parser(models.TOKEN_MODELS, models.TREE_MODELS)
