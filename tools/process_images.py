"""Clean up the 13 book illustrations for print.

1. Crop off the photographed-book mock-up frame (white background, page stack, navy board).
2. Upscale with Lanczos resampling to ~300 ppi at printed size (no AI / no repainting).
3. Re-letter baked-in chapter numbers, series wording and page numbers so they match
   the corrected book sequence. Only the label pixels are touched; characters and
   artwork are left as-is.
"""
import json, sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WORK = sys.argv[1]      # folder with img-000.jpg ... img-012.jpg
OUT = sys.argv[2]       # output folder
FONTS = sys.argv[3]

CROP = dict(l=34, r=34, t=12, b=36)
SCALE = 2.5

# Label edits, in ORIGINAL image coordinates.
# 'line': a navy small-caps text line; box = (x0, y0, x1, y1) where y0..y1 is the exact
#         row band of the line (measured from ink profiles) so the title below is untouched.
# 'folio': a baked page number; box = exact digit bounding box; polarity dark/light.
# New page numbers follow the corrected layout (illustration pages are right-hand pages).
EDITS = {
    0:  [('folio', (483, 1205, 490, 1222), '5', 'dark')],
    1:  [('folio', (488, 1211, 500, 1229), '7', 'dark')],
    2:  [('block', (732, 423, 918, 572),
          ['The land of Canaan', '(today: Israel, Palestine,', 'Lebanon, and parts of',
           'Syria and Jordan).', 'Known for fertile land,', 'cities, and trade routes.',
           'Canaan was cursed', '(Genesis 9:25), not Ham and', 'not all of his descendants.'],
          dict(align='center', cx=825, ref_text='cities, and trade routes.', ref_w=173, size_k=0.82,
               baselines=[441 + k * 15.9 for k in range(9)], font='LiberationSerif-Regular',
               ink=135, dark=True)),
         ('line', (280, 19, 560, 49), 'CHAPTER 4', 'CHAPTER 7'), ('folio', (440, 1202, 458, 1219), '11', 'dark')],
    3:  [('folio', (484, 1197, 505, 1216), '9', 'light')],
    4:  [('block', (548, 306, 925, 413),
          ['In Genesis 9, Ham saw his father',
           'uncovered and told his brothers.',
           'Because of Ham\u2019s actions, Noah',
           'cursed Ham\u2019s son, Canaan:'],
          dict(ref_text='In Genesis 9, Noah saw something', ref_w=333, left=552,
               baselines=[325.5, 352, 378.5, 405])),
         ('plain', (598, 463, 890, 481), 'shall he be unto his brothers.”', 'shall be be unto his brothers.”'),
         ('folio', (487, 1203, 511, 1223), '13', 'light')],
    5:  [('block', (124, 202, 506, 418),
          'After the flood, the families of Ham\u2019s sons Cush, Mizraim, and Put built great '
          'nations in Africa. The land was rich with rivers, fertile soil, gold, minerals, and '
          'wisdom. The people created advanced cities, learned systems of mathematics, medicine, '
          'and astronomy, and built monuments that still inspire the world today.',
          dict(wrap=True, max_w=372, ref_text='After the flood, Ham\u2019s descendants', ref_w=338,
               left=130, baselines=[224, 250.5, 277, 303.5, 330, 356.5, 383, 409.5],
               font='LiberationSerif-Regular', ink=110, dark=True)),
         ('line', (200, 35, 420, 63), 'CHAPTER 6', 'CHAPTER 8'), ('folio', (432, 1204, 450, 1221), '15', 'dark')],
    6:  [('line', (230, 33, 440, 63), 'CHAPTER 7', 'CHAPTER 9', 'CHAPTER 11'), ('folio', (479, 1209, 497, 1226), '17', 'dark')],
    7:  [('line', (360, 26, 600, 56), 'CHAPTER 8', 'CHAPTER 10', 'CHAPTER 12'), ('folio', (468, 1209, 487, 1226), '19', 'dark')],
    8:  [('block', (688, 80, 942, 220),
          ['\u201cYou intended to harm me,', 'but God intended it', 'for good.\u201d'],
          dict(align='center', cx=815, ref_text='\u201cGod allowed everything', ref_w=220,
               baselines=[112, 139, 166], font='LiberationSerif-Italic', ink=110, dark=True,
               extra=[dict(text='Genesis 50:20', font='LiberationSerif-Regular',
                           ref_text='Genesis 37:28, 36', ref_w=127, baseline=212)])),
         ('line', (245, 31, 470, 60), 'CHAPTER 9', 'CHAPTER 11'), ('folio', (496, 1202, 514, 1219), '21', 'dark')],
    9:  [('block', (58, 255, 321, 315),
          ['Joseph worked in Potiphar\u2019s house.',
           'He was honest, skilled, and trusted',
           'with responsibility.'],
          dict(ref_text='He was honest, skilled, and trusted', ref_w=254, left=63,
               baselines=[269, 290, 311], font='LiberationSerif-Regular', ink=110, dark=True, stroke=1)),
         ('folio', (460, 1203, 481, 1219), '27', 'dark')],   # original label CHAPTER 12 is now correct
    10: [('line', (245, 38, 480, 69), 'CHAPTER 11', 'CHAPTER 15'), ('folio', (489, 1196, 509, 1212), '25', 'dark')],
    11: [('line', (425, 34, 665, 65), 'CHAPTER 13', 'CHAPTER 17'),
         ('folio', (474, 1197, 495, 1214), '29', 'dark')],
    12: [('folio', (470, 1201, 490, 1217), '31', 'dark')],
}


