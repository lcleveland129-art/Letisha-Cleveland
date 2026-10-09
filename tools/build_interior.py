"""Build the KDP paperback interior PDF: 8.5 x 11 in trim, with bleed (8.625 x 11.25 in pages).

KDP bleed convention: bleed is added to the top, bottom, and OUTSIDE edge only.
  - Right-hand (odd) pages:  trim x = 0 .. 8.5 in   (bleed on the right)
  - Left-hand  (even) pages: trim x = 0.125 .. 8.625 in (bleed on the left)
  - All pages:               trim y = 0.125 .. 11.125 in
Everything that is not a bleed background is kept at least 0.375 in inside the trim
(KDP minimum for books with bleed), and the inside (gutter) margin is >= 0.375 in.
"""
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

sys.path.insert(0, sys.argv[1])
import content as C  # noqa: E402

FONTS = sys.argv[2]
ILL = sys.argv[3]
OUT = sys.argv[4]

for name, f in [('Cinzel', 'Cinzel-Regular'), ('Cinzel-Bold', 'Cinzel-Bold'), ('Cinzel-Black', 'Cinzel-Black'),
                ('Literata', 'Literata-Regular'), ('Literata-Bold', 'Literata-Bold'),
                ('Literata-Italic', 'Literata-Italic'), ('Literata-BoldItalic', 'Literata-BoldItalic')]:
    pdfmetrics.registerFont(TTFont(name, f'{FONTS}/{f}.ttf'))
from reportlab.lib.fonts import addMapping
addMapping('Literata', 0, 0, 'Literata'); addMapping('Literata', 1, 0, 'Literata-Bold')
addMapping('Literata', 0, 1, 'Literata-Italic'); addMapping('Literata', 1, 1, 'Literata-BoldItalic')

PW, PH = 8.625 * inch, 11.25 * inch
BLEED = 0.125 * inch
TRIM_W, TRIM_H = 8.5 * inch, 11 * inch
SAFE = 0.375 * inch

NAVY = HexColor('#1B2A4A')
INK = HexColor('#2A2522')
GOLD = HexColor('#B8913A')
GOLD_DK = HexColor('#8A6A1F')
CREAM = HexColor('#FBF6EA')
PARCH = HexColor('#F3E7C9')
MAROON = HexColor('#7A2418')
NIGHT = HexColor('#14213D')


def trim_box(page):
    """(x0, y0, x1, y1) of the trimmed page in PDF coordinates."""
    x0 = BLEED if page % 2 == 0 else 0
    return x0, BLEED, x0 + TRIM_W, BLEED + TRIM_H


def text_margins(page):
    """Live text area. Inside (gutter) 0.875 in, outside 0.75 in, top 0.7 in, bottom 0.75 in (from trim)."""
    x0, y0, x1, y1 = trim_box(page)
    inside, outside = 0.875 * inch, 0.75 * inch
    if page % 2 == 1:   # right page: gutter on the left
        return x0 + inside, y0 + 0.75 * inch, x1 - outside, y1 - 0.7 * inch
    return x0 + outside, y0 + 0.75 * inch, x1 - inside, y1 - 0.7 * inch


def bg(c, color):
    c.setFillColor(color)
    c.rect(0, 0, PW, PH, stroke=0, fill=1)


def frame(c, page):
    """Thin double gold rule inside the trim, 0.45 in from trim edges (inside the 0.375 in safe line)."""
    x0, y0, x1, y1 = trim_box(page)
    m = 0.45 * inch
    c.setStrokeColor(GOLD); c.setLineWidth(0.9)
    c.rect(x0 + m, y0 + m, (x1 - x0) - 2 * m, (y1 - y0) - 2 * m, stroke=1, fill=0)
    c.setLineWidth(0.4)
    c.rect(x0 + m + 3, y0 + m + 3, (x1 - x0) - 2 * m - 6, (y1 - y0) - 2 * m - 6, stroke=1, fill=0)


def folio(c, page):
    x0, y0, x1, y1 = trim_box(page)
    c.setFillColor(GOLD_DK); c.setFont('Literata', 10)
    c.drawCentredString((x0 + x1) / 2, y0 + 0.5 * inch + 6, str(page))


