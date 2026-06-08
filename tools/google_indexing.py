#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""구글 Indexing API 제출기 — URL_UPDATED 통보.

  python3 tools/google_indexing.py            # sitemap 전체
  python3 tools/google_indexing.py --changed  # 변경된 페이지만(자동화용)
  python3 tools/google_indexing.py /a/ /b/    # 특정 경로

준비물(둘 중 하나):
  - 환경변수 GOOGLE_APPLICATION_CREDENTIALS = 서비스계정 JSON 파일 경로
  - 환경변수 GOOGLE_SERVICE_ACCOUNT_JSON   = 서비스계정 JSON 원문(깃허브 Secret용)
설치:  pip install google-auth requests

설정 절차:
  1) Google Cloud 프로젝트에서 'Indexing API' 사용 설정
  2) 서비스 계정 생성 → JSON 키 발급
  3) Search Console에서 해당 서비스계정 이메일을 '소유자'로 추가
  4) 위 환경변수에 키를 넣고 실행

※ 정책 주의: 구글 Indexing API는 공식적으로 JobPosting·BroadcastEvent 용도입니다.
   일반 페이지에는 'Search Console 사이트맵 제출 + URL 검사'가 권장 방식이며,
   본 스크립트는 보조 수단으로만 사용하세요.
"""
import os, sys, json, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import indexnow  # sitemap_urls / changed_urls / DOMAIN 재사용

ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]


def _credentials_path():
    p = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if p and os.path.exists(p):
        return p
    raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if raw:
        fd, tmp = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w") as f:
            f.write(raw)
        return tmp
    return None


def main():
    args = [a for a in sys.argv[1:] if a.strip()]
    if args == ["--changed"]:
        urls = indexnow.changed_urls()
    elif args:
        urls = [a if a.startswith("http")
                else f"{indexnow.DOMAIN}{a if a.startswith('/') else '/' + a}" for a in args]
    else:
        urls = indexnow.sitemap_urls()
    if not urls:
        print("제출할 URL이 없습니다.")
        return

    cred_path = _credentials_path()
    if not cred_path:
        print("서비스계정 키가 없습니다(GOOGLE_APPLICATION_CREDENTIALS 또는 "
              "GOOGLE_SERVICE_ACCOUNT_JSON). 건너뜁니다.")
        return
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        print("google-auth 미설치. 'pip install google-auth requests' 후 실행하세요.")
        return

    creds = service_account.Credentials.from_service_account_file(cred_path, scopes=SCOPES)
    session = AuthorizedSession(creds)
    ok = fail = 0
    for u in urls:
        try:
            r = session.post(ENDPOINT, json={"url": u, "type": "URL_UPDATED"}, timeout=30)
            if r.status_code == 200:
                ok += 1
            else:
                fail += 1
                print(f"  실패 {r.status_code}: {u} — {r.text[:160]}")
        except Exception as e:
            fail += 1
            print(f"  오류: {u} — {e}")
    print(f"구글 Indexing API 제출 완료: 성공 {ok} / 실패 {fail} (총 {len(urls)})")


if __name__ == "__main__":
    main()
