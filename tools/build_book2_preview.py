"""Part 2 layout preview: the real KDP page design (same engine as Book 1) filled with the
Book 2 chapter drafts, and labelled placeholders where the illustrations will go.

usage: build_book2_preview.py <scratch dir with build_interior.py> <fonts> <book2 dir> <out.pdf>
"""
import re
import sys
import types

SCR, FONTS, B2, OUT = sys.argv[1:5]

# ------------------------------------------------------------ Book 2 content from the drafts
def inline(t):
    t = t.replace('&', '&amp;')
    t = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<i>\1</i>', t)
    return t


def parse(path):
    lines = open(path, encoding='utf-8').read().split('### Notes for you')[0].splitlines()
    title, blocks, i = None, [], 0
    while i < len(lines):
        ln = lines[i].strip()
        i += 1
        if not ln or ln.startswith('# ') or re.match(r'^\*\*CHAPTER \d+\*\*$', ln):
            continue
        if ln.startswith('## '):
            title = ln[3:].strip()
            continue
        if ln == '---':
            # Book 3 teaser box (Chapter 14): skip its lines, render as the 'end' block
            if i < len(lines) and any('THE JOURNEY CONTINUES' in l for l in lines[i:i + 3]):
                blocks.append(('end',))
                while i < len(lines) and not lines[i].strip().startswith('*God keeps'):
                    i += 1
            continue
        if ln.startswith('> Know the Word'):
            blocks.append(('motto',)); continue
        m = re.match(r'^>\s*(.+?)\s+—\s*(.+)$', ln)
        if m:
            blocks.append(('quote', inline(m.group(1)), m.group(2))); continue
        if ln.startswith('**READ IT FOR YOURSELF:**'):
            blocks.append(('read', 'READ IT FOR YOURSELF', inline(ln.split(':**', 1)[1].strip()))); continue
        if ln.startswith("**ON TODAY'S MAP**"):
            items = []
            while i < len(lines) and lines[i].strip().startswith('- '):
                b = lines[i].strip()[2:]
                mm = re.match(r'^\*\*(.+?):\*\*\s*(.+)$', b)
                items.append((inline(mm.group(1)), inline(mm.group(2))) if mm else ('', inline(b)))
                i += 1
            blocks.append(('map', 'ON TODAY’S MAP', items)); continue
        if re.match(r'^\*[^*].*\*$', ln):
            blocks.append(('thought', '', inline(ln[1:-1]))); continue
        if '•' in ln and ln.upper() == ln:
            names = [x.strip() for x in ln.split('•')]
            if blocks and blocks[-1][0] == 'names':
                blocks[-1] = ('names', blocks[-1][1] + names)
            else:
                blocks.append(('names', names))
            continue
        if re.match(r'^[A-Z][A-Z ]+ — ', ln):
            name, desc = ln.split(' — ', 1)
            if blocks and blocks[-1][0] == 'timeline':
                blocks[-1][1].append((name, desc))
            else:
                blocks.append(('timeline', [(name, desc)]))
            continue
        blocks.append(('p', inline(ln)))
    return title, blocks


C = types.ModuleType('content_b2')
C.TITLE, C.SUBTITLE, C.SERIES, C.BOOK_NO = 'Joesiah & Malani', 'From Abraham to Moses', 'Joesiah & Malani', 2
C.AUTHOR = 'LeTisha C. Cleveland'
C.TAGLINE = 'God keeps His promises, even when it takes generations.'
C.MOTTO = 'Know the Word. Seek the Truth. Remember who you are. Walk in the purpose God gave you.'
C.NEXT_BOOK = 'From Moses to Yeshua: The Promise Fulfilled'
C.END_LINE = 'The promise God made to Abraham keeps going, all the way to <b>Yeshua</b>.'
C.CHAPTERS = []
for n in range(1, 15):
    t, b = parse(f'{B2}/Chapter_{n:02d}_Draft.md')
    C.CHAPTERS.append((n, t, b))
C.CHAPTER_ART = {n: n for n in range(1, 15)}
C.SPOTLIGHT = None
sys.modules['content'] = C