def ornament(c, cx, y, w=1.6 * inch):
    c.setStrokeColor(GOLD); c.setLineWidth(0.8)
    c.line(cx - w / 2, y, cx - 7, y); c.line(cx + 7, y, cx + w / 2, y)
    c.setFillColor(GOLD)
    p = c.beginPath(); p.moveTo(cx, y + 4); p.lineTo(cx + 4, y); p.lineTo(cx, y - 4); p.lineTo(cx - 4, y); p.close()
    c.drawPath(p, stroke=0, fill=1)


# ---------------------------------------------------------------- styles
def styles(size, lf=1.38):
    lead = size * lf
    return {
        'p': ParagraphStyle('p', fontName='Literata', fontSize=size, leading=lead, textColor=INK,
                            alignment=TA_LEFT, spaceAfter=size * 0.42),
        'quote': ParagraphStyle('q', fontName='Literata-Italic', fontSize=size, leading=lead, textColor=NAVY,
                                leftIndent=0.35 * inch, rightIndent=0.35 * inch, spaceAfter=1),
        'qref': ParagraphStyle('qr', fontName='Cinzel-Bold', fontSize=size * 0.72, leading=size * 1.1,
                               textColor=GOLD_DK, alignment=TA_RIGHT, rightIndent=0.35 * inch, spaceAfter=size * 0.7),
        'names': ParagraphStyle('n', fontName='Cinzel-Bold', fontSize=size * 1.15, leading=size * 1.6,
                                textColor=NAVY, alignment=TA_CENTER, spaceAfter=size * 0.6),
        'emph': ParagraphStyle('e', fontName='Cinzel-Bold', fontSize=size * 1.15, leading=size * 1.6,
                               textColor=NAVY, alignment=TA_CENTER, spaceAfter=size * 0.6),
        'motto': ParagraphStyle('m', fontName='Literata-Italic', fontSize=size * 0.95, leading=size * 1.35,
                                textColor=NAVY, alignment=TA_CENTER),
        'thought': ParagraphStyle('t', fontName='Literata-BoldItalic', fontSize=size * 0.98, leading=size * 1.38,
                                  textColor=NAVY),
        'tlabel': ParagraphStyle('tl', fontName='Cinzel-Bold', fontSize=size * 0.72, leading=size * 1.05,
                                 textColor=GOLD_DK, spaceAfter=2),
        'pledge': ParagraphStyle('pl', fontName='Cinzel-Black', fontSize=size * 1.12, leading=size * 1.5,
                                 textColor=MAROON, alignment=TA_CENTER, spaceBefore=0, spaceAfter=size * 0.45),
        'turn': ParagraphStyle('tu', fontName='Literata-Italic', fontSize=size * 0.95, leading=size * 1.35,
                               textColor=NAVY, alignment=TA_RIGHT, spaceBefore=2),
        'read': ParagraphStyle('r', fontName='Literata', fontSize=size * 0.88, leading=size * 1.25,
                               textColor=INK, alignment=TA_CENTER),
        'end': ParagraphStyle('en', fontName='Literata', fontSize=size, leading=size * 1.4,
                              textColor=NAVY, alignment=TA_CENTER),
    }


def boxed(paras, width, fill, border, pad=9, left_bar=False):
    t = Table([[paras]], colWidths=[width])
    st = [('FONT', (0, 0), (-1, -1), 'Literata', 10), ('BACKGROUND', (0, 0), (-1, -1), fill),
          ('LEFTPADDING', (0, 0), (-1, -1), pad + (4 if left_bar else 0)), ('RIGHTPADDING', (0, 0), (-1, -1), pad),
          ('TOPPADDING', (0, 0), (-1, -1), pad * 0.75), ('BOTTOMPADDING', (0, 0), (-1, -1), pad * 0.85)]
    if left_bar:
        st.append(('LINEBEFORE', (0, 0), (0, -1), 3, border))
    else:
        st.append(('BOX', (0, 0), (-1, -1), 0.8, border))
    t.setStyle(TableStyle(st))
    return t


