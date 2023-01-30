from typing import Union, Dict, List

import pytest

from trino_query_parser import parse_statement, TrinoSyntaxError
from trino_query_parser.parser import parse_statement_tree


def test_parse_statement():
    parsed = parse_statement("select * from x.y")
    assert parsed == [["SELECT", "*", "FROM", ["X", ".", "Y"]], "<EOF>"]


def test_parse_statement_raises():
    with pytest.raises(TrinoSyntaxError):
        parse_statement("select * from")


def compress_tree(tree: Union[str, Dict, List]):
    if isinstance(tree, dict):
        assert len(tree) == 1
        return compress_tree(next(iter(tree.values())))
    elif isinstance(tree, list):
        return [compress_tree(node) for node in tree]
    elif isinstance(tree, str):
        return tree
    else:
        raise RuntimeError(f"unexpected type {type(tree)} of value {tree}")


def test_parse_statement_tree():
    tree = parse_statement_tree("select * from x.y")
    compressed = compress_tree(tree)
    assert compressed == [["SELECT", "*", "FROM", ["X", ".", "Y"]], "<EOF>"]