SCENES = {
    1: 'Grandma, Joesiah & Malani at the family-tree scroll; a glowing path from Shem to Abram; a dreamlike view of Ur and the road to Haran.',
    2: 'Sunrise: Abram, Sarai, Lot and the caravan set out from Haran; the children walk alongside.',
    3: 'Night in the desert: Abram outside his tent beneath a sky blazing with stars; Malani tries to count them.',
    4: 'Hagar, a young Egyptian woman, kneels by a desert spring in soft heavenly light.',
    5: 'Mountaintop at dawn: Abraham and young Isaac see the ram caught in the thicket. God provides.',
    6: 'Rebekah at the well, watering ten camels; Abraham’s servant watches in amazement.',
    7: 'Jacob asleep on a stone; a glowing stairway with angels rises into the stars.',
    8: 'Old Jacob crosses his arms to bless Ephraim and Manasseh; Joseph and Asenath beside them.',
    9: 'Shiphrah and Puah stand calm and courageous before Pharaoh’s throne.',
    10: 'Pharaoh’s daughter lifts baby Moses’ basket from the Nile; Miriam peeks from the reeds.',
    11: 'Moses, barefoot, kneels before the burning bush; his sheep graze nearby.',
    12: 'An Israelite family shares the Passover meal by lamplight, dressed and ready to travel.',
    13: 'Miriam dances with her tambourine on the far shore; walls of water and the pillar of fire behind.',
    14: 'Mount Sinai at dawn: Moses carries the stone tablets; the family-tree scroll on a rock below.',
    'preview': 'Part 3 preview: our three on a hill at sunset, a road from Sinai toward Bethlehem under a bright star.',
}

# ------------------------------------------------------------ reuse the Book 1 page engine
src = open(f'{SCR}/build_interior.py', encoding='utf-8').read()
src = src.replace("sys.path.insert(0, sys.argv[1])\nimport content as C  # noqa: E402", "C = sys.modules['content']")
src = src.replace("FONTS = sys.argv[2]\nILL = sys.argv[3]\nOUT = sys.argv[4]", "")
src = src.replace("'<font name=\"Literata-Bold\">%s:</font> %s' % (name, today)",
                  "(('<font name=\"Literata-Bold\">%s:</font> %s' % (name, today)) if name else today)")
src = src.replace("Time Travel Adventure • Part 2</font>", "Time Travel Adventure • Part 3</font>")
src = src.replace("c.setTitle('Joesiah & Malani Time Travel Adventure: Part 1: Noah’s Bloodline')", "c.setTitle('Joesiah & Malani Time Travel Adventure: Part 2: From Abraham to Moses')")
src = src.replace('    for f, h in zip(fl, hs):\n        w, hh = f.wrap(width, 10000)\n        y -= f.getSpaceBefore()\n        f.drawOn(c, x0 + (width - w) / 2 if isinstance(f, Table) else x0, y - hh)\n        y -= hh + f.getSpaceAfter() + extra', "    floor = y0 + band_h + (12 if band else 0) + folio_room\n    over = False\n    for f, h in zip(fl, hs):\n        w, hh = f.wrap(width, 10000)\n        y -= f.getSpaceBefore()\n        if y - hh < floor + 16:\n            parts = f.split(width, y - floor - 16) if hasattr(f, 'split') else []\n            if parts:\n                w2, h2 = parts[0].wrap(width, 10000)\n                parts[0].drawOn(c, x0, y - h2)\n            over = True\n            break\n        f.drawOn(c, x0 + (width - w) / 2 if isinstance(f, Table) else x0, y - hh)\n        y -= hh + f.getSpaceAfter() + extra\n    if over:\n        words = int(round(-leftover / (size * lf) * 13 / 5.0) * 5)\n        c.setFillColorRGB(0.78, 0.1, 0.1)\n        c.setFont('Literata-Bold', 9.5)\n        c.drawCentredString((x0 + x1) / 2, floor + 2, '\\u25bc TEXT CONTINUES \\u2014 chapter is about %d words too long for one page \\u25bc' % max(words, 5))")
assert 'TEXT CONTINUES' in src
src = src.replace("Paragraph('<i>%s</i>' % C.MOTTO, S['motto'])]", "Paragraph('<i>%s</i>' % C.END_LINE, S['motto'])]")
# timeline block (Chapter 14's five stops)
src = src.replace("        elif k == 'pledge':",
"""        elif k == 'timeline':
            for name, desc in b[1]:
                out.append(Paragraph('<font name="Cinzel-Bold" color="#1B2A4A">%s</font>  <font name="Literata-Italic" color="#8A6A1F">%s</font>' % (name, desc), S['tline']))
            out.append(Spacer(1, S['p'].fontSize * 0.5))
        elif k == 'pledge':""", 1)
