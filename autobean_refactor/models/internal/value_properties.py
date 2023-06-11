import bisect
import datetime
import decimal
import abc
import itertools
from typing import Any, Callable, Collection, Generic, Iterable, Iterator, MutableSequence, Optional, Type, TypeGuard, TypeVar, cast, overload
from typing_extensions import Self
from .. import base
from . import indexes, base_property, properties


_V = TypeVar('_V')
_M = TypeVar('_M', bound=base.RawModel)
_M2 = TypeVar('_M2', bound=base.RawModel)
_U = TypeVar('_U', bound=base.RawTreeModel)
_SV = TypeVar('_SV', bound='RWValue[str]')
_ISV = TypeVar('_ISV', bound='RWValueWithIndent[str]')
_DV = TypeVar('_DV', bound='RWValue[decimal.Decimal]')
_DateV = TypeVar('_DateV', bound='RWValue[datetime.date]')


class RWValue(base.RawModel, abc.ABC, Generic[_V]):
    @property
    def value(self) -> _V:
        raise NotImplementedError()

    @value.setter
    def value(self, value: _V) -> None:
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def from_value(cls, value: _V) -> Self:
        raise NotImplementedError()


class RWValueWithIndent(RWValue[_V]):
    @property
    def indent(self) -> str:
        raise NotImplementedError()

    @indent.setter
    def indent(self, indent: str) -> None:
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def from_value(cls, value: _V, *, indent: str = '') -> Self:
        raise NotImplementedError()


class required_value_property(properties.base_rw_property[_V, _U]):
    def __init__(self, inner_property: base_property.base_ro_property[RWValue[_V], _U]):
        self._inner_property = inner_property

    def _get(self, instance: _U) -> _V:
        return self._inner_property.__get__(instance).value
    
    def __set__(self, instance: _U, value: _V) -> None:
        self._inner_property.__get__(instance).value = value


class optional_string_property(properties.base_rw_property[Optional[str], _U]):
    def __init__(self, inner_property: base_property.base_rw_property[Optional[_SV], _U], inner_type: Type[_SV]):
        self._inner_property = inner_property
        self._inner_type = inner_type

    def _get(self, instance: _U) -> Optional[str]:
        s = self._inner_property.__get__(instance)
        return s.value if s is not None else None
    
    def __set__(self, instance: _U, value: Optional[str]) -> None:
        current = self._inner_property.__get__(instance)
        if current is not None and value is not None:
            current.value = value
        else:
            s = self._inner_type.from_value(value) if value is not None else None
            self._inner_property.__set__(instance, s)


class optional_indented_string_property(properties.base_rw_property[Optional[str], _U]):
    def __init__(
            self,
            inner_property: base_property.base_rw_property[Optional[_ISV], _U],
            inner_type: Type[_ISV],
            indent_property: base_property.base_ro_property[_SV, base.RawTreeModel]):
        self._inner_property = inner_property
        self._inner_type = inner_type
        self._indent_property = indent_property

    def _get(self, instance: _U) -> Optional[str]:
        s = self._inner_property.__get__(instance)
        return s.value if s is not None else None
    
    def __set__(self, instance: _U, value: Optional[str]) -> None:
        current = self._inner_property.__get__(instance)
        if current is not None and value is not None:
            current.value = value
        else:
            indent = self._indent_property.__get__(instance).value
            s = self._inner_type.from_value(value, indent=indent) if value is not None else None
            self._inner_property.__set__(instance, s)


class optional_decimal_property(properties.base_rw_property[Optional[decimal.Decimal], _U]):
    def __init__(self, inner_property: base_property.base_rw_property[Optional[_DV], _U], inner_type: Type[_DV]):
        self._inner_property = inner_property
        self._inner_type = inner_type

    def _get(self, instance: _U) -> Optional[decimal.Decimal]:
        s = self._inner_property.__get__(instance)
        return s.value if s is not None else None
    
    def __set__(self, instance: _U, value: Optional[decimal.Decimal]) -> None:
        current = self._inner_property.__get__(instance)
        if current is not None and value is not None:
            current.value = value
        else:
            s = self._inner_type.from_value(value) if value is not None else None
            self._inner_property.__set__(instance, s)


