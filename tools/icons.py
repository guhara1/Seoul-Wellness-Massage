#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""순수 파이썬 PNG/ICO 생성기 — 외부 의존성 없이 파비콘·아이콘·OG 이미지 생성."""
import os, sys, zlib, struct

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")

BG = (11, 11, 14)              # #0b0b0e
G0 = (244, 210, 156)          # #f4d29c
G1 = (233, 184, 167)          # #e9b8a7
G2 = (201, 138, 107)          # #c98a6b
INK = (26, 18, 8)             # #1a1208


def _lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def grad(t):
    """0..1 → 3색 골드 그라데이션."""
    if t < 0.45:
        return _lerp(G0, G1, t / 0.45)
    return _lerp(G1, G2, (t - 0.45) / 0.55)


def new_canvas(w, h, color):
    return [[list(color) + [255] for _ in range(w)] for _ in range(h)]


def fill_grad_diag(px, w, h):
    for y in range(h):
        for x in range(w):
            t = (x + y) / (w + h - 2) if (w + h - 2) else 0
            c = grad(t)
            px[y][x] = [c[0], c[1], c[2], 255]


def _plot(px, w, h, x, y, color, r):
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r:
                xx, yy = x + dx, y + dy
                if 0 <= xx < w and 0 <= yy < h:
                    px[yy][xx] = [color[0], color[1], color[2], 255]


def draw_polyline(px, w, h, pts, color, thick):
    r = max(1, thick // 2)
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]; x1, y1 = pts[i + 1]
        x0 = int(x0 * w); y0 = int(y0 * h); x1 = int(x1 * w); y1 = int(y1 * h)
        steps = max(abs(x1 - x0), abs(y1 - y0), 1)
        for s in range(steps + 1):
            t = s / steps
            _plot(px, w, h, int(x0 + (x1 - x0) * t), int(y0 + (y1 - y0) * t), color, r)


W_PTS = [(0.20, 0.27), (0.33, 0.73), (0.50, 0.42), (0.67, 0.73), (0.80, 0.27)]


def write_png(path, px):
    h = len(px); w = len(px[0])
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        for x in range(w):
            raw += bytes(px[y][x])
    comp = zlib.compress(bytes(raw), 9)

    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        return c + struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff)

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
    with open(path, "wb") as f:
        f.write(sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", comp) + chunk(b"IEND", b""))


def icon(size, maskable=False):
    px = new_canvas(size, size, BG)
    fill_grad_diag(px, size, size)
    # 마스커블은 안전영역 고려해 W를 약간 작게
    pts = W_PTS
    if maskable:
        pts = [(0.5 + (x - 0.5) * 0.7, 0.5 + (y - 0.5) * 0.7) for x, y in W_PTS]
    draw_polyline(px, size, size, pts, INK, max(4, size // 9))
    return px


def og_cover(w=1200, h=630):
    px = new_canvas(w, h, BG)
    # 어두운 배경에 우상단 골드 발광 느낌(간단 대각 그라데이션 박스)
    box = int(h * 0.42)
    bx, by = int(w * 0.5 - box / 2), int(h * 0.28)
    sub = new_canvas(box, box, BG)
    fill_grad_diag(sub, box, box)
    draw_polyline(sub, box, box, W_PTS, INK, max(6, box // 9))
    # 둥근 느낌 없이 박스 합성
    for y in range(box):
        for x in range(box):
            yy, xx = by + y, bx + x
            if 0 <= yy < h and 0 <= xx < w:
                px[yy][xx] = sub[y][x]
    # 하단 골드 라인
    line_y = int(h * 0.78)
    for x in range(w):
        c = grad(x / (w - 1))
        for dy in range(6):
            px[line_y + dy][x] = [c[0], c[1], c[2], 255]
    return px


def write_ico(path, png_path):
    """32x32 PNG를 ICO 컨테이너로 감싸기(PNG 압축 엔트리 지원)."""
    with open(png_path, "rb") as f:
        png = f.read()
    header = struct.pack("<HHH", 0, 1, 1)
    entry = struct.pack("<BBBBHHII", 32, 32, 0, 0, 1, 32, len(png), 22)
    with open(path, "wb") as f:
        f.write(header + entry + png)


def main():
    os.makedirs(ASSETS, exist_ok=True)
    write_png(os.path.join(ROOT, "icon-192.png"), icon(192))
    write_png(os.path.join(ROOT, "icon-512.png"), icon(512))
    write_png(os.path.join(ROOT, "icon-maskable.png"), icon(512, maskable=True))
    write_png(os.path.join(ROOT, "apple-touch-icon.png"), icon(180))
    write_png(os.path.join(ROOT, "favicon-32.png"), icon(32))
    write_ico(os.path.join(ROOT, "favicon.ico"), os.path.join(ROOT, "favicon-32.png"))
    write_png(os.path.join(ASSETS, "og-cover.png"), og_cover())
    print("아이콘/OG 이미지 생성 완료")


if __name__ == "__main__":
    main()
