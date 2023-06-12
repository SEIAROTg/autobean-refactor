import ast
import functools
import inspect
import re
import textwrap
import types
from typing import Any, ClassVar, Optional, Type
import typing
from sphinx import application
from sphinx.ext import autodoc
from sphinx.ext.autosummary import generate
from sphinx.util import docutils
from docutils import nodes, statemachine
from autobean_refactor import models
from autobean_refactor.models import internal
from autobean_refactor.models import meta_item_internal


def _get_class_attributes(cls: Type[models.RawModel]) -> dict[str, ast.stmt]:
    src = inspect.getsource(cls)
    (class_def,) = ast.parse(src).body
    assert isinstance(class_def, ast.ClassDef)
    ret = dict[str, ast.stmt]()
    for entry in class_def.body:
        if isinstance(entry, ast.Assign):
            (target,) = entry.targets
            assert isinstance(target, ast.Name)
            ret[target.id] = entry
        elif isinstance(entry, ast.FunctionDef):
            ret[entry.name] = entry
    return ret


@functools.lru_cache(maxsize=1000)
def _get_class_attributes_recursive(cls: Type[models.RawModel]) -> dict[str, ast.stmt]:
    ret = {}
    for c in reversed(inspect.getmro(cls)[:-1]):
        ret.update(_get_class_attributes(c))
    return ret


def _get_field_name(cls: Type[models.RawModel], prop_name: str) -> str:
    prop_def = _get_class_attributes_recursive(cls)[prop_name]
    assert isinstance(prop_def, ast.Assign)
    assert isinstance(prop_def.value, ast.Call)
    first_arg = prop_def.value.args[0]
    if isinstance(first_arg, ast.Name):
        name = first_arg.id
    elif isinstance(first_arg, ast.Attribute):  # for inherited attributes (e.g. _leading_comment)
        name = first_arg.attr
    else:
        assert False
    return name


def _get_field_type(cls: Type[models.RawModel], name: str) -> str:
    field_def = _get_class_attributes_recursive(cls)[name]
    assert isinstance(field_def, ast.Assign)
    assert isinstance(field_def.value, ast.Call)
    assert isinstance(field_def.value.func, ast.Subscript)
    type_arg = field_def.value.func.slice
    return ast.unparse(type_arg)


def _get_attribute_type(cls: Type[models.RawModel], property: Any, name: str) -> str:
    attr_def = _get_class_attributes_recursive(cls)[name]
    if isinstance(attr_def, ast.Assign) and isinstance(attr_def.value, ast.Name):  # alias
        name = attr_def.value.id
        return _get_attribute_type(cls, getattr(cls, name), name)
    elif isinstance(attr_def, ast.FunctionDef):
        assert attr_def.returns
        if isinstance(attr_def.returns, ast.Subscript):
            t = ast.unparse(attr_def.returns.value)
            if t == 'internal.RepeatedValueWrapper':
                inner = attr_def.returns.slice
                assert isinstance(inner, ast.Tuple)
                return f'typing.MutableSequence[{ast.unparse(inner.elts[1])}]'
        return ast.unparse(attr_def.returns)
    elif isinstance(property, internal.data_field):
        return _get_field_type(cls, name)
    elif isinstance(property, internal.unordered_node_property):
        assert isinstance(attr_def, ast.Assign)
        assert isinstance(attr_def.value, ast.Call)
        assert isinstance(attr_def.value.args[1], ast.Name)
        return attr_def.value.args[1].id
    else:
        field_name = _get_field_name(cls, name)
        return _get_attribute_type(cls, getattr(cls, field_name), field_name)


def _get_value_type(model_name: str) -> str:
    return {
        'Date': 'datetime.date',
        'Account': 'str',
        'EscapedString': 'str',
        'Indent': 'str',
        'Whitespace': 'str',
        'InlineComment': 'str',
        'BlockComment': 'str',
        'MetaKey': 'str',
        'Currency': 'str',
        'Tag': 'str',
        'Link': 'str',
        'NumberExpr': 'decimal.Decimal',
        'TransactionFlag': 'str',
    }[model_name]


