#!/usr/bin/env python3
"""Genere les icones PWA : un gros « + » sur une tuile jaune, sur un ciel
violet etoile (le look par defaut du moteur pwa-engine).

Sorties (a la racine du projet) :
    icons/icon-192.png
    icons/icon-512.png
    icons/icon-512-maskable.png   (motif reduit + marge de securite)
    icons/apple-touch-icon.png    (180x180, opaque)
    favicon.ico                   (16 / 32 / 48)

Depend de Pillow :  python3 -m pip install pillow

--- Personnaliser ---
Change les couleurs et les proportions dans la section « reglages » ci-dessous,
puis relance le script. Le « + » est dessine avec des primitives ImageDraw
(pas de police necessaire) : voir draw_glyph().
"""
import os

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except ImportError:
    raise SystemExit("Pillow requis :  python3 -m pip install pillow")

try:
    LANCZOS = Image.Resampling.LANCZOS
except AttributeError:                       # Pillow < 9.1
    LANCZOS = Image.LANCZOS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ICONS = os.path.join(ROOT, "icons")

# ------------------------------------------------------------------ reglages
S = 2048                         # resolution de travail (reduite ensuite)

BASE_TOP = (28, 13, 47)          # #1C0D2F  haut du fond
BASE_LOW = (18, 7, 31)           # #12071F  bas du fond
GLOW = (124, 92, 255)            # halo violet
INK = (24, 12, 40)               # couleur du glyphe
Y_TOP = (255, 233, 110)          # haut de la tuile
Y_BOT = (244, 196, 0)            # bas de la tuile
Y_RIM = (206, 150, 0)            # lisere

TILE = 0.72                      # cote de la tuile, fraction de l'icone
TILE_RADIUS = 0.34               # arrondi des coins (fraction du cote)
PLUS_SPAN = 0.58                 # envergure du « + », fraction du cote de la tuile
PLUS_THICK = 0.16                # epaisseur des barres, fraction du cote de la tuile

STARS = [(0.16, 0.14, 7, 90), (0.83, 0.11, 10, 120), (0.90, 0.44, 6, 80),
         (0.10, 0.52, 8, 95), (0.22, 0.83, 6, 80), (0.78, 0.85, 9, 110),
         (0.50, 0.07, 5, 70), (0.93, 0.70, 5, 70), (0.07, 0.30, 5, 65)]


# ------------------------------------------------------------------ helpers
def vgrad(w, h, top, bot):
    base = Image.new("RGB", (w, h), top)
    grad = Image.new("L", (1, h))
    for y in range(h):
        grad.putpixel((0, y), int(255 * y / max(1, h - 1)))
    return Image.composite(Image.new("RGB", (w, h), bot), base, grad.resize((w, h)))


def background(scale):
    img = vgrad(S, S, BASE_TOP, BASE_LOW).convert("RGBA")
    g = Image.radial_gradient("L").resize((int(S * 2.2), int(S * 2.2)), LANCZOS)
    glow_a = Image.new("L", (S, S), 0)
    glow_a.paste(g, (int(S * 0.5 - g.width / 2), int(S * 0.26 - g.height / 2)))
    glow_a = glow_a.point(lambda v: int(v * 0.50))
    img = Image.composite(Image.new("RGBA", (S, S), GLOW + (255,)), img, glow_a)

    d = ImageDraw.Draw(img)
    cx = cy = S / 2
    for fx, fy, rr, a in STARS:
        x = cx + (fx * S - cx) * scale
        y = cy + (fy * S - cy) * scale
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(255, 255, 255, a))
    return img


def draw_tile(img, scale):
    cx = cy = S / 2
    tw = S * TILE * scale
    x0, y0 = cx - tw / 2, cy - tw / 2
    x1, y1 = x0 + tw, y0 + tw
    rad = tw * TILE_RADIUS

    shape = Image.new("L", (S, S), 0)
    ImageDraw.Draw(shape).rounded_rectangle([x0, y0, x1, y1], radius=rad, fill=255)

    sh = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    sh.paste((0, 0, 0, 140), (0, int(S * 0.015)), shape)
    sh = sh.filter(ImageFilter.GaussianBlur(int(S * 0.03)))
    img.alpha_composite(sh)

    grad = vgrad(int(tw), int(tw), Y_TOP, Y_BOT).convert("RGBA")
    tile_mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(tile_mask).rounded_rectangle([x0, y0, x1, y1], radius=rad, fill=255)
    canvas = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    canvas.paste(grad, (int(x0), int(y0)))
    img.paste(canvas, (0, 0), tile_mask)

    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y0, x1, y1], radius=rad, outline=Y_RIM + (170,), width=int(S * 0.006))
    # reflet doux en haut de la tuile
    gloss = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(gloss).rounded_rectangle(
        [x0 + tw * 0.10, y0 + tw * 0.08, x1 - tw * 0.10, y0 + tw * 0.30],
        radius=rad * 0.6, fill=(255, 255, 255, 32))
    img.alpha_composite(gloss.filter(ImageFilter.GaussianBlur(int(S * 0.006))))
    return (x0, y0, x1, y1)


def draw_glyph(img, box):
    x0, y0, x1, y1 = box
    tw = x1 - x0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    half = tw * PLUS_SPAN / 2
    t = tw * PLUS_THICK / 2
    r = t * 0.55
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([cx - half, cy - t, cx + half, cy + t], radius=r, fill=INK + (255,))
    d.rounded_rectangle([cx - t, cy - half, cx + t, cy + half], radius=r, fill=INK + (255,))


def compose(size, maskable=False, opaque=False):
    scale = 0.68 if maskable else 1.0
    img = background(scale)
    box = draw_tile(img, scale)
    draw_glyph(img, box)

    if not maskable and not opaque:
        mask = Image.new("L", (S, S), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=255)
        img.putalpha(Image.composite(img.getchannel("A"), Image.new("L", (S, S), 0), mask))

    img = img.resize((size, size), LANCZOS)
    if opaque:
        out = Image.new("RGB", img.size, BASE_LOW)
        out.paste(img, (0, 0), img)
        return out
    return img


def main():
    os.makedirs(ICONS, exist_ok=True)
    compose(192).save(os.path.join(ICONS, "icon-192.png"))
    compose(512).save(os.path.join(ICONS, "icon-512.png"))
    compose(512, maskable=True).save(os.path.join(ICONS, "icon-512-maskable.png"))
    compose(180, opaque=True).save(os.path.join(ICONS, "apple-touch-icon.png"))
    compose(64, opaque=True).save(os.path.join(ROOT, "favicon.ico"),
                                  sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print("Icones regenerees dans", ICONS, "+ favicon.ico")


if __name__ == "__main__":
    main()
