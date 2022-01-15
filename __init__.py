import os
import re
from cudatext import *
from collections import Counter

from cudax_lib import get_translation
_ = get_translation(__file__)  # I18N

COMMON_COUNT = 30
SENTENCE_WORDS = 10
REPORT = _("""Statistics for {}

Lines: {}
Words: {}
Letters: {}
All chars: {}

Most common words ({}):
{}

Sentences with n words:
{}
""")


def count_chars():
    res = [len(ed.get_text_line(i)) for i in range(ed.get_line_count())]
    return sum(res)

def get_sel_lines_():
    sel_lines_ = ed.get_sel_lines()
    return sel_lines_[1] - sel_lines_[0] + 1

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
        res.append(_('{} words: {}').format(count, len(found)))
    return '\n'.join(res)

def get_title(ed, is_sel):
    s = ed.get_filename()
    if s:
        s = '"'+os.path.basename(s)+'"'
    else:
        s = '"'+ed.get_prop(PROP_TAB_TITLE, '')+'"'
    if is_sel:
        s = _('selection in')+' '+s
    return s


class Command:

    def run(self):
        s = ed.get_text_all()
        common_info = get_common_words(s)
        sent_info = get_sentences_stat(s)

        text = REPORT.format(
            get_title(ed, False),
            ed.get_line_count(),
            count_words(s),
            count_letters(s),
            count_chars(),
            COMMON_COUNT,
            common_info,
            sent_info
            )

        res = msg_box_ex('CudaText', text, [_('OK'), _('To a new tab')], MB_ICONINFO, 0)
        if res==1:
            file_open('')
            ed.set_text_all(text)

    def run_sel(self):
        if len(ed.get_carets())!=1:
            return msg_status(_('Need single selection'))
        s = ed.get_text_sel()
        if not s:
            return msg_status(_('Need single selection'))
        common_info = get_common_words(s)
        sent_info = get_sentences_stat(s)

        text = REPORT.format(
            get_title(ed, True),
            get_sel_lines_(),
            count_words(s),
            count_letters(s),
            len(s),
            COMMON_COUNT,
            common_info,
            sent_info
            )

        res = msg_box_ex('CudaText', text, [_('OK'), _('To a new tab')], MB_ICONINFO, 0)
        if res==1:
            file_open('')
            ed.set_text_all(text)

    def run_doc(self):
        s = ed.get_text_all()
        common_info = get_common_words(s)
        sent_info = get_sentences_stat(s)

        text = REPORT.format(
            get_title(ed, False),
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

    def run_doc_sel(self):
        if len(ed.get_carets())!=1:
            return msg_status(_('Need single selection'))
        s = ed.get_text_sel()
        if not s:
            return msg_status(_('Need single selection'))
        common_info = get_common_words(s)
        sent_info = get_sentences_stat(s)

        text = REPORT.format(
            get_title(ed, True),
            get_sel_lines_(),
            count_words(s),
            count_letters(s),
            len(s),
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