def text_mask(rgb, box, mode):
    """Mask of label glyph pixels inside box (working coords)."""
    x0, y0, x1, y1 = box
    roi = rgb[y0:y1, x0:x1].astype(np.int32)
    lum = roi.mean(axis=2)
    if mode == 'dark':
        bg = cv2.medianBlur(lum.astype(np.uint8), 2 * int(SCALE * 12) + 1).astype(np.int32)
        m = (bg - lum) > 45
    else:  # contrast either way (folio on glow or gold-on-dark badge)
        bg = cv2.medianBlur(lum.astype(np.uint8), 2 * int(SCALE * 10) + 1).astype(np.int32)
        m = np.abs(bg - lum) > 40
    m = m.astype(np.uint8)
    # drop tiny specks
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = np.zeros_like(m)
    for j in range(1, n):
        if stats[j, cv2.CC_STAT_AREA] >= SCALE * SCALE * 4:
            keep[lab == j] = 1
    full = np.zeros(rgb.shape[:2], np.uint8)
    full[y0:y1, x0:x1] = keep
    return full


def glyph_color(rgb, mask, mode):
    px = rgb[mask > 0].astype(np.float32)
    lum = px.mean(axis=1)
    if mode == 'dark':
        sel = px[lum <= np.percentile(lum, 35)]
    else:
        # choose the side that differs from surroundings: take extreme 35%
        sel = px[lum <= np.percentile(lum, 35)] if np.median(lum) < 128 else px[lum >= np.percentile(lum, 65)]
    return tuple(int(c) for c in sel.mean(axis=0))


def erase(rgb, mask, grow):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * grow + 1, 2 * grow + 1))
    m = cv2.dilate(mask * 255, k)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    out = cv2.inpaint(bgr, m, int(SCALE * 5), cv2.INPAINT_TELEA)
    out = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
    # restore a little grain so the patch does not look airbrushed
    rng = np.random.default_rng(7)
    noise = rng.normal(0, 3.0, out.shape)
    mm = (m > 0)[..., None]
    out = np.where(mm, np.clip(out + noise, 0, 255), out).astype(np.uint8)
    return out


def _runs(text, fb, fs):
    runs = []
    for wi, word in enumerate(text.split(' ')):
        if wi:
            runs.append((' ', fb))
        small_word = word.islower()
        for ci, c in enumerate(word):
            big = c.isdigit() or (ci == 0 and not small_word)
            runs.append((c.upper(), fb if big else fs))
    return runs


def _width(runs, track):
    return sum(f.getlength(c) + track for c, f in runs) - track


def draw_smallcaps(img, text, cx, baseline, orig_w, old_text, color, fonts):
    """Draw text in Cinzel Bold mimicking the art lettering: first letter of each word in
    full caps, remaining letters small caps, digits full height. The size is chosen so the
    replaced label (old_text) would occupy exactly the original label width, so the new
    label keeps the same scale as the artwork."""
    path = fonts + '/Cinzel-Bold.ttf'
    def fonts_at(sz):
        return ImageFont.truetype(path, sz), ImageFont.truetype(path, max(1, int(round(sz * 0.80))))
    fb, fs = fonts_at(100)
    w_old = _width(_runs(old_text, fb, fs), 0)
    size = max(8, int(round(100 * orig_w / w_old)))
    fb, fs = fonts_at(size)
    runs = _runs(text, fb, fs)
    total = _width(runs, 0)
    x = cx - total / 2
    d = ImageDraw.Draw(img)
    for c, f in runs:
        d.text((x, baseline), c, font=f, fill=color, anchor='ls')
        x += f.getlength(c)


