---
jupytext:
  text_representation:
    format_name: myst
---

# Spacing

## Basic access

Spacing (whitespace, tab, or newline) can be accessed in the similar way as other optional properties, through `raw_spacing_before`, `spacing_before`, `raw_spacing_after`, and `spacing_after`.

```{note}
Indentation is NOT considered as spacing here.
```

```{code-cell} python
:load: ../code/basics.py
:tags: [remove-cell]
```

```{code-cell} python
file = p.parse('''\
2000-01-01 open Assets:Foo

\t

2000-01-02close Assets:Foo
''', models.File)
open, close = file.directives
```

Read:

```{code-cell} python
(close.spacing_before, close.raw_spacing_before)
```

```{code-cell} python
(close.raw_date.spacing_after, close.raw_date.raw_spacing_after)
```

Write:

```{code-cell} python
close.spacing_before = '\n\n'

_print_model(file)
```

## Ownership

Unlikely other models, spacing has no ownership. In the example above, the space between `open` and `close` can be accessed through **both** `open.spacing_after` and `close.spacing_before`.

```{code-cell} python
(open.raw_spacing_after, close.raw_spacing_before)
```