def flowables(blocks, S, width):
    """Body flowables (excluding the READ band, which is anchored at the page bottom)."""
    out = []
    for b in blocks:
        k = b[0]
        if k == 'p':
            out.append(Paragraph(b[1], S['p']))
        elif k == 'quote':
            out.append(Paragraph(b[1], S['quote']))
            out.append(Paragraph('—' + b[2], S['qref']))
        elif k == 'names':
            out.append(Paragraph('  •  '.join(n.upper() for n in b[1]), S['names']))
        elif k == 'emph':
            out.append(Paragraph(b[1].upper() if b[1].endswith('.') and len(b[1]) < 12 else b[1], S['emph']))
        elif k == 'motto':
            out.append(Spacer(1, 2))
            out.append(boxed([Paragraph(C.MOTTO, S['motto'])], width - 0.5 * inch, PARCH, GOLD, pad=6))
            out.append(Spacer(1, S['p'].fontSize * 0.55))
        elif k == 'thought':
            inner = []
            if b[1]:
                inner.append(Paragraph(b[1], S['tlabel']))
            inner.append(Paragraph(b[2], S['thought']))
            out.append(boxed(inner, width, HexColor('#F7EED8'), GOLD, pad=6, left_bar=True))
            out.append(Spacer(1, S['p'].fontSize * 0.5))
        elif k == 'pledge':
            out.append(Paragraph(b[1], S['pledge']))
        elif k == 'turn':
            out.append(Paragraph('<font name="Cinzel-Bold" color="#8A6A1F" size="%.1f">TURN THE PAGE</font> <font name="Literata-Bold" color="#8A6A1F">→</font>&nbsp;&nbsp;%s'
                                 % (S['p'].fontSize * 0.72, b[1]), S['turn']))
        elif k == 'end':
            inner = [Paragraph('<font name="Cinzel-Bold" size="%.1f" color="#8A6A1F">THE JOURNEY CONTINUES</font>' % (S['p'].fontSize * 0.95), S['end']),
                     Spacer(1, 4),
                     Paragraph('<font name="Cinzel-Bold" size="%.1f">%s • Book 2</font>' % (S['p'].fontSize * 1.05, C.SERIES.replace('&', '&amp;')), S['end']),
                     Paragraph('<i>%s</i>' % C.NEXT_BOOK, S['end']),
                     Spacer(1, 6),
                     Paragraph('<i>%s</i>' % C.MOTTO, S['motto'])]
            out.append(Spacer(1, 6))
            out.append(boxed(inner, width - 0.3 * inch, PARCH, GOLD, pad=12))
    return out


def read_band(b, S, width):
    if not b:
        return None
    inner = [Paragraph('<font name="Cinzel-Bold" color="#8A6A1F" size="%.1f">%s</font>' % (S['p'].fontSize * 0.74, b[1]), S['read']),
             Paragraph(b[2], S['read'])]
    t = Table([[inner]], colWidths=[width])
    t.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'Literata', 10), ('LINEABOVE', (0, 0), (-1, 0), 0.8, GOLD), ('TOPPADDING', (0, 0), (-1, -1), 6),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 0), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                           ('RIGHTPADDING', (0, 0), (-1, -1), 0)]))
    return t


def header_height(c_title, width, size):
    """Height of chapter header block (label + title + ornament)."""
    tstyle = ParagraphStyle('ct', fontName='Cinzel-Bold', fontSize=size * 1.6, leading=size * 1.9,
                            textColor=NAVY, alignment=TA_CENTER)
    p = Paragraph(c_title.replace('&', '&amp;'), tstyle)
    _, h = p.wrap(width, 1000)
    return p, h


