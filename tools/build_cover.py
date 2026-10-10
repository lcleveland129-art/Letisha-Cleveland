"""Build the KDP full-wrap paperback cover PDF from the author's cover draft artwork.

Layout (KDP): width = bleed + back + spine + front + bleed, height = bleed + trim + bleed.
  8.5 x 11 in trim, 0.125 in bleed, premium color on white paper: spine = pages x 0.002347 in.
The draft's back and front panels are each 8.625 x 11.25 in (trim + outer bleed), so they
are placed edge-to-edge with the spine between them.

Changes to the draft:
  - back-cover motto replaced with the book's motto (same maroon italic)
  - 'BOOK 1' set in the gold rule under the title (replacing the small ankh)
  - author banner re-lettered "By LeTisha C. Cleveland" (matches interior + KDP listing)
  - the invalid placeholder ISBN/barcode label is covered by a clean white box that also
    contains KDP's barcode position (2 x 1.2 in, 0.25 in from spine and bottom trim)
  - spine filled with the adjoining panel edges so a thin-book spine shift is invisible
  - panels enlarged to ~300 ppi (Lanczos; no AI redraw)
"""
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BACK, FRONT, FONTS, OUTDIR = sys.argv[1:5]
PAGES = int(sys.argv[5]) if len(sys.argv) > 5 else 32

IN = 72.0
BLEED, TRIM_W, TRIM_H = 0.125, 8.5, 11.0
SPINE = PAGES * 0.002347
PANEL_W, PANEL_H = TRIM_W + BLEED, TRIM_H + 2 * BLEED          # 8.625 x 11.25
TOTAL_W = 2 * PANEL_W + SPINE
K = 3.5                                                           # upscale factor


def upscale(path):
    im = Image.open(path).convert('RGB')
    up = im.resize((round(im.width * K), round(im.height * K)), Image.LANCZOS)
    return up.filter(ImageFilter.UnsharpMask(radius=2, percent=35, threshold=2))


def reletter_author(front):
    """Replace 'By LeTisha Cleveland' in the navy banner (original px coords below)."""
    rgb = np.array(front).astype(np.float32)
    s = lambda v: int(round(v * K))
    x0, y0, x1, y1 = s(192), s(934), s(528), s(978)                # text area
    bx0, by0, bx1, by1 = s(110), s(931), s(575), s(976)            # navy banner interior
    reg = rgb[by0:by1, bx0:bx1]
    lum = reg.mean(axis=2)
    txt = np.zeros(lum.shape, bool)
    txt[y0 - by0:y1 - by0, x0 - bx0:x1 - bx0] = lum[y0 - by0:y1 - by0, x0 - bx0:x1 - bx0] > 60
    big = cv2.dilate(txt.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))) > 0
    wgt = (~big).astype(np.float32)
    fill = np.zeros_like(reg); done = np.zeros(wgt.shape, bool)
    for sig in (12, 30, 80, 200):
        num = cv2.GaussianBlur(reg * wgt[..., None], (0, 0), sig)
        den = cv2.GaussianBlur(wgt, (0, 0), sig)
        ok = (den > 0.2) & ~done
        fill[ok] = num[ok] / den[ok][:, None]; done |= ok
    fill += np.random.default_rng(3).normal(0, 2.0, fill.shape)
    reg[big] = fill[big]
    rgb[by0:by1, bx0:bx1] = reg
    out = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))

    # new lettering: same cap height / centre as the original, EB Garamond SemiBold, gold gradient
    old, new = 'By LeTisha Cleveland', 'By LeTisha C. Cleveland'
    path = FONTS + '/EBGaramond-SemiBold.ttf'
    f100 = ImageFont.truetype(path, 100)
    size = int(round(100 * (516 - 202) * K / f100.getlength(old)))
    f = ImageFont.truetype(path, size)
    cx, base = (202 + 516) / 2 * K, 966 * K
    mask = Image.new('L', out.size, 0)
    ImageDraw.Draw(mask).text((cx, base), new, font=f, fill=255, anchor='ms')
    mask = mask.filter(ImageFilter.GaussianBlur(0.8))
    top, bot = np.array([246, 226, 160]), np.array([206, 160, 88])
    grad = np.zeros((out.height, out.width, 3), np.float32)
    t = np.clip((np.arange(out.height) - 938 * K) / (28 * K), 0, 1)[:, None]
    grad[:] = (top * (1 - t) + bot * t)[:, None, :]
    shadow = mask.filter(ImageFilter.GaussianBlur(3 * K / 3.5))
    o = np.array(out).astype(np.float32)
    sa = np.array(shadow, np.float32)[..., None] / 255 * 0.55
    o = o * (1 - sa)                                                 # soft dark halo for legibility
    a = np.array(mask, np.float32)[..., None] / 255
    o = o * (1 - a) + grad * a
    return Image.fromarray(np.clip(o, 0, 255).astype(np.uint8)), (old, new, size)


