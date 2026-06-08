#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IndexNow 제출기 — 빙(Bing)·얀덱스(Yandex)·Seznam 즉시 색인 요청.

  python3 tools/indexnow.py              # sitemap 전체 제출
  python3 tools/indexnow.py --changed    # 직전 커밋 대비 변경된 페이지만 제출(자동화용)
  python3 tools/indexnow.py /a/ /b/      # 특정 경로만 제출

키 파일(<KEY>.txt)은 build.py가 사이트 루트에 생성한다.
참고: 구글은 IndexNow 미참여 → tools/google_indexing.py 또는 Search Console 사용.
      네이버는 서치어드바이저에 sitemap.xml + rss.xml 제출.
"""
import os, sys, json, re, subprocess, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

DOMAIN = "https://seoul-wellness-massage.pages.dev"
KEY = "a3f1c9e2b7d44f08a1c6e5b9d2074f3c"
HOST = DOMAIN.split("://", 1)[1].rstrip("/")
ENDPOINT = "https://api.indexnow.org/indexnow"


def sitemap_urls():
    p = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return re.findall(r"<loc>([^<]+)</loc>", f.read())


def _path_to_url(rel):
    """저장소 상대경로(index.html) → 사이트 URL."""
    rel = rel.strip()
    if rel == "index.html":
        return DOMAIN + "/"
    if rel.endswith("/index.html"):
        return DOMAIN + "/" + rel[: -len("index.html")]
    return None


def changed_urls(ref="HEAD~1"):
    """직전 커밋 대비 추가/수정된 index.html → URL 목록(글 올릴 때마다 자동 제출용)."""
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only", "--diff-filter=AM", ref, "HEAD"],
            cwd=ROOT, text=True)
    except Exception as e:
        print(f"git diff 실패({e}) → sitemap 전체로 대체")
        return sitemap_urls()
    urls = []
    for line in out.splitlines():
        u = _path_to_url(line)
        if u:
            urls.append(u)
    return sorted(set(urls))


def submit(urls):
    # IndexNow 1회 요청 최대 10,000 URL
    out = []
    for i in range(0, len(urls), 10000):
        batch = urls[i:i + 10000]
        payload = {"host": HOST, "key": KEY,
                   "keyLocation": f"{DOMAIN}/{KEY}.txt", "urlList": batch}
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(ENDPOINT, data=data,
                                     headers={"Content-Type": "application/json; charset=utf-8"})
        with urllib.request.urlopen(req, timeout=30) as r:
            out.append(r.status)
    return out


def main():
    args = [a for a in sys.argv[1:] if a.strip()]
    if args == ["--changed"]:
        urls = changed_urls()
    elif args:
        urls = [a if a.startswith("http")
                else f"{DOMAIN}{a if a.startswith('/') else '/' + a}" for a in args]
    else:
        urls = sitemap_urls()
    if not urls:
        print("제출할 URL이 없습니다.")
        return
    print(f"IndexNow 제출: {len(urls)}개 URL")
    for u in urls[:20]:
        print("  -", u)
    if len(urls) > 20:
        print(f"  … 외 {len(urls) - 20}개")
    try:
        print("응답 상태:", submit(urls), "(200/202 = 정상 접수)")
    except Exception as e:
        print(f"제출 실패: {e}")


if __name__ == "__main__":
    main()
