
all_key_words = {"::", "asm", "do", "for", "##", "int", "const", "struct", "#assert",
                 "continue", "const_cast", "static", "virtual", "unsigned", "goto", "__asm",
                 "static_cast", "__asm__", "__signed", "auto", "__signed__", "__attribute",
                 "__attribute__", "#unassert", "false", "#error", "mutable", "try", "case",
                 "inline", "volatile", "namespace", "throw", "export", "new", "#else", "return",
                 "__P", "signed", "__thread", "char", "catch", "extern", "__const", "#include",
                 "__const__", "#elif", "#undef", "wchar_t", "#include_next", "using", "#ident",
                 "protected", "union", "delete", "#pragma", "__inline", "__inline__", "#endif",
                 "#import", "register", "long", "#sccs", "sizeof", "#if", "class", "#ifndef",
                 "template", "if", "else", "__volatile", "friend", "__volatile__", "this", "short",
                 "reinterpret_cast", "dynamic_cast", "#warning", "default", "explicit", "enum",
                 "break", "double", "void", "public", "true", "typeid", "typedef", "typename",
                 "__extension__", "#ifdef", "bool", "#line", "float", "switch", "private", "operator",
                 "while", "#define"}


def is_keyword(word):
    if word in all_key_words:
        return True
    return False


class Token:
    def __init__(self):
        pass

    def Token(self, ):
        pass


class Parser:
    def __init__(self, lines):
        self._lines = lines
        self._cur_line = 0
        self._cur_col = 0

    def Parser(self):
        pass

    def all_char(self):
        for line in self._lines:
            self._cur_line += 1
            self._cur_col = 0
            for col in line:
                yield col
                self._cur_col += 1

    def next_char(self):
        if (self._cur_col) < len(self._lines[self._cur_line]):
            return self._lines[self._cur_line][self._cur_col]

    def next_token(self, keys):
        for c in self.all_char():
            if c in keys:
                return self.next_char()


if __name__ == '__main__':
    lines = list(open('D:\github\kingfisher\\test\\test1.h', encoding='utf-8'))
    p = Parser(lines)
    print(p.next_token('{}(),='))
