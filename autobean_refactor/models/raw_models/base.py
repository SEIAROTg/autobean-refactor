import abc
from typing import ClassVar, Optional, Type, TypeVar
from autobean_refactor import token_store as token_store_lib

_T = TypeVar('_T', bound='RawTokenModel')


class RawModel(abc.ABC):
    RULE: ClassVar[str]

    @property
    @abc.abstractmethod
    def token_store(self) -> Optional[token_store_lib.TokenStore]:
        ...

    @property
    @abc.abstractmethod
    def first_token(self) -> Optional[token_store_lib.Token]:
        ...

    @property
    @abc.abstractmethod
    def last_token(self) -> Optional[token_store_lib.Token]:
        ...


class RawTokenModel(token_store_lib.Token, RawModel):
    def __init__(self, raw_text: str) -> None:
        super().__init__(raw_text)

    @classmethod
    def from_raw_text(cls: Type[_T], raw_text: str) -> _T:
        return cls(raw_text)

    @property
    def token_store(self) -> Optional[token_store_lib.TokenStore]:
        return self.store_handle.store if self.store_handle else None

    @property
    def first_token(self) -> Optional[token_store_lib.Token]:
        return self

    @property
    def last_token(self) -> Optional[token_store_lib.Token]:
        return self


class RawTreeModel(RawModel):
    def __init__(self, token_store: token_store_lib.TokenStore) -> None:
        super().__init__()
        self._token_store = token_store

    @property
    def token_store(self) -> token_store_lib.TokenStore:
        return self._token_store


TOKEN_MODELS: list[Type[RawTokenModel]] = []
TREE_MODELS: list[Type[RawTreeModel]] = []
_V = TypeVar('_V', bound=Type[RawTokenModel])
_W = TypeVar('_W', bound=Type[RawTreeModel])


def token_model(cls: _V) -> _V:
    TOKEN_MODELS.append(cls)
    return cls


def tree_model(cls: _W) -> _W:
    TREE_MODELS.append(cls)
    return cls


@token_model
class Newline(RawTokenModel):
    RULE = '_NL'


@token_model
class Indent(RawTokenModel):
    RULE = 'INDENT'


@token_model
class Whitespace(RawTokenModel):
    RULE = 'WS_INLINE'


@token_model
class InlineComment(RawTokenModel):
    RULE = 'COMMENT_INLINE'


@token_model
class LineComment(RawTokenModel):
    RULE = 'COMMENT_LINE'
