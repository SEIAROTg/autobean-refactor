import copy
import dataclasses
from typing import Any, Generic, Iterable, Iterator, Optional, Sequence, TypeVar
from typing_extensions import Self

_LOAD_FACTOR = 1000
_DOUBLE_LOAD_FACTOR = _LOAD_FACTOR * 2
_HALF_LOAD_FACTOR = _LOAD_FACTOR // 2
_ONE_HALF_LOAD_FACTOR = _LOAD_FACTOR + _HALF_LOAD_FACTOR
_T = TypeVar('_T', bound='Token')


@dataclasses.dataclass(slots=True)
class Position:
    line: int = 0
    column: int = 0

    def __iadd__(self, other: Any) -> 'Position':
        if not isinstance(other, Position):
            return NotImplemented
        self.line += other.line
        if other.line:
            self.column = other.column
        else:
            self.column += other.column
        return self

    def __add__(self, other: Any) -> 'Position':
        pos = copy.copy(self)
        pos += other
        return pos


class Token:
    _raw_text: str
    store_handle: Optional['_StoreHandle']
    size: 'Position'

    def __init__(self, raw_text: str) -> None:
        self._raw_text = raw_text
        self.store_handle = None
        self.size = _token_size(self._raw_text)

    @property
    def raw_text(self) -> str:
        return self._raw_text

    @raw_text.setter
    def raw_text(self, value: str) -> None:
        self._update_raw_text(value)

    # property setter override is painful. use setter method instead.
    def _update_raw_text(self, value: str) -> None:
        size = _token_size(value)
        if self.store_handle:
            self.store_handle.block.store.update(self, value, size)
        self._raw_text = value
        self.size = size

    def __repr__(self) -> str:
        return f'<{type(self).__name__}: {self._raw_text!r}>'


@dataclasses.dataclass(slots=True, eq=False)
class _StoreHandle(Generic[_T]):
    block: '_StoreBlock[_T]'
    index: int


@dataclasses.dataclass(slots=True, eq=False)
class _StoreBlock(Generic[_T]):
    store: 'TokenStore[_T]'
    index: int
    tokens: list[_T] = dataclasses.field(default_factory=list)
    size: Position = dataclasses.field(default_factory=Position)
    last_newline_index: int = -1

    @classmethod
    def from_tokens(cls, tokens: Sequence[_T], store: 'TokenStore[_T]', index: int) -> Self:
        block = cls(store, index, tokens if isinstance(tokens, list) else list(tokens))
        for i, token in enumerate(tokens):
            block.size += token.size
            if token.size.line:
                block.last_newline_index = i
            token.store_handle = _StoreHandle(block=block, index=i)
        return block

    def rebuild(self) -> None:
        size = Position()
        last_newline_index = -1
        for i, token in enumerate(self.tokens):
            size += token.size
            if token.size.line:
                last_newline_index = i
            token.store_handle = _StoreHandle(block=self, index=i)
        self.size = size
        self.last_newline_index = last_newline_index

    def extend(self, tokens: Iterable[_T]) -> None:
        start = len(self.tokens)
        self.tokens.extend(tokens)
        for i in range(start, len(self.tokens)):
            token = self.tokens[i]
            self.size += token.size
            if token.size.line:
                self.last_newline_index = i
            token.store_handle = _StoreHandle(self, i)


def _check_store_handle(token: _T) -> _StoreHandle[_T]:
    if not token.store_handle:
        raise ValueError('Token is not in a store.')
    return token.store_handle


def _token_size(raw_text: str) -> Position:
    return Position(
        line=raw_text.count('\n'),
        column=len(raw_text) - raw_text.rfind('\n') - 1)


def _build_blocks(store: 'TokenStore[_T]', start_index: int, tokens: list[_T]) -> list[_StoreBlock[_T]]:
    blocks = []
    start = 0
    remaining = len(tokens)
    while remaining:
        if remaining > _ONE_HALF_LOAD_FACTOR:
            blocks.append(_StoreBlock.from_tokens(tokens[start:start+_LOAD_FACTOR], store, start_index))
            start_index += 1
            start += _LOAD_FACTOR
            remaining -= _LOAD_FACTOR
        elif remaining > _LOAD_FACTOR:
            length = remaining // 2
            blocks.append(_StoreBlock.from_tokens(tokens[start:start+length], store, start_index))
            blocks.append(_StoreBlock.from_tokens(tokens[start+length:], store, start_index + 1))
            break
        else:
            blocks.append(_StoreBlock.from_tokens(tokens[start:], store, start_index))
            break
    return blocks