class optional_date_property(properties.base_rw_property[Optional[datetime.date], _U]):
    def __init__(self, inner_property: base_property.base_rw_property[Optional[_DateV], _U], inner_type: Type[_DateV]):
        self._inner_property = inner_property
        self._inner_type = inner_type

    def _get(self, instance: _U) -> Optional[datetime.date]:
        s = self._inner_property.__get__(instance)
        return s.value if s is not None else None
    
    def __set__(self, instance: _U, value: Optional[datetime.date]) -> None:
        current = self._inner_property.__get__(instance)
        if current is not None and value is not None:
            current.value = value
        else:
            s = self._inner_type.from_value(value) if value is not None else None
            self._inner_property.__set__(instance, s)


class _RepeatedValueWrapperUpdateHandler(properties.RepeatedNodeWrapperUpdateHandler):
    def __init__(
            self,
            raw_wrapper: properties.RepeatedNodeWrapper[Any],
            raw_type: Type[_M] | tuple[Type[_M], ...],
            raw_indexes: list[int],
    ) -> None:
        self._raw_wrapper = raw_wrapper
        self._raw_type = raw_type
        self._raw_indexes = raw_indexes

    def handle(self) -> None:
        self._raw_indexes[:] = [
            i for i, model in enumerate(self._raw_wrapper)
            if isinstance(model, self._raw_type)]

    def handle_splice(self, l: int, r: int, values: list[Any]) -> None:
        filtered_indexes = [
            l + i
            for i, value in enumerate(values)
            if isinstance(value, self._raw_type)
        ]
        ll = bisect.bisect_left(self._raw_indexes, l)
        rr = bisect.bisect_left(self._raw_indexes, r)
        diff = len(values) - r + l
        self._raw_indexes[ll:rr] = filtered_indexes
        if diff:
            for i in range(ll + len(filtered_indexes), len(self._raw_indexes)):
                self._raw_indexes[i] += diff


