import collections
import copy
import enum
import glob
import os.path
import pathlib
import re
from typing import Iterable, Iterator, Optional, Type, TypeVar
import lark
from lark import exceptions
from lark import lexer
from lark import load_grammar
from autobean_refactor import models
from autobean_refactor.models import internal

_T = TypeVar('_T', bound=models.RawTokenModel)
_U = TypeVar('_U', bound=models.RawTreeModel)


with open(pathlib.Path(__file__).parent / 'beancount.lark') as f:
    _GRAMMAR, _ = load_grammar.load_grammar(
        grammar=f.read(),
        source=f.name,
        import_paths=[],
        global_keep_all_tokens=False)
    _IGNORED_TOKENS = frozenset(_GRAMMAR.ignore)
    _GRAMMAR.ignore.clear()


class PostLexInline(lark.lark.PostLex):
    always_accept = _IGNORED_TOKENS

    def process(self, stream: Iterator[lark.Token]) -> Iterator[lark.Token]:
        return stream


class PostLex(lark.lark.PostLex):
    _NEWLINE_INDENT_COMMENT_SPLIT_RE = re.compile(r'([\r\n]*)([ \t]*)(;.*)?', re.S)
    _NEWLINE_INDENT_COMMENT = '_NEWLINE_INDENT_COMMENT'
    _NEWLINE = '_NEWLINE'
    _EOL = 'EOL'
    _INDENT_MARK = 'INDENT_MARK'
    _DEDENT_MARK = 'DEDENT_MARK'
    _INDENT = 'INDENT'
    _BLOCK_COMMENT = 'BLOCK_COMMENT'

    # Contextual lexer only sees _EOL and will thus reject _NEWLINE by default.
    always_accept = _IGNORED_TOKENS | {_NEWLINE_INDENT_COMMENT}

    def process(self, stream: Iterator[lark.Token]) -> Iterator[lark.Token]:
        indented = False
        token = None
        prev_is_block_comment = False
        for token in stream:
            if token.type != self._NEWLINE_INDENT_COMMENT:
                yield token
                continue
            match = self._NEWLINE_INDENT_COMMENT_SPLIT_RE.fullmatch(token.value)
            assert match
            newline_text, indent_text, comment_text = match.groups()
            if newline_text and not prev_is_block_comment:
                yield lark.Token.new_borrow_pos(self._EOL, '', token)
            if not indent_text and indented:
                indented = False
                yield lark.Token.new_borrow_pos(self._DEDENT_MARK, '', token)
            if newline_text:
                yield lark.Token.new_borrow_pos(self._NEWLINE, newline_text, token)
            prev_is_block_comment = False
            if indent_text and not indented:
                indented = True
                yield lark.Token.new_borrow_pos(self._INDENT_MARK, '', token)
            if comment_text:
                prev_is_block_comment = True
                yield lark.Token.new_borrow_pos(self._BLOCK_COMMENT, indent_text + comment_text, token)
            elif indent_text:
                yield lark.Token.new_borrow_pos(self._INDENT, indent_text, token)
        if not prev_is_block_comment:
            yield lark.Token(self._EOL, '')
        if indented:
            yield lark.Token(self._DEDENT_MARK, '')


class _Floating(enum.Enum):
    LEFT = enum.auto()
    RIGHT = enum.auto()


def _get_include_paths(path: str, file: models.File) -> Iterable[str]:
    for directive in file.raw_directives:
        if not isinstance(directive, models.Include):
            continue
        matches = glob.glob(os.path.join(os.path.dirname(path), directive.filename), recursive=True)
        if not matches:
            lineno = directive.token_store.get_position(directive.first_token).line
            raise ValueError(f'No files match {directive.filename!r} ({path}:{lineno})')
        for match in matches:
            yield os.path.normpath(match)