def draw_plain(img, text, cx, baseline, orig_w, old_text, color, fonts):
    path = fonts + '/Literata-Bold.ttf'
    f = ImageFont.truetype(path, 100)
    size = max(8, int(round(100 * orig_w / f.getlength(old_text))))
    f = ImageFont.truetype(path, size)
    ImageDraw.Draw(img).text((cx, baseline), text, font=f, fill=color, anchor='ms')


def _wrap(text, f, max_w):
    lines, cur = [], ''
    for w in text.split(' '):
        t = (cur + ' ' + w).strip()
        if f.getlength(t) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines


def draw_block(img, lines, ref, color, fonts):
    """Re-set a short paragraph on the original baselines. The type size is chosen so the
    original reference line would have exactly its measured width (ref_w, scaled by `size_k`).
      wrap=True : `lines` is one string, re-wrapped to max_w (size shrinks if it needs more
                  lines than there are baselines)
      align     : 'left' (x = left) or 'center' (x = cx)
      extra     : further single lines (e.g. a Scripture reference) with their own font/size
    """
    def font_for(name, ref_text, ref_w):
        path = fonts + '/' + name + '.ttf'
        f = ImageFont.truetype(path, 100)
        return path, max(8, int(round(100 * ref_w * SCALE / f.getlength(ref_text))))
    path, size = font_for(ref.get('font', 'Literata-Regular'), ref['ref_text'], ref['ref_w'] * ref.get('size_k', 1))
    f = ImageFont.truetype(path, size)
    if ref.get('wrap'):
        while True:
            f = ImageFont.truetype(path, size)
            out = _wrap(lines, f, ref['max_w'] * SCALE)
            if len(out) <= len(ref['baselines']) or size < 10:
                break
            size -= 1
        lines = out
    d = ImageDraw.Draw(img)

    def put(text, font, b, align):
        y = (b - CROP['t']) * SCALE
        x, anchor = ((ref['cx'] - CROP['l']) * SCALE, 'ms') if align == 'center' else ((ref['left'] - CROP['l']) * SCALE, 'ls')
        d.text((x, y), text, font=font, fill=color, anchor=anchor,
               stroke_width=ref.get('stroke', 0), stroke_fill=color)
    for line, b in zip(lines, ref['baselines']):
        put(line, f, b, ref.get('align', 'left'))
    for ex in ref.get('extra', []):
        p2, s2 = font_for(ex['font'], ex['ref_text'], ex['ref_w'])
        put(ex['text'], ImageFont.truetype(p2, s2), ex['baseline'], ref.get('align', 'left'))


def draw_folio(img, text, cx, baseline, cap_h, color, fonts):
    f0 = ImageFont.truetype(fonts + '/Literata-Regular.ttf', 100)
    ch = f0.getbbox('8')[3] - f0.getbbox('8')[1]
    f = ImageFont.truetype(fonts + '/Literata-Regular.ttf', int(round(100 * cap_h / ch)))
    d = ImageDraw.Draw(img)
    d.text((cx, baseline), text, font=f, fill=color, anchor='ms')


