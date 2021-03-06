class CobLex():
    """Lexical analyzer for the cobweb search query DSL."""
    def parse(self, query):
        """Parse a cobweb search query, returns a parse tree of the statement."""
        cobweb_components = self.parse_cobweb(query)
        
    def parse_cobweb(self, line):
        """Make a parse tree from the line containing the query."""
        query = None
        reverse_index = range(((len(line) - 1) * -1), 1)
        escape_char = None
        escaped = False
        for char in reverse_index:
            if line[char] == '|' and escaped is False:
                query = line[char + 1:].strip()
                declarations_columns = line[:char - 1]
            elif line[char] == '"' or line[char] == "'" and escaped is False:
                escape_char = line[char]
                escaped = True
            elif line[char] == escape_char:
                escape_char = None
                escaped = False
        d_c_split = declarations_columns.rsplit("(")
        if len(d_c_split) is 1:
            error = self.SyntaxError("Column declaration missing left "
                                     "parenthesis.")
            return error
        aliases = d_c_split[0].strip()
        columns = d_c_split[1].strip(")")
        return {"aliases":aliases, "columns":columns, "query":query}

    def parse_aliases(self, aliases):
        """Parse a set of aliases as part of a cobweb search query and return a
        dictionary mapping."""
        aliases = aliases + " "
        alias_dict = {}
        key = None
        value = None
        escape_char = None
        escaped = False
        start = 0
        for char in range(0, len(aliases)):
            if key and value:
                alias_dict[key] = value
                key = None
                value = None
            elif aliases[char] == ':' and escaped is False:
                colon = char
                key = "%" + aliases[start:colon].strip(" ;")
            elif aliases[char] == ';' and escaped is False:
                start = char
                value = aliases[colon:start].strip(":")
            elif aliases[char] == '"' and escaped is False:
                escape_char = aliases[char]
                escaped = True
            elif aliases[char] == escape_char:
                escape_char = None
                escaped = False
        return alias_dict

    class SyntaxError():
        """Construct a syntax error notice for the caller to return."""
        def __init__(self, errormsg, at_position=None):
            self.at_position = at_position
            self.errormsg = str(errormsg)
