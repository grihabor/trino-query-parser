import functools
import re
from typing import Callable, Generic, TypeVar, Type, Iterator, Any, Union, List

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ConsoleErrorListener

from .SqlBaseLexer import SqlBaseLexer
from .SqlBaseParser import SqlBaseParser
from .SqlBaseVisitor import SqlBaseVisitor
from .error import TrinoErrorListener


class _TokenVisitor(SqlBaseVisitor):
    def visitTerminal(self, node):
        return str(node)

    def aggregateResult(self, aggregate, nextResult):
        if aggregate is None:
            return [nextResult]
        elif isinstance(aggregate, list):
            aggregate.append(nextResult)
            return aggregate
        else:
            raise RuntimeError("unexpected case: {}, {}".format(aggregate, nextResult))


def _flatten(tree: Union[str, List]):
    """Recursively flattens lists if they store a single item"""
    if isinstance(tree, list) and len(tree) == 1:
        return _flatten(tree[0])
    elif isinstance(tree, list):
        return [_flatten(node) for node in tree]
    elif isinstance(tree, str):
        return tree
    elif isinstance(tree, dict):
        return {key: _flatten(value) for key, value in tree.items()}
    else:
        return tree
        # raise RuntimeError("unexpected type {} of value {}".format(type(tree), tree))


def parse_statement(_stmt: str):
    visitor = _TokenVisitor()
    return _parse_statement(_stmt, visitor=_TokenVisitor())


def parse_statement_tree(_stmt: str):
    return _parse_statement(_stmt, visitor=_DictVisitor())


def _parse_statement(_stmt: str, visitor: SqlBaseVisitor):
    s = InputStream(_stmt.upper())
    lexer = SqlBaseLexer(s)
    stream = CommonTokenStream(lexer)
    parser = SqlBaseParser(stream)
    parser.removeErrorListener(ConsoleErrorListener.INSTANCE)
    parser.addErrorListener(TrinoErrorListener)
    tree = parser.singleStatement()
    return _flatten(visitor.visit(tree))


F = TypeVar("F", bound=Callable)


class OverrideMethods(Generic[F]):
    def __init__(self, methods: Iterator[tuple[str, Callable]]):
        self.methods = methods

    def __call__(self, cls: Type):
        for name, method in self.methods:
            setattr(cls, name, method)

        return cls


def camel_case_to_snake_case(s: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()


def decorate_visit_method(f: Callable) -> Callable:
    @functools.wraps(f)
    def visitAny(self, ctx):
        key = camel_case_to_snake_case(f.__name__[len("visit") :])
        return {key: self.visitChildren(ctx)}

    return visitAny


def iter_visit_methods(cls: Any) -> Iterator[Callable]:
    for name, method in vars(cls).items():
        if name.startswith("visit"):
            yield name, method


@OverrideMethods(
    (name, decorate_visit_method(f)) for name, f in iter_visit_methods(SqlBaseVisitor)
)
class _DictVisitor(_TokenVisitor):
    pass
