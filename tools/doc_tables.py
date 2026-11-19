# Parse the Google Doc HTML export into tables plus the paragraphs before each table.
import json, re, sys
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []          # ('p', text) or ('table', rows)
        self.depth = 0
        self.rows = None
        self.cell = None
        self.buf = []
        self.in_style = False

    def handle_starttag(self, tag, attrs):
        if tag == 'style': self.in_style = True
        if tag == 'table':
            self.depth += 1
            if self.depth == 1: self.rows = []
        elif tag == 'tr' and self.depth == 1:
            self.rows.append([])
        elif tag == 'td' and self.depth == 1:
            self.cell = []
        elif tag in ('p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.buf = []
        elif tag == 'br':
            self.buf.append('\n')

    def handle_endtag(self, tag):
        if tag == 'style': self.in_style = False
        if tag in ('p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            text = re.sub(r'[ \t\xa0]+', ' ', ''.join(self.buf)).strip()
            if self.depth >= 1 and self.cell is not None:
                if text: self.cell.append(text)
            elif text:
                self.items.append(('p', text))
            self.buf = []
        elif tag == 'td' and self.depth == 1:
            self.rows[-1].append('\n'.join(self.cell))
            self.cell = None
        elif tag == 'table':
            if self.depth == 1:
                self.items.append(('table', self.rows))
            self.depth -= 1

    def handle_data(self, data):
        if not self.in_style:
            self.buf.append(data)

p = P()
p.feed(open(sys.argv[1], encoding='utf-8').read())
out = []
ctx = []
for kind, val in p.items:
    if kind == 'p':
        ctx.append(val)
    else:
        out.append({'context': ctx[-14:], 'rows': val})
        ctx = []
json.dump(out, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'tables')
