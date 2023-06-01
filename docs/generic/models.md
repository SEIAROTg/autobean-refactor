---
jupytext:
  text_representation:
    format_name: myst
---

# Models

```{code-cell} python
:load: ../code/basics.py
:tags: [remove-cell]
```

Models model beancount AST nodes. There are two types of models, [token models](./token-models.md) and [tree models](./tree-models.md).

## Common interfaces

The following interfaces are shared by all models, whether token or not.

### `__deepcopy__`

All models can be deep-copied, which makes an exact copy of everything in the model, into a separate token store.

```{code-cell} python
:tags: [raises-exception]
file = p.parse('''\
2000-01-01  * ; inline comment
2000-01-02 *
''', models.File)
file.directives.append(file.directives[0])
```

```{code-cell} python
txn_copy = copy.deepcopy(file.directives[0])
file.directives.append(txn_copy)

_print_model(file)
```

### `__eq__`

All models supports equality check. Two models are only equal if and only if:

* They have the exact same type, and
* They have the exact same text representations, and
* They have the exact same structure.

### `tokens`

All models have a property `tokens` which returns a list of tokens inside that model. For a token, this returns itself.

```{code-cell} python
close = p.parse('2000-01-01 close Assets:Foo ; inline comment', models.Close)
close.tokens
```

```{code-cell} python
close.raw_inline_comment.tokens
```
