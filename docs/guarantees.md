# Guarantees

`autobean-refactor` is a **lossless** beancount manipulation library by providing the following guarantees, not subject to legal liability:
* ✅ If no operations are performed, the output is **character-by-character** idential to the input.
* ✅ If a fragment is modified, everything outside that fragment remains character-by-character identical to the input.
* ✅ If a fragment is added or removed, everything outside that fragment remains character-by-character identical to the input, except that its surrounding spaces may be added or removed.

Notably, the following are usually true but **NOT** 100% guaranteed:
* ❗ `autobean-refactor` and beancount v2 parser has exactly same grammar.
    * Out-of-line tags / links in transaction are not supported yet.
    * `autobean-refactor` is based on Unicode while the beancount v2 parser is based on bytes.
* ❗ The output is always syntatically valid.
  * It's possible to remove necessary spaces or indent and make it no longer valid.
  * It's possible to forcefully put string into a number token and make it no longer valid.
* ❗ If no operations are performed, the output is **byte-to-byte** identical to the input.
  * `autobean-refactor` is based on Unicode and does not guarantee byte-level preservation.
* ❗ `model.value = model.value` does not change anything.
  * [Example](./special/numbers.md#value-access).
