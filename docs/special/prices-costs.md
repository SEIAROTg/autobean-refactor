---
jupytext:
  text_representation:
    format_name: myst
---

# Prices and Costs

```{code-cell} python
:load: ../code/basics.py
:tags: [remove-cell]
```

## Beancount limitation

One limitation of the official beancount data model is that the distinction of total price and unit price disappears during parsing, and therefore with the official library, there is no way to tell which form the original definition uses, to read the total cost, or to output a total cost.

## Basic access

Fortunately, `autobean-refactor` does not have the same issue. In `autobean-refactor`, there are {py:class}`UnitPrice <autobean_refactor.models.UnitPrice>`, {py:class}`TotalPrice <autobean_refactor.models.TotalPrice>`, {py:class}`UnitCost <autobean_refactor.models.UnitCost>`, and {py:class}`TotalCost <autobean_refactor.models.TotalCost>`. The `Unit-` and `Total-` versions are almost identical except being different type, allowing case distinction.

## Price access

To check type:

```{code-cell} python
posting = p.parse('    Assets:Foo 100.00 GBP @@ 130.00 USD', models.Posting)
assert isinstance(posting.price, models.TotalPrice)
assert not isinstance(posting.price, models.UnitPrice)
_print_model(posting)
```

To read value:

```{code-cell} python
(posting.price.number, posting.price.currency)
```

To modify value:

```{code-cell} python
posting.price.number = decimal.Decimal('135.00')
_print_model(posting)
```

To flip type:

```{code-cell} python
posting.price = models.UnitPrice.from_value(
    number=posting.price.number / posting.number,
    currency=posting.price.currency)
_print_model(posting)
```

## Cost access

The interface for costs is more complex as costs can carry more information.

To check type:

```{code-cell} python
posting = p.parse(
    '    Assets:Foo 100.00 GBP { 1.30 USD, 2000-01-01, "foo", * }',
    models.Posting)
assert isinstance(posting.cost.raw_cost, models.UnitCost)
assert not isinstance(posting.cost.raw_cost, models.TotalCost)
_print_model(posting)
```

To read value:

```{code-cell} python
(posting.cost.number_per, posting.cost.number_total, posting.cost.currency)
```

To modify value:

```{code-cell} python
posting.cost.number_per = decimal.Decimal('1.35')
posting.cost.label = 'bar'
_print_model(posting)
```

To flip type:

```{code-cell} python
num = posting.cost.number_per
posting.cost.number_per = None
posting.cost.number_total = num * posting.number
_print_model(posting)
```
