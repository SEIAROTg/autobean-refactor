---
jupytext:
  text_representation:
    format_name: myst
---

# Token Models

Token models model leaf nodes in the AST, who may not have children.

```{code-cell} python
:load: ../code/parsing.py
:tags: [hide-input]
```

## Common interfaces

### `raw_text`

All token models have a string property `raw_text` which returns the raw text of the token.

`value` usually gives a more useful representation of the token, but `raw_text` allows more precise manipulation of the token.

```{code-cell} python
(comment.raw_text, string1.raw_text, string2.raw_text, number.raw_text)
```

### `value`

Many token models have a property `value` which returns the semantic value of the token.

```{code-cell} python
(comment.value, string1.value, string2.value, number.value)
```

### `from_raw_text`

All token models have a class method `from_raw_text` which constructs a new token model from the raw text.

This constructs a token model with the exact raw text, and therefore:
* ✅ `type(token).from_raw_text(token.raw_text) == token`
* ✅ `type(token).from_value(token.value).value == token.value` (if `value` is supported)

```python
>>> comment == models.BlockComment.from_raw_text('; comment')
True
>>> comment == models.BlockComment.from_raw_text(';comment')
False
```

### `from_value`

Many token models have a class method `from_value` which constructs a new token model from the semantic value.

Some default formatting will apply, and therefore:
* ❌ `type(token).from_value(token.value) == token`
* ✅ `type(token).from_value(x).value == token.value`

```python
>>> models.BlockComment.from_value('comment').raw_text
'; comment'
>>> models.EscapedString.from_value('foo\n').raw_text
'foo\n'
>>> models.Number.from_value(decimal.Decimal('1234.56')).raw_text
'1234.56'
```

## List of all token models

```{code-cell} python
sorted([
    model.__name__ for model in models.__dict__.values()
    if isinstance(model, type) and issubclass(model, models.RawTokenModel)])
```
