
import abc
from typing import TypeVar, final
from typing_extensions import Self
from .. import base
from .value_properties import RWValue

_V = TypeVar('_V')


class SimpleRawTokenModel(base.RawTokenModel):
    @final
    def __init__(self, raw_text: str) -> None:
        super().__init__(raw_text)

    def _clone(self) -> Self:
        return type(self)(self.raw_text)


class SingleValueRawTokenModel(base.RawTokenModel, RWValue[_V]):
    @final
    def __init__(self, raw_text: str, value: _V) -> None:
        super().__init__(raw_text)
        self._value = value

    @classmethod
    def from_raw_text(cls, raw_text: str) -> Self:
        return cls(raw_text, cls._parse_value(raw_text))

    @classmethod
    def from_value(cls, value: _V) -> Self:
        return cls(cls._format_value(value), value)

    @property
    def raw_text(self) -> str:
        return super().raw_text

    @raw_text.setter
    def raw_text(self, raw_text: str) -> None:
        self._update_raw_text(raw_text)
        self._value = self._parse_value(raw_text)

    @property
    def value(self) -> _V:
        return self._value

    @value.setter
    def value(self, value: _V) -> None:
        self._value = value
        self._raw_text = self._format_value(value)

    @classmethod
    @abc.abstractmethod
    def _parse_value(cls, raw_text: str) -> _V:
        pass

    @classmethod
    @abc.abstractmethod
    def _format_value(cls, value: _V) -> str:
        pass

    def _clone(self) -> Self:
        return type(self)(self.raw_text, self.value)


class SimpleSingleValueRawTokenModel(SingleValueRawTokenModel[str]):
    @classmethod
    def _parse_value(cls, raw_text: str) -> str:
        return raw_text

    @classmethod
    def _format_value(cls, value: str) -> str:
        return value


class DefaultRawTokenModel(base.RawTokenModel):
    # not using @classmethod here because it suppresses abstractmethod errors.
    @property
    @abc.abstractmethod
    def DEFAULT(self) -> str:
        ...

    @classmethod
    def from_default(cls) -> Self:
        return cls.from_raw_text(cls.DEFAULT)  # type: ignore[arg-type]


class SimpleDefaultRawTokenModel(SimpleRawTokenModel, DefaultRawTokenModel):
    pass
