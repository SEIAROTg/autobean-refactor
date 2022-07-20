import abc
import copy
from typing import Any, ClassVar, Optional, Type, TypeVar, cast
from autobean_refactor import token_store as token_store_lib

_OT = TypeVar('_OT', bound=Optional['RawTokenModel'])
# TODO: replace with PEP 673 Self once supported
_SelfRawModel = TypeVar('_SelfRawModel', bound='RawModel')
_SelfRawTokenModel = TypeVar('_SelfRawTokenModel', bound='RawTokenModel')  
_SelfRawTreeModel = TypeVar('_SelfRawTreeModel', bound='RawTreeModel')
TokenStore = token_store_lib.TokenStore['RawTokenModel']


class RawModel(abc.ABC):
    RULE: ClassVar[str]

    @property
    @abc.abstractmethod
    def token_store(self) -> Optional[TokenStore]:
        ...

    @property
    @abc.abstractmethod
    def first_token(self) -> Optional['RawTokenModel']:
        ...

    @property
    @abc.abstractmethod
    def last_token(self) -> Optional['RawTokenModel']:
        ...

    @abc.abstractmethod
    def __deepcopy__(self: _SelfRawModel, memo: dict[int, Any]) -> _SelfRawModel:
        ...

    def detach(self) -> list['RawTokenModel']:
        if not self.token_store:
            return []
        if (
                self.first_token is not self.token_store.get_first() or
                self.last_token is not self.token_store.get_last()):
            raise ValueError('Cannot reuse node. Consider making a copy.')
        tokens = list(self.token_store)
        if tokens:
            self.token_store.remove(tokens[0], tokens[-1])
        return tokens


class RawTokenModel(token_store_lib.Token, RawModel):
    def __init__(self, raw_text: str) -> None:
        super().__init__(raw_text)

    @classmethod
    def from_raw_text(cls: Type[_SelfRawTokenModel], raw_text: str) -> _SelfRawTokenModel:
        return cls(raw_text)

    @property
    def token_store(self) -> Optional[TokenStore]:
        return self.store_handle.store if self.store_handle else None

    @property
    def first_token(self) -> 'RawTokenModel':
        return self

    @property
    def last_token(self) -> 'RawTokenModel':
        return self

    @abc.abstractmethod
    def _clone(self: _SelfRawTokenModel) -> _SelfRawTokenModel:
        ...

    def __deepcopy__(self: _SelfRawTokenModel, memo: dict[int, Any]) -> _SelfRawTokenModel:
        del memo  # unused
        return self._clone()

    def detach(self) -> list['RawTokenModel']:
        if not self.store_handle:
            return [self]
        return super().detach()


# This could technically be replaced with map.__getitem__ but that didn't work well with mypy.
# https://github.com/python/mypy/issues/1317
class TokenTransformer(abc.ABC):
    @abc.abstractmethod
    def transform(self, token: _OT) -> _OT:
        ...


class MappingTokenTransformer(TokenTransformer):
    def __init__(self, map: dict[int, RawTokenModel]) -> None:
        self._map = map

    def transform(self, token: _OT) -> _OT:
        if token is None:
            return None
        return cast(_OT, self._map[id(token)])


class IdentityTokenTransformer(TokenTransformer):
    def transform(self, token: _OT) -> _OT:
        return token


_IDENTITY_TOKEN_TRANSFORMER = IdentityTokenTransformer()


class RawTreeModel(RawModel):
    def __init__(self, token_store: TokenStore) -> None:
        super().__init__()
        self._token_store = token_store

    @classmethod
    def from_children(cls: Type[_SelfRawTreeModel], token_store: TokenStore, *children: Optional[RawModel]) -> _SelfRawTreeModel:
        return cls(token_store, *children)

    @property
    def token_store(self) -> TokenStore:
        return self._token_store

    def __deepcopy__(self: _SelfRawTreeModel, memo: dict[int, Any]) -> _SelfRawTreeModel:
        del memo  # unused
        tokens: list[RawTokenModel] = []
        token_map: dict[int, RawTokenModel] = {}
        if self.first_token and self.last_token:
            for token in self._token_store.iter(self.first_token, self.last_token):
                new_token = copy.deepcopy(token)
                tokens.append(new_token)
                token_map[id(token)] = new_token
        token_store = TokenStore.from_tokens(tokens)
        return self.clone(token_store, MappingTokenTransformer(token_map))

    @abc.abstractmethod
    def clone(self: _SelfRawTreeModel, token_store: TokenStore, token_transformer: TokenTransformer) -> _SelfRawTreeModel:
        ...

    def reattach(self, token_store: TokenStore, token_transformer: TokenTransformer = _IDENTITY_TOKEN_TRANSFORMER) -> None:
        self._reattach(token_store, token_transformer)

    @abc.abstractmethod
    def _reattach(self, token_store: TokenStore, token_transformer: TokenTransformer) -> None:
        ...
