from antlr4.error.ErrorListener import ErrorListener


def _truncate_msg(msg: str, *, limit: int) -> str:
    if len(msg) <= limit:
        return msg
    else:
        return msg[: limit - 3] + "..."


class TrinoSyntaxError(ValueError):
    def __init__(self, msg, *, recognizer, offending_symbol, line, column, e):
        self.msg = msg
        self.line = line
        self.column = column
        self.recognizer = recognizer
        self.offending_symbol = offending_symbol
        self.e = e

    def __str__(self):
        return "{line}:{column} {msg}".format(
            line=self.line,
            column=self.column,
            msg=_truncate_msg(self.msg, limit=100),
        )


class TrinoErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise TrinoSyntaxError(
            msg,
            recognizer=recognizer,
            offending_symbol=offendingSymbol,
            line=line,
            column=column,
            e=e,
        )
