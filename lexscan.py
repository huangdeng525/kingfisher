

import os


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


class Proc:
    def __init__(self, file, all_file):
        self.parser = []
        self.all_file = all_file
        self.parser.append(self)
        self._file = []
        self._file.append(file)
        self._tmp = ''
        self._string_flag = ''

    def push_file(self, file):
        self._file.append(file)

    def push_parser(self, parser):
        self.parser.append(parser)

    def pop_file(self):
        if len(self._file) > 1:
            self._file.pop(-1)

    def pop_parser(self):
        if len(self.parser) > 1:
            self.parser.pop(-1)

    def entry(self):
        while True:
            n_char = self._file[-1].next_char()
            self.parser[-1].process(n_char)

    def process(self, c):
        # skip spaces
        if c in {' ', '\t'}:
            return
        # finish once token
        if c == '\n':
            return

        if c in {'"', "'"}:
            self._string_flag = c

    def analyse(self):
        pass

class Enum(Proc):
    def __init__(self):
        pass


class Include(Proc):
    def __init__(self):
        pass

    def Parser(self):
        string_flag = ''
        for c in self.all_char():
            # skip spaces
            if c in {' ', '\t'}:
                continue
            # finish once token
            if c == '\n':
                self.once()

            if c in {'"', "'"}:
                string_flag = c

class File:
    def __init__(self, full_name):
        f = open(full_name, encoding='utf-8')
        self._content = f.read()
        f.close()
        self._cur_line = 1
        self._cur_loc = 0
        self._len = len(self._content)

    def get_cur_line(self):
        return self._cur_line

    def next_char(self, newline=True):
        if self._cur_loc < self._len:
            ret = self._content[self._cur_loc]
            if ret == '\n':
                if not newline:
                    return None
                self._cur_line += 1
            self._cur_loc += 1
            return ret
        return None

    def all_char(self):
        ''' 暂时不用 '''
        return
        for line in self._lines:
            self._cur_line += 1
            self._cur_col = 0
            for col in line:
                yield col
                self._cur_col += 1


class AllFile:
    def __init__(self, root):
        self._dict = dict()
        for cur_path, dirs, files in os.walk(root):
            for file in files:
                full_name = os.path.join(cur_path, file)
                if file in self._dict:
                    print('Error: Same Name File')
                else:
                    self._dict[file] = full_name

    def get_file(self, name):
        if name in self._dict:
            return self._dict[name]
        return None


if __name__ == '__main__':
    p = AllFile('D:\\github\\kingfisher\\test')
    p1 = File(p.get_file('test1.h'))
    for x in range(1000):
        t = p1.next_char(newline=True)
        if t:
            print(t)
        else:
            break