src = src.replace("        'pledge': ParagraphStyle(",
"""        'tline': ParagraphStyle('tli', fontName='Literata', fontSize=size * 0.95, leading=size * 1.32,
                                textColor=NAVY, alignment=TA_CENTER),
        'pledge': ParagraphStyle(""", 1)
for a in ("C = sys.modules['content']", "• Part 3</font>", "C.END_LINE", "'timeline'", "'tline'", "if name else today"):
    assert a in src, a

g = {'__name__': 'b2engine', 'FONTS': FONTS, 'ILL': '', 'OUT': OUT}
exec(compile(src, 'build_interior.py', 'exec'), g)

from reportlab.lib.units import inch  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.enums import TA_CENTER  # noqa: E402
from reportlab.platypus import Paragraph  # noqa: E402

g['PLAN'][32] = ('art', 'preview')
OVERSIZE = 11.75
def pick_size():
    leads = {}
    for n, t, b in C.CHAPTERS:
        leads[n] = g['fit_lead'](n, t, b, OVERSIZE) or 1.30
    return OVERSIZE, leads
g['pick_size'] = pick_size
g['NPAGES'] = 32


def draw_art(c, page, idx):
    """Placeholder in exactly the space the real illustration will fill."""
    g['bg'](c, g['NIGHT'])
    x0, y0, x1, y1 = g['trim_box'](page)
    h = 10.1 * inch
    w = h * 3 / 4
    ix, iy = (x0 + x1) / 2 - w / 2, (y0 + y1) / 2 - h / 2
    c.setStrokeColor(g['GOLD']); c.setLineWidth(1.2)
    c.rect(ix - 4, iy - 4, w + 8, h + 8, stroke=1, fill=0)
    c.setFillColor(g['PARCH']); c.rect(ix, iy, w, h, stroke=0, fill=1)
    c.setStrokeColor(g['GOLD']); c.setLineWidth(0.6); c.setDash(6, 5)
    c.rect(ix + 18, iy + 18, w - 36, h - 36, stroke=1, fill=0); c.setDash()
    cx = (x0 + x1) / 2
    c.setFillColor(g['GOLD_DK']); c.setFont('Cinzel-Bold', 15)
    c.drawCentredString(cx, iy + h * 0.66, 'ILLUSTRATION COMING')
    g['ornament'](c, cx, iy + h * 0.66 - 18, 2.4 * inch)
    label = 'PART 3 PREVIEW PAGE' if idx == 'preview' else 'CHAPTER %d' % idx
    c.setFillColor(g['NAVY']); c.setFont('Cinzel-Black', 26)
    c.drawCentredString(cx, iy + h * 0.66 - 60, label)
    if idx != 'preview':
        c.setFont('Cinzel-Bold', 15)
        c.drawCentredString(cx, iy + h * 0.66 - 88, dict((n, t) for n, t, _ in C.CHAPTERS)[idx])
    st = ParagraphStyle('sc', fontName='Literata-Italic', fontSize=14, leading=20, textColor=g['INK'], alignment=TA_CENTER)
    p = Paragraph(SCENES[idx], st)
    pw, ph = p.wrap(w - 1.6 * inch, 400)
    p.drawOn(c, cx - pw / 2, iy + h * 0.66 - 130 - ph)
    c.setFont('Literata', 10); c.setFillColor(g['GOLD_DK'])
    c.drawCentredString(cx, iy + 40, 'Art size: 2,550 × 3,400 px or larger · no text in the artwork')
    return dict(page=page, placeholder=idx)


