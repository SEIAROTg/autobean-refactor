import datetime
import itertools
from typing import Iterable, Mapping, Optional
from typing_extensions import Self
from . import internal, meta_item_internal
from .date import Date
from .account import Account
from .block_comment import BlockComment
from .escaped_string import EscapedString
from .inline_comment import InlineComment
from .link import Link
from .tag import Tag
from .generated import note
from .generated.note import NoteLabel
from .meta_value import MetaRawValue, MetaValue



@internal.tree_model
class Note(note.Note):
    tags = internal.repeated_string_property(note.Note.raw_tags_links, Tag)
    links = internal.repeated_string_property(note.Note.raw_tags_links, Link)

    @classmethod
    def from_value(
            cls,
            date: datetime.date,
            account: str,
            comment: str,
            *,
            tags: Iterable[str] = (),
            links: Iterable[str] = (),
            leading_comment: Optional[str] = None,
            inline_comment: Optional[str] = None,
            meta: Optional[Mapping[str, MetaValue | MetaRawValue]] = None,
            trailing_comment: Optional[str] = None,
            indent_by: str = '    ',
    ) -> Self:
        return cls.from_children(
            date=Date.from_value(date),
            account=Account.from_value(account),
            comment=EscapedString.from_value(comment),
            tags_links=itertools.chain(map(Tag.from_value, tags), map(Link.from_value, links)),
            leading_comment=BlockComment.from_value(leading_comment) if leading_comment is not None else None,
            inline_comment=InlineComment.from_value(inline_comment) if inline_comment is not None else None,
            meta=meta_item_internal.from_mapping(meta, indent=indent_by) if meta is not None else (),
            trailing_comment=BlockComment.from_value(trailing_comment) if trailing_comment is not None else None,
            indent_by=indent_by,
        )