def layout_chapter(num, title, blocks, page, size, dry=False, c=None, lf=1.38):
    """Return (fits, leftover). If not dry, draw on canvas c."""
    S = styles(size, lf)
    x0, y0, x1, y1 = text_margins(page)
    width = x1 - x0
    label_h = size * 1.2
    tp, th = header_height(title, width - 0.3 * inch, size)
    head_h = label_h + 6 + th + 18
    body = [b for b in blocks if b[0] != 'read']
    rb = [b for b in blocks if b[0] == 'read']
    band = read_band(rb[0] if rb else None, S, width)
    band_h = band.wrap(width, 1000)[1] if band else 0
    folio_room = 0.12 * inch
    avail = (y1 - y0) - head_h - band_h - (12 if band else 0) - folio_room
    fl = flowables(body, S, width)
    hs = []
    for f in fl:
        _, h = f.wrap(width, 10000)
        hs.append(h + f.getSpaceBefore() + f.getSpaceAfter())
    used = sum(hs)
    leftover = avail - used
    if dry:
        return leftover >= 0, leftover
    # spread a little of the leftover between paragraphs (capped) so short chapters do not look empty
    gaps = max(1, len(fl) - 1)
    extra = min(max(leftover, 0) * 0.5 / gaps, size * 0.6)
    rest = max(leftover, 0) - extra * gaps
    sink = rest * 0.42          # balance the remaining space: a bit more below than above
    # draw header
    cx = (x0 + x1) / 2
    y = y1
    c.setFillColor(GOLD_DK); c.setFont('Cinzel-Bold', size * 0.95)
    lab = 'CHAPTER %d' % num
    c.drawCentredString(cx, y - size * 0.95, lab)
    y -= label_h + 6
    tp.wrap(width - 0.3 * inch, 1000)
    tp.drawOn(c, x0 + 0.15 * inch, y - th)
    y -= th + 9
    ornament(c, cx, y)
    y -= 9 + sink
    for f, h in zip(fl, hs):
        w, hh = f.wrap(width, 10000)
        y -= f.getSpaceBefore()
        f.drawOn(c, x0 + (width - w) / 2 if isinstance(f, Table) else x0, y - hh)
        y -= hh + f.getSpaceAfter() + extra
    if band:
        band.wrap(width, 1000)
        band.drawOn(c, x0, y0 + folio_room)
    return True, leftover


LEADS = [1.38, 1.36, 1.34, 1.32, 1.30, 1.28, 1.26]


def fit_lead(n, t, b, s):
    for lf in LEADS:
        if layout_chapter(n, t, b, PAGE_OF_CH[n], s, dry=True, lf=lf)[0]:
            return lf
    return None


def pick_size():
    """Largest single body size (pt) at which every chapter fits on its one text page,
    allowing long chapters slightly tighter line spacing (1.38 down to 1.26)."""
    s = 13.0
    while s >= 10.5:
        leads = {n: fit_lead(n, t, b, s) for n, t, b in C.CHAPTERS}
        if all(leads.values()):
            return s, leads
        s -= 0.25
    raise SystemExit('Text does not fit at 10.5 pt')


# ---------------------------------------------------------------- page plan
PAGE_OF_CH = {n: 2 * n + 2 for n in range(1, 12)}
PAGE_OF_CH.update({12: 26, 13: 28, 14: 30})
PLAN = {1: ('title',), 2: ('copyright',), 3: ('contents',)}
for n in range(1, 12):
    PLAN[2 * n + 2] = ('chapter', n)
    PLAN[2 * n + 3] = ('art', C.CHAPTER_ART[n])
PLAN[26] = ('chapter', 12)
PLAN[27] = ('spotlight',)
PLAN[28] = ('chapter', 13)
PLAN[29] = ('art', C.CHAPTER_ART[13])
PLAN[30] = ('chapter', 14)
PLAN[31] = ('art', C.CHAPTER_ART[14])
NPAGES = max(PLAN)


def draw_art(c, page, idx):
    bg(c, NIGHT)
    x0, y0, x1, y1 = trim_box(page)
    h = 10.1 * inch
    from PIL import Image
    im = Image.open(f'{ILL}/ill-{idx:02d}.jpg')
    w = h * im.width / im.height
    ix = (x0 + x1) / 2 - w / 2
    iy = (y0 + y1) / 2 - h / 2
    assert ix - x0 >= SAFE and x1 - (ix + w) >= SAFE and iy - y0 >= SAFE and y1 - (iy + h) >= SAFE
    c.setStrokeColor(GOLD); c.setLineWidth(1.2)
    c.rect(ix - 4, iy - 4, w + 8, h + 8, stroke=1, fill=0)
    c.drawImage(f'{ILL}/ill-{idx:02d}.jpg', ix, iy, w, h)
    return dict(page=page, ill=idx, w_in=w / inch, h_in=h / inch, ppi=im.width / (w / inch))


