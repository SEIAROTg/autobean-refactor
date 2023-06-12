---
jupytext:
  text_representation:
    format_name: myst
---

# Meta

```{code-cell} python
:load: ../code/basics.py
:tags: [remove-cell]
```

For models that could carry meta, they are accessible through three attributes:
* `raw_meta_with_comments`: {py:class}`MutableSequence[MetaItem | BlockComment] <collections.abc.MutableSequence>`, providing by-index access to {py:class}`MetaItem <autobean_refactor.models.MetaItem>` and [](../special/comments.md#standalone-comments).
* `raw_meta`: {py:class}`MutableSequence[MetaItem] <collections.abc.MutableSequence>` and {py:class}`MutableMapping[str, MetaItem] <collections.abc.MutableMapping>`, providing by-index and by-key access to {py:class}`MetaItem <autobean_refactor.models.MetaItem>`.
* `meta`: {py:class}`MutableSequence[MetaItem] <collections.abc.MutableSequence>` and {py:class}`MutableMapping[str, MetaValue | MetaRawValue] <collections.abc.MutableMapping>`, providing by-index access to {py:class}`MetaItem <autobean_refactor.models.MetaItem>` and by-key access to {py:class}`MetaValue <autobean_refactor.models.MetaValue>`.

```{code-cell} python
:tags: [remove-output]

txn = p.parse('''\
2000-01-01 *
    foo: 1
    ; comment
    bar: 2''', models.Transaction, auto_claim_comments=False)
txn.raw_meta_with_comments.claim_interleaving_comments()
```

Read:

```{code-cell} python
_print_model(txn.raw_meta_with_comments[1])
_print_model(txn.raw_meta[1])
_print_model(txn.raw_meta['bar'])
print(txn.raw_meta[1].key)
print(repr(txn.meta['bar']))
print(list(txn.raw_meta.keys()))
print(list(txn.meta.values()))
```

Write:

```{code-cell} python
for i, item in enumerate(txn.raw_meta):
    item.key += '-updated'
    item.value = str(i)
_print_model(txn)

txn.raw_meta.pop(0)
txn.meta['baz'] = models.Account.from_value('Assets:Foo')
_print_model(txn)
```
