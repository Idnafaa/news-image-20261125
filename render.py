#!/usr/bin/env python3
"""Front page for Wednesday 25 November 2026, drawn as a 1024x1024 PNG.

Clean build for the make.fun news-image-20261125 bounty. The 27 stories
on the page were all checked against reporting dated 24-25 November 2026
(full list with sources: research-notes.md). Every illustration is
hand-drawn vector art with Pillow - no photographs, no network access, no
clock - so the file is identical on every run.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
NAVY = (16, 42, 67)
RED = (178, 34, 34)
TEAL = (14, 110, 110)
GREY = (90, 88, 82)
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def load(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


class Fonts:
    serif = staticmethod(lambda s: load("DejaVuSerif-Bold.ttf", s))
    serif_text = staticmethod(lambda s: load("DejaVuSerif.ttf", s))
    sans = staticmethod(lambda s: load("DejaVuSans-Bold.ttf", s))
    sans_text = staticmethod(lambda s: load("DejaVuSans.ttf", s))


def wrap(draw, text, font, width):
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


class Page:
    def __init__(self):
        self.image = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
        self.d = ImageDraw.Draw(self.image)
        self.margin = 28

    def text(self, x, y, s, font, fill=INK):
        self.d.text((x, y), s, font=font, fill=fill)

    def rule(self, y, weight=2, fill=INK, x0=None, x1=None):
        m = self.margin
        self.d.line([(x0 or m, y), (x1 or PAGE_W - m, y)], fill=fill, width=weight)

    def para(self, x, y, s, font, width, fill=INK, leading=None):
        step = leading if leading is not None else int(font.size * 1.3)
        for line in wrap(self.d, s, font, width):
            self.d.text((x, y), line, font=font, fill=fill)
            y += step
        return y

    def paste_art(self, art, x, y):
        self.image.paste(art, (x, y))


# ---------------------------------------------------------------- artwork
def burst(d, cx, cy, r, colours):
    """A jagged starburst: outer ring, mid ring, bright core."""
    for radius, colour in zip((r, int(r * 0.65), int(r * 0.35)), colours):
        pts = []
        for k in range(12):
            stretch = 1.25 if k % 2 == 0 else 0.8
            ang = k * math.pi / 6
            pts.append((cx + radius * stretch * math.cos(ang),
                        cy + radius * stretch * math.sin(ang)))
        d.polygon(pts, fill=colour)


def art_sea(w, h):
    img = Image.new("RGB", (w, h), (23, 52, 84))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, int(h * 0.42)], fill=(216, 134, 62))
    d.ellipse([w - 78, 12, w - 18, 72], fill=(245, 214, 130))
    for i in range(5):
        d.line([(0, int(h * 0.42) + i * 3), (w, int(h * 0.42) + i * 3)],
               fill=(23, 52, 84), width=1)
    d.polygon([(24, h - 96), (142, h - 96), (128, h - 66), (38, h - 66)],
              fill=(12, 26, 44))
    d.rectangle([64, h - 122, 102, h - 96], fill=(12, 26, 44))
    d.line([(82, h - 140), (82, h - 122)], fill=(12, 26, 44), width=3)
    d.polygon([(w - 190, h - 88), (w - 40, h - 88), (w - 58, h - 54),
               (w - 172, h - 54)], fill=(8, 18, 32))
    d.rectangle([w - 138, h - 118, w - 92, h - 88], fill=(8, 18, 32))
    for j, r in enumerate((15, 11, 8)):
        d.ellipse([w - 128 + j * 6, h - 146 - j * 12,
                   w - 128 + j * 6 + 2 * r, h - 146 - j * 12 + 2 * r],
                  fill=(96, 96, 96))
    burst(d, w // 2 - 6, h - 128, 34,
          [(255, 176, 32), (255, 110, 30), (255, 240, 180)])
    dx, dy = w // 2 + 52, 26
    d.ellipse([dx - 8, dy - 5, dx + 8, dy + 5], fill=(20, 20, 20))
    d.line([(dx - 26, dy), (dx - 8, dy)], fill=(20, 20, 20), width=3)
    d.line([(dx + 8, dy), (dx + 26, dy)], fill=(20, 20, 20), width=3)
    d.ellipse([dx - 32, dy - 3, dx - 20, dy + 3], fill=(60, 60, 60))
    d.ellipse([dx + 20, dy - 3, dx + 32, dy + 3], fill=(60, 60, 60))
    for wy in (h - 34, h - 18):
        for wx in range(8, w - 8, 46):
            d.arc([wx, wy, wx + 34, wy + 14], 180, 360, fill=(140, 180, 210), width=2)
    return img


def art_climate(w, h):
    img = Image.new("RGB", (w, h), (226, 232, 222))
    d = ImageDraw.Draw(img)
    cx, cy, r = w // 2, h // 2 + 8, 52
    d.ellipse([cx - 26, 8, cx + 26, 60], fill=(240, 180, 60))
    for k in range(8):
        ang = k * math.pi / 4
        d.line([(cx + 34 * math.cos(ang), 34 + 34 * math.sin(ang)),
                (cx + 46 * math.cos(ang), 34 + 46 * math.sin(ang))],
               fill=(240, 180, 60), width=3)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 110, 160))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=3)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(120, 200, 130), width=10)
    d.arc([cx - r, cy - r, cx + r, cy + r], 20, 110, fill=(120, 200, 130), width=8)
    d.line([(cx - 8, cy - r + 6), (cx + 6, cy - 18), (cx - 4, cy + 4),
            (cx + 10, cy + 26), (cx - 2, cy + r - 8)], fill=INK, width=4)
    d.line([(cx + 6, cy - 18), (cx + 26, cy - 6)], fill=INK, width=3)
    return img


def art_chip(w, h):
    img = Image.new("RGB", (w, h), (16, 42, 36))
    d = ImageDraw.Draw(img)
    for gy in range(12, h, 22):
        d.line([(8, gy), (w - 8, gy)], fill=(28, 74, 62), width=1)
    for gx in range(12, w, 22):
        d.line([(gx, 8), (gx, h - 8)], fill=(28, 74, 62), width=1)
    cx, cy = w // 2 - 18, h // 2 + 4
    d.rectangle([cx - 46, cy - 46, cx + 46, cy + 46], fill=(34, 160, 90),
                outline=(220, 240, 220), width=3)
    d.rectangle([cx - 26, cy - 26, cx + 26, cy + 26], fill=(16, 90, 50))
    d.text((cx - 15, cy - 11), "AI", font=Fonts.sans(22), fill=(220, 240, 220))
    for px in (-46, -23, 0, 23, 46):
        d.line([(cx + px, cy - 46), (cx + px, cy - 58)], fill=(200, 220, 200), width=3)
        d.line([(cx + px, cy + 46), (cx + px, cy + 58)], fill=(200, 220, 200), width=3)
    ax, ay = w - 66, h - 30
    d.line([(ax, ay), (ax + 34, ay - 40), (ax + 58, ay - 58)],
           fill=(255, 200, 60), width=5)
    d.polygon([(ax + 58, ay - 58), (ax + 40, ay - 58), (ax + 58, ay - 40)],
              fill=(255, 200, 60))
    return img


def art_tower(w, h):
    img = Image.new("RGB", (w, h), (24, 28, 52))
    d = ImageDraw.Draw(img)
    rnd = random.Random(20261125)
    for _ in range(40):
        d.point((rnd.randint(4, w - 4), rnd.randint(4, int(h * 0.5))),
                fill=(255, 255, 200))
    for fx, fh in ((0.06, 0.42), (0.24, 0.58), (0.66, 0.5), (0.84, 0.38)):
        tx, tw, th = int(w * fx), int(w * 0.13), int(h * fh)
        d.rectangle([tx, h - th, tx + tw, h], fill=(52, 60, 96))
        for wy in range(h - th + 10, h - 8, 14):
            for wx in range(tx + 5, tx + tw - 5, 11):
                if rnd.random() < 0.5:
                    d.rectangle([wx, wy, wx + 5, wy + 6], fill=(255, 214, 90))
    tx, tw = int(w * 0.44), int(w * 0.13)
    th = int(h * 0.72)
    d.rectangle([tx, h - th, tx + tw, h], fill=(52, 60, 96))
    d.rectangle([tx - 3, h - th - 8, tx + tw + 3, h - th], fill=(52, 60, 96))
    burst(d, tx + tw // 2, h - int(h * 0.52), 26,
          [(255, 176, 32), (255, 110, 30), (255, 240, 180)])
    return img


def art_space(w, h):
    img = Image.new("RGB", (w, h), (6, 8, 18))
    d = ImageDraw.Draw(img)
    rnd = random.Random(1125)
    for _ in range(60):
        d.point((rnd.randint(3, w - 3), rnd.randint(3, h - 3)), fill=(230, 230, 255))
    cx, cy = w // 2, h // 2 + 22
    d.ellipse([cx - 62, cy - 40, cx + 62, cy + 40], fill=(120, 110, 100))
    d.ellipse([cx - 62, cy - 40, cx + 62, cy + 40], outline=(200, 190, 175), width=2)
    for ox, oy, o in ((-30, -12, 9), (14, 8, 12), (34, -16, 6), (-6, 18, 7)):
        d.ellipse([cx + ox - o, cy + oy - o, cx + ox + o, cy + oy + o],
                  fill=(92, 84, 76))
    d.polygon([(cx - 22, cy - 40), (cx - 4, cy - 40), (cx - 20, cy + 40),
               (cx - 38, cy + 40)], fill=(30, 28, 26))
    mx, my = cx + 8, 26
    d.ellipse([mx - 20, my - 15, mx + 20, my + 15], fill=(150, 142, 130))
    d.ellipse([mx - 20, my - 15, mx + 20, my + 15], outline=(210, 200, 185), width=2)
    d.line([(mx - 14, my + 15), (cx - 20, cy - 40)], fill=(90, 90, 110), width=1)
    return img


def art_cricket(w, h):
    img = Image.new("RGB", (w, h), (34, 120, 60))
    d = ImageDraw.Draw(img)
    d.ellipse([-60, h - 46, w + 60, h + 90], fill=(46, 140, 72))
    for sx in (w - 96, w - 80, w - 64):
        d.rectangle([sx, h - 78, sx + 8, h - 30], fill=(240, 220, 150))
    d.polygon([(66, 34), (92, 40), (132, 112), (110, 124)], fill=(222, 184, 120),
              outline=(120, 80, 20))
    d.line([(62, 30), (92, 40)], fill=(90, 60, 20), width=6)
    d.ellipse([w - 66, 18, w - 42, 42], fill=(178, 34, 34))
    d.arc([w - 66, 18, w - 42, 42], 300, 60, fill=(255, 255, 255), width=2)
    for k in range(3):
        d.line([(150 + k * 16, 66 + k * 6), (190 + k * 16, 52 + k * 6)],
               fill=(255, 255, 255), width=2)
    d.text((14, h - 26), "85 off 32", font=Fonts.sans(15), fill=(255, 255, 255))
    return img


def art_turkey(w, h):
    img = Image.new("RGB", (w, h), (196, 208, 226))
    d = ImageDraw.Draw(img)
    d.rectangle([0, h - 34, w, h], fill=(120, 140, 110))
    for cx in range(18, w - 10, 44):
        d.rectangle([cx, 18, cx + 14, h - 34], fill=(250, 248, 240))
        d.rectangle([cx - 3, 12, cx + 17, 18], fill=(250, 248, 240))
    d.rectangle([0, 6, w, 14], fill=(250, 248, 240))
    for tx in (96, 196):
        d.ellipse([tx, h - 58, tx + 44, h - 22], fill=(120, 74, 40))
        d.ellipse([tx + 30, h - 74, tx + 50, h - 52], fill=(140, 90, 50))
        d.polygon([(tx + 40, h - 74), (tx + 52, h - 66), (tx + 40, h - 62)],
                  fill=(240, 160, 40))
        d.ellipse([tx + 42, h - 70, tx + 46, h - 66], fill=INK)
        for fx in range(5):
            ang = math.pi * (0.15 + 0.175 * fx)
            d.line([(tx + 8, h - 40),
                    (tx + 8 - 26 * math.cos(ang), h - 40 - 26 * math.sin(ang))],
                   fill=(90, 50, 30), width=4)
    return img


ART = {"sea": art_sea, "climate": art_climate, "chip": art_chip,
       "tower": art_tower, "space": art_space, "cricket": art_cricket,
       "turkey": art_turkey}

# ---------------------------------------------------------------- content
LEAD = {
    "tag": "WAR AT SEA",
    "head": "Ukraine strikes Russian ships in two seas",
    "deck": ("President Zelenskyy confirms Kyiv's drones hit a Russian cargo "
             "ship in the Gulf of Finland \u2014 and sank a warship off "
             "Benghazi, Libya. Moscow calls the attacks \u201cterrorism\u201d; "
             "Putin vows retaliation."),
    "note": ("The widest reach yet for Kyiv's sea-drone campaign: one strike "
             "in the Baltic, another 3,000 km away in the Mediterranean."),
}

CARDS = [
    ("CLIMATE", "COP31 collapses with no deal",
     "The Antalya summit ends without agreement \u2014 the first failed "
     "climate summit since Copenhagen 2009 \u2014 after the EU rejects a "
     "text with no fossil-fuel phaseout.", "climate"),
    ("TECH", "Huang is back \u2014 and so is the rally",
     "Nvidia reinstates Jensen Huang as chief executive 11 days after he "
     "quit; shares jump 31.5% on Monday, adding about $1 trillion, then "
     "fall 7% on Tuesday.", "chip"),
    ("MIDDLE EAST", "Riyadh tower hit a second time",
     "Houthi fighters strike Riyadh's tallest tower again in a week, "
     "wounding 11, as their forces advance to within 60 km of Aden.",
     "tower"),
    ("SPACE", "An asteroid's eclipse, up close",
     "ESA's Hera probe photographs little Dimorphos casting its shadow on "
     "Didymos \u2014 and today reveals the first close-ups of the crater "
     "left by NASA's DART impact.", "space"),
    ("SPORT", "Donald's 85 levels the series",
     "Aneurin Donald smashes 85 off 32 balls as England chase 185 in 13.1 "
     "overs to beat Australia by eight wickets in Carrara. Series 1\u20131.",
     "cricket"),
    ("AMERICA", "Turkeys pardoned, honours given",
     "On the eve of Thanksgiving, Trump spares turkeys Freedom and Feathers "
     "at the White House and awards Rudy Giuliani the Medal of Freedom.",
     "turkey"),
]

BRIEFS = [
    ("JUSTICE", "Huawei convicted in Brooklyn on 10 of 12 counts \u2014 trade-secret theft and bank fraud; acquitted of racketeering."),
    ("MARKETS", "US consumer confidence hits its highest level in nearly two years after the midterm elections."),
    ("TRADE", "Trump administration set to unveil new tariffs after a probe into excess factory capacity."),
    ("POLITICS", "Senate panel investigates JD Vance's ties to a Venezuelan oil deal awarded to Vitol."),
    ("COURTS", "Fort Hood gunman Nidal Hasan seeks a stay of execution set for next week."),
    ("FRANCE", "Sarkozy and his wife Carla Bruni are ordered to stand trial in a corruption case."),
    ("EUROPE", "NATO plans early-warning aircraft for Poland after missiles landed in the country."),
    ("ENERGY", "Iran says three oil tankers were hit by naval mines in the Strait of Hormuz."),
    ("GAZA", "UN warns of a deepening humanitarian crisis; the death toll reaches 74,746, WAFA says."),
    ("WAR", "Analysis finds more than 700,000 Russian soldiers have been killed in the Ukraine war."),
    ("MEDIA", "RFE/RL returns to shortwave radio with lessons for Afghan girls barred from school."),
    ("IRAN", "Winter gas shortages loom as war damage deepens the energy crisis; power rationing begins."),
    ("INDIA", "BJP and the Akali Dal reunite for Punjab polls after a six-year split."),
    ("NEPAL", "PM Balendra Shah ends a state visit to India; Delhi pledges Rs 15,000 crore in aid."),
    ("CRICKET", "Vaibhav Sooryavanshi, 15, smashes the fastest List A double hundred: 204 off 53 balls."),
    ("MARKETS", "Anthropic shares slide below their $83 IPO price; Dell's sales more than double on AI servers."),
    ("USA", "Mayor-elect Mamdani plans to close Rikers Island and replace it with borough jails by 2032."),
    ("TRAVEL", "A radar outage delays flights at Chicago O'Hare, the FAA says."),
    ("SPORT", "The United States will host the Copa America for a second straight tournament in 2028."),
    ("TODAY", "25 November is the International Day for the Elimination of Violence against Women."),
]


def build():
    p = Page()
    m = p.margin
    # masthead
    p.rule(22, 4)
    p.text(m, 30, "THE WORLD IN ONE DAY", Fonts.serif(56))
    p.text(m, 96, "WEDNESDAY, 25 NOVEMBER 2026", Fonts.sans(15))
    tagline = "ONE IMAGE  \u00b7  THE DAY'S NEWS"
    p.text(PAGE_W - m - p.d.textlength(tagline, font=Fonts.sans(15)), 96,
           tagline, Fonts.sans(15), RED)
    p.rule(122, 2)
    # ticker
    p.d.rectangle([m, 130, PAGE_W - m, 156], fill=NAVY)
    p.text(m + 10, 136,
           "UKRAINE HITS RUSSIAN SHIPS  \u2022  COP31 COLLAPSES  \u2022  HUANG "
           "BACK AT NVIDIA  \u2022  HOUTHIS STRIKE RIYADH TOWER",
           Fonts.sans(13), (255, 255, 255))
    # lead
    ly, lw = 168, 560
    p.text(m, ly, LEAD["tag"], Fonts.sans(13), RED)
    y = p.para(m, ly + 20, LEAD["head"], Fonts.serif(32), lw, leading=36)
    y = p.para(m, y + 6, LEAD["deck"], Fonts.serif_text(15), lw,
               fill=(40, 40, 40), leading=20)
    p.para(m, y + 8, LEAD["note"], Fonts.sans_text(12), lw, fill=GREY, leading=16)
    ix = m + lw + 16
    iw = PAGE_W - m - ix
    p.paste_art(ART["sea"](iw, 216), ix, ly)
    p.d.rectangle([ix, ly, ix + iw, ly + 216], outline=INK, width=2)
    p.rule(396, 2)
    # cards
    cw = (PAGE_W - 2 * m - 24) // 3
    ch = 196
    for row in range(2):
        for col in range(3):
            tag, head, body, art = CARDS[row * 3 + col]
            x = m + col * (cw + 12)
            y = 408 + row * (ch + 12)
            p.d.rectangle([x, y, x + cw, y + ch], fill=(255, 255, 255),
                          outline=(200, 194, 178), width=1)
            p.paste_art(ART[art](cw - 2, 96), x + 1, y + 1)
            ty = y + 104
            p.text(x + 10, ty, tag, Fonts.sans(11), RED)
            ty = p.para(x + 10, ty + 16, head, Fonts.serif(16), cw - 20, leading=19)
            p.para(x + 10, ty + 2, body, Fonts.sans_text(11), cw - 20,
                   fill=(50, 50, 50), leading=14)
    p.rule(828, 2)
    # briefs
    p.text(m, 838, "IN BRIEF", Fonts.serif(20))
    stamp = "REPORTED 24\u201325 NOVEMBER 2026"
    p.text(PAGE_W - m - p.d.textlength(stamp, font=Fonts.sans(10)), 844,
           stamp, Fonts.sans(10), GREY)
    colw = (PAGE_W - 2 * m - 24) // 2
    for i, (tag, text) in enumerate(BRIEFS):
        bx = m + (i // 10) * (colw + 24)
        by = 862 + (i % 10) * 13
        tagfont = Fonts.sans(10)
        tw = p.d.textlength(tag + "  ", font=tagfont)
        p.text(bx, by, tag, tagfont, TEAL)
        line, bodyfont = text, Fonts.sans_text(11)
        while p.d.textlength(line, font=bodyfont) > colw - tw - 2 and len(line) > 10:
            line = line.rsplit(" ", 1)[0]
        if line != text:
            line += "\u2026"
        p.text(bx + tw, by, line, bodyfont)
    # footer
    p.rule(1004, 1, GREY)
    p.text(m, 1010,
           "Sources: Reuters, AP, RFE/RL, ESA, ESPNcricinfo, BBC, UNFCCC. "
           "All stories reported 24\u201325 November 2026.",
           Fonts.sans_text(9), GREY)
    p.image.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    build()
