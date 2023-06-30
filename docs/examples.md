---
jupytext:
  text_representation:
    format_name: myst
---

# Examples

```{code-cell} python
:load: ./code/basics.py
:tags: [hide-input, remove-output]
```

## Rename accounts

```{code-cell} python
def rename_account(model: models.RawModel, from_account: str, to_account: str):
    for token in model.tokens:
        if isinstance(token, models.Account) and token.value == from_account:
            token.value = to_account


file = p.parse('''\
; leading comment
2000-01-01 open Assets:Foo ; inline comment
2000-01-01 open Assets:Bar
2000-01-01 *
    Assets:Foo -100.00 USD
    Assets:Bar 100.00 USD
2000-01-02 balance Assets:Foo -100.00 USD
''', models.File)

rename_account(file, 'Assets:Foo', 'Liabilities:Foo')

_print_model(file)
```

## Rename accounts based on narration

```{code-cell} python
file = p.parse('''\
2000-01-01 * "groceries"
    Assets:Foo -100.00 USD
    Expenses:Unclassified 100.00 USD ; inline comment
    ; trailing comment
2000-01-01 * "fuel"
    Assets:Foo -100.00 USD
    Expenses:Unclassified 100.00 USD
2000-01-01 *
    Assets:Foo -100.00 USD
    Expenses:Unclassified 100.00 USD
''', models.File)

for directive in file.directives:
    if isinstance(directive, models.Transaction) and directive.narration == 'groceries':
        rename_account(directive, 'Expenses:Unclassified', 'Expenses:Groceries')

_print_model(file)
```

## Reorder meta

```{code-cell} python
file = p.parse('''\
2000-01-01 *
    time: "08:00"
    foo: "xxx"
2000-01-01 *
    foo: "xxx"
    ; leading comment
    time: "10:00" ; inline comment
    bar: "xxx"
2000-01-01 *
    foo: "xxx"
''', models.File)

for directive in file.directives:
    if isinstance(directive, models.Transaction):
        # make "time" the first meta
        time_meta = directive.raw_meta.pop('time', None)
        if time_meta:
            directive.raw_meta.insert(0, time_meta)

_print_model(file)
```
