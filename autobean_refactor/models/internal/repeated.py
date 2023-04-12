import copy
from typing import Generic, Iterable, Iterator, Optional, TypeVar
from typing_extensions import Self
from .. import base
from .placeholder import Placeholder

_M = TypeVar('_M', bound=base.RawModel)

class Repeated(base.RawTreeModel, Generic[_M]):
    def __init__(
            self,
            token_store: base.TokenStore,
            items: Iterable[_M],
            placeholder: Placeholder,
    ) -> None:
        super().__init__(token_store)
        self.items = list(items)
        self._placeholder = placeholder

    @property
    def placeholder(self) -> Placeholder:
        return self._placeholder

    @property
    def first_token(self) -> base.RawTokenModel:
        return self._placeholder

    @property
    def last_token(self) -> base.RawTokenModel:
        if self.items:
            return self.items[-1].last_token
        return self._placeholder

    def _eq(self, other: base.RawTreeModel) -> bool:
        return isinstance(other, Repeated) and self.items == other.items

    @classmethod
    def from_children(
            cls,
            items: Iterable[_M],
            *,
            separators: tuple[base.RawTokenModel, ...],
            separators_before: Optional[tuple[base.RawTokenModel, ...]] = None,
    ) -> Self:
        placeholder = Placeholder.from_default()
        items = list(items)
        tokens: list[base.RawTokenModel] = [placeholder]
        for i, item in enumerate(items):
            if i == 0 and separators_before is not None:
                tokens.extend(copy.deepcopy(separators_before))
            else:
                tokens.extend(copy.deepcopy(separators))
            tokens.extend(item.detach())
        token_store = base.TokenStore.from_tokens(tokens)
        for item in items:
            item.reattach(token_store)
        return cls(token_store, items, placeholder)

    def clone(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> Self:
        return type(self)(
            token_store,
            (item.clone(token_store, token_transformer) for item in self.items),
            self.placeholder.clone(token_store, token_transformer))

    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self.items = [item.reattach(token_store, token_transformer) for item in self.items]
        self._placeholder = self._placeholder.reattach(token_store, token_transformer)

    def auto_claim_comments(self) -> None:
        for item in reversed(self.items):
            item.auto_claim_comments()

    def iter_children_formatted(self) -> Iterator[tuple[base.RawModel, bool]]:
        # should have been handled in repeated_field, who has access to separators
        raise NotImplementedError()