def process(i):
    src = Image.open(f'{WORK}/img-{i:03d}.jpg').convert('RGB')
    W, H = src.size
    c = src.crop((CROP['l'], CROP['t'], W - CROP['r'], H - CROP['b']))
    nw, nh = int(round(c.width * SCALE)), int(round(c.height * SCALE))
    up = c.resize((nw, nh), Image.LANCZOS)
    up = up.filter(ImageFilter.UnsharpMask(radius=2, percent=35, threshold=2))
    rgb = np.array(up)
    log = []
    for spec in EDITS.get(i, []):
        kind, box, new = spec[:3]
        old_text = spec[3] if kind in ('line', 'plain', 'block') else None
        pad = 3
        bx = [int((box[0] - CROP['l'] - pad) * SCALE), int((box[1] - CROP['t'] - pad) * SCALE),
              int((box[2] - CROP['l'] + pad) * SCALE), int((box[3] - CROP['t'] + pad) * SCALE)]
        bx = [max(0, bx[0]), max(0, bx[1]), min(nw, bx[2]), min(nh, bx[3])]
        x0, y0, x1, y1 = bx
        roi = rgb[y0:y1, x0:x1].astype(np.int32)
        lum = roi.mean(axis=2)
        if kind in ('line', 'plain', 'block'):
            ink = lum < 150
            core = lum < 110
        else:
            pol = spec[3]
            bg = np.median(lum)
            ink = (bg - lum) > 30 if pol == 'dark' else (lum - bg) > 30
            core = (bg - lum) > 70 if pol == 'dark' else (lum - bg) > 70
        if not core.any():
            log.append((kind, new, 'NO GLYPHS'))
            continue
        if kind == 'block' and old_text.get('dark'):
            color = tuple(int(v) for v in np.median(roi[lum < 70] if (lum < 70).sum() > 50 else roi[core], axis=0))
        elif kind in ('plain', 'block'):
            color = tuple(int(v) for v in np.median(roi[core], axis=0))
        elif kind == 'line':
            # solid stroke colour of the original lettering (darkest ink pixels)
            color = tuple(int(v) for v in np.median(roi[lum < 70] if (lum < 70).sum() > 50 else roi[core], axis=0))
        else:
            color = tuple(int(v) for v in np.median(roi[core], axis=0))
        ys, xs = np.nonzero(core)
        gx0, gx1, gy0, gy1 = xs.min() + x0, xs.max() + x0, ys.min() + y0, ys.max() + y0
        m = np.zeros(rgb.shape[:2], np.uint8)
        m[y0:y1, x0:x1] = ink.astype(np.uint8)
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        m = cv2.dilate(m * 255, k)
        # never let the erase mask leave the padded band (protects the title line below)
        clip = np.zeros_like(m); clip[y0:y1, x0:x1] = 255
        m = cv2.bitwise_and(m, clip)
        if kind == 'block':
            # large text block: cover the letters AND their light sharpening halo, then fill
            # from the surrounding clean parchment only (normalized convolution) plus grain
            region = rgb[y0:y1, x0:x1].astype(np.float32)
            core_m = (lum < old_text.get('ink', 150)).astype(np.uint8)
            big = cv2.dilate(core_m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (23, 23))) > 0
            wgt = (~big).astype(np.float32)
            # normalized convolution; widen the sampling radius where nearby clean parchment
            # is scarce (dense text blocks), so the fill never collapses toward black
            fill = np.zeros_like(region); done = np.zeros(wgt.shape, bool)
            for sig in (14, 40, 100, 250):
                num = cv2.GaussianBlur(region * wgt[..., None], (0, 0), sig)
                den = cv2.GaussianBlur(wgt, (0, 0), sig)
                ok = (den > 0.2) & ~done
                fill[ok] = (num[ok] / den[ok][:, None])
                done |= ok
            if (~done).any():
                fill[~done] = np.median(region[wgt > 0], axis=0)
            rng2 = np.random.default_rng(42)
            fill += rng2.normal(0, 3.0, fill.shape)
            region[big] = fill[big]
            rgb = rgb.copy(); rgb[y0:y1, x0:x1] = np.clip(region, 0, 255).astype(np.uint8)
            m = np.zeros(rgb.shape[:2], np.uint8)   # nothing further to inpaint
        else:
            bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            bgr = cv2.inpaint(bgr, m, 7, cv2.INPAINT_TELEA)
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        rng = np.random.default_rng(i)
        noise = rng.normal(0, 2.5, rgb.shape)
        mm = (m > 0)[..., None]
        rgb = np.where(mm, np.clip(rgb + noise, 0, 255), rgb).astype(np.uint8)
        base = Image.fromarray(rgb)
        img = Image.new('RGBA', base.size, (0, 0, 0, 0))
        cx = (gx0 + gx1) / 2
        hgt = gy1 - gy0 + 1
        if kind == 'line':
            draw_smallcaps(img, new, cx, gy1 + 1, gx1 - gx0 + 1, old_text, color, FONTS)
        elif kind == 'block':
            draw_block(img, new, old_text, color, FONTS)
        elif kind == 'plain':
            draw_plain(img, new, cx, gy1 + 1, gx1 - gx0 + 1, old_text, color, FONTS)
        else:
            draw_folio(img, new, cx, gy1 + 1, hgt, color, FONTS)
        img = img.filter(ImageFilter.GaussianBlur(0.7))
        base.paste(img, (0, 0), img)
        rgb = np.array(base.convert('RGB'))
        log.append((kind, new, f'glyphs=({gx0},{gy0},{gx1},{gy1}) color={color}'))
    out = Image.fromarray(rgb)
    out.save(f'{OUT}/ill-{i:02d}.jpg', quality=93, subsampling=0, dpi=(300, 300))
    return (i, out.size, log)


if __name__ == '__main__':
    for i in range(13):
        print(process(i))