def draw_title(c, page):
    bg(c, CREAM); frame(c, page)
    x0, y0, x1, y1 = trim_box(page)
    cx = (x0 + x1) / 2
    c.setFillColor(NAVY); c.setFont('Cinzel-Black', 50)
    c.drawCentredString(cx, y1 - 3.3 * inch, 'JOESIAH')
    c.setFont('Cinzel-Bold', 34); c.setFillColor(GOLD_DK)
    c.drawCentredString(cx, y1 - 3.95 * inch, '&')
    c.setFillColor(NAVY); c.setFont('Cinzel-Black', 50)
    c.drawCentredString(cx, y1 - 4.75 * inch, 'MALANI')
    ornament(c, cx, y1 - 5.25 * inch, 2.6 * inch)
    c.setFont('Cinzel-Bold', 30); c.setFillColor(MAROON)
    c.drawCentredString(cx, y1 - 5.95 * inch, 'NOAH’S BLOODLINE')
    c.setFont('Cinzel-Bold', 13); c.setFillColor(GOLD_DK)
    c.drawCentredString(cx, y1 - 6.45 * inch, 'BOOK %d' % C.BOOK_NO)
    c.setFont('Literata-Italic', 15); c.setFillColor(NAVY)
    c.drawCentredString(cx, y1 - 7.15 * inch, C.TAGLINE)
    c.setFont('Literata', 13); c.setFillColor(INK)
    c.drawCentredString(cx, y0 + 2.0 * inch, 'Written by')
    c.setFont('Cinzel-Bold', 20); c.setFillColor(NAVY)
    c.drawCentredString(cx, y0 + 1.6 * inch, C.AUTHOR.upper())


def draw_copyright(c, page):
    bg(c, CREAM)
    x0, y0, x1, y1 = text_margins(page)
    width = x1 - x0
    st = ParagraphStyle('c', fontName='Literata', fontSize=9.5, leading=13.5, textColor=INK, alignment=TA_CENTER, spaceAfter=8)
    sb = ParagraphStyle('cb', parent=st, fontName='Cinzel-Bold', fontSize=11, leading=15, textColor=NAVY, spaceAfter=2)
    paras = [
        Paragraph('Joesiah &amp; Malani: Noah’s Bloodline', sb),
        Paragraph('Joesiah &amp; Malani, Book 1', st),
        Paragraph('Text copyright © 2026 %s<br/>All rights reserved.' % C.AUTHOR, st),
        Paragraph('No part of this book may be reproduced, stored in a retrieval system, or transmitted in any form '
                  'or by any means—electronic, mechanical, photocopying, recording, or otherwise—without the '
                  'prior written permission of the author, except for brief quotations used in reviews.', st),
        Paragraph('Unless otherwise noted, Scripture quotations in the story text are taken from the Holy Bible, '
                  'New International Version®, NIV®. Copyright © 1973, 1978, 1984, 2011 by Biblica, '
                  'Inc.® Used by permission. All rights reserved worldwide. Scripture quotations within the '
                  'illustrations are drawn from or adapted from several English translations.', st),
        Paragraph('First edition, 2026', st),
    ]
    hs = [p.wrap(width, 1000)[1] + 8 for p in paras]
    y = y0 + sum(hs) + 0.2 * inch
    for p, h in zip(paras, hs):
        p.drawOn(c, x0, y - (h - 8)); y -= h


