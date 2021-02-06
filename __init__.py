import os
import re
from cudatext import *
from collections import Counter

COMMON_COUNT = 30
SENTENCE_WORDS = 10
REPORT = """Text Statistics for "%s"

Lines: %d
Words: %d
Letters: %d
All chars: %d

Most common words (%d):
%s

Sentences with n words:
%s
"""


def count_chars():
    res = [len(ed.get_text_line(i)) for i in range(ed.get_line_count())]
    return sum(res)

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


def get_sentences(s):
    REGEX_SENT = r'\b[A-Z0-9][^\.\?\!\*]+?[\.\?\!]'
    res = re.findall(REGEX_SENT, s, flags=re.M)
    res = [s.strip(' ') for s in res]
    return res

def get_sentences_stat(s):
    res = []
    items = get_sentences(s)
    for count in range(1, SENTENCE_WORDS):
        found = [item for item in items if count==len(re.findall(r'\w+', item))]
        res.append('%d words: %d' % (count, len(found)))
    return '\n'.join(res)


class Command:
    def run(self):
        s = ed.get_text_all()
        common_info = get_common_words(s)
        sent_info = get_sentences_stat(s)

        text = REPORT % (
            os.path.basename(ed.get_filename()),
            ed.get_line_count(),
            count_words(s),
            count_letters(s),
            count_chars(),
            COMMON_COUNT,
            common_info,
            sent_info
            )

        res = msg_box(text+'\nShow report in a new tab?', MB_OKCANCEL+MB_ICONINFO)
        if res==ID_OK:
            file_open('')
            ed.set_text_all(text)

    def run_doc(self):
        s = ed.get_text_all()
        common_info = get_common_words(s)
        sent_info = get_sentences_stat(s)

        text = REPORT % (
            os.path.basename(ed.get_filename()),
            ed.get_line_count(),
            count_words(s),
            count_letters(s),
            count_chars(),
            COMMON_COUNT,
            common_info,
            sent_info
            )

        file_open('')
        ed.set_text_all(text)

    def show_sent(self):
        s = ed.get_text_all()
        sent = get_sentences(s)
        text = '\n'.join(sorted(sent))+'\n'
        file_open('')
        ed.set_text_all(text)