class Parser:
    _lark: lark.Lark
    _token_models: dict[str, Type[models.RawTokenModel]]
    _tree_models: dict[str, Type[models.RawTreeModel]]

    def __init__(self) -> None:
        start = list(models.TREE_MODELS.keys())
        self._lark = lark.Lark(
            _GRAMMAR, lexer='contextual', parser='lalr', postlex=PostLex(), start=start)
        self._lark_inline = lark.Lark(
            _GRAMMAR, lexer='contextual', parser='lalr', postlex=PostLexInline(), start=start)

    def parse_token(self, text: str, target: Type[_T]) -> _T:
        """Parses one token.

        This is a separate method to ease typing and support ignored tokens.
        """
        lexer_conf = copy.deepcopy(self._lark.parser.lexer_conf)
        lexer_conf.terminals = [lexer_conf.terminals_by_name[target.RULE]]
        basic_lexer = lexer.BasicLexer(lexer_conf)
        lexer_thread = lexer.LexerThread.from_text(basic_lexer, text)
        tokens = list(lexer_thread.lex(None))
        if not tokens:
            raise exceptions.UnexpectedToken(
                lark.Token('$END', '', 0, 1, 1), {target.RULE})
        if tokens[0].type != target.RULE:
            raise exceptions.UnexpectedToken(tokens[0], {target.RULE})
        if len(tokens) > 1:
            raise exceptions.UnexpectedToken(tokens[1], {'$END'})
        return target.from_raw_text(tokens[0].value)

    def parse(self, text: str, target: Type[_U]) -> _U:
        if target.INLINE:
            return self._parse(text, target, self._lark_inline)
        else:
            return self._parse(text, target, self._lark)

    def parse_file_recursive(self, path: str) -> dict[str, models.File]:
        files = {}
        queue = collections.deque([path])

        while queue:
            path = queue.popleft()
            if path in files:
                continue
            with open(path) as f:
                text = f.read()
            file = self.parse(text, models.File)
            files[path] = file
            queue.extend(_get_include_paths(path, file))
        
        return files

    def _parse(self, text: str, target: Type[_U], lark_instance: lark.Lark) -> _U:
        parser = lark_instance.parse_interactive(text=text, start=target.RULE)
        tokens = []
        for token in parser.lexer_thread.lex(parser.parser_state):
            tokens.append(token)
            if token.type not in _IGNORED_TOKENS or token.type in parser.choices():
                parser.feed_token(token)
        tree = parser.feed_eof()

        return ModelBuilder(tokens).build(tree, target)


class ModelBuilder:
    def __init__(self, tokens: list[lark.Token]):
        self._tokens = tokens
        self._built_tokens: list[models.RawTokenModel] = []
        self._token_to_index = {id(token): i for i, token in enumerate(tokens)}
        self._cursor = 0
        self._token_store = models.TokenStore.from_tokens([])

    def _add_tokens(self, tokens: Iterable[models.RawTokenModel]) -> None:
        self._built_tokens.extend(tokens)

    def _fix_gap(self, cursor: int) -> None:
        for token in self._tokens[self._cursor:cursor]:
            if not token.value:  # skips EOL, INDENT_MARK, DEDENT_MARK, etc. if outside a model.
                continue
            built_token = models.TOKEN_MODELS[token.type].from_raw_text(token.value)
            if isinstance(built_token, models.BlockComment):
                built_token.claimed = False
            self._add_tokens([built_token])
        self._cursor = cursor

    def _build_indent(self) -> models.RawTokenModel:
        cursor = self._cursor
        while cursor < len(self._tokens):
            token = self._tokens[cursor]
            if token.value:
                if token.type == 'INDENT':
                    self._fix_gap(cursor)
                    return self._build_token(token)
                if not token.type in _IGNORED_TOKENS:
                    break
            cursor += 1
        raise exceptions.UnexpectedInput('Missing indent.')

    def _build_placeholder(self, floating: _Floating) -> internal.Placeholder:
        placeholder = internal.Placeholder.from_default()
        if floating == _Floating.RIGHT:
            assert False, 'deprecated code path'
        elif floating == _Floating.LEFT:
            self._built_tokens.append(placeholder)
        else:
            assert False
        return placeholder

    def _build_token(self, token: lark.Token) -> models.RawTokenModel:
        self._fix_gap(self._token_to_index[id(token)])
        built_token = models.TOKEN_MODELS[token.type].from_raw_text(token.value)
        self._add_tokens([built_token])
        self._cursor += 1
        return built_token

    def _build_tree(self, tree: lark.Tree) -> models.RawTreeModel:
        model_type = models.TREE_MODELS[tree.data]
        children: list[Optional[models.RawModel]] = []
        for child in tree.children:
            is_tree = isinstance(child, lark.Tree)
            if child is None:
                children.append(child)
            elif is_tree and child.data in ('repeated', 'repeated_sep'):
                children.append(self._build_repeated_node(child))
            elif is_tree and child.data in ('indent', 'indent2'):
                children.append(self._build_indent())
            elif is_tree and child.data.endswith('_'):
                continue
            else:
                children.append(self._build_required_node(child))
        return model_type.from_parsed_children(self._token_store, *children)

    def _build_required_node(self, node: lark.Token | lark.Tree) -> models.RawModel:
        if isinstance(node, lark.Token):
            return self._build_token(node)
        if isinstance(node, lark.Tree):
            return self._build_tree(node)
        assert False

    def _build_repeated_node(self, node: lark.Tree) -> models.RawModel:
        placeholder = self._build_placeholder(_Floating.LEFT)
        items = [
            self._build_required_node(child) for child in node.children
            if not (isinstance(child, lark.Tree) and child.data.endswith('_'))
        ]
        return internal.Repeated(self._token_store, items, placeholder)

    def build(self, tree: lark.Tree, model_type: Type[_U]) -> _U:
        model = self._build_tree(tree)
        self._fix_gap(len(self._tokens))
        self._token_store.insert_after(None, self._built_tokens)
        assert isinstance(model, model_type)
        return model