def add_book_label(front):
    """Replace the small ankh in the gold rule under the title with 'BOOK 1'."""
    rgb = np.array(front).astype(np.float32)
    s = lambda v: int(round(v * K))
    # navy of the 'NOAH'S BLOODLINE' lettering
    t = rgb[s(196):s(211), s(150):s(590)]
    navy = np.median(t[t.mean(axis=2) < 60], axis=0)
    gx0, gx1 = 316, 420            # gap opened in the gold rule (original px)
    x0, y0, x1, y1 = s(gx0), s(215), s(gx1), s(245)
    reg = rgb[y0:y1, x0:x1]
    lum = reg.mean(axis=2)
    ink = (lum < 185) & (reg[..., 0] > reg[..., 2] + 25)          # gold-brown rule + ankh
    big = cv2.dilate(ink.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))) > 0
    # sample clean sky from a wider window around the gap
    wx0, wy0, wx1, wy1 = s(gx0 - 30), s(214), s(gx1 + 30), s(246)
    win = rgb[wy0:wy1, wx0:wx1]
    wl = win.mean(axis=2)
    wink = (wl < 185) & (win[..., 0] > win[..., 2] + 25)
    wbig = cv2.dilate(wink.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))) > 0
    wgt = (~wbig).astype(np.float32)
    fill = np.zeros_like(win); done = np.zeros(wgt.shape, bool)
    for sig in (10, 25, 60, 150):
        num = cv2.GaussianBlur(win * wgt[..., None], (0, 0), sig)
        den = cv2.GaussianBlur(wgt, (0, 0), sig)
        ok = (den > 0.2) & ~done
        fill[ok] = num[ok] / den[ok][:, None]; done |= ok
    fill += np.random.default_rng(5).normal(0, 1.5, fill.shape)
    ox, oy = x0 - wx0, y0 - wy0
    sub = fill[oy:oy + (y1 - y0), ox:ox + (x1 - x0)]
    reg[big] = sub[big]
    rgb[y0:y1, x0:x1] = reg
    out = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    # 'BOOK 1' in Cinzel Bold, cap height ~15 px (original), centred on the rule
    path = FONTS + '/Cinzel-Bold.ttf'
    f100 = ImageFont.truetype(path, 100)
    bb = f100.getbbox('H'); cap = bb[3] - bb[1]
    f = ImageFont.truetype(path, int(round(100 * 15.5 * K / cap)))
    cx, base = 368 * K, 239.5 * K
    mask = Image.new('L', out.size, 0)
    ImageDraw.Draw(mask).text((cx, base), 'BOOK 1', font=f, fill=255, anchor='ms')
    mask = mask.filter(ImageFilter.GaussianBlur(0.7))
    o = np.array(out).astype(np.float32)
    a = np.array(mask, np.float32)[..., None] / 255
    o = o * (1 - a) + navy * a
    w = ImageDraw.Draw(mask).textlength('BOOK 1', font=f) / K
    return Image.fromarray(np.clip(o, 0, 255).astype(np.uint8)), round(w, 1)


