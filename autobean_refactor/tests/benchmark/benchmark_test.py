import pytest
from pytest_benchmark.fixture import BenchmarkFixture  # type: ignore[import]
from autobean_refactor import parser as parser_lib
from autobean_refactor import models

_FILE_SIMPLE = '''\
2000-01-01 *
    Assets:Foo   100.00 USD
    Assets:Bar  -100.00 USD

'''

_FILE_COMPLEX = '''\
; comment
2000-01-01 * "payee" "narration" #tag-a #tag-b ^link-a
    meta-a: 1
    ; comment
    meta-b: 2
    ; comment
    Assets:Foo       100.00 USD
        ; comment
        meta-c: 3
    Assets:Bar      -100.00 DSU {{}}
; comment

'''


def _parse_file(parser: parser_lib.Parser, text: str) -> models.File:
    return parser.parse(text, models.File)


def _update_comment(transaction: models.Transaction) -> None:
    transaction.leading_comment = transaction.leading_comment[::-1]  # type: ignore[index]


def _getitem_repeated(file: models.File) -> models.Directive | models.BlockComment:
    return file.raw_directives_with_comments[-1]


def _getitem_repeated_filtered(file: models.File) -> models.Directive:
    return file.raw_directives[-1]


def _insert_meta(transaction: models.Transaction) -> None:
    meta = transaction.raw_meta_with_comments.pop(-1)
    transaction.raw_meta_with_comments.insert(0, meta)


@pytest.mark.benchmark(group='parse_simple')
@pytest.mark.parametrize('repeat', [1, 10, 100, 1000])
def test_parse_simple(repeat: int, benchmark: BenchmarkFixture, parser: parser_lib.Parser) -> None:
    benchmark(_parse_file, parser, _FILE_SIMPLE * repeat)


@pytest.mark.benchmark(group='parse_complex')
@pytest.mark.parametrize('repeat', [1, 10, 100, 1000])
def test_parse_complex(repeat: int, benchmark: BenchmarkFixture, parser: parser_lib.Parser) -> None:
    benchmark(_parse_file, parser, _FILE_COMPLEX * repeat)


@pytest.mark.benchmark(group='update_end')
@pytest.mark.parametrize('repeat', [1, 10, 100, 1000])
def test_update_end(repeat: int, benchmark: BenchmarkFixture, parser: parser_lib.Parser) -> None:
    file = parser.parse(_FILE_COMPLEX * repeat, models.File, auto_claim_comments=False)
    txn = file.raw_directives_with_comments[-1]
    txn.auto_claim_comments()
    assert isinstance(txn, models.Transaction)
    assert txn.leading_comment is not None

    benchmark(_update_comment, txn)


@pytest.mark.benchmark(group='update_start')
@pytest.mark.parametrize('repeat', [1, 10, 100, 1000])
def test_update_start(repeat: int, benchmark: BenchmarkFixture, parser: parser_lib.Parser) -> None:
    file = parser.parse(_FILE_COMPLEX * repeat, models.File, auto_claim_comments=False)
    txn = file.raw_directives_with_comments[0]
    txn.auto_claim_comments()
    assert isinstance(txn, models.Transaction)
    assert txn.leading_comment is not None

    benchmark(_update_comment, txn)


@pytest.mark.benchmark(group='getitem_repeated')
@pytest.mark.parametrize('repeat', [1, 10, 100, 1000])
def test_getitem_repeated(repeat: int, benchmark: BenchmarkFixture, parser: parser_lib.Parser) -> None:
    file = parser.parse(_FILE_COMPLEX * repeat, models.File)
    benchmark(_getitem_repeated, file)


@pytest.mark.benchmark(group='getitem_repeated_filtered')
@pytest.mark.parametrize('repeat', [1, 10, 100, 1000])
def test_getitem_repeated_filtered(repeat: int, benchmark: BenchmarkFixture, parser: parser_lib.Parser) -> None:
    file = parser.parse(_FILE_COMPLEX * repeat, models.File)
    benchmark(_getitem_repeated_filtered, file)


@pytest.mark.benchmark(group='insert_meta_end')
@pytest.mark.parametrize('repeat', [1, 10, 100, 1000])
def test_insert_meta_end(repeat: int, benchmark: BenchmarkFixture, parser: parser_lib.Parser) -> None:
    file = parser.parse(_FILE_COMPLEX * repeat, models.File)
    txn = file.raw_directives_with_comments[-1]
    assert isinstance(txn, models.Transaction)
    benchmark(_insert_meta, txn)


@pytest.mark.benchmark(group='insert_meta_start')
@pytest.mark.parametrize('repeat', [1, 10, 100, 1000])
def test_insert_meta_start(repeat: int, benchmark: BenchmarkFixture, parser: parser_lib.Parser) -> None:
    file = parser.parse(_FILE_COMPLEX * repeat, models.File)
    txn = file.raw_directives_with_comments[0]
    assert isinstance(txn, models.Transaction)
    benchmark(_insert_meta, txn)
