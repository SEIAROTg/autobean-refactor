import itertools
from typing import Generator, Iterable, TypeVar
import pytest
from autobean_refactor import token_store

_T = TypeVar('_T')


@pytest.fixture(autouse=True, scope='module')
def set_load_factor() -> Generator[None, None, None]:
    backup = token_store._LOAD_FACTOR, token_store._DOUBLE_LOAD_FACTOR, token_store._HALF_LOAD_FACTOR, token_store._ONE_HALF_LOAD_FACTOR
    token_store._LOAD_FACTOR, token_store._DOUBLE_LOAD_FACTOR, token_store._HALF_LOAD_FACTOR, token_store._ONE_HALF_LOAD_FACTOR = 10, 20, 5, 15
    yield
    token_store._LOAD_FACTOR, token_store._DOUBLE_LOAD_FACTOR, token_store._HALF_LOAD_FACTOR, token_store._ONE_HALF_LOAD_FACTOR = backup


def check_consistency(store: token_store.TokenStore[token_store.Token]) -> None:
    if len(store._blocks) > 1:
        for block in store._blocks:
            assert token_store._HALF_LOAD_FACTOR < len(block.tokens) < token_store._DOUBLE_LOAD_FACTOR
    
    length = 0
    for block_index, block in enumerate(store._blocks):
        size = token_store.Position()
        last_newline_index = -1
        for token_index, token in enumerate(block.tokens):
            size += token.size
            if token.size.line:
                last_newline_index = token_index
            assert token.store_handle
            assert token.store_handle.block is block
            assert token.store_handle.index == token_index
        assert block.index == block_index
        assert block.size == size
        assert block.last_newline_index == last_newline_index
        length += len(block.tokens)
    assert len(store) == length


def create_test_tokens(length: int) -> list[token_store.Token]:
    tokens = []
    for i in range(length):
        if i % 7 == 0:
            text = f'{i}\n{i}'
        else:
            text = str(i)
        tokens.append(token_store.Token(text))
    return tokens


def assert_same_tokens(xs: Iterable[_T], ys: Iterable[_T]) -> None:
    for x, y in itertools.zip_longest(xs, ys):
        assert x is y


class TestTokenStore:

    @pytest.mark.parametrize(
        'length', [0, 1, 5, 9, 10, 15, 20, 99, 102],
    )
    def test_from_tokens(self, length: int) -> None:
        tokens = create_test_tokens(length)
        store = token_store.TokenStore.from_tokens(tokens[:])
        assert list(store) == tokens
        check_consistency(store)

    @pytest.mark.parametrize(
        'l,r', [(0, 0), (27, 27), (0, 104), (27, 92), (104, 104)],
    )
    def test_iter(self, l: int, r: int) -> None:
        tokens = create_test_tokens(105)
        store = token_store.TokenStore.from_tokens(tokens[:])
        assert_same_tokens(store.iter(tokens[l], tokens[r]), tokens[l:r+1])

    def test_get_index(self) -> None:
        tokens = create_test_tokens(105)
        store = token_store.TokenStore.from_tokens(tokens[:])
        for i in range(len(tokens)):
            assert store.get_index(tokens[i]) == i

    def test_get_position(self) -> None:
        tokens = create_test_tokens(105)
        store = token_store.TokenStore.from_tokens(tokens[:])
        pos = token_store.Position()
        for token in tokens:
            assert store.get_position(token) == pos
            pos += token.size

    def test_get_prev(self) -> None:
        tokens = create_test_tokens(105)
        store = token_store.TokenStore.from_tokens(tokens[:])
        assert store.get_prev(tokens[0]) is None
        for i in range(1, len(tokens)):
            assert store.get_prev(tokens[i]) is tokens[i - 1]

    def test_get_next(self) -> None:
        tokens = create_test_tokens(105)
        store = token_store.TokenStore.from_tokens(tokens[:])
        for i in range(1, len(tokens)):
            assert store.get_next(tokens[i - 1]) is tokens[i]
        assert store.get_next(tokens[-1]) is None

    @pytest.mark.parametrize(
        'length', [0, 1, 9, 20, 99, 102],
    )
    def test_get_first(self, length: int) -> None:
        tokens = create_test_tokens(length)
        store = token_store.TokenStore.from_tokens(tokens[:])
        assert store.get_first() is next(iter(tokens), None)

    @pytest.mark.parametrize(
        'length', [0, 1, 9, 20, 99, 102],
    )
    def test_get_last(self, length: int) -> None:
        tokens = create_test_tokens(length)
        store = token_store.TokenStore.from_tokens(tokens[:])
        assert store.get_last() is next(reversed(tokens), None)

    @pytest.mark.parametrize(
        'index', [0, 1, 5, 7, 10, 15, 20, 99, 102],
    )
    def test_update(self, index: int) -> None:
        tokens = create_test_tokens(105)
        store = token_store.TokenStore.from_tokens(tokens[:])
        tokens[index].raw_text = 'foo'
        check_consistency(store)
        tokens[index].raw_text = 'foo\n\nbar'
        check_consistency(store)
        tokens[index].raw_text = 'baz123'
        check_consistency(store)

    @pytest.mark.parametrize(
        'index,length', [(0, 1), (0, 8), (0, 10), (0, 47), (8, 8), (30, 47), (35, 47), (39, 47), (40, 47), (104, 1), (104, 47)],
    )
    def test_insert_before(self, index: int, length: int) -> None:
        tokens = create_test_tokens(105)
        store = token_store.TokenStore.from_tokens(tokens[:])
        inserts = create_test_tokens(length)
        store.insert_before(tokens[index], inserts)
        tokens[index:index] = inserts
        assert_same_tokens(list(store), tokens)
        check_consistency(store)

    @pytest.mark.parametrize(
        'index,length', [(0, 1), (0, 8), (0, 10), (0, 47), (8, 8), (30, 47), (35, 47), (39, 47), (40, 47), (104, 1), (104, 47)],
    )
    def test_insert_after(self, index: int, length: int) -> None:
        tokens = create_test_tokens(105)
        store = token_store.TokenStore.from_tokens(tokens[:])
        inserts = create_test_tokens(length)
        store.insert_after(tokens[index], inserts)
        tokens[index+1:index+1] = inserts
        assert_same_tokens(list(store), tokens)
        check_consistency(store)

    @pytest.mark.parametrize(
        'l,r,length', [
            # insert only
            (0, 0, 5),
            (13, 13, 5),
            (13, 13, 13),
            # same line
            (32, 38, 5),
            (32, 38, 25),
            (30, 39, 5),
            (30, 39, 25),
            # multi-line
            (32, 72, 0),
            (32, 72, 5),
            (32, 72, 25),
            (0, 104, 0),
            (0, 104, 5),
            (0, 104, 45),
            (0, 104, 207),
        ],
    )
    def test_splice(self, l: int, r: int, length: int) -> None:
        tokens = create_test_tokens(105)
        store = token_store.TokenStore.from_tokens(tokens[:])
        inserts = create_test_tokens(length)
        store.splice(inserts, tokens[l], tokens[r])
        tokens[l:r+1] = inserts
        assert_same_tokens(list(store), tokens)
        check_consistency(store)
