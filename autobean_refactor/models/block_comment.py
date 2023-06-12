from typing import final
from typing_extensions import Self
from . import base
from .internal import registry as _registry
from .internal import spacing_accessors as _spacing_accessors
from .internal import value_properties as _value_properties


def _splitlines(s: str) -> list[str]:
    lines = s.splitlines(keepends=True)
    if not lines or lines[-1].endswith('\n'):
        lines.append('')
    return lines


@_registry.token_model
class BlockComment(base.RawTokenModel, _value_properties.RWValueWithIndent[str], _spacing_accessors.SpacingAccessorsMixin):
    """Comment that occupies one or more whole lines."""
    RULE = 'BLOCK_COMMENT'

    @final
    def __init__(self, raw_text: str, indent: str, value: str, *, claimed: bool = True) -> None:
        super().__init__(raw_text)
        self._value = value
        self._indent = indent
        self._claimed = claimed

    @property
    def raw_text(self) -> str:
        return super().raw_text

    @raw_text.setter
    def raw_text(self, raw_text: str) -> None:
        self._update_raw_text(raw_text)
        self._indent, self._value = self._parse_value(raw_text)

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._value = value
        self._update_raw_text(self._format_value(self._indent, value))

    @property
    def indent(self) -> str:
        return self._indent

    @indent.setter
    def indent(self, indent: str) -> None:
        self._indent = indent
        self._update_raw_text(self._format_value(indent, self._value))

    @property
    def claimed(self) -> bool:
        return self._claimed

    @claimed.setter
    def claimed(self, claimed: bool) -> None:
        self._claimed = claimed

    @classmethod
    def from_value(cls, value: str, *, indent: str = '') -> Self:
        return cls(cls._format_value(indent, value), indent, value)

    @classmethod
    def from_raw_text(cls, raw_text: str) -> Self:
        indent, value = cls._parse_value(raw_text)
        return cls(raw_text, indent, value)

    @classmethod
    def _parse_value(cls, raw_text: str) -> tuple[str, str]:
        indents, values = zip(*(
            tuple(line.split(';', maxsplit=1))
            for line in _splitlines(raw_text)
        ))
        lines = list(values)
        spaced = all(not line.rstrip('\r\n') or line.startswith(' ') for line in lines)
        if spaced:
            lines = [line.removeprefix(' ') for line in lines]

        return indents[0], ''.join(lines)

    @classmethod
    def _format_value(cls, indent: str, value: str) -> str:
        return ''.join(
            f'{indent}; {line}' if line.rstrip('\r\n') else f'{indent};{line}'
            for line in _splitlines(value)
        )

    def _clone(self: 'BlockComment') -> 'BlockComment':
        return type(self)(self.raw_text, self.indent, self.value, claimed=self.claimed)
