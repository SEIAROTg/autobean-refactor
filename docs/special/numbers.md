---
jupytext:
  text_representation:
    format_name: myst
---

# Numbers

```{code-cell} python
:load: ../code/basics.py
:tags: [remove-cell]
```

Beancount supports arithmetic expressions almost wherever numbers are accepted.

## Construction

{py:class}`NumberExpr <autobean_refactor.models.NumberExpr>` supports construction with {py:meth}`from_value <autobean_refactor.models.NumberExpr.from_value>`:

```{code-cell} python
expr = models.NumberExpr.from_value(decimal.Decimal(42))
assert isinstance(expr, models.NumberExpr)
```

## Value access

{py:class}`NumberExpr <autobean_refactor.models.NumberExpr>` supports value reading and writing. Note that value writing essentially replaces the whole expression.

```{code-cell} python
expr = p.parse('1+2*3', models.NumberExpr)
_print_model(expr)
print(expr.value)

expr.value = 8
_print_model(expr)
print(expr.value)
```

## Arithmetic

The following arithmetic operations are supported on {py:class}`NumberExpr <autobean_refactor.models.NumberExpr>`:
* `+`, `-`, `*`, `/`, `//`
* `+=`, `-=`, `*=`, `/=`, `//=`
* `+`, `-` (unary)

The operands may be {py:class}`int`, {py:class}`decimal.Decimal`, or {py:class}`NumberExpr <autobean_refactor.models.NumberExpr>`.

```{code-cell} python
expr = p.parse('1*2+3', models.NumberExpr)
expr *= 4
expr += 5
expr = -expr

_print_model(expr)
print(expr.value)
```

## Ambiguity

One confusing issue with beancount arithmetic expressions is about `custom` where multiple of them can appear consecutively. For example, what does the following `custom` encode?

```beancount
2000-01-01 custom "foo" 1 2 -3
```

Somewhat surprisingly:
```sh
$ echo '2000-01-01 custom "foo" 1 2 -3' | bean-report /dev/stdin print
2000-01-01 custom "foo" 1 -1
```

If we want the arguments to be `[1, 2, -3]`, it must be represented as `2000-01-01 "foo" 1 2 (-3)`:
```sh
$ echo '2000-01-01 custom "foo" 1 2 (-3)' | bean-report /dev/stdin print
2000-01-01 custom "foo" 1 2 -3
```

`autobean-refactor` automatically disambiguates `custom` when constructed with {py:meth}`Custom.from_children <autobean_refactor.models.Custom.from_children>` or {py:meth}`Custom.from_value <autobean_refactor.models.Custom.from_value>`:
```{code-cell} python
custom = models.Custom.from_value(
    date=datetime.date(2000, 1, 1),
    type='foo',
    values=map(decimal.Decimal, [1, 2, -3]))
_print_model(custom)
```

However, that doesn't cover all the cases, you may still accidentally create ambiguity when adding, removing, or modifying arguments, in which case you may manually disambiguate with {py:meth}`NumberExpr.wrap_with_parenthesis <autobean_refactor.models.NumberExpr.wrap_with_parenthesis>`.

```{code-cell} python
custom = p.parse('2000-01-01 custom "foo" 1 2', models.Custom)

custom.values[1] = decimal.Decimal('-2')
_print_model(custom)

custom.raw_values[1].wrap_with_parenthesis()
_print_model(custom)
