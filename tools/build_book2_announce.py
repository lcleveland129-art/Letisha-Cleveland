"""'Book 2 is on the way' announcement graphics (feed 1080x1350 and story 1080x1920)."""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ART, COVER1, FONTS, OUT = sys.argv[1:5]
NAVY_DK = (11, 19, 38)
GOLD = (226, 186, 104)
GOLD_LT = (246, 224, 162)
CREAM = (251, 246, 234)
WHITE = (255, 255, 255)


def font(n, s):
    return ImageFont.truetype(f'{FONTS}/{n}.ttf', s)


def fit(im, w=None, h=None):
    k = min(w / im.width, h / im.height) if (w and h) else (w / im.width if w else h / im.height)
    return im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)


def cover_fill(im, W, H, blur, darken):
    k = max(W / im.width, H / im.height)
    r = im.resize((round(im.width * k) + 1, round(im.height * k) + 1), Image.LANCZOS)
    x, y = (r.width - W) // 2, (r.height - H) // 2
    r = r.crop((x, y, x + W, y + H)).filter(ImageFilter.GaussianBlur(blur))
    return Image.blend(r, Image.new('RGB', r.size, NAVY_DK), darken)


def stext(img, xy, text, f, fill, anchor='ma', spacing=10):
    lay = Image.new('L', img.size, 0)
    ImageDraw.Draw(lay).multiline_text(xy, text, font=f, fill=210, anchor=anchor, spacing=spacing, align='center')
    lay = lay.filter(ImageFilter.GaussianBlur(7))
    img.paste(Image.new('RGB', img.size, NAVY_DK), (0, 0), lay)
    d = ImageDraw.Draw(img)
    d.multiline_text(xy, text, font=f, fill=fill, anchor=anchor, spacing=spacing, align='center')
    return d.multiline_textbbox(xy, text, font=f, anchor=anchor, spacing=spacing, align='center')


def framed(img, a, x, y, b=4):
    sh = Image.new('L', img.size, 0)
    ImageDraw.Draw(sh).rectangle((x + 10, y + 14, x + a.width + 10, y + a.height + 14), fill=170)
    img.paste(Image.new('RGB', img.size, (0, 0, 0)), (0, 0), sh.filter(ImageFilter.GaussianBlur(14)))
    ImageDraw.Draw(img).rectangle((x - b, y - b, x + a.width + b - 1, y + a.height + b - 1), fill=GOLD)
    img.paste(a, (x, y))


def rule(d, cx, y, w=300):
    d.line((cx - w / 2, y, cx - 10, y), fill=GOLD, width=2)
    d.line((cx + 10, y, cx + w / 2, y), fill=GOLD, width=2)
    d.polygon([(cx, y - 6), (cx + 6, y), (cx, y + 6), (cx - 6, y)], fill=GOLD)


art = Image.open(ART).convert('RGB')
art = art.crop((0, 0, art.width, art.height - 120))   # drop Book 1's page number at the bottom
c1 = Image.open(COVER1).convert('RGB')


def make(W, H, name, art_h, sizes):
    img = cover_fill(art, W, H, 28, 0.72)
    d = ImageDraw.Draw(img)
    cx = W / 2
    y = sizes['top']
    bb = stext(img, (cx, y), 'BOOK 2', font('Cinzel-Bold', sizes['eyebrow']), GOLD)
    bb = stext(img, (cx, bb[3] + 8), 'IS ON THE WAY!', font('Cinzel-Black', sizes['head']), GOLD_LT)
    rule(d, cx, bb[3] + 26)
    a = fit(art, h=art_h)
    ay = bb[3] + 52
    framed(img, a, int(cx - a.width / 2), ay)
    y = ay + a.height + 30
    bb = stext(img, (cx, y), 'The story is written.\nThe illustrations are coming next!',
               font('Literata-Italic', sizes['sub']), CREAM, spacing=10)
    # Book 1 strip
    y = bb[3] + sizes['gap']
    th = fit(c1, h=sizes['thumb'])
    lines = 'Start the journey with Book 1:\nNOAH’S BLOODLINE\nAvailable now on Amazon'
    f1 = font('Literata-Italic', sizes['strip'])
    f2 = font('Cinzel-Bold', sizes['strip'] + 4)
    tw = max(d.textlength('Start the journey with Book 1:', font=f1), d.textlength('NOAH’S BLOODLINE', font=f2),
             d.textlength('Available now on Amazon', font=f1))
    total = th.width + 30 + tw
    x0 = int(cx - total / 2)
    framed(img, th, x0, y, b=3)
    tx = x0 + th.width + 30
    ty = y + (th.height - (sizes['strip'] * 3 + 34)) / 2
    stext(img, (tx, ty), 'Start the journey with Book 1:', f1, CREAM, anchor='la')
    stext(img, (tx, ty + sizes['strip'] + 14), 'NOAH’S BLOODLINE', f2, GOLD_LT, anchor='la')
    stext(img, (tx, ty + 2 * sizes['strip'] + 30), 'Available now on Amazon', f1, CREAM, anchor='la')
    img.save(f'{OUT}/{name}', quality=92)


make(1080, 1350, 'book2_announcement_post.jpg', 760,
     dict(top=36, eyebrow=40, head=64, sub=32, gap=26, thumb=150, strip=28))
make(1080, 1920, 'book2_announcement_story.jpg', 1060,
     dict(top=170, eyebrow=48, head=76, sub=38, gap=40, thumb=200, strip=34))
print('ok')
