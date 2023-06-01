---
jupytext:
  text_representation:
    format_name: myst
---

# Getting started

autobean-refactor is an ergonomic and lossless beancount manipulation library, offering easy interfaces to parse, manipulate, construct, and print [beancount](https://github.com/beancount/beancount) ledger.

## Install

```sh
pip install autobean-refactor
```

## Parsing

```{code-cell} python
:load: ./code/parsing.py
```

## Printing

```{code-cell} python
import io
from autobean_refactor import printer

printer.print_model(file, io.StringIO()).getvalue()
```

```{tableofcontents}
```