class PropertyDocumenter(autodoc.ClassLevelDocumenter):
    objtype = 'model_property'
    directivetype = 'property'
    priority = 1000

    @classmethod
    def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
        return isinstance(member, internal.base_ro_property)
                          
    def add_directive_header(self, sig: str) -> None:
        super().add_directive_header(sig)
        property_type = _get_attribute_type(self.parent, self.object, self.object_name)
        match self.object:
            case internal.data_field():
                prop_type = property_type
            case internal.required_node_property():
                prop_type = property_type
            case _ if type(self.object) is internal.custom_property:
                prop_type = property_type
            case _ if type(self.object) is internal.cached_custom_property:
                prop_type = property_type
            case internal.optional_node_property():
                prop_type = f'typing.Optional[{property_type}]'
            case internal.unordered_node_property():
                prop_type = f'typing.Optional[{property_type}]'
            case internal.repeated_node_property():
                prop_type = f'typing.MutableSequence[{property_type}]'
            case internal.repeated_filtered_node_property():
                prop_type = f'typing.MutableSequence[{property_type}]'
            case internal.repeated_node_with_interleaving_comments_property():
                prop_type = f'typing.MutableSequence[{property_type}]'
            case internal.required_value_property():
                prop_type = _get_value_type(property_type)
            case internal.optional_string_property():
                prop_type = 'typing.Optional[str]'
            case internal.optional_indented_string_property():
                prop_type = 'typing.Optional[str]'
            case internal.optional_date_property():
                prop_type = 'typing.Optional[date]'
            case internal.optional_decimal_property():
                prop_type = 'typing.Optional[decimal.Decimal]'
            case internal.repeated_string_property():
                prop_type = 'typing.MutableSequence[str]'
            case meta_item_internal.repeated_raw_meta_item_property():
                prop_type = 'Intersection[typing.MutableSequence[MetaItem], typing.MutableMapping[str, MetaItem]]'
            case meta_item_internal.repeated_meta_item_property():
                prop_type = 'Intersection[typing.MutableSequence[MetaItem], typing.MutableMapping[str, MetaValue | MetaRawValue]]'
            case _:
                assert False
        self.add_line(f'   :type: {prop_type}', self.get_sourcename())


_RE_COMMENT_METHODS = re.compile(r'((un)?claim_(leading|trailing)_comment)|auto_claim_comments')


def _get_sort_key(entry: tuple[autodoc.Documenter, bool]) -> Any:
    documenter, isattr = entry
    if isinstance(documenter, autodoc.AttributeDocumenter):
        return (0,)
    if isinstance(documenter, PropertyDocumenter):
        return (1, 1)
    elif isinstance(documenter, autodoc.PropertyDocumenter):
        return (1, 2)
    elif isinstance(documenter, autodoc.MethodDocumenter):
        method_name = documenter.name.rsplit('.', 1)[-1]
        if _RE_COMMENT_METHODS.fullmatch(method_name):
            return (3, 0)
        return (1, 3)
    else:
        return (2, documenter.member_order)


def patched_class_sort_members(
        self: autodoc.Documenter,
        documenters: list[tuple[autodoc.Documenter, bool]],
        order: str,
) -> list[tuple[autodoc.Documenter, bool]]:
    documenters.sort(key=_get_sort_key)
    return documenters


autodoc.ClassDocumenter.sort_members = patched_class_sort_members  # type: ignore[method-assign]


def patched_find_autosummary_in_lines(
        lines: list[str],
        module: Optional[str] = None,
        filename: Optional[str] = None,
) -> list[generate.AutosummaryEntry]:
    updated_lines = []
    for line in lines:
        if line.strip() == '.. autobean-refactor-token-models::':
            updated_lines.extend(ListTokenModelsDirective.STATIC_CONTENTS)
        if line.strip() == '.. autobean-refactor-tree-models::':
            updated_lines.extend(ListTreeModelsDirective.STATIC_CONTENTS)
        else:
            updated_lines.append(line)    
    return _original_find_autosummary_in_lines(updated_lines, module, filename)  # type: ignore[arg-type]


