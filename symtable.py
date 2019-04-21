# 保存符号表


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


g_symtable = Symtable()


if __name__ == '__main__':
    pass