def draw_title(c, page):
    g['bg'](c, g['CREAM']); g['frame'](c, page)
    x0, y0, x1, y1 = g['trim_box'](page)
    cx = (x0 + x1) / 2
    c.setFillColor(g['NAVY']); c.setFont('Cinzel-Black', 50)
    c.drawCentredString(cx, y1 - 2.9 * inch, 'JOESIAH')
    c.setFont('Cinzel-Bold', 34); c.setFillColor(g['GOLD_DK'])
    c.drawCentredString(cx, y1 - 3.55 * inch, '&')
    c.setFillColor(g['NAVY']); c.setFont('Cinzel-Black', 50)
    c.drawCentredString(cx, y1 - 4.35 * inch, 'MALANI')
    c.setFont('Cinzel-Bold', 20); c.setFillColor(g['GOLD_DK'])
    c.drawCentredString(cx, y1 - 4.85 * inch, 'TIME TRAVEL ADVENTURE')
    g['ornament'](c, cx, y1 - 5.15 * inch, 2.6 * inch)
    c.setFont('Cinzel-Bold', 28); c.setFillColor(g['MAROON'])
    c.drawCentredString(cx, y1 - 6.05 * inch, 'FROM ABRAHAM TO MOSES')
    c.setFont('Cinzel-Bold', 18)
    c.drawCentredString(cx, y1 - 6.5 * inch, 'THE JOURNEY TO FREEDOM')
    c.setFont('Cinzel-Bold', 13); c.setFillColor(g['GOLD_DK'])
    c.drawCentredString(cx, y1 - 5.6 * inch, 'PART 2')
    c.setFont('Literata-Italic', 15); c.setFillColor(g['NAVY'])
    c.drawCentredString(cx, y1 - 7.3 * inch, C.TAGLINE)
    c.setFont('Literata', 13); c.setFillColor(g['INK'])
    c.drawCentredString(cx, y0 + 2.0 * inch, 'Written by')
    c.setFont('Cinzel-Bold', 20); c.setFillColor(g['NAVY'])
    c.drawCentredString(cx, y0 + 1.6 * inch, C.AUTHOR.upper())


def draw_copyright(c, page):
    g['bg'](c, g['CREAM'])
    x0, y0, x1, y1 = g['text_margins'](page)
    width = x1 - x0
    st = ParagraphStyle('c', fontName='Literata', fontSize=9.5, leading=13.5, textColor=g['INK'], alignment=TA_CENTER, spaceAfter=8)
    sb = ParagraphStyle('cb', parent=st, fontName='Cinzel-Bold', fontSize=11, leading=15, textColor=g['NAVY'], spaceAfter=2)
    paras = [
        Paragraph('Joesiah &amp; Malani Time Travel Adventure: Part 2: From Abraham to Moses — The Journey to Freedom', sb),
        Paragraph('Joesiah &amp; Malani Time Travel Adventure, Part 2 of 3', st),
        Paragraph('Text copyright © [year] %s<br/>All rights reserved.' % C.AUTHOR, st),
        Paragraph('No part of this book may be reproduced, stored in a retrieval system, or transmitted in any form '
                  'or by any means—electronic, mechanical, photocopying, recording, or otherwise—without the '
                  'prior written permission of the author, except for brief quotations used in reviews.', st),
        Paragraph('Unless otherwise noted, Scripture quotations are taken from the Holy Bible, New International '
                  'Version®, NIV®. Copyright © 1973, 1978, 1984, 2011 by Biblica, Inc.® Used by permission. All '
                  'rights reserved worldwide.', st),
        Paragraph('First edition, [year]', st),
    ]
    hs = [p.wrap(width, 1000)[1] + 8 for p in paras]
    y = y0 + sum(hs) + 0.2 * inch
    for p, h in zip(paras, hs):
        p.drawOn(c, x0, y - (h - 8)); y -= h


g['draw_art'], g['draw_title'], g['draw_copyright'] = draw_art, draw_title, draw_copyright
import os
if os.environ.get('DIAG'):
    for n, t, b in C.CHAPTERS:
        s = 14.0
        while s >= 9 and not any(g['layout_chapter'](n, t, b, g['PAGE_OF_CH'][n], s, dry=True, lf=lf)[0] for lf in g['LEADS']):
            s -= 0.25
        print(n, t, s, round(g['layout_chapter'](n, t, b, g['PAGE_OF_CH'][n], 11.75, dry=True, lf=1.30)[1]))
else:
    g['main']()
