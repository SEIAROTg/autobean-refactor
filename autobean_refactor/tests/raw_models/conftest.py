import pytest
from autobean_refactor import parser as parser_lib
from autobean_refactor.models import raw_models


@pytest.fixture(scope='package')
def parser() -> parser_lib.Parser:
    return parser_lib.Parser(raw_models.TOKEN_MODELS, raw_models.TREE_MODELS)
