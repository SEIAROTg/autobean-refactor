---
jupytext:
  text_representation:
    format_name: myst
---

# Comments

```{code-cell} python
:load: ../code/basics.py
:tags: [remove-cell]
```

## Leading, trailing, and inline comments

Leading, trailing, and inline comments can be accessed similar to other optional string properties, through `raw_leading_comment`, `leading_comment`, `raw_inline_comment`, `inline_comment`, `raw_trailing_comment`, and `trailing_comment` attributes.

```{code-cell} python
close = p.parse('''\
; leading
2000-01-01 close Assets:Foo ; inline
; trailing\
''', models.Close)
```

Read:

```{code-cell} python
(close.leading_comment, close.inline_comment, close.raw_trailing_comment.raw_text)
```

Write:

```{code-cell} python
close.leading_comment = 'updated'
close.inline_comment = None
close.raw_trailing_comment = models.BlockComment.from_raw_text(';nospace')

_print_model(close)
```

## Standalone comments

Some comments don't really belong to a model. These are standalone comments (or sometimes referred to as interleaving comments), which is accessible in the same repeated fields with its peer models.

```{code-cell} python
file = p.parse('''\
; standalone

2000-01-01 open Assets:Foo''', models.File)
```

Read:

```{code-cell} python
file.raw_directives_with_comments[0].value
```

Write:

```{code-cell} python
file.raw_directives_with_comments[0].value = 'updated'

_print_model(file)
```

## Ownership

Same as other models, comments have unique ownership and can only be accessed through its owner. In the example below, `; inline comment` clearly belongs to `open` and can therefore be accessed through `open.inline_comment`. `; block comment` is more complex. It may be the trailing comment for `open`, or the leading comment for `close`, or a standalone comment between them, but it may only belong to one of them at any given time.

```beancount
2000-01-01 open Assets:Foo ; inline comment
; block comment
2000-01-01 close Assets:Foo
```

But which one exactly? As a generic library, `autobean-refactor` doesn't know the answer for sure. It therefore tries to do something reasonable, while allowing manual adjustment if needed.

### Automatic comment attribution

All models have a method `auto_claim_comments` which attributes comments to children models following the default rules:

* If it's immediately before a model with the same indentation and no blank lines in betwen, it's a leading comment.
* Otherwise, if it's immediately after a model with the same indentation and no blank lines in betwen, it's a trailing comment.
* Otherwise, it's a standalone comment.

This happens by default at the end of `parse` but you may opt-out with `auto_claim_comments=False`.

```{code-cell} python
file = p.parse('''\
; standalone
2000-01-01 open Assets:Foo\
''', models.File, auto_claim_comments=False)

(len(file.raw_directives_with_comments), file.directives[0].leading_comment)
```

### Manual comment attribution

If you don't want the default automatic comment attribution, or want to make some adjustments, you may do so with:
* (for leading and trailing comments) `claim_leading_comment`, `unclaim_leading_comment`, `claim_trailing_comment`, and `unclaim_trailing_comment`.
* (for standalone comments) `claim_interleaving_comments`, and `unclaim_interleaving_comments`.

```{code-cell} python
file = p.parse('''\
2000-01-01 open Assets:Foo
; comment
2000-01-02 close Assets:Foo\
''', models.File)

open, close = file.raw_directives_with_comments
close.unclaim_leading_comment()
open.claim_trailing_comment()

(open.trailing_comment, close.leading_comment)
```

```{code-cell} python
file.raw_directives_with_comments.claim_interleaving_comments([
    open.unclaim_trailing_comment(),
])

(open.trailing_comment, file.raw_directives_with_comments[1].raw_text)
```