class RepeatedValueWrapper(MutableSequence[_V], Generic[_M, _V]):
    def __init__(
            self,
            raw_wrapper: properties.RepeatedNodeWrapper[_M | Any],
            raw_type: Type[_M] | tuple[Type[_M], ...],
            from_raw_type: Callable[[_M], _V],
            to_raw_type: Callable[[_V], _M],
            update_raw: Callable[[_M, _V], bool],
    ):
        self._raw_wrapper = raw_wrapper
        self._raw_type = raw_type
        self._from_raw_type = from_raw_type
        self._to_raw_type = to_raw_type
        self._update_raw = update_raw
        self._raw_indexes = [
            i for i, item in enumerate(self._raw_wrapper) if isinstance(item, self._raw_type)]
        self._raw_wrapper.register_update_handler(
            _RepeatedValueWrapperUpdateHandler(raw_wrapper, raw_type, self._raw_indexes))

    def _check_type(self, v: Any) -> TypeGuard[_M]:
        return isinstance(v, self._raw_type)

    def __len__(self) -> int:
        return len(self._raw_indexes)

    def __iter__(self) -> Iterator[_V]:
        return (
            self._from_raw_type(self._raw_wrapper[i]) for i in self._raw_indexes)

    @overload
    def __getitem__(self, index: int) -> _V:
        ...
    @overload
    def __getitem__(self, index: slice) -> list[_V]:
        ...
    def __getitem__(self, index: int | slice) -> _V | list[_V]:
        if isinstance(index, int):
            return self._from_raw_type(self._raw_wrapper[self._raw_indexes[index]])
        return [self._from_raw_type(self._raw_wrapper[i]) for i in self._raw_indexes[index]]

    def __delitem__(self, index: int | slice) -> None:
        r = indexes.range_from_index(index, len(self._raw_indexes))
        self._raw_wrapper.drop_many(self._raw_indexes[i] for i in r)

    @overload
    def __setitem__(self, index: int, value: _V) -> None:
        ...
    @overload
    def __setitem__(self, index: slice, value: Iterable[_V]) -> None:
        ...
    def __setitem__(self, index: int | slice, value: _V | Iterable[_V]) -> None:
        if isinstance(index, int):
            values = [cast(_V, value)]
        else:
            assert isinstance(value, Iterable)
            values = list(value)
        r = indexes.range_from_index(index, len(self._raw_indexes))
        raw_indexes_to_update = self._raw_indexes[indexes.slice_from_range(r)]
        # We don't allow assignment with distinct length here because the underlying models may not be consecutive.
        if len(raw_indexes_to_update) != len(values):
            raise ValueError(
                f'attempt to assign sequence of size {len(values)} to extended slice of size '
                f'{len(raw_indexes_to_update)}')
        for raw_index, value in zip(raw_indexes_to_update, values):
            if not self._update_raw(self._raw_wrapper[raw_index], value):
                self._raw_wrapper[raw_index] = self._to_raw_type(value)

    def insert(self, index: int, value: _V) -> None:
        if index >= len(self._raw_indexes):
            raw_index = len(self._raw_wrapper)
        elif index < -len(self._raw_indexes):
            raw_index = 0
        else:
            raw_index = self._raw_indexes[index]
        self._raw_wrapper.insert(raw_index, self._to_raw_type(value))

    def append(self, value: _V) -> None:
        self._raw_wrapper.append(self._to_raw_type(value))

    def clear(self) -> None:
        self._raw_wrapper.drop_many(self._raw_indexes)

    def extend(self, values: Iterable[_V]) -> None:
        self._raw_wrapper.extend(self._to_raw_type(value) for value in values)

    def pop(self, index: int = -1) -> _V:
        if not -len(self._raw_indexes) <= index < len(self._raw_indexes):
            raise IndexError('pop index out of range')
        raw_index = self._raw_indexes[index]
        return self._from_raw_type(self._raw_wrapper.pop(raw_index))

    def remove(self, value: _V) -> None:
        for raw_index in self._raw_indexes:
            if self._from_raw_type(self._raw_wrapper[raw_index]) == value:
                self._raw_wrapper.pop(raw_index)
                return
        raise ValueError(f'{value!r} not found in list')

    def discard(self, value: _V) -> None:
        self._raw_wrapper.drop_many(
            i for i in self._raw_indexes if self._from_raw_type(self._raw_wrapper[i]) == value)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Collection) and
            all(a == b for a, b in itertools.zip_longest(self, other)))


def _update_raw(raw_value: _SV, value: str) -> bool:
    raw_value.value = value
    return True


class repeated_string_property(properties.cached_custom_property[RepeatedValueWrapper[_SV, str], base.RawTreeModel]):
    def __init__(
            self,
            inner_property: base_property.base_ro_property[properties.RepeatedNodeWrapper[_SV | _M], base.RawTreeModel],
            inner_type: Type[_SV]):
        super().__init__(lambda instance: RepeatedValueWrapper[_SV, str](
            raw_wrapper=inner_property.__get__(instance),
            raw_type=inner_type,
            from_raw_type=lambda x: x.value,
            to_raw_type=inner_type.from_value,
            update_raw=_update_raw,
        ))


class RepeatedFilteredNodeWrapper(RepeatedValueWrapper[_M, _M]):
    def __init__(
            self,
            raw_wrapper: properties.RepeatedNodeWrapper[_M | _M2],
            type: Type[_M] | tuple[Type[_M], ...]):
        super().__init__(
            raw_wrapper=raw_wrapper,
            raw_type=type,
            from_raw_type=lambda x: x,
            to_raw_type=lambda x: x,
            update_raw=lambda _, __: False,
        )


class repeated_filtered_node_property(
        properties.cached_custom_property[RepeatedFilteredNodeWrapper[_M], base.RawTreeModel]):
    def __init__(
            self,
            inner_property: base_property.base_ro_property[properties.RepeatedNodeWrapper[_M | Any], base.RawTreeModel],
            type: Type[_M] | tuple[Type[_M], ...]):
        super().__init__(
            lambda instance: RepeatedFilteredNodeWrapper(inner_property.__get__(instance), type))
