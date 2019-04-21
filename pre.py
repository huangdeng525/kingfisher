

from base_func import File


class Pre:
    def __init__(self, file):
        self.file = file
        self.content = []

    def process(self):
        p = File()
        if not p.read(self.file):
            return False

        all_lines = p.all_lines()
        ret = self.move_annotation(all_lines)
        self.expansion(ret)

    def move_annotation(self, all_lines):
        ret = []
        flag = False
        for line in all_lines:
            line = line.rstrip(' \t').lstrip(' \t')
            if '//' in line:
                line = line[:line.find('//')].rstrip(' \t').lstrip(' \t')
            if len(line) > 0:
                ret.append(line)
        return ret

    def expansion(self, all_lines):
        for line in all_lines:
            words = line.split(' ')
            if words[0] == '#include':
                File = words[1].rstrip(' \t"').lstrip(' \t"')
                p = Pre(File)
                p.process()
                for one in p.get_all():
                    self.content.append(one)
                continue
            self.content.append(line)

    def get_all(self):
        return self.content

    def get_all_in_one(self):
        ret = ''
        for one in self.content:
            ret += one
            ret += '\n'
        return ret


if __name__ == '__main__':
    p = Pre('test.h')
    p.process()
    for one in p.get_all():
        print(one)
