---
jupytext:
  text_representation:
    format_name: myst
---

# Tree Models

```{code-cell} python
:load: ../code/basics.py
:tags: [remove-cell]
```

Tree models model the AST nodes that may have children.

## Raw and value properties

Tree models have many properties, some have a `raw_` prefix (raw properties) and many raw properties have a corresponding value property without the `raw_` prefix. The raw properties provide raw access to children, while the value properties provide access to the semantic value of those children. For example:

```{code-cell} python
balance = p.parse('2000-01-01 balance Assets:Foo 100 * 2.00 USD ; comment', models.Balance)
_print_model(balance.raw_number)
```

```{code-cell} python
(balance.number, balance.raw_number.value)
```

Value properties should suffice for most cases but raw properties are provided to allow more fine-grained and lossless access to the tree structure, for example, when you want to access the expression above.

Value properties sometimes also returns models, usually to make distinction between different types of values (e.g. unit cost vs total cost; string vs currency).

Not all raw properties have corresponding value properties. For example, `File.raw_directives_with_comments` doesn't have a obvious way to simplify.

## Required properties

Some children of a model is required by the beancount syntax, and those children are modeled in required properties.

Required properties always have values. They may be read, updated, but cannot be deleted, or created.

```{code-cell} python
(balance.raw_date, balance.date)
```

```{code-cell} python
balance.date = datetime.date(2000, 1, 2)
balance.raw_currency = models.Currency.from_value('GBP')

_print_model(balance)
```

## Optional properties

Some children of a model is optional, and those children are modeled in optional properties.

Optional properties may be `None`, and may be set to and from `None` in order to delete or create them.

```{code-cell} python
balance.raw_inline_comment = None
balance.tolerance = decimal.Decimal('0.01')

_print_model(balance)
```

## Repeated properties

Repeated properties returns a wrapper that implements {py:class}`MutableSequence <collections.abc.MutableSequence>`.

```{code-cell} python
custom = p.parse('2000-01-01 custom "type" 123.45 Assets:Foo TRUE "foo"', models.Custom)

(custom.values[1], list(custom.raw_values))
```

```{code-cell} python
custom.values[3] = datetime.date(2000, 1, 2)
del custom.values[1:3]

_print_model(custom)
```

### Filtered repeated properties

Filtered repeated properties is a special type of repeated properties. This can be useful when the gramma allows multiple types of children to interleave, but you are only interested in a certain type.

```{code-cell} python
note = p.parse('2000-01-01 note Assets:Foo "note" #tag0 ^link0 #tag1 ^link1', models.Note)
note.tags[1] = 'updated'

_print_model(note)
```

## Construction

Most tree models can be constructed with class methods `from_children`, which takes children models, or `from_value`, which takes semantic values. Refer to the method signature for accepted arguments.

```{warning}
Do not construct models directly with `ModelType(...)`.
```

```{code-cell} python
close1 = models.Close.from_children(
    date=models.Date.from_value(datetime.date(2000, 1, 2)),
    account=models.Account.from_value('Assets:Foo'),
    inline_comment=models.InlineComment.from_value('comment'),
)
close2 = models.Close.from_value(
    date=datetime.date(2000, 1, 2),
    account='Assets:Foo',
    inline_comment='comment',
)
_print_model(close1)
_print_model(close2)
```

## List of all tree models

```{code-cell} python
sorted([
    model.__name__ for model in models.__dict__.values()
    if isinstance(model, type) and issubclass(model, models.RawTreeModel)])
```
