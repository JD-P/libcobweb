import sys

from os import path

source_dir = path.split(path.abspath(""))[0]

sys.path.append(source_dir)

import unittest

import CobLex

class TestLexicalAnalyzer(unittest.TestCase):
    """Test the lexical analysis functions of libcobweb."""
    def test_parse_cobweb(self):
        case1 = "() | <query>"
        self.assertEqual(CobLex.parse_cobweb(CobLex, case1), 
                         {"aliases":'', "columns":'', "query":"<query>"})
        case2 = "(test1, test2, test3) | <query>"
        self.assertEqual(CobLex.parse_cobweb(CobLex, case2), 
                         {"aliases":'', "columns":("test1, test2, test3"),
                          "query":"<query>"})
        case3 = "test1:foo; test2:bar; (a) | <query>"
        self.assertEqual(CobLex.parse_cobweb(CobLex, case3), 
                         {"aliases":"test1:foo; test2:bar;", "columns":"a",
                          "query":"<query>"})
        case4 = "(a, b, c) | \"'cat'\" IN titles OR \"'dog'\" IN titles;"
        self.assertEqual(CobLex.parse_cobweb(CobLex, case4),
                         {"aliases":'', "columns":"a, b, c", "query":
                                                              
