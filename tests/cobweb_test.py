import sys

from os import path

source_dir = path.split(path.abspath(""))[0]

sys.path.append(source_dir)

import unittest

from CobLex import CobLex


class TestLexicalAnalyzer(unittest.TestCase):
    """Test the lexical analysis functions of libcobweb."""
    
    def test_parse_cobweb(self):
        case1 = "() | <query>"
        output1 = {"aliases":'', "columns":'', "query":"<query>"}
        msg = ("This tests that the basic case of two elements divided by a |"
               " works.")
        self.assertEqual(CobLex.parse_cobweb(CobLex, case1), output1, msg)
        case2 = "(test1, test2, test3) | <query>"
        output2 =  {"aliases":'', "columns":("test1, test2, test3"), 
                    "query":"<query>"}
        msg = ("This tests that columns are parsed correctly.")
        self.assertEqual(CobLex.parse_cobweb(CobLex, case2), output2, msg)
        case3 = "test1:foo; test2:bar; (a) | <query>"
        output3 = {"aliases":"test1:foo; test2:bar;", "columns":"a",
                          "query":"<query>"}
        msg = ("This tests that aliases are parsed correctly.")
        self.assertEqual(CobLex.parse_cobweb(CobLex, case3), output3, msg)
        case4 = "(a, b, c) | \"'cat'\" IN titles OR \"'dog'\" IN titles;"
        output4 = {"aliases":'', "columns":"a, b, c", "query":"\"'cat'\" "
                          "IN titles OR \"'dog'\" IN titles;"}
        msg = ("This tests that double quote escaping works correctly.")
        self.assertEqual(CobLex.parse_cobweb(CobLex, case4), output4, msg)
        case5 = "(a, b, c) | \"'|cat'\" IN titles OR \"'|dog'\" IN titles;"
        output5 = {"aliases":'', "columns":"a, b, c", "query":"\"'|cat'\""
                          " IN titles OR \"'|dog'\" IN titles;"}
        msg = ("This tests that double quote escaping properly fails to parse |"
               " characters.")
        self.assertEqual(CobLex.parse_cobweb(CobLex, case5), output5, msg)
        case6 = "(a, b, c) | '\"|cat\"' IN titles OR '\"|dog\"' IN titles;"
        output6 = {"aliases":'', "columns":"a, b, c", "query":"'\"|cat\"'"
                          " IN titles OR '\"|dog\"' IN titles;"}
        msg = ("This tests that single quote escaping properly fails to parse |"
               " characters. It is also a super test of case 4.")
        self.assertEqual(CobLex.parse_cobweb(CobLex, case6), output6, msg)

    def test_parse_aliases(self):
        case1 = "test1:foo; test2:bar; test3:foobar;"
        output1 = {"%test1":"foo", "%test2":"bar", "%test3":"foobar"}
        msg = "This tests basic alias parsing functionality."
        self.assertEqual(CobLex.parse_aliases(CobLex, case1), output1, msg)
        case2 = "test1:\";foo\"; test2:\";bar\"; test3:\";foobar\";"
        output2 = {"%test1":"\";foo\"", "%test2":"\";bar\"", "%test3":"\";foobar\""}
        msg = ("This tests double quote escaping, and that the function won't"
               " parse a semicolon while escaped.")
        self.assertEqual(CobLex.parse_aliases(CobLex, case2), output2, msg)

unittest.main()                                                              