_original_find_autosummary_in_lines = generate.find_autosummary_in_lines
generate.find_autosummary_in_lines = patched_find_autosummary_in_lines


def autodoc_skip_member(app: application.Sphinx, what: str, name: str, obj: Any, skip: bool, options: dict[str, Any]) -> bool:
    if getattr(obj, '__func__', None) is internal.custom_property.setter:
        return True
    return skip


_RE_REDUNDANT_QUALIFICATIONS = re.compile(r'autobean_refactor\.models\.[^A-Z]*')


def autodoc_process_signature(
        app: application.Sphinx,
        what: str,
        name: str,
        obj: Any,
        options: dict[str, Any],
        signature: str,
        return_annotation: str,
) -> tuple[str, str]:
    if signature:
        signature = re.sub(_RE_REDUNDANT_QUALIFICATIONS, '', signature)
    if what == 'method':
        # unresolve union types
        n = ast.parse(textwrap.dedent(inspect.getsource(obj)))
        method_def = n.body[0]
        assert isinstance(method_def, ast.FunctionDef)
        method_def.args.args.pop(0)
        signature = f'({ast.unparse(method_def.args)})'
    return (signature, return_annotation)


class _BaseStaticDirective(docutils.SphinxDirective):
    has_content = True
    STATIC_CONTENTS: ClassVar[list[str]]

    def run(self) -> list[nodes.Node]:
        content = statemachine.StringList()
        for line in self.STATIC_CONTENTS:
            content.append(line, 'generated')
        node = nodes.paragraph()
        with docutils.switch_source_input(self.state, content):
            node.document = self.state.document
            self.state.nested_parse(content, 0, node)
            return node.children


@functools.cache
def _get_type_aliases() -> list[str]:
    return sorted(
        name
        for name, obj in models.__dict__.items()
        if not name.startswith('_') and typing.get_origin(obj) in (types.UnionType, typing.Union)
    )


class ListTypeAliasesDirective(_BaseStaticDirective):
    STATIC_CONTENTS = [
        f'.. autoclass:: {type_alias}'
        for type_alias in _get_type_aliases()
    ]


@functools.cache
def _get_token_models() -> list[str]:
    return sorted(
        name
        for name, cls in models.__dict__.items()
        if isinstance(cls, type) and issubclass(cls, models.RawTokenModel)
    )


class ListTokenModelsDirective(_BaseStaticDirective):
    STATIC_CONTENTS = [
        '.. autosummary::',
        '  :nosignatures:',
        '  :template: model.rst',
        '  :toctree: token-models',
        '',
        *(f'  {token_model}' for token_model in _get_token_models()),
    ]


@functools.cache
def _get_tree_models() -> list[str]:
    return sorted(
        name
        for name, cls in models.__dict__.items()
        if isinstance(cls, type) and issubclass(cls, models.RawTreeModel)
    )


class ListTreeModelsDirective(_BaseStaticDirective):
    STATIC_CONTENTS = [
        '.. autosummary::',
        '  :nosignatures:',
        '  :template: model.rst',
        '  :toctree: tree-models',
        '',
        *(f'  {tree_model}' for tree_model in _get_tree_models()),
    ]


def setup(app: application.Sphinx) -> None:
    app.add_autodocumenter(PropertyDocumenter)
    app.connect('autodoc-skip-member', autodoc_skip_member)
    app.connect('autodoc-process-signature', autodoc_process_signature)

    app.add_directive('autobean-refactor-type-aliases', ListTypeAliasesDirective)
    app.add_directive('autobean-refactor-token-models', ListTokenModelsDirective)
    app.add_directive('autobean-refactor-tree-models', ListTreeModelsDirective)
