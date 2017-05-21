import os
import re
from cudatext import *
from collections import Counter

COMMON_COUNT = 30
REPORT = """Text Statistics for "%s"

Lines: %d
Words: %d
Letters: %d
All chars: %d

Most common words (%d):
%s
"""


def count_words(s):
    return len(re.findall(r'\w+', s))

def count_letters(s):
    return len(re.findall(r'\w', s))

def get_common_words(s):
    words = re.findall(r'\w{2,}', s)
    words = [w.lower() for w in words]
    a = Counter(words)
    res = a.most_common()[:COMMON_COUNT]
    res = ['%s (%d)'%(item[0], item[1]) for item in res]
    return ', '.join(res)


class Command:
    def run(self):
        s = ed.get_text_all()

        n_words = count_words(s)
        n_letters = count_letters(s)
        n_lines = ed.get_line_count()
        n_chars = sum([len(ed.get_text_line(i)) for i in range(ed.get_line_count())])

        common = get_common_words(s)
        text = REPORT % (
            os.path.basename(ed.get_filename()),
            n_lines, n_words, n_letters, n_chars,
            COMMON_COUNT,
            common
            )

        res = msg_box(text+'\nShow report in a new tab?', MB_OKCANCEL+MB_ICONINFO)
        if res==ID_OK:
            file_open('')
            ed.set_text_all(text)
