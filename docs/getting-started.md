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

## In-place editing

```{code-cell}python
import pathlib
import tempfile
from autobean_refactor import editor, models

e = editor.Editor()

with tempfile.TemporaryDirectory() as tmpdir:
    p = pathlib.Path(tmpdir)

    # creates some files
    (p / 'index.bean').write_text('include "??.bean"')
    (p / '01.bean').write_text('2000-01-01 *')
    (p / '02.bean').write_text('2000-01-01 *')

    # edits a single file
    with e.edit_file(p / '01.bean') as file:
        # appends a comment to 01.bean
        file.raw_directives_with_comments.append(models.BlockComment.from_value('updated1'))

    # edits files recursively (follows includes)
    with e.edit_file_recursive(p / 'index.bean') as files:
        # appends a comment to 01.bean
        files[str(p / '01.bean')].raw_directives_with_comments.append(
            models.BlockComment.from_value('updated2'))
        # deletes 02.bean
        files.pop(str(p / '02.bean'))

    for path in p.iterdir():
        print(f'{"=" * 20}[{path}]{"=" * 20}')
        print((p / path).read_text())
```

```{tableofcontents}
```