class TokenStore(Generic[_T]):
    """Storage for tokens allowing insertion, deletion and lookup by position."""

    _blocks: list[_StoreBlock[_T]]
    _len: int

    def __init__(self) -> None:
        self._blocks = [_StoreBlock(self, 0, [])]
        self._len = 0

    @classmethod
    def from_tokens(cls, tokens: list[_T]) -> Self:
        for token in tokens:
            if token.store_handle:
                raise ValueError('Token already in a store.')
        store = cls()
        if tokens:
            store._blocks[:] = list(_build_blocks(store, 0, tokens))
            store._len = len(tokens)
        return store

    def _update_block_indexes(self, i: int) -> None:
        while i < len(self._blocks):
            self._blocks[i].index = i
            i += 1

    def _split_block(self, block: _StoreBlock[_T]) -> None:
        new_blocks = _build_blocks(self, block.index, block.tokens)
        self._blocks[block.index:block.index+1] = new_blocks
        self._update_block_indexes(new_blocks[-1].index + 1)

    def _merge_blocks(self, a: _StoreBlock[_T], b: _StoreBlock[_T]) -> None:
        a.tokens += b.tokens
        if len(a.tokens) < _DOUBLE_LOAD_FACTOR:
            a.rebuild()
            self._blocks.pop(b.index)
            self._update_block_indexes(b.index)
        else:
            length = len(a.tokens) >> 1
            b.tokens[:] = a.tokens[length:]
            del a.tokens[length:]
            a.rebuild()
            b.rebuild()

    def _update_block(self, block: _StoreBlock[_T]) -> None:
        length = len(block.tokens)
        if length >= _DOUBLE_LOAD_FACTOR:
            self._split_block(block)
        elif length <= _HALF_LOAD_FACTOR and len(self._blocks) > 1:
            if block.index:
                prev_block = self._blocks[block.index - 1]
                self._merge_blocks(prev_block, block)
            else:
                next_block = self._blocks[block.index + 1]
                self._merge_blocks(block, next_block)
        else:
            block.rebuild()
            next_block_index = block.index + 1
            if next_block_index < len(self._blocks) and self._blocks[next_block_index].index != next_block_index:
                self._update_block_indexes(next_block_index)

    def _splice(self, tokens: Sequence[_T], start: tuple[int, int], end: tuple[int, int]) -> None:
        start_i, start_j = start
        end_i, end_j = end

        for token in tokens:
            if token.store_handle is not None and not start <= (token.store_handle.block.index, token.store_handle.index) <= end:
                raise ValueError('Token already in a store.')

        if start_i == end_i:
            len_removed = end_j - start_j
            block = self._blocks[start_i]
            lines_diff = 0
            for j in range(start_j, end_j):
                block.tokens[j].store_handle = None
                lines_diff -= block.tokens[j].size.line
            block.tokens[start_j:end_j] = tokens

            if (
                    len(block.tokens) < _DOUBLE_LOAD_FACTOR and
                    (len(block.tokens) > _HALF_LOAD_FACTOR or len(self._blocks) == 1) and
                    block.last_newline_index >= end_j
            ):
                for token in tokens:
                    lines_diff += token.size.line
                for j in range(start_j, len(block.tokens)):
                    block.tokens[j].store_handle = _StoreHandle(block=block, index=j)
                block.last_newline_index += len(tokens) - len_removed
                block.size.line += lines_diff
            else:
                self._update_block(block)
        else:
            len_removed = len(self._blocks[start_i].tokens) - start_j + end_j
            for j in range(start_j, len(self._blocks[start_i].tokens)):
                self._blocks[start_i].tokens[j].store_handle = None
            for i in range(start_i + 1, end_i):
                for token in self._blocks[i].tokens:
                    token.store_handle = None
                len_removed += len(self._blocks[i].tokens)
            for j in range(end_j):
                self._blocks[end_i].tokens[j].store_handle = None
            self._blocks[start_i:end_i + 1] = [
                _StoreBlock(self, start_i, [
                    *self._blocks[start_i].tokens[:start_j],
                    *tokens,
                    *self._blocks[end_i].tokens[end_j:], 
                ])
            ]
            self._update_block(self._blocks[start_i])
        self._len += len(tokens) - len_removed

    def splice(self, tokens: Sequence[_T], ref: Optional[_T], del_end: Optional[_T] = None) -> None:
        if ref is None:
            start = (0, 0)
        else:
            start_handle = _check_store_handle(ref)
            start = (start_handle.block.index, start_handle.index)
        if del_end is None:
            end = start
        else:
            end_handle = _check_store_handle(del_end)
            end = (end_handle.block.index, end_handle.index + 1)
        self._splice(tokens, start, end)

    def insert_after(self, ref: Optional[_T], tokens: Sequence[_T]) -> None:
        if ref is None:
            start = (0, 0)
        else:
            start_handle = _check_store_handle(ref)
            start = (start_handle.block.index, start_handle.index + 1)
        self._splice(tokens, start, start)

    def insert_before(self, ref: Optional[_T], tokens: Sequence[_T]) -> None:
        self.splice(tokens, ref)

    def update(self, token: _T, raw_text: str, size: Position) -> None:
        handle = _check_store_handle(token)
        handle.block.size.line += size.line - token.size.line
        if handle.index < handle.block.last_newline_index:
            return
        if size.line and not token.size.line:  # create new line
            handle.block.last_newline_index = handle.index
            col = size.column
            for i in range(handle.index + 1, len(handle.block.tokens)):
                col += handle.block.tokens[i].size.column
            handle.block.size.column = col
        elif token.size.line and not size.line:  # remove new line
            col = handle.block.size.column + size.column - token.size.column
            for i in range(handle.index - 1, -1, -1):
                col += handle.block.tokens[i].size.column
                if handle.block.tokens[i].size.line:
                    handle.block.last_newline_index = i
                    break
            else:
                handle.block.last_newline_index = -1
            handle.block.size.column = col
        else:
            handle.block.size.column += size.column - token.size.column

    def replace(self, token: _T, repl: _T) -> None:
        self.splice([repl], token, token)

    def remove(self, start: _T, end: Optional[_T] = None) -> None:
        self.splice([], start, end or start)

    def iter(self, start: _T, end: _T) -> Iterator[_T]:
        start_handle = _check_store_handle(start)
        end_handle = _check_store_handle(end)
        if start_handle.block is end_handle.block:
            yield from start_handle.block.tokens[start_handle.index:end_handle.index+1]
        else:
            yield from start_handle.block.tokens[start_handle.index:]
            for i in range(start_handle.block.index + 1, end_handle.block.index):
                yield from self._blocks[i].tokens
            yield from end_handle.block.tokens[:end_handle.index+1]

    def get_index(self, token: _T) -> int:
        handle = _check_store_handle(token)
        index = handle.index
        for i in range(handle.block.index):
            index += len(self._blocks[i].tokens)
        return index

    def get_position(self, token: _T) -> Position:
        handle = _check_store_handle(token)
        pos = Position()
        for i in range(handle.block.index):
            pos += self._blocks[i].size
        for i in range(handle.index):
            pos += handle.block.tokens[i].size
        return pos

    def get_prev(self, token: _T) -> Optional[_T]:
        handle = _check_store_handle(token)
        if handle.index:
            return handle.block.tokens[handle.index - 1]
        if handle.block.index and self._blocks[handle.block.index - 1].tokens:
            return self._blocks[handle.block.index - 1].tokens[-1]
        return None

    def get_next(self, token: _T) -> Optional[_T]:
        handle = _check_store_handle(token)
        if handle.index + 1 < len(handle.block.tokens):
            return handle.block.tokens[handle.index + 1]
        if handle.block.index + 1 < len(self._blocks):
            return self._blocks[handle.block.index + 1].tokens[0]
        return None

    def get_first(self) -> Optional[_T]:
        return self._blocks and self._blocks[0].tokens and self._blocks[0].tokens[0] or None

    def get_last(self) -> Optional[_T]:
        return self._blocks and self._blocks[0].tokens and self._blocks[-1].tokens[-1] or None

    def __iter__(self) -> Iterator[_T]:
        for block in self._blocks:
            yield from block.tokens

    def __len__(self) -> int:
        return self._len