def replace_motto(back):
    """Back cover: replace 'Know Your History. / Be Proud of Your Story. / Walk in Your Purpose.'
    with the book's motto, in the same maroon semibold italic, centred on the same axis."""
    rgb = np.array(back).astype(np.float32)
    s = lambda v: int(round(v * K))
    x0, y0, x1, y1 = s(345), s(415), s(592), s(498)
    wx0, wy0, wx1, wy1 = s(320), s(408), s(615), s(518)
    win = rgb[wy0:wy1, wx0:wx1]
    r, g, b = win[..., 0], win[..., 1], win[..., 2]
    lum = win.mean(axis=2)
    ink = (r > g + 25) & (r > b + 30) & (lum < 165)
    inside = np.zeros(ink.shape, bool); inside[y0 - wy0:y1 - wy0, x0 - wx0:x1 - wx0] = True
    ink &= inside
    color = np.median(win[ink & (lum < 90)], axis=0)
    big = cv2.dilate(ink.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))) > 0
    wgt = (~big).astype(np.float32)
    fill = np.zeros_like(win); done = np.zeros(wgt.shape, bool)
    for sig in (10, 25, 60, 150):
        num = cv2.GaussianBlur(win * wgt[..., None], (0, 0), sig)
        den = cv2.GaussianBlur(wgt, (0, 0), sig)
        ok = (den > 0.2) & ~done
        fill[ok] = num[ok] / den[ok][:, None]; done |= ok
    fill += np.random.default_rng(9).normal(0, 2.0, fill.shape)
    win[big] = fill[big]
    rgb[wy0:wy1, wx0:wx1] = win
    out = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    path = FONTS + '/EBGaramond-SemiBoldItalic.ttf'
    f100 = ImageFont.truetype(path, 100)
    size = int(round(100 * (571 - 357) * K / f100.getlength('Be Proud of Your Story.') * 0.92))
    f = ImageFont.truetype(path, size)
    lines = ['Know the Word.', 'Seek the Truth.', 'Remember who you are.', 'Walk in the purpose God gave you.']
    mask = Image.new('L', out.size, 0); d = ImageDraw.Draw(mask)
    cx = 463 * K
    widths = []
    for i, ln in enumerate(lines):
        d.text((cx, (436 + 23 * i) * K), ln, font=f, fill=255, anchor='ms')
        widths.append(round(f.getlength(ln) / K))
    mask = mask.filter(ImageFilter.GaussianBlur(0.7))
    o = np.array(out).astype(np.float32)
    a = np.array(mask, np.float32)[..., None] / 255
    o = o * (1 - a) + color * a
    return Image.fromarray(np.clip(o, 0, 255).astype(np.uint8)), dict(color=[int(v) for v in color], widths_px=widths)


def main():
    back, motto = replace_motto(upscale(BACK))
    front, info = reletter_author(upscale(FRONT))
    front, book_w = add_book_label(front)
    back.save(OUTDIR + '/cover_back.jpg', quality=93, subsampling=0, dpi=(300, 300))
    front.save(OUTDIR + '/cover_front.jpg', quality=93, subsampling=0, dpi=(300, 300))
    # spine strip: right edge of back + left edge of front (seamless if the spine shifts)
    px_per_in = back.width / PANEL_W
    sw = max(2, int(round(SPINE * px_per_in)))
    left = back.crop((back.width - sw // 2 - (sw % 2), 0, back.width, back.height)).transpose(Image.FLIP_LEFT_RIGHT)
    right = front.crop((0, 0, sw // 2, front.height)).transpose(Image.FLIP_LEFT_RIGHT)
    spine = Image.new('RGB', (sw, back.height)); spine.paste(left, (0, 0)); spine.paste(right, (left.width, 0))
    spine.save(OUTDIR + '/cover_spine.jpg', quality=93, subsampling=0)

    pdfmetrics.registerFont(TTFont('EBGaramond', FONTS + '/EBGaramond-Medium.ttf'))
    out = OUTDIR + '/cover.pdf'
    c = canvas.Canvas(out, pagesize=(TOTAL_W * IN, PANEL_H * IN), initialFontName='EBGaramond')
    c.setTitle("Joesiah & Malani: Noah’s Bloodline – Cover"); c.setAuthor('LeTisha C. Cleveland')
    c.drawImage(OUTDIR + '/cover_back.jpg', 0, 0, PANEL_W * IN, PANEL_H * IN)
    c.drawImage(OUTDIR + '/cover_spine.jpg', PANEL_W * IN, 0, SPINE * IN, PANEL_H * IN)
    c.drawImage(OUTDIR + '/cover_front.jpg', (PANEL_W + SPINE) * IN, 0, PANEL_W * IN, PANEL_H * IN)
    # barcode area: covers the old placeholder label (x 440-597, y 48-146 pt) and contains
    # KDP's barcode spot (2 x 1.2 in, 0.25 in from spine and bottom trim)
    spine_x = PANEL_W * IN
    bx1 = spine_x - 0.25 * IN
    by0 = (BLEED + 0.25) * IN
    bx0 = 436.0
    by1 = 150.0
    c.setFillColor(white); c.setStrokeColor(white)
    c.roundRect(bx0, by0, bx1 - bx0, by1 - by0, 6, stroke=0, fill=1)
    c.showPage(); c.save()
    print(dict(pages=PAGES, spine_in=round(SPINE, 4), width_in=round(TOTAL_W, 4), height_in=PANEL_H,
               ppi=round(back.width / PANEL_W, 1), author=info, book_label_w_px=book_w, motto=motto,
               barcode_box_in=(round(bx0 / IN, 3), round(by0 / IN, 3), round((bx1 - bx0) / IN, 3), round((by1 - by0) / IN, 3))))


if __name__ == '__main__':
    main()
