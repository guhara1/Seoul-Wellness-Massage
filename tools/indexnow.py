#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IndexNow 제출기 — 빙(Bing)·야ндекс(Yandex)·Seznam 즉시 색인 요청.

배포 후 실행하면 sitemap.xml의 전 URL을 IndexNow에 한 번에 제출한다.
키 파일(<KEY>.txt)은 build.py가 사이트 루트에 생성한다.

  python3 tools/indexnow.py            # sitemap 전체 제출
  python3 tools/indexnow.py /a/ /b/     # 특정 경로만 제출

참고: 구글은 IndexNow를 쓰지 않는다 → Search Console에 sitemap 제출.
      네이버는 서치어드바이저에 sitemap.xml + rss.xml 제출.
"""
import os, sys, json, re, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

DOMAIN = "https://seoul-wellness-massage.pages.dev"
KEY = "a3f1c9e2b7d44f08a1c6e5b9d2074f3c"
HOST = DOMAIN.split("://", 1)[1].rstrip("/")
ENDPOINT = "https://api.indexnow.org/indexnow"


def sitemap_urls():
    p = os.path.join(ROOT, "sitemap.xml")
    with open(p, encoding="utf-8") as f:
        return re.findall(r"<loc>([^<]+)</loc>", f.read())


def submit(urls):
    # IndexNow 1회 요청 최대 10,000 URL
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": f"{DOMAIN}/{KEY}.txt",
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=data,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status


def main():
    args = [a for a in sys.argv[1:] if a.strip()]
    if args:
        urls = [a if a.startswith("http") else f"{DOMAIN}{a if a.startswith('/') else '/' + a}" for a in args]
    else:
        urls = sitemap_urls()
    if not urls:
        print("제출할 URL이 없습니다.")
        return
    print(f"IndexNow 제출: {len(urls)}개 URL → {ENDPOINT}")
    try:
        status = submit(urls)
        print(f"응답 상태: {status} (200/202 = 정상 접수)")
    except Exception as e:
        print(f"제출 실패: {e}")


if __name__ == "__main__":
    main()
