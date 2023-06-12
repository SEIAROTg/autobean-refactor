from . import internal


@internal.token_model
class InlineComment(internal.SingleValueRawTokenModel[str]):
    """Comment that does not occupies a whole line."""
    RULE = 'INLINE_COMMENT'

    @classmethod
    def _parse_value(cls, raw_text: str) -> str:
        return raw_text.removeprefix(';').lstrip(' ')

    @classmethod
    def _format_value(cls, value: str) -> str:
        return f'; {value}' if value else ';'
