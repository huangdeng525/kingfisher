

from pre import Pre
from symtable import g_symtable

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


def gen_new_Parse(word, proc):
    if word == 'enum':
        return Enum(proc)
    return None


class ParseBase:
    def __init__(self, proc):
        self.proc = proc
        self._tmp = ''
        self._string_flag = ''

    def process(self, in_c):
        token = '{}()'
        rsp, c = self.next_token(in_c, token)
        if c == '':
            return

        if is_keyword(rsp):
            p = gen_new_Parse(rsp, self.proc)
            if p:
                self.proc.push_parser(p)

    def next_token(self, c, token, skip_space=False):
        # skip spaces
        if c in {' ', '\t'} and skip_space == False:
            tmp = self._tmp
            self._tmp = ''
            return tmp, c
        if c in {' ', '\t'}:
            return '', ''
        # finish once token
        if c == '\n':
            tmp = self._tmp
            self._tmp = ''
            return tmp, c

        if c in {'"', "'"}:
            if self._string_flag == c:
                self._string_flag = ''
                tmp = self._tmp
                self._tmp = ''
                return tmp, c
            else:
                self._string_flag = c

        if c in token:
            tmp = self._tmp
            self._tmp = ''
            return tmp, c

        self._tmp += c

        return '', ''


class op:
    def __init__(self):
        self.value = 0
        self.in_value = []
        self.state = True

    def push(self, one):
        if type(one) == type(int(0)):
            self.in_value.append(one)

        if type(one) == type(str('')):
            if len(one) > 2 and one[:2].lower() == '0x':
                self.in_value.append(int(one, base=16))
            else:
                self.in_value.append(int(one))
        self.calc()
        return self

    def get(self):
        return self.value

    def calc(self):
        pass

    def finish(self):
        return self.state

class Add(op):
    def __init__(self):
        op.__init__(self)
        self.state = False

    def calc(self):
        if len(self.in_value) == 2:
            self.value = self.in_value[0] + self.in_value[1]
            self.state = True

class Inc(op):
    def __init__(self):
        op.__init__(self)
        self.state = False

    def calc(self):
        if len(self.in_value) == 1:
            self.value = self.in_value[0]
            self.state = True

class Dcop(op):
    def __init__(self):
        op.__init__(self)
        self.state = False

    def calc(self):
        if len(self.in_value) == 3:
            self.value = self.in_value[0] * 65536 + self.in_value[1] * 4096 + self.in_value[2]
            self.state = True

class Equal(op):
    def __init__(self, key):
        op.__init__(self)
        self.key = key
        self.state = False

    def calc(self):
        if len(self.in_value) == 1:
            self.value = self.in_value[0]
            self.state = True

    def get(self):
        return self.key, self.value

class Enum(ParseBase):
    def __init__(self, proc):
        ParseBase.__init__(self, proc)
        self.last_value = 0
        self.last_enum_str = ''
        self.parser = proc
        self.last_proc = []
        self.last_state = []
        self.state = 'init'

    def push(self, proc, state):
        self.last_proc.append(proc)
        self.last_state.append(state)

    def pop(self):
        return self.last_proc.pop(-1), self.last_state.pop(-1)

    def get_last(self):
        return self.last_proc[-1], self.last_state[-1]

    def calc(self):
        proc, state = self.pop()
        if proc.finish():
            if type(proc) == type(Equal('')):
                key, val = proc.get()
                self.mark_one(key, val)
                return
        while proc.finish():
            if len(self.last_proc) == 0:
                return
            up_proc, up_state = self.pop()
            up_proc.push(proc.get())
            proc = up_proc
            if type(proc) == type(Equal('')):
                key, val = proc.get()
                self.mark_one(key, val)


    def process(self, in_c):

        token = ',{}()+-<>;='
        rsp, c = self.next_token(in_c, token, skip_space=True)
        if c == '':
            return

        if c == ';':
            self.proc.pop_parser()

        if self.state == 'init' and c == '{':
            self.state = 'in'
            return

        if self.state == 'init':
            return

        if c == '=':
            self.push(Equal(rsp), c)
            return

        if c == '+':
            self.push(Add().push(g_symtable.get(rsp)), c)
            return

        if rsp == 'DCOP_ERRCODE' and c == '(':
            self.push(Dcop(), 'dcop')
            return

        if c in ',\n})' and len(rsp) > 0:
            if len(self.last_proc) == 0:
                self.push(Equal(rsp).push(self.last_value), '=')
                self.calc()
                return
            proc, state = self.get_last()
            proc.push(g_symtable.get(rsp))
            if proc.finish():
                self.calc()


    def mark_one(self, enum_str, enum_value):
        self.last_value = enum_value + 1
        g_symtable.put(enum_str, enum_value)
        print(enum_str, enum_value)



class Proc:
    def __init__(self, file):
        self.parser = []
        self.parser.append(ParseBase(self))
        p = Pre(file)
        p.process()
        self.content = p.get_all_in_one()
        self.loc = 0
        self.total_len = len(self.content)

    def push_parser(self, parser):
        self.parser.append(parser)

    def pop_parser(self):
        if len(self.parser) > 1:
            self.parser.pop(-1)

    def next_char(self):
        return self.content[self.loc]

    def entry(self):
        while True:
            if self.loc >= self.total_len:
                return
            n_char = self.content[self.loc]
            self.parser[-1].process(n_char)
            self.loc += 1


if __name__ == '__main__':
    p2 = Proc('test.h')
    p2.entry()


