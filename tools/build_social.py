"""Social-media promo kit for Joesiah & Malani: Noah's Bloodline.

Outputs (OUT dir):
  instagram_1..4.jpg   1080x1350 carousel (4:5 feed)
  facebook_post.jpg    1080x1350 single image
  tiktok_video.mp4     1080x1920, 30 fps, ~25 s, silent (add a sound in the TikTok app)
  tiktok_cover.jpg     1080x1920 still (TikTok cover frame / Reels / Stories)
"""
import subprocess
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ILL, COVER, FONTS, OUT = sys.argv[1:5]

NAVY = (20, 33, 61)
NAVY_DK = (11, 19, 38)
GOLD = (226, 186, 104)
GOLD_LT = (246, 224, 162)
CREAM = (251, 246, 234)
WHITE = (255, 255, 255)


def font(name, size):
    return ImageFont.truetype(f'{FONTS}/{name}.ttf', size)


def art(i):
    return Image.open(f'{ILL}/ill-{i:02d}.jpg').convert('RGB')


def fit(im, w=None, h=None):
    if w and h:
        k = min(w / im.width, h / im.height)
    elif w:
        k = w / im.width
    else:
        k = h / im.height
    return im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)


def cover_fill(im, W, H, blur=0, darken=0.0):
    k = max(W / im.width, H / im.height)
    r = im.resize((round(im.width * k) + 1, round(im.height * k) + 1), Image.LANCZOS)
    x, y = (r.width - W) // 2, (r.height - H) // 2
    r = r.crop((x, y, x + W, y + H))
    if blur:
        r = r.filter(ImageFilter.GaussianBlur(blur))
    if darken:
        r = Image.blend(r, Image.new('RGB', r.size, NAVY_DK), darken)
    return r


def shadow_text(img, xy, text, f, fill, anchor='ma', blur=6, alpha=200, spacing=10, align='center'):
    """Text with a soft dark shadow for legibility on artwork."""
    layer = Image.new('L', img.size, 0)
    ImageDraw.Draw(layer).multiline_text(xy, text, font=f, fill=alpha, anchor=anchor, spacing=spacing, align=align)
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    img.paste(Image.new('RGB', img.size, NAVY_DK), (0, 0), layer)
    ImageDraw.Draw(img).multiline_text(xy, text, font=f, fill=fill, anchor=anchor, spacing=spacing, align=align)


def framed(img, art_im, box, border=4):
    """Paste art inside a thin gold frame with a drop shadow."""
    x, y = box
    sh = Image.new('L', img.size, 0)
    ImageDraw.Draw(sh).rectangle((x + 10, y + 14, x + art_im.width + 10, y + art_im.height + 14), fill=170)
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    img.paste(Image.new('RGB', img.size, (0, 0, 0)), (0, 0), sh)
    ImageDraw.Draw(img).rectangle((x - border, y - border, x + art_im.width + border - 1, y + art_im.height + border - 1), fill=GOLD)
    img.paste(art_im, (x, y))


def rule(d, cx, y, w=260):
    d.line((cx - w / 2, y, cx - 10, y), fill=GOLD, width=2)
    d.line((cx + 10, y, cx + w / 2, y), fill=GOLD, width=2)
    d.polygon([(cx, y - 6), (cx + 6, y), (cx, y + 6), (cx - 6, y)], fill=GOLD)


def bg_navy(W, H, src=None):
    if src is not None:
        return cover_fill(src, W, H, blur=28, darken=0.72)
    return Image.new('RGB', (W, H), NAVY)


# ------------------------------------------------------------------ Instagram / Facebook (1080x1350)
W, H = 1080, 1350
cover = Image.open(COVER).convert('RGB')


