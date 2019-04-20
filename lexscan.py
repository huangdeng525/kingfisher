

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


_all_files = None


def is_keyword(word):
    if word in all_key_words:
        return True
    return False


class ParseBase:
    def __init__(self, proc):
        self.proc = proc
        self._tmp = ''
        self._string_flag = ''

    def process(self, c):
        rsp = self.next_token(c, '')
        if not rsp:
            return
        if rsp == '#include':
            self.proc.push_parser(Include(self.proc))

    def next_token(self, c, token, need_next_line=True):
        # skip spaces
        if c in {' ', '\t'}:
            tmp = self._tmp
            self._tmp = ''
            return tmp
        # finish once token
        if c == '\n':
            tmp = self._tmp
            self._tmp = ''
            return tmp

        if c in {'"', "'"}:
            if self._string_flag == c:
                self._string_flag = ''
                tmp = self._tmp
                self._tmp = ''
                return tmp
            else:
                self._string_flag = c

        if c in token:
            tmp = self._tmp
            self._tmp = ''
            return tmp

        self._tmp += c

        return None

    def analyse(self):
        pass

class Enum(ParseBase):
    def __init__(self, proc):
        ParseBase.__init__(self, proc)

    def process(self, c):
        pass

class Include(ParseBase):
    def __init__(self, proc):
        ParseBase.__init__(self, proc)
        self.proc = proc

    def process(self, c):
        file = self.next_token(c, '"\'', False)
        if file and _all_files:
            new_file = _all_files.get_file(file)
            if new_file:
                self.proc.push_file(File(new_file))
                return

class Proc:
    def __init__(self, file):
        self.parser = []
        self.parser.append(ParseBase(self))
        self._file = []
        self._file.append(file)


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
            if not n_char and len(self._file) > 1:
                self._file.pop(-1)
                self._tmp = ''
                continue
            self.parser[-1].process(n_char)


class File:
    def __init__(self, full_name):
        f = open(full_name, encoding='utf-8')
        self._content = f.read()
        f.close()
        self._cur_line = 1
        self._cur_loc = 1
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
    p = AllFile('D:\\git\\kingfisher\\test')
    _all_files = p
    p1 = File(p.get_file('test.h'))
    p2 = Proc(p1)
    p2.entry()


