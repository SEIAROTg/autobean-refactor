import abc
from typing import Generic, Optional, Type, TypeVar, overload
from typing_extensions import Self
from .. import base

_U = TypeVar('_U', bound=base.RawTreeModel)
_V = TypeVar('_V')
_V_cov = TypeVar('_V_cov', covariant=True)


class base_ro_property(Generic[_V_cov, _U], abc.ABC):

    @abc.abstractmethod
    def _get(self, instance: _U) -> _V_cov:
        ...

    @overload
    def __get__(self, instance: _U, owner: Optional[Type[_U]] = None) -> _V_cov:
        ...

    @overload
    def __get__(self, instance: None, owner: Type[_U]) -> Self:
        ...

    def __get__(self, instance: Optional[_U], owner: Optional[Type[_U]] = None) -> _V_cov | Self:
        del owner
        if instance is None:
            return self
        return self._get(instance)


class base_rw_property(base_ro_property[_V, _U]):

    @abc.abstractmethod
    def __set__(self, instance: _U, value: _V) -> None:
        ...
