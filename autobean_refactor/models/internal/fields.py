import abc
import copy
from typing import Iterable, Optional, Type, TypeVar
from .. import base
from .repeated import Repeated
from .base_property import base_rw_property

_V = TypeVar('_V')
_M = TypeVar('_M', bound=base.RawModel)


class data_field(base_rw_property[_V, base.RawTreeModel]):

    def __set_name__(self, owner: Type[base.RawTreeModel], name: str) -> None:
        self._attr = name

    def _get(self, instance: base.RawTreeModel) -> _V:
        return instance.__dict__[self._attr]

    def __set__(self, instance: base.RawTreeModel, value: _V) -> None:
        instance.__dict__[self._attr] = value


class field(data_field[_V]):

    @abc.abstractmethod
    def clone(
            self,
            value: _V,
            token_store: base.TokenStore,
            token_transformer: base.TokenTransformer,
    ) -> _V:
        ...

    @abc.abstractmethod
    def reattach(
            self,
            value: _V,
            token_store: base.TokenStore,
            token_transformer: base.TokenTransformer = base.IDENTITY_TOKEN_TRANSFORMER,
    ) -> _V:
        ...

    @abc.abstractmethod
    def auto_claim_comments(self, value: _V) -> None:
        ...

    @abc.abstractmethod
    def detach_with_separators(self, value: _V) -> list[base.RawTokenModel]:
        ...


class required_field(field[_M]):

    def clone(
            self,
            value: _M,
            token_store: base.TokenStore,
            token_transformer: base.TokenTransformer,
    ) -> _M:
        return value.clone(token_store, token_transformer)

    def reattach(
            self,
            value: _M,
            token_store: base.TokenStore,
            token_transformer: base.TokenTransformer = base.IDENTITY_TOKEN_TRANSFORMER,
    ) -> _M:
        return value.reattach(token_store, token_transformer)

    def auto_claim_comments(self, value: _M) -> None:
        value.auto_claim_comments()

    def detach_with_separators(self, value: _M) -> list[base.RawTokenModel]:
        return value.detach()

    def iter_children_formatted(self, value: _M, indented: bool) -> Iterable[tuple[base.RawModel, bool]]:
        yield value, indented


class optional_field(field[Optional[_M]]):

    def __init__(self, *, separators: tuple[base.RawTokenModel, ...]) -> None:
        super().__init__()
        self._separators = separators

    @property
    def separators(self) -> tuple[base.RawTokenModel, ...]:
        return self._separators

    def clone(
            self,
            value: Optional[_M],
            token_store: base.TokenStore,
            token_transformer: base.TokenTransformer,
    ) -> Optional[_M]:
        return value.clone(token_store, token_transformer) if value is not None else None

    def reattach(
            self,
            value: Optional[_M],
            token_store: base.TokenStore,
            token_transformer: base.TokenTransformer = base.IDENTITY_TOKEN_TRANSFORMER,
    ) -> Optional[_M]:
        return value.reattach(token_store, token_transformer) if value is not None else None

    def auto_claim_comments(self, value: Optional[_M]) -> None:
        if value is not None:
            value.auto_claim_comments()

    @abc.abstractmethod
    def iter_children_formatted(self, value: Optional[_M], indented: bool) -> Iterable[tuple[base.RawModel, bool]]:
        ...

    @abc.abstractmethod
    def _create_node(
            self,
            token_store: base.TokenStore,
            pivot: base.RawTokenModel,
            value: _M,
    ) -> None:
        ...

    @abc.abstractmethod
    def _remove_node(
            self,
            token_store: base.TokenStore,
            pivot: base.RawTokenModel,
            current: _M,
    ) -> None:
        ...


class optional_left_field(optional_field[_M]):

    def detach_with_separators(self, value: Optional[_M]) -> list[base.RawTokenModel]:
        return [*copy.deepcopy(self.separators), *value.detach()] if value is not None else []

    def iter_children_formatted(self, value: Optional[_M], indented: bool) -> Iterable[tuple[base.RawModel, bool]]:
        if value is not None:
            for separator in self.separators:
                yield separator, indented
            yield value, indented

    def _create_node(
            self,
            token_store: base.TokenStore,
            pivot: base.RawTokenModel,
            value: _M,
    ) -> None:
        token_store.insert_after(pivot, [
            *copy.deepcopy(self.separators),
            *value.detach(),
        ])
        value.reattach(token_store)

    def _remove_node(
            self,
            token_store: base.TokenStore,
            pivot: base.RawTokenModel,
            current: _M,
    ) -> None:
        first = token_store.get_next(pivot)
        assert first is not None
        token_store.remove(first, current.last_token)


class optional_right_field(optional_field[_M]):

    def detach_with_separators(self, value: Optional[_M]) -> list[base.RawTokenModel]:
        return [*value.detach(), *copy.deepcopy(self.separators)] if value is not None else []

    def iter_children_formatted(self, value: Optional[_M], indented: bool) -> Iterable[tuple[base.RawModel, bool]]:
        if value is not None:
            yield value, indented
            for separator in self.separators:
                yield separator, indented

    def _create_node(
            self,
            token_store: base.TokenStore,
            pivot: base.RawTokenModel,
            value: _M,
    ) -> None:
        token_store.insert_before(pivot, [
            *value.detach(),
            *copy.deepcopy(self.separators),
        ])
        value.reattach(token_store)

    def _remove_node(
            self,
            token_store: base.TokenStore,
            pivot: base.RawTokenModel,
            current: _M,
    ) -> None:
        last = token_store.get_prev(pivot)
        assert last is not None
        token_store.remove(current.first_token, last)


class repeated_field(field[Repeated[_M]]):
    def __init__(
            self,
            *,
            separators: tuple[base.RawTokenModel, ...],
            separators_before: Optional[tuple[base.RawTokenModel, ...]] = None,
    ) -> None:
        super().__init__()
        self._separators = separators
        self._separators_before = separators_before

    @property
    def separators(self) -> tuple[base.RawTokenModel, ...]:
        return self._separators

    @property
    def separators_before(self) -> Optional[tuple[base.RawTokenModel, ...]]:
        return self._separators_before

    def create_repeated(self, values: Iterable[_M]) -> Repeated[_M]:
        return Repeated.from_children(
            values,
            separators=self.separators,
            separators_before=self.separators_before)

    def clone(
            self,
            value: Repeated[_M],
            token_store: base.TokenStore,
            token_transformer: base.TokenTransformer,
    ) -> Repeated[_M]:
        return value.clone(token_store, token_transformer)

    def reattach(
            self,
            value: Repeated[_M],
            token_store: base.TokenStore,
            token_transformer: base.TokenTransformer = base.IDENTITY_TOKEN_TRANSFORMER,
    ) -> Repeated[_M]:
        return value.reattach(token_store, token_transformer)

    def auto_claim_comments(self, value: Repeated[_M]) -> None:
        value.auto_claim_comments()

    def detach_with_separators(self, value: Repeated[_M]) -> list[base.RawTokenModel]:
        return value.detach()

    def iter_children_formatted(self, value: Repeated[_M], indented: bool) -> Iterable[tuple[base.RawModel, bool]]:
        for i, item in enumerate(value.items):
            if i == 0 and self.separators_before is not None:
                separators = self.separators_before
            else:
                separators = self.separators
            for separator in separators:
                yield separator, indented
            yield item, indented
