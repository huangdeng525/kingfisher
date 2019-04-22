# 保存符号表

import json

class Symtable:
    def __init__(self):
        self._dict = dict()

    def put(self, key, value):
        if key in self._dict:
            return
        self._dict[key] = value

    def get(self, key):
        if key in self._dict:
            return self._dict[key]
        return key

    def Dump(self, f):
        with open(f, mode='w') as f:
            json.dump(self._dict, f, indent=4, ensure_ascii=False)

g_symtable = Symtable()


class ErrInfo:
    def __init__(self):
        self._dict = dict()

    def put(self, macros):
        value = g_symtable.get(macros[0])
        if type(value) == type(int(0)):
            self.inner_put(value, macros[0], macros[1], macros[2])

        if type(value) == type(str('')):
            if len(value) > 2 and value[:2].lower() == '0x':
                self.inner_put(int(value, base=16), macros[0], macros[1], macros[2])
            else:
                self.inner_put(int(value), macros[0], macros[1], macros[2])

    def inner_put(self, value, ErrMacro, ErrEnglish, ErrChinese):
        # NE错误码
        self._dict[value] = [ErrMacro, ErrEnglish, ErrChinese]
        if value > 0:
            # NCS错误码
            self._dict[value + 0x80000000] = [ErrMacro, ErrEnglish, ErrChinese]

    def Dump(self, f):
        with open(f, mode='w') as f:
            json.dump(self._dict, f, indent=4, ensure_ascii=False)


g_errinfo = ErrInfo()


if __name__ == '__main__':
    pass
