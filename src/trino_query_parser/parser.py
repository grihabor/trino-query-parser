from antlr4 import CommonTokenStream, InputStream
from .SqlBaseLexer import SqlBaseLexer
from .SqlBaseParser import SqlBaseParser
from .SqlBaseVisitor import SqlBaseVisitor


class JSONVisitor(SqlBaseVisitor):
    def visitTerminal(self, node):
        return str(node)

    def aggregateResult(self, aggregate, nextResult):
        if aggregate is None:
            return nextResult
        elif not isinstance(aggregate, list):
            return [aggregate, nextResult]
        else:
            aggregate.append(nextResult)
            return aggregate


def parse_statement(_stmt: str):
    s = InputStream(_stmt.upper())
    lexer = SqlBaseLexer(s)
    stream = CommonTokenStream(lexer)
    parser = SqlBaseParser(stream)
    tree = parser.singleStatement()
    visitor = JSONVisitor()
    return visitor.visit(tree)