def slide_cover(eyebrow, foot):
    img = bg_navy(W, H, cover)
    d = ImageDraw.Draw(img)
    shadow_text(img, (W / 2, 52), eyebrow, font('Cinzel-Bold', 40), GOLD_LT)
    rule(d, W / 2, 118, 320)
    c = fit(cover, h=1000)
    framed(img, c, ((W - c.width) // 2, 150))
    shadow_text(img, (W / 2, 1185), foot, font('Literata-Italic', 34), CREAM, spacing=12)
    return img


def slide_art(i, head, sub, crop_top=0.0):
    img = bg_navy(W, H, art(i))
    d = ImageDraw.Draw(img)
    shadow_text(img, (W / 2, 46), head, font('Cinzel-Bold', 46), GOLD_LT, spacing=8)
    hb = d.multiline_textbbox((W / 2, 46), head, font=font('Cinzel-Bold', 46), anchor='ma', spacing=8)
    y = hb[3] + 22
    rule(d, W / 2, y)
    shadow_text(img, (W / 2, y + 22), sub, font('Literata-Italic', 32), CREAM, spacing=10)
    sb = d.multiline_textbbox((W / 2, y + 22), sub, font=font('Literata-Italic', 32), anchor='ma', spacing=10)
    top = sb[3] + 30
    a = fit(art(i), h=H - top - 50)
    framed(img, a, ((W - a.width) // 2, top))
    return img


def slide_motto():
    img = bg_navy(W, H, art(11))
    d = ImageDraw.Draw(img)
    shadow_text(img, (W / 2, 120), 'THE BOOK’S PROMISE', font('Cinzel-Bold', 40), GOLD)
    rule(d, W / 2, 190, 320)
    lines = 'Know the Word.\nSeek the Truth.\nRemember who you are.\nWalk in the purpose\nGod gave you.'
    shadow_text(img, (W / 2, 260), lines, font('Literata-BoldItalic', 64), WHITE, spacing=26)
    rule(d, W / 2, 830, 320)
    shadow_text(img, (W / 2, 880), 'Joesiah & Malani', font('Cinzel-Black', 64), GOLD_LT)
    shadow_text(img, (W / 2, 965), 'NOAH’S BLOODLINE · BOOK 1', font('Cinzel-Bold', 40), CREAM)
    shadow_text(img, (W / 2, 1060), 'A faith-filled illustrated chapter book for ages 8–12\nby LeTisha C. Cleveland',
                font('Literata-Italic', 34), CREAM, spacing=14)
    shadow_text(img, (W / 2, 1220), 'Available on Amazon • Link in bio', font('Cinzel-Bold', 38), GOLD_LT)
    return img


ig = [
    slide_cover('NEW BOOK • AGES 8–12', 'Grandma, Joesiah & Malani take a journey\nfrom Noah’s Ark to Joseph in Egypt.'),
    slide_art(4, 'WHAT DOES THE BIBLE\nACTUALLY SAY?', 'Genesis 9:25 names Canaan—not Ham, and not African people.'),
    slide_art(5, 'AFRICA’S STORY DOESN’T\nBEGIN WITH SLAVERY', 'Kingdoms, scholars, builders, and trade—thousands of years of history.'),
    slide_motto(),
]
for n, im in enumerate(ig, 1):
    im.save(f'{OUT}/instagram_{n}.jpg', quality=92)

# Facebook: one image that tells the whole story (cover + 3 interior pages)
fb = bg_navy(W, H, cover)
d = ImageDraw.Draw(fb)
shadow_text(fb, (W / 2, 44), 'NOW AVAILABLE', font('Cinzel-Bold', 44), GOLD_LT)
rule(d, W / 2, 112, 320)
c = fit(cover, h=760)
framed(fb, c, ((W - c.width) // 2, 140))
thumbs = [fit(art(i), h=300) for i in (1, 2, 8)]
gap = 30
tw = sum(t.width for t in thumbs) + gap * 2
x = (W - tw) // 2
for t in thumbs:
    framed(fb, t, (x, 945)); x += t.width + gap
shadow_text(fb, (W / 2, 1275), 'Ages 8–12 • 13 full-color illustrations • Paperback on Amazon',
            font('Literata-Italic', 30), CREAM)
fb.save(f'{OUT}/facebook_post.jpg', quality=92)

# ------------------------------------------------------------------ TikTok (1080x1920)
TW, TH, FPS = 1080, 1920, 30
SCENES = [  # (illustration index or 'cover', caption, seconds)
    (4, 'What does the Bible\nACTUALLY say\nabout Ham?', 4.0),
    (0, 'Meet Grandma,\nJoesiah & Malani', 3.5),
    (1, 'From Noah’s Ark…', 3.0),
    (5, '…to the great kingdoms\nof Africa…', 3.5),
    (8, '…to Joseph in Egypt.', 3.0),
    (11, 'I WILL READ\nBEFORE I REPEAT.', 3.5),
    ('cover', 'Joesiah & Malani\nNOAH’S BLOODLINE', 5.0),
]
XF = 0.5  # crossfade seconds


def scene_base(src, caption, last=False):
    """Static layers: blurred background, caption, and the art (returned separately for zoom)."""
    im = cover if src == 'cover' else art(src)
    bg = cover_fill(im, TW, TH, blur=30, darken=0.7)
    top = Image.new('RGBA', (TW, TH), (0, 0, 0, 0))
    f = font('Cinzel-Black', 76 if not last else 72)
    # caption sits in the upper-middle: clear of TikTok's top tabs and bottom caption/UI
    cap_layer = Image.new('RGB', (TW, TH))
    shadow_text(cap_layer, (TW / 2 - 30, 250), caption, f, GOLD_LT, blur=8, alpha=230, spacing=14)
    m = Image.new('L', (TW, TH), 0)
    ImageDraw.Draw(m).multiline_text((TW / 2 - 30, 250), caption, font=f, fill=255, anchor='ma', spacing=14, align='center')
    m = m.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(10))
    top.paste(cap_layer, (0, 0), m)
    cap_box = ImageDraw.Draw(Image.new('L', (TW, TH))).multiline_textbbox((TW / 2 - 30, 250), caption, font=f, anchor='ma', spacing=14, align='center')
    if last:
        dd = ImageDraw.Draw(top)
        for k, (txt, fn, sz, col) in enumerate([
                ('BOOK 1 • AGES 8–12', 'Cinzel-Bold', 44, CREAM),
                ('by LeTisha C. Cleveland', 'Literata-Italic', 40, CREAM),
                ('Available on Amazon', 'Cinzel-Bold', 48, GOLD_LT)]):
            y = 1440 + k * 72
            lay = Image.new('RGB', (TW, TH)); shadow_text(lay, (TW / 2 - 30, y), txt, font(fn, sz), col)
            mm = Image.new('L', (TW, TH), 0)
            ImageDraw.Draw(mm).text((TW / 2 - 30, y), txt, font=font(fn, sz), fill=255, anchor='ma')
            mm = mm.filter(ImageFilter.MaxFilter(13)).filter(ImageFilter.GaussianBlur(8))
            top.paste(lay, (0, 0), mm)
    art_top = cap_box[3] + 50
    art_h = (1400 if not last else 1420 - art_top - 20) if not last else 1420 - art_top - 20
    art_h = min(art_h, TH - art_top - 60)
    a = fit(im, h=art_h)
    if a.width > 920:
        a = fit(im, w=920)
    return bg, a, art_top, top


def frames():
    bases = [scene_base(s, c, last=(k == len(SCENES) - 1)) for k, (s, c, _) in enumerate(SCENES)]
    rendered = []
    for k, ((s, c, dur), (bg, a, at, top)) in enumerate(zip(SCENES, bases)):
        n = int(round(dur * FPS))
        seq = []
        for t in range(n):
            z = 1.0 + 0.06 * t / n                            # slow push-in on the art
            aw, ah = round(a.width * z), round(a.height * z)
            az = a.resize((aw, ah), Image.BILINEAR)
            fr = bg.copy()
            x = (TW - 60 - aw) // 2
            y = at - (ah - a.height) // 2
            ImageDraw.Draw(fr).rectangle((x - 4, y - 4, x + aw + 3, y + ah + 3), fill=GOLD)
            fr.paste(az, (x, y))
            fr.paste(top, (0, 0), top)
            seq.append(np.asarray(fr))
        rendered.append(seq)
    # concatenate with crossfades
    xf = int(XF * FPS)
    out = list(rendered[0])
    for seq in rendered[1:]:
        tail = out[-xf:]
        out = out[:-xf]
        for j in range(xf):
            a_ = j / xf
            out.append((tail[j] * (1 - a_) + seq[j] * a_).astype(np.uint8))
        out.extend(seq[xf:])
    # fade in/out
    for j in range(10):
        out[j] = (out[j] * (j / 10)).astype(np.uint8)
        out[-1 - j] = (out[-1 - j] * (j / 10)).astype(np.uint8)
    return out


fr = frames()
Image.fromarray(fr[-int(2.5 * FPS)]).save(f'{OUT}/tiktok_cover.jpg', quality=92)
p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                      '-s', f'{TW}x{TH}', '-r', str(FPS), '-i', '-',
                      '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
                      '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '20',
                      '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-movflags', '+faststart',
                      '-c:a', 'aac', '-b:a', '128k', f'{OUT}/tiktok_video.mp4'], stdin=subprocess.PIPE)
for f_ in fr:
    p.stdin.write(f_.tobytes())
p.stdin.close(); p.wait()
print('frames', len(fr), 'seconds', round(len(fr) / FPS, 1))
