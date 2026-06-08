# 웰니스센터 — 서울 출장마사지·홈타이

서울 전역 출장마사지·홈타이 안내 정적 사이트입니다. 순수 HTML + 인라인 CSS/JS,
외부 의존성 0개로 동작하며 Python 생성기로 전체 페이지를 일괄 생성합니다.

## 구성

| 항목 | 값 |
|---|---|
| 상호 | 웰니스센터 |
| 대표 | 데이비드존 |
| 예약·상담 | 0508-202-4743 (연중무휴 24시간) |
| 도메인(예정) | https://seoul-wellness-massage.pages.dev |
| 호스팅 | Cloudflare Pages (정적) |
| 총 페이지 | **460** (홈 + 자치구 25 + 지하철역 290 + 테마 14 + 코스 8 + 매거진 60 + 허브/정책 등) |

## 생성 방법

```bash
python3 tools/icons.py   # 파비콘·앱 아이콘·OG 이미지 생성 (assets/, 루트)
python3 tools/build.py   # 전체 HTML + sitemap.xml/robots.txt/site.webmanifest 생성
```

> 표준 라이브러리만 사용합니다(외부 패키지 불필요).

## tools/ 구조

```
tools/
 ├ lib.py        # 사업자 설정 + 전역 CSS + head/header/footer/플로팅버튼/스크립트 + 공통 조각
 ├ data.py       # 권역 6 / 자치구 25 / 테마 14 / 코스 8 / 지하철 노선·역 / 내비게이션 생성
 ├ art.py        # 매거진 기본 10편 (+ P() 헬퍼)
 ├ a_region.py   # 지역별 마사지 10편
 ├ a_swedish.py  # 스웨디시 10편
 ├ a_visiting.py # 출장마사지 10편
 ├ a_korean.py   # 한국인 관리사 10편
 ├ a_thai.py     # 태국 관리사 10편
 ├ icons.py      # 순수 파이썬 PNG/ICO 생성기 (파비콘·아이콘·OG)
 └ build.py      # 전체 사이트 생성기 (실행 진입점)
```

## 값 변경 가이드

- **사업자 정보·도메인·브랜드**: `tools/lib.py` 상단 상수만 수정.
- **요금**: `tools/lib.py` 의 `PRICES`.
- **지역/역/테마/코스**: `tools/data.py`.
- **매거진 글**: `tools/art.py` 및 `tools/a_*.py` 에 `A()` 형식으로 추가 후 재생성.
- **디자인 컬러**: `tools/lib.py` 의 `CSS` 내 `:root` 변수.

재실행 시 기존 출력 위로 덮어씁니다.

## SEO / 기술

- 모든 페이지: canonical · hreflang(ko-KR/x-default) · Open Graph · Twitter Card · robots 메타
- 구조화 데이터: 홈 `LocalBusiness`, 매거진 글 `BreadcrumbList`+`BlogPosting`,
  매거진/카테고리 목록 `Blog`, 안내 페이지 `FAQPage`
- `sitemap.xml`(460 URL), `robots.txt`(`/tools/` Disallow, AI 크롤러 Allow), `site.webmanifest`

전체 설계 사양은 [`SITE-SPEC.md`](./SITE-SPEC.md) 참고.

---

> 본 서비스는 의료 행위가 아닌 건강관리(이완·휴식) 목적의 방문 관리 서비스이며,
> 만 19세 이상 성인을 대상으로 합니다. 불법·퇴폐 행위는 일절 제공하지 않습니다.
