# DO NOT EDIT
# This file is automatically generated by autobean_refactor.modelgen.

from typing import Optional, Type, TypeVar, final
from .. import base, internal
from ..escaped_string import EscapedString
from ..punctuation import Eol, Whitespace

_Self = TypeVar('_Self', bound='Plugin')


@internal.token_model
class PluginLabel(internal.SimpleDefaultRawTokenModel):
    RULE = 'PLUGIN'
    DEFAULT = 'plugin'


@internal.tree_model
class Plugin(base.RawTreeModel):
    RULE = 'plugin'

    _label = internal.required_field[PluginLabel]()
    _name = internal.required_field[EscapedString]()
    _config = internal.optional_field[EscapedString](separators=(Whitespace.from_default(),))
    _eol = internal.required_field[Eol]()

    raw_name = internal.required_node_property(_name)
    raw_config = internal.optional_node_property(_config)

    name = internal.required_string_property(raw_name)
    config = internal.optional_string_property(raw_config, EscapedString)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            label: PluginLabel,
            name: EscapedString,
            config: internal.Maybe[EscapedString],
            eol: Eol,
    ):
        super().__init__(token_store)
        self._label = label
        self._name = name
        self._config = config
        self._eol = eol

    @property
    def first_token(self) -> base.RawTokenModel:
        return self._label.first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return self._eol.last_token

    def clone(self: _Self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> _Self:
        return type(self)(
            token_store,
            self._label.clone(token_store, token_transformer),
            self._name.clone(token_store, token_transformer),
            self._config.clone(token_store, token_transformer),
            self._eol.clone(token_store, token_transformer),
        )

    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._label = self._label.reattach(token_store, token_transformer)
        self._name = self._name.reattach(token_store, token_transformer)
        self._config = self._config.reattach(token_store, token_transformer)
        self._eol = self._eol.reattach(token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, Plugin)
            and self._label == other._label
            and self._name == other._name
            and self._config == other._config
            and self._eol == other._eol
        )

    @classmethod
    def from_children(
            cls: Type[_Self],
            name: EscapedString,
            config: Optional[EscapedString] = None,
    ) -> _Self:
        label = PluginLabel.from_default()
        maybe_config = internal.MaybeL.from_children(config, separators=cls._config.separators)
        eol = Eol.from_default()
        tokens = [
            *label.detach(),
            Whitespace.from_default(),
            *name.detach(),
            *maybe_config.detach(),
            *eol.detach(),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        label.reattach(token_store)
        name.reattach(token_store)
        maybe_config.reattach(token_store)
        eol.reattach(token_store)
        return cls(token_store, label, name, maybe_config, eol)

    @classmethod
    def from_value(
            cls: Type[_Self],
            name: str,
            config: Optional[str] = None,
    ) -> _Self:
        return cls.from_children(
            EscapedString.from_value(name),
            EscapedString.from_value(config) if config is not None else None,
        )
