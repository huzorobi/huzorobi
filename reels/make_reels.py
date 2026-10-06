"""HuzoSecurity daily fact Reels.

Builds a 9:16 motion piece for each daily fact card:

  Scene 1  the stat counts up over a slowly turning dotted globe, with live
           attack arcs leaving Manchester. Headline wipes in, then the
           "why it matters" line.
  Scene 2  "What to do this week": the two actions land one at a time.
  Scene 3  the finished card rises into frame with the call to action.

Usage:
  python3 make_reels.py <repo_dir> <out_dir> [day ...]

Reads:  <repo_dir>/huzosecurity-fact-NN.png  (the approved cards)
        <repo_dir>/instagram/schedule.json    (captions: body, steps, source)
        reels/cards.json                      (tag, stat, headline per card)
        reels/assets/                         (fonts + land dots for the globe)

Audio is an original generated bed, so there is nothing to license.
"""
import json
import math
import os
import re
import subprocess
import sys
import wave

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H, FPS = 1080, 1920, 30
DUR = 14.0
NAVY = np.array([12, 31, 46], np.float32)
RED = (229, 83, 60)
WHITE = (255, 255, 255)
SOFT = (214, 224, 232)
GREY = (132, 152, 170)
LEFT = 84            # left text margin
TEXT_W = 850         # keeps clear of the Reels buttons on the right

T_S1_OUT = 5.5
T_S2_IN = 5.9
T_S2_OUT = 10.1
T_S3_IN = 10.3
T_END = 13.55
SCRIM = None


def F(name, size):
    return ImageFont.truetype(os.path.join(ASSETS, name), size)


