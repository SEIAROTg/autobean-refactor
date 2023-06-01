---
jupytext:
  text_representation:
    format_name: myst
---

# Indent

```{code-cell} python
:load: ../code/basics.py
:tags: [remove-cell]
```

In `autobean-refactor`, indent is not considered spacing and handled separately.

## The beancount indentation

The indentation in beancount v2 is handled in a somewhat surprising way. The only distinction is whether a line is indented or not, while the indentation characters / levels don't matter.

``````{list-table}
:header-rows: 1

* - Valid
  - Formatted
* - ```beancount
    2000-01-01 *
        foo: 1
       Assets:Foo 100.00 USD
      Assets:Bar -100.00 USD
     bar: 4
    ````
  - ```beancount
    2000-01-01 *
        foo: 1
        Assets:Foo 100.00 USD
        Assets:Bar -100.00 USD
            bar: 4
    ```
``````

## Basic access

In `autobean-refactor`, indent is a children of indentable models (e.g. {py:class}`Posting`, {py:class}`Meta`, {py:class}`BlockComment`), which can be accessed as a simple string model.

```{code-cell} python
txn = p.parse('''\
2000-01-01 *
    foo: 1
   Assets:Foo 100.00 USD
  Assets:Bar -100.00 USD
 bar: 4''', models.Transaction)
txn.postings[1].indent
```

```{code-cell} python
txn.postings[1].indent = ' ' * 4
_print_model(txn)
```

Note that the indent of each line is independent and therefore changing the indent of a posting will have no impact on its meta.

## `indent_by`

When new children are added to a repeated field, its indent is determined as follows:
* For raw models, their own indent is used as is;
* Otherwise, if there are existing children, the indent of the last one is copied over;
* Otherwise, the indent is constructed from the parent's indentation and its `indent_by`.

`indent_by` defaults to four spaces and can be explicitly set at construction in `from_children` or `from_value`, or after construction with the `indent_by` attribute.

```{code-cell} python
txn = p.parse('2000-01-01 *', models.Transaction)
txn.indent_by = ' ' * 2
txn.meta['foo'] = 'foo'
txn.indent_by = ' ' * 8
txn.meta['bar'] = 'bar'
_print_model(txn)
```

```{code-cell} python
txn.meta.clear()
txn.meta['bar'] = 'bar'
_print_model(txn)
```

```{code-cell} python
txn.meta.clear()
meta_item = models.MetaItem.from_value(
    key='qux',
    value=decimal.Decimal(4),
    indent=' ' * 1)
txn.raw_meta.append(meta_item)
_print_model(txn)
```
