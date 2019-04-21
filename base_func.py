
import os


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


all_file = AllFile('d:\\github\\kingfisher\\test')


class File:
    def __init__(self):
        self._content = None
        self._cur_line = 1
        self._cur_loc = 1
        self._len = 0

    def read(self, file):
        f = all_file.get_file(file)
        if not f:
            return False
        f = open(f, encoding='utf-8')
        self._content = f.read()
        f.close()
        self._len = len(self._content)
        if self._len > 0:
            return True
        return False

    def get_cur_line(self):
        return self._cur_line

    def next_char(self, newline=True):
        if self._len == 0:
            return None

        if self._cur_loc < self._len:
            ret = self._content[self._cur_loc]
            if ret == '\n':
                if not newline:
                    return None
                self._cur_line += 1
            self._cur_loc += 1
            return ret
        return None

    def all_lines(self):
        return self._content.split('\n')