def draw_contents(c, page, size):
    bg(c, CREAM); frame(c, page)
    x0, y0, x1, y1 = text_margins(page)
    cx = (x0 + x1) / 2
    c.setFillColor(NAVY); c.setFont('Cinzel-Bold', 28)
    c.drawCentredString(cx, y1 - 0.55 * inch, 'CONTENTS')
    ornament(c, cx, y1 - 0.85 * inch, 2.2 * inch)
    y = y1 - 1.45 * inch
    step = (y - (y0 + 0.5 * inch)) / 14
    for n, t, _ in C.CHAPTERS:
        c.setFont('Cinzel-Bold', 11); c.setFillColor(GOLD_DK)
        c.drawString(x0 + 0.1 * inch, y, '%d' % n)
        c.setFont('Literata', 12.5); c.setFillColor(INK)
        c.drawString(x0 + 0.5 * inch, y, t)
        tw = c.stringWidth(t, 'Literata', 12.5)
        pg = str(PAGE_OF_CH[n])
        c.setFont('Literata', 12.5)
        pw = c.stringWidth(pg, 'Literata', 12.5)
        c.drawRightString(x1 - 0.1 * inch, y, pg)
        # dotted leader
        c.setFillColor(GOLD)
        lx = x0 + 0.5 * inch + tw + 8
        while lx < x1 - 0.1 * inch - pw - 8:
            c.circle(lx, y + 3, 0.6, stroke=0, fill=1); lx += 6
        y -= step


def draw_spotlight(c, page):
    bg(c, CREAM); frame(c, page)
    x0, y0, x1, y1 = text_margins(page)
    cx = (x0 + x1) / 2
    width = x1 - x0 - 0.6 * inch
    c.setFillColor(GOLD_DK); c.setFont('Cinzel-Bold', 14)
    c.drawCentredString(cx, (y0 + y1) / 2 + 2.3 * inch, C.SPOTLIGHT['label'])
    ornament(c, cx, (y0 + y1) / 2 + 2.0 * inch, 2.2 * inch)
    c.setFont('Literata-Italic', 13); c.setFillColor(INK)
    c.drawCentredString(cx, (y0 + y1) / 2 + 1.55 * inch, C.SPOTLIGHT['intro'])
    st = ParagraphStyle('s', fontName='Literata-Italic', fontSize=22, leading=33, textColor=NAVY, alignment=TA_CENTER)
    p = Paragraph(C.SPOTLIGHT['text'], st)
    w, h = p.wrap(width, 1000)
    top = (y0 + y1) / 2 + 1.1 * inch
    p.drawOn(c, x0 + 0.3 * inch, top - h)
    c.setFont('Cinzel-Bold', 14); c.setFillColor(GOLD_DK)
    c.drawCentredString(cx, top - h - 0.5 * inch, '—' + C.SPOTLIGHT['ref'].upper())
    folio(c, page)


def main():
    size, LEAD = pick_size()
    c = canvas.Canvas(OUT, pagesize=(PW, PH), pageCompression=1, initialFontName='Literata', initialFontSize=11)
    c.setTitle('%s: %s' % (C.TITLE, C.SUBTITLE)); c.setAuthor(C.AUTHOR)
    c.setSubject('%s, Book %d' % (C.SERIES, C.BOOK_NO)); c.setCreator('KDP interior build')
    report = {'body_pt': size, 'leading': LEAD, 'pages': []}
    chap = {n: (t, b) for n, t, b in C.CHAPTERS}
    for page in range(1, NPAGES + 1):
        kind = PLAN[page]
        c.setPageSize((PW, PH))
        # Boxes for prepress checks: TrimBox/BleedBox
        x0, y0, x1, y1 = trim_box(page)
        c.setCropBox((0, 0, PW, PH)); c.setTrimBox((x0, y0, x1, y1)); c.setBleedBox((0, 0, PW, PH))
        if kind[0] == 'title':
            draw_title(c, page)
        elif kind[0] == 'copyright':
            draw_copyright(c, page)
        elif kind[0] == 'contents':
            draw_contents(c, page, size)
        elif kind[0] == 'chapter':
            n = kind[1]
            bg(c, CREAM); frame(c, page)
            ok, left = layout_chapter(n, chap[n][0], chap[n][1], page, size, c=c, lf=LEAD[n])
            folio(c, page)
            report['pages'].append(dict(page=page, chapter=n, leftover_pt=round(left, 1)))
        elif kind[0] == 'art':
            report['pages'].append(draw_art(c, page, kind[1]))
        elif kind[0] == 'spotlight':
            draw_spotlight(c, page)
        c.showPage()
    c.save()
    import json
    print(json.dumps(report, indent=1))


if __name__ == '__main__':
    main()