def ease_out(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def ease_io(t):
    t = min(max(t, 0.0), 1.0)
    return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2


def prog(t, start, dur):
    return ease_out((t - start) / dur)


# ---------------------------------------------------------------- text layers

class Layer:
    """Pre-rendered RGBA element with a home position."""

    def __init__(self, img, x, y):
        self.a = np.asarray(img).astype(np.float32)
        self.x, self.y = x, y
        self.h, self.w = self.a.shape[:2]


def text_img(text, font, fill, pad=8):
    l, t, r, b = font.getbbox(text)
    img = Image.new("RGBA", (r - l + pad * 2, b - t + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((pad - l, pad - t), text, font=font, fill=fill)
    return img


def wrap(words, font, width):
    lines, cur = [], []
    for w in words:
        test = " ".join([x for x, _ in cur] + [w[0]])
        if cur and font.getlength(test) > width:
            lines.append(cur)
            cur = []
        cur.append(w)
    if cur:
        lines.append(cur)
    return lines


def rich_paragraph(segments, font_reg, font_bold, width, leading):
    """segments: list of (text, colour, bold). Returns RGBA image."""
    words = []
    for text, col, bold in segments:
        for w in text.split():
            words.append((w, (col, bold)))
    lines = wrap(words, font_bold, width)
    asc = font_reg.getmetrics()[0]
    img = Image.new("RGBA", (width + 20, leading * len(lines) + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y = 4
    for line in lines:
        x = 0
        for w, (col, bold) in line:
            f = font_bold if bold else font_reg
            d.text((x, y + asc), w, font=f, fill=col, anchor="ls")
            x += f.getlength(w + " ")
        y += leading
    return img


def label_lines(text, font, width):
    words = [(w, None) for w in text.split()]
    return [" ".join(w for w, _ in ln) for ln in wrap(words, font, width)]


# ---------------------------------------------------------------- globe

CITIES = [(-74.0, 40.7), (3.4, 6.5), (55.3, 25.2), (72.9, 19.1), (103.8, 1.35),
          (-46.6, -23.5), (37.6, 55.8), (18.4, -33.9), (139.7, 35.7), (-118.2, 34.1),
          (28.0, 41.0)]
MAN = (-2.24, 53.48)


def to_xyz(lon, lat):
    lo, la = np.radians(lon), np.radians(lat)
    return np.stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)], -1)


def slerp(a, b, n):
    om = math.acos(max(-1.0, min(1.0, float(np.dot(a, b)))))
    s = np.linspace(0, 1, n)
    out = (np.sin((1 - s) * om)[:, None] * a + np.sin(s * om)[:, None] * b) / math.sin(om)
    lift = 1 + 0.18 * np.sin(np.pi * s) * (om / math.pi + 0.3)
    return out * lift[:, None]


class Globe:
    def __init__(self):
        pts = np.array(json.load(open(os.path.join(ASSETS, "land_dots.json"))), np.float32)
        self.dots = to_xyz(pts[:, 0], pts[:, 1])
        man = to_xyz(*MAN)
        self.man = man
        self.arcs = [slerp(man, to_xyz(*c), 64) for c in CITIES]
        self.cx, self.cy, self.r = 790, 600, 560

    def project(self, xyz, lon0, lat0):
        lo, la = math.radians(lon0), math.radians(lat0)
        # rotate around z by -lon0, then around y by lat0
        x, y, z = xyz[..., 0], xyz[..., 1], xyz[..., 2]
        x1 = x * math.cos(lo) + y * math.sin(lo)
        y1 = -x * math.sin(lo) + y * math.cos(lo)
        x2 = x1 * math.cos(la) + z * math.sin(la)
        z2 = -x1 * math.sin(la) + z * math.cos(la)
        sx = self.cx + y1 * self.r
        sy = self.cy - z2 * self.r
        return sx, sy, x2  # x2 > 0 faces the viewer

    def draw(self, t, intensity):
        """Return float32 additive light layer (H, W, 3)."""
        layer = np.zeros((H, W, 3), np.float32)
        if intensity <= 0:
            return layer
        lon0 = -12 + t * 2.2
        lat0 = 34
        sx, sy, depth = self.project(self.dots, lon0, lat0)
        vis = depth > 0.02
        img = np.zeros((H, W, 3), np.uint8)
        # faint rim
        cv2.circle(img, (self.cx, self.cy), self.r, (40, 62, 80), 2, cv2.LINE_AA)
        for x, y, d in zip(sx[vis], sy[vis], depth[vis]):
            c = int(55 + 95 * d)
            cv2.circle(img, (int(x), int(y)), 3, (c, int(c * 1.12), int(c * 1.3)), -1, cv2.LINE_AA)
        # arcs from Manchester, drawn on in a stagger and then travelling
        for k, arc in enumerate(self.arcs):
            ax, ay, ad = self.project(arc, lon0, lat0)
            start = 0.25 + k * 0.12
            p = ease_out((t - start) / 1.1)
            n = max(2, int(len(arc) * p))
            pts = [(int(ax[i]), int(ay[i])) for i in range(n) if ad[i] > -0.05]
            if len(pts) > 1:
                cv2.polylines(img, [np.array(pts, np.int32)], False, RED[::-1], 2, cv2.LINE_AA)
            if p >= 1 and ad[-1] > 0:
                cv2.circle(img, (int(ax[-1]), int(ay[-1])), 5, RED[::-1], -1, cv2.LINE_AA)
            # travelling pulse
            if p >= 1:
                ph = ((t - start - 1.1) * 0.45 + k * 0.17) % 1.0
                i = int(ph * (len(arc) - 1))
                if ad[i] > 0:
                    cv2.circle(img, (int(ax[i]), int(ay[i])), 4, (255, 220, 210), -1, cv2.LINE_AA)
        mx, my, md = self.project(self.man[None], lon0, lat0)
        if md[0] > 0:
            pulse = (t * 0.8) % 1.0
            cv2.circle(img, (int(mx[0]), int(my[0])), int(8 + 26 * pulse), RED[::-1], 2, cv2.LINE_AA)
            cv2.circle(img, (int(mx[0]), int(my[0])), 7, (255, 255, 255), -1, cv2.LINE_AA)
        img = img[..., ::-1]  # BGR -> RGB
        return img.astype(np.float32) * intensity


# ---------------------------------------------------------------- composition

def blend(canvas, L, dx=0, dy=0, alpha=1.0, wipe=1.0, scale=1.0):
    if alpha <= 0.003 or wipe <= 0:
        return
    a = L.a
    if scale != 1.0:
        nh, nw = max(1, int(L.h * scale)), max(1, int(L.w * scale))
        a = cv2.resize(a, (nw, nh), interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_LINEAR)
        x = int(L.x + (L.w - nw) / 2 + dx)
        y = int(L.y + (L.h - nh) / 2 + dy)
    else:
        x, y = int(L.x + dx), int(L.y + dy)
    h, w = a.shape[:2]
    if wipe < 1:
        w = int(w * wipe)
        a = a[:, :w]
    x0, y0 = max(x, 0), max(y, 0)
    x1, y1 = min(x + w, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0:
        return
    src = a[y0 - y:y1 - y, x0 - x:x1 - x]
    al = src[..., 3:4] / 255.0 * alpha
    reg = canvas[y0:y1, x0:x1]
    reg[:] = reg * (1 - al) + src[..., :3] * al


def build_layers(day, card_png, cap, meta):
    L = {}
    card = Image.open(card_png).convert("RGB")
    ca = np.asarray(card)

    # logo: white pixels only from the card header
    region = ca[60:170, 60:520].astype(np.float32)
    lum = region.min(axis=2)
    alpha = np.clip((lum - 120) * 2.2, 0, 255)
    logo = np.dstack([np.full_like(lum, 255)] * 3 + [alpha]).astype(np.uint8)
    L["logo"] = Layer(Image.fromarray(logo, "RGBA"), LEFT - 14, 150)

    # tag chip + "did you know"
    fm = F("IBMPlexMono-SemiBold.ttf", 30)
    tag = meta["tag"]
    tb = fm.getbbox(tag)
    tw = tb[2] - tb[0]
    chip_w = tw + 36
    chip = Image.new("RGBA", (chip_w + 40 + 320, 56), (0, 0, 0, 0))
    d = ImageDraw.Draw(chip)
    d.rectangle((0, 0, chip_w, 55), fill=RED)
    d.text((18 - tb[0], 28), tag, font=fm, fill=WHITE, anchor="lm")
    d.text((chip_w + 24, 28), "DID YOU KNOW?", font=F("IBMPlexMono-Regular.ttf", 28), fill=GREY, anchor="lm")
    L["chip"] = Layer(chip, LEFT, 560)

    # stat size: as big as fits the width, capped
    stat = meta["stat"]
    size = 360
    while F("Anton-Regular.ttf", size).getlength(stat) > TEXT_W and size > 120:
        size -= 6
    L["stat_font"] = F("Anton-Regular.ttf", size)
    L["stat_y"] = 640
    sb = L["stat_font"].getbbox(stat)
    stat_h = sb[3] - sb[1]

    # headline lines
    fl = F("Anton-Regular.ttf", 86)
    lines = label_lines(meta["label"], fl, TEXT_W)
    y = 640 + stat_h + 70
    L["label"] = []
    for ln in lines:
        img = text_img(ln, fl, WHITE, pad=6)
        L["label"].append(Layer(img, LEFT - 6, y))
        y += 96

    # body: first sentence soft white, the rest red (as on the card)
    body = cap["body"]
    m = re.match(r"(.+?[.!?])\s+(.*)", body)
    segs = [(m.group(1), SOFT, False), (m.group(2), RED, True)] if m else [(body, SOFT, False)]
    para = rich_paragraph(segs, F("WorkSans-Regular.ttf", 46), F("WorkSans-SemiBold.ttf", 46), TEXT_W, 62)
    L["body"] = Layer(para, LEFT, y + 34)

    L["source"] = Layer(text_img("SOURCE: " + cap["source"].upper(), F("IBMPlexMono-Regular.ttf", 24), GREY), LEFT - 8, 1585)

    # scene 2
    L["s2_head"] = Layer(text_img("WHAT TO DO THIS WEEK", F("IBMPlexMono-SemiBold.ttf", 38), RED), LEFT - 8, 640)
    fn = F("Anton-Regular.ttf", 170)
    fs = F("WorkSans-SemiBold.ttf", 62)
    L["steps"] = []
    y = 790
    for i, s in enumerate(cap["steps"]):
        num = Layer(text_img(str(i + 1), fn, RED, pad=4), LEFT - 4, y - 18)
        txt = rich_paragraph([(s, WHITE, True)], fs, fs, 690, 78)
        tl = Layer(txt, LEFT + 150, y + 6)
        L["steps"].append((num, tl))
        y += max(250, tl.h + 90)
    L["s2_rule_y"] = 720

    # scene 3: the card itself, with a soft shadow
    cw = 892
    ch = int(1350 * cw / 1080)
    small = card.resize((cw, ch), Image.LANCZOS)
    pad = 60
    sh = Image.new("RGBA", (cw + pad * 2, ch + pad * 2), (0, 0, 0, 0))
    shadow = np.zeros((ch + pad * 2, cw + pad * 2), np.float32)
    shadow[pad + 18:pad + 18 + ch, pad:pad + cw] = 1
    shadow = cv2.GaussianBlur(shadow, (0, 0), 22) * 170
    sh_arr = np.zeros((ch + pad * 2, cw + pad * 2, 4), np.uint8)
    sh_arr[..., 3] = shadow.astype(np.uint8)
    sh = Image.fromarray(sh_arr, "RGBA")
    sh.paste(small.convert("RGBA"), (pad, pad))
    # thin light border so the card reads against the navy background
    bd = ImageDraw.Draw(sh)
    bd.rectangle((pad, pad, pad + cw - 1, pad + ch - 1), outline=(60, 86, 108, 255), width=2)
    L["card"] = Layer(sh, (W - cw) // 2 - pad, 200 - pad)
    cy = 200 + ch + 40
    # The offer, word for word as on the cards and captions
    L["cta1"] = Layer(text_img("Secure? It costs you nothing.", F("WorkSans-SemiBold.ttf", 44), WHITE), 0, cy)
    L["cta1"].x = (W - L["cta1"].w) // 2
    L["cta1b"] = Layer(text_img("Not secure? Your second test is free.", F("WorkSans-SemiBold.ttf", 44), RED), 0, cy + 60)
    L["cta1b"].x = (W - L["cta1b"].w) // 2
    L["cta2"] = Layer(text_img("LINK IN BIO  /  HUZOSECURITY.COM", F("IBMPlexMono-SemiBold.ttf", 28), GREY), 0, cy + 132)
    L["cta2"].x = (W - L["cta2"].w) // 2
    return L


def parse_stat(stat):
    m = re.match(r"^([^\d]*)(\d+(?:\.\d+)?)(.*)$", stat)
    if not m:
        return None
    pre, num, suf = m.groups()
    dec = len(num.split(".")[1]) if "." in num else 0
    return pre, float(num), suf, dec


def background():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - 780) / 900) ** 2 + ((yy - 620) / 1100) ** 2)
    glow = np.clip(1 - d, 0, 1)[..., None] ** 2
    bg = NAVY[None, None, :] + glow * np.array([10, 18, 26], np.float32)
    # very fine grain so gradients don't band after compression
    # left-hand scrim so text always reads over the globe
    xs = np.linspace(0, 1, W, dtype=np.float32)
    scrim = np.clip(1 - xs / 0.78, 0, 1) ** 1.6
    bg_s = scrim[None, :, None]
    rng = np.random.default_rng(3)
    bg = bg + rng.normal(0, 1.2, bg.shape).astype(np.float32)
    return bg, bg_s


def frames(L, globe, bg, stat):
    n = int(DUR * FPS)
    parsed = parse_stat(stat)
    for i in range(n):
        t = i / FPS
        f = bg.copy()

        # globe intensity by scene
        gi = 0.62 * prog(t, 0, 0.8)
        if t > T_S3_IN - 0.4:
            gi = 0.62 - 0.36 * prog(t, T_S3_IN - 0.4, 0.8)
        f += globe.draw(t, gi) * (1 - 0.55 * SCRIM)
        np.clip(f, 0, 255, out=f)

        # progress rule along the top
        pw = int(W * min(t / T_END, 1.0))
        f[0:6, :pw] = RED

        # ---------------- scene 1
        out1 = prog(t, T_S1_OUT, 0.45)
        if out1 < 1:
            a1, dy1 = 1 - out1, -50 * out1
            blend(f, L["logo"], alpha=prog(t, 0.05, 0.5) * a1, dy=dy1)
            blend(f, L["chip"], dx=-40 * (1 - prog(t, 0.15, 0.5)), alpha=prog(t, 0.15, 0.4) * a1, dy=dy1)
            # count-up stat
            p = prog(t, 0.25, 1.15)
            if parsed:
                pre, val, suf, dec = parsed
                cur = val * ease_io(min(max((t - 0.25) / 1.15, 0), 1))
                s = f"{pre}{cur:.{dec}f}{suf}"
            else:
                s = stat
            if p > 0:
                img = text_img(s, L["stat_font"], WHITE, pad=6)
                lay = Layer(img, LEFT - 10, L["stat_y"])
                blend(f, lay, alpha=min(1, p * 2.5) * a1, dy=dy1 + 30 * (1 - p), scale=1.0)
            for k, ln in enumerate(L["label"]):
                st = 1.05 + k * 0.14
                wp = prog(t, st, 0.55)
                blend(f, ln, alpha=a1, dy=dy1, wipe=wp)
                if 0 < wp < 1 and a1 > 0:
                    bx = int(ln.x + ln.w * wp)
                    by = int(ln.y + dy1 + 10)
                    if bx + 7 < W:
                        f[by:by + ln.h - 20, bx:bx + 7] = RED
            blend(f, L["body"], alpha=prog(t, 1.95, 0.6) * a1, dy=dy1 + 30 * (1 - prog(t, 1.95, 0.6)))
            blend(f, L["source"], alpha=prog(t, 2.4, 0.6) * a1 * 0.95)

        # ---------------- scene 2
        if T_S2_IN - 0.1 < t < T_S2_OUT + 0.6:
            out2 = prog(t, T_S2_OUT, 0.45)
            a2, dy2 = 1 - out2, -50 * out2
            blend(f, L["logo"], alpha=prog(t, T_S2_IN, 0.4) * a2, dy=dy2)
            blend(f, L["s2_head"], alpha=prog(t, T_S2_IN, 0.4) * a2, dx=-30 * (1 - prog(t, T_S2_IN, 0.5)), dy=dy2)
            rw = int(TEXT_W * prog(t, T_S2_IN + 0.15, 0.7))
            if rw > 0 and a2 > 0:
                y = L["s2_rule_y"] + int(dy2)
                f[y:y + 4, LEFT:LEFT + rw] = f[y:y + 4, LEFT:LEFT + rw] * (1 - a2) + np.array(RED) * a2
            for k, (num, txt) in enumerate(L["steps"]):
                st = T_S2_IN + 0.45 + k * 1.15
                p = prog(t, st, 0.55)
                blend(f, num, alpha=p * a2, dy=dy2 + 60 * (1 - p))
                blend(f, txt, alpha=prog(t, st + 0.12, 0.55) * a2, dx=40 * (1 - prog(t, st + 0.12, 0.6)), dy=dy2)
            blend(f, L["source"], alpha=prog(t, T_S2_IN, 0.5) * a2 * 0.95)

        # ---------------- scene 3
        if t > T_S3_IN:
            p = prog(t, T_S3_IN, 0.9)
            blend(f, L["card"], alpha=min(1, p * 1.8), dy=220 * (1 - p), scale=0.94 + 0.06 * p)
            blend(f, L["cta1"], alpha=prog(t, T_S3_IN + 0.6, 0.5), dy=20 * (1 - prog(t, T_S3_IN + 0.6, 0.5)))
            blend(f, L["cta1b"], alpha=prog(t, T_S3_IN + 0.85, 0.5), dy=20 * (1 - prog(t, T_S3_IN + 0.85, 0.5)))
            blend(f, L["cta2"], alpha=prog(t, T_S3_IN + 1.1, 0.5))

        # fade to navy at the very end so the loop is clean
        if t > T_END:
            k = min(1, (t - T_END) / (DUR - T_END))
            f = f * (1 - k) + bg * k
        yield np.clip(f, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------- audio

def make_audio(path):
    sr = 44100
    t = np.arange(int(sr * DUR)) / sr
    out = np.zeros_like(t)
    # warm minor pad, slowly breathing
    for fr, amp in ((55.0, 0.22), (110.0, 0.20), (164.81, 0.12), (220.0, 0.09), (261.63, 0.07), (329.63, 0.04)):
        det = np.sin(2 * np.pi * fr * t) + np.sin(2 * np.pi * fr * 1.003 * t)
        lfo = 0.65 + 0.35 * np.sin(2 * np.pi * (0.11 + fr / 5000) * t + fr)
        out += amp * 0.5 * det * lfo
    # muted pulse, 100 bpm
    beat = 60 / 100
    for s in np.arange(0.0, DUR, beat):
        idx = (t >= s) & (t < s + 0.35)
        tt = t[idx] - s
        out[idx] += 0.28 * np.exp(-tt * 14) * np.sin(2 * np.pi * (48 + 30 * np.exp(-tt * 40)) * tt)
    # airy riser into each scene + soft tick on each step
    rng = np.random.default_rng(11)
    noise = rng.standard_normal(len(t))
    noise = np.convolve(noise, np.ones(30) / 30, mode="same")
    for s in (0.0, T_S2_IN - 0.5, T_S3_IN - 0.5):
        idx = (t >= s) & (t < s + 0.9)
        tt = t[idx] - s
        out[idx] += 0.55 * noise[idx] * np.sin(np.pi * tt / 0.9) ** 2
    for s in (T_S2_IN + 0.45, T_S2_IN + 1.6, 0.25):
        idx = (t >= s) & (t < s + 0.12)
        tt = t[idx] - s
        out[idx] += 0.18 * np.exp(-tt * 50) * np.sin(2 * np.pi * 1320 * tt)
    env = np.minimum(1, t / 0.6) * np.minimum(1, (DUR - t) / 0.9)
    out *= env
    out = np.tanh(out * 1.4)
    out = out / np.abs(out).max() * 0.5
    data = (out * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(data.tobytes())


# ---------------------------------------------------------------- captions

def parse_caption(c):
    parts = [p.strip() for p in c.split("\n\n")]
    body = parts[1]
    steps = [re.sub(r"^\d\.\s*", "", s) for s in parts[2].split("\n")[1:3]]
    source = parts[3].replace("Source:", "").strip()
    return {"body": body, "steps": steps, "source": source}


def main():
    repo, outdir = sys.argv[1:3]
    days = [int(d) for d in sys.argv[3:]] or list(range(1, 31))
    meta = json.load(open(os.path.join(HERE, "cards.json")))
    sched = {}
    for name in ("schedule.json", "reels.json"):
        path = os.path.join(repo, "instagram", name)
        if os.path.exists(path):
            sched.update({e["day"]: e for e in json.load(open(path))})
    os.makedirs(outdir, exist_ok=True)
    audio = os.path.join(outdir, f"_bed_{os.getpid()}.wav")
    make_audio(audio)
    globe = Globe()
    global SCRIM
    bg, SCRIM = background()
    for day in days:
        cap = parse_caption(sched[day]["caption"])
        card = os.path.join(repo, f"huzosecurity-fact-{day:02d}.png")
        L = build_layers(day, card, cap, meta[str(day)])
        dst = os.path.join(outdir, f"huzosecurity-reel-{day:02d}.mp4")
        cmd = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
            "-i", audio,
            "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p",
            "-profile:v", "high", "-level", "4.1", "-g", "60",
            "-c:a", "aac", "-b:a", "160k", "-ar", "44100",
            "-shortest", "-movflags", "+faststart", dst,
        ]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for fr in frames(L, globe, bg, meta[str(day)]["stat"]):
            p.stdin.write(fr.tobytes())
        p.stdin.close()
        p.wait()
        print(dst, os.path.getsize(dst) // 1024, "KB", flush=True)
    os.remove(audio)


if __name__ == "__main__":
    main()
