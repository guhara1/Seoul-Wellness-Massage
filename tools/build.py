#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""웰니스센터 정적 사이트 생성기.

실행: python3 tools/build.py
출력: 저장소 루트에 정적 HTML + sitemap.xml/robots.txt/manifest/아이콘 생성.
"""
import os, sys, json, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import lib
import data
import art, a_region, a_swedish, a_visiting, a_korean, a_thai

lib.NAV_HTML = data.build_nav()

ARTICLES = (art.ARTICLES + a_region.ARTICLES + a_swedish.ARTICLES
            + a_visiting.ARTICLES + a_korean.ARTICLES + a_thai.ARTICLES)

PAGES = []   # (path, priority, changefreq) for sitemap
esc = lib.esc


def write(path, html):
    """path 예: '/seoul/' -> seoul/index.html ; '/' -> index.html"""
    rel = path.strip("/")
    out = os.path.join(ROOT, rel, "index.html") if rel else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)


def add(path, html, prio="0.6", freq="weekly"):
    write(path, html)
    PAGES.append((path, prio, freq))


# ────────────────────────── 공통 조각 ──────────────────────────
def cards(items):
    """items: [(eyebrow, title, desc, href, morelabel)]"""
    out = []
    for k, t, d, href, more in items:
        out.append(
            f'<a class="card reveal" href="{href}"><div class="k">{esc(k)}</div>'
            f'<h3>{esc(t)}</h3><p>{d}</p><span class="more">{esc(more)} →</span></a>')
    return f'<div class="grid g3">{"".join(out)}</div>'


def lux_sections(secs):
    out = []
    for i, (h, body) in enumerate(secs, 1):
        out.append(f'<section class="lux-sec reveal" id="sec-{i}"><h2>{esc(h)}</h2>{body}</section>')
    return "".join(out)


def lux_page(title, desc, path, eyebrow, h1, lead, secs, crumb_items,
             faq=None, byline=None, related=None, og_type="website", jsonld=None,
             prio="0.6", freq="weekly"):
    toc = "".join(f'<li><a href="#sec-{i}">{esc(h)}</a></li>' for i, (h, _) in enumerate(secs, 1))
    rel = ""
    if related:
        links = "".join(f'<li><a href="{href}">{esc(lab)}</a></li>' for href, lab in related)
        secs_extra = (f'<section class="lux-sec reveal" id="sec-rel"><h2>함께 보면 좋은 안내</h2>'
                      f'<ul>{links}</ul></section>')
        toc += '<li><a href="#sec-rel">함께 보면 좋은 안내</a></li>'
    else:
        secs_extra = ""
    body = (lib.crumb(crumb_items)
            + lib.lux_hero(eyebrow, h1, lead, byline=byline)
            + '<section class="block lux-body" style="padding-top:34px"><div class="wrap"><div class="lux-grid">'
            + f'<aside class="toc"><div class="toc-inner"><span class="toc-label">목차</span><ul>{toc}</ul></div></aside>'
            + '<div class="lux-main">' + lux_sections(secs) + secs_extra + '</div>'
            + '</div></div></section>')
    if faq:
        body += lib.faq_block(faq)
    body += lib.cta_band()
    add(path, lib.document(title, desc, path, body, og_type=og_type, jsonld=jsonld), prio, freq)


# ────────────────────────── 홈 ──────────────────────────
def build_home():
    region_cards = []
    for rk, rl, gus in data.REGIONS:
        names = " · ".join(n for _, n in gus)
        region_cards.append((f"AREA · {rk.upper()}", rl, names, f"/seoul/area/#{rk}", "지역 보기"))
    theme_cards = [(f"THEME", n, d, f"/theme/{s}/", "자세히")
                   for s, n, d in data.THEMES[:6]]

    reviews = [
        ("★★★★★", "퇴근 후 집에서 바로 받을 수 있어서 정말 편했어요. 어깨 뭉친 게 한결 가벼워졌습니다.", "강남구 · 30대 직장인"),
        ("★★★★★", "기념일에 커플로 받았는데 두 명 다 만족했어요. 향도 좋고 압도 딱 맞았습니다.", "마포구 · 커플 이용"),
        ("★★★★★", "출장 와서 호텔에서 받았는데 여독이 싹 풀렸어요. 시간 약속도 정확했습니다.", "중구 · 출장 고객"),
    ]
    review_html = "".join(
        f'<div class="review reveal"><div class="stars">{s}</div><p>"{t}"</p><div class="who">{w}</div></div>'
        for s, t, w in reviews)

    notes = [
        ("01", "이동·대기 없는 방문 관리", "예약한 시간에 관리사가 직접 방문해 익숙한 공간에서 바로 휴식할 수 있습니다."),
        ("02", "투명한 정찰 요금", "60·90·120분 정찰 요금을 사전에 안내드립니다. 임의 추가 요금은 없습니다."),
        ("03", "철저한 위생·안전", "타월은 매회 교체하고 도구는 위생적으로 관리합니다. 건강관리 목적의 정중한 관리만 제공합니다."),
    ]
    note_html = "".join(
        f'<div class="note-card reveal"><div class="note-num">{n}</div><div class="note-text">'
        f'<div class="note-title">{t}</div><p>{d}</p></div></div>'
        for n, t, d in notes)

    body = f"""
<section class="hero"><div class="hero-inner">
  <div class="hero-text">
    <span class="eyebrow"><span class="pulse"></span>SEOUL · 출장마사지 · 홈타이</span>
    <h1>집에서 받는 <span class="grad">프리미엄</span> 출장마사지</h1>
    <p class="lead">서울 전역 어디든 방문합니다. 스웨디시·아로마·타이·스포츠까지, 원하는 코스를 예약한 시간에 편안하게 받아보세요.</p>
    <div class="actions">
      <a class="btn btn-primary" href="tel:{lib.PHONE_T}">{lib.PHONE_D} 예약하기</a>
      <a class="btn btn-ghost" href="/course/">코스 둘러보기</a>
    </div>
    <div class="trust">
      <span><b>연중무휴</b> 24시간 상담</span>
      <span><b>서울 25개 구</b> 전역 방문</span>
      <span><b>정찰 요금</b> 사전 안내</span>
    </div>
  </div>
  <div class="hero-visual">
    <div class="glass">
      <h3>오늘의 예약<b>지금 바로 가능</b></h3>
      <div class="book-row"><span>60분 코스</span><span>90,000원</span></div>
      <div class="book-row"><span>90분 코스</span><span>150,000원</span></div>
      <div class="book-row"><span>120분 코스</span><span>180,000원</span></div>
      <a class="bk" href="tel:{lib.PHONE_T}">전화로 예약하기</a>
    </div>
    <div class="floating fl-1"><span class="dot"></span>지금 예약 접수 중</div>
    <div class="floating fl-2">서울 전역 방문 가능</div>
  </div>
</div></section>

<div class="marquee"><div class="marquee-track">
  <span>스웨디시</span><span>아로마테라피</span><span>타이마사지</span><span>로미로미</span><span>스포츠·경락</span>
  <span>발마사지</span><span>홈케어</span><span>호텔식마사지</span><span>커플 관리</span><span>24시간</span>
  <span>스웨디시</span><span>아로마테라피</span><span>타이마사지</span><span>로미로미</span><span>스포츠·경락</span>
  <span>발마사지</span><span>홈케어</span><span>호텔식마사지</span><span>커플 관리</span><span>24시간</span>
</div></div>

<section class="block" id="region"><div class="wrap">
  <span class="eyebrow"><span class="pulse"></span>AREA</span>
  <h2 class="sec">서울 전역 어디든 방문합니다</h2>
  <p class="sec-lead">강남권부터 서북권까지 6개 권역 25개 자치구로 출장합니다. 가까운 지역을 선택해 안내를 확인하세요.</p>
  <div style="margin-top:30px">{cards(region_cards)}</div>
</div></section>

<section class="block" id="theme" style="padding-top:0"><div class="wrap">
  <span class="eyebrow"><span class="pulse"></span>THEME</span>
  <h2 class="sec">원하는 테마로 골라보세요</h2>
  <p class="sec-lead">컨디션과 목적에 맞춰 다양한 관리 테마를 제공합니다.</p>
  <div style="margin-top:30px">{cards(theme_cards)}</div>
  <div style="margin-top:18px"><a class="btn btn-ghost" href="/theme/">전체 테마 보기 →</a></div>
</div></section>

<section class="block" id="price" style="padding-top:0"><div class="wrap">
  <span class="eyebrow"><span class="pulse"></span>PRICE</span>
  <h2 class="sec">코스별 기본 요금</h2>
  <p class="sec-lead">시간에 따라 관리 범위가 달라집니다. 처음이라면 90분 코스를 추천드립니다.</p>
  {lib.pmenu()}
</div></section>

<section class="block" id="process" style="padding-top:0"><div class="wrap">
  <span class="eyebrow"><span class="pulse"></span>WHY</span>
  <h2 class="sec">웰니스센터를 선택하는 이유</h2>
  <div class="note-stack" style="margin-top:30px">{note_html}</div>
</div></section>

<section class="block" id="reviews" style="padding-top:0"><div class="wrap">
  <span class="eyebrow"><span class="pulse"></span>REVIEW</span>
  <h2 class="sec">고객 후기</h2>
  <div class="grid g3" style="margin-top:30px">{review_html}</div>
  <div style="margin-top:18px"><a class="btn btn-ghost" href="/reviews/">후기 더 보기 →</a></div>
</div></section>
"""
    faq = [
        ("출장 지역은 어디까지인가요", "서울 25개 자치구 전역으로 방문하며, 일부 인근 지역도 가능합니다. 자세한 내용은 예약 시 확인해 드립니다."),
        ("예약은 어떻게 하나요", f"전화 한 통이면 됩니다. {lib.PHONE_D}로 원하는 시간·코스·주소를 알려주세요."),
        ("심야에도 이용할 수 있나요", "네. 연중무휴 24시간 상담·예약이 가능합니다."),
        ("요금 외 추가 비용이 있나요", "기본은 정찰 요금이며, 코스·지역 차이는 예약 시 미리 안내해 임의 추가는 없습니다."),
    ]
    body += lib.faq_block(faq)
    body += lib.cta_band("지금 바로 예약하세요", "연중무휴 · 24시간 상담 · 서울 전역 출장 가능합니다.")
    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "LocalBusiness",
        "name": lib.SITE, "telephone": lib.PHONE_D, "url": lib.DOMAIN,
        "image": lib.OG_IMG, "areaServed": "서울특별시",
        "priceRange": "₩₩", "openingHours": "Mo-Su 00:00-24:00",
    }, ensure_ascii=False)
    desc = "서울 전역 출장마사지·홈타이 안내. 스웨디시·아로마·타이·스포츠 코스를 예약한 시간에 편안하게. 연중무휴 24시간 상담."
    add("/", lib.document("서울 출장마사지·홈타이 24시간 예약 안내", desc, "/", body, jsonld=jsonld), "1.0", "daily")


# ────────────────────────── 서울 허브 / 지역 ──────────────────────────
def build_seoul_hub():
    # /seoul/
    secs = [
        ("서울 출장마사지 안내", lib.P(
            "웰니스센터는 서울 25개 자치구 전역으로 방문하는 출장마사지·홈타이 서비스입니다. "
            "관리사가 자택·호텔·오피스텔로 직접 방문해 익숙한 공간에서 편안하게 관리받으실 수 있습니다.",
            "스웨디시·아로마·타이·스포츠 등 원하는 코스를 예약한 시간에 받아보세요.")),
        ("서울 홈타이 안내", lib.P(
            "홈타이는 집에서 받는 타이식 스트레칭·지압 관리입니다. 옷을 입은 채 진행되어 부담이 적고 "
            "활력 회복에 좋습니다. 자세한 내용은 <a href='/theme/thai-massage/'>타이마사지</a>와 "
            "<a href='/course/home/'>홈타이 코스</a>를 참고하세요.")),
        ("서울 전지역 출장 가능 안내", lib.P(
            "강남권·강서권·서남권·동북권·도심권·서북권 6개 권역 어디든 방문합니다. "
            "가까운 지역은 <a href='/seoul/area/'>지역별 안내</a>에서 확인하세요.")),
        ("지하철역 인근 안내", lib.P(
            "주요 지하철역 인근은 접근성이 좋아 빠른 방문이 가능합니다. "
            "<a href='/seoul/stations/'>지하철역별 안내</a>에서 가까운 역을 찾아보세요.")),
    ]
    # id 매핑(메뉴 앵커용): home/allarea/station
    secs_html = (
        f'<section class="lux-sec reveal" id="sec-1"><h2>{secs[0][0]}</h2>{secs[0][1]}</section>'
        f'<section class="lux-sec reveal" id="home"><h2>{secs[1][0]}</h2>{secs[1][1]}</section>'
        f'<section class="lux-sec reveal" id="allarea"><h2>{secs[2][0]}</h2>{secs[2][1]}</section>'
        f'<section class="lux-sec reveal" id="station"><h2>{secs[3][0]}</h2>{secs[3][1]}</section>')
    toc = ('<li><a href="#sec-1">서울 출장마사지 안내</a></li>'
           '<li><a href="#home">홈타이 안내</a></li>'
           '<li><a href="#allarea">전지역 출장</a></li>'
           '<li><a href="#station">지하철역 인근</a></li>')
    body = (lib.crumb([("/", "홈"), (None, "서울 출장마사지")])
            + lib.lux_hero("SEOUL · 출장마사지", "서울 출장마사지·홈타이 안내",
                "서울 전역으로 방문하는 출장마사지·홈타이. 원하는 코스를 예약한 시간에 편안하게 받아보세요.")
            + '<section class="block lux-body" style="padding-top:34px"><div class="wrap"><div class="lux-grid">'
            + f'<aside class="toc"><div class="toc-inner"><span class="toc-label">목차</span><ul>{toc}</ul></div></aside>'
            + f'<div class="lux-main">{secs_html}</div></div></div></section>')
    body += lib.cta_band()
    add("/seoul/", lib.document("서울 출장마사지·홈타이 안내",
        "서울 25개 자치구 전역 출장마사지·홈타이 안내. 스웨디시·아로마·타이·스포츠 코스를 예약한 시간에.",
        "/seoul/", body), "0.9", "weekly")

    # /seoul/faq/
    faq = [
        ("출장 지역은 어디까지인가요", "서울 25개 자치구 전역으로 방문합니다. 인근 지역도 가능 여부를 안내해 드립니다."),
        ("예약은 얼마나 미리 해야 하나요", "당일 예약도 시간대에 따라 가능합니다. 원하는 시간이 있으면 미리 문의해 주세요."),
        ("코스는 어떻게 고르나요", "처음이면 90분 스웨디시가 무난합니다. <a href='/course/guide/'>코스 선택 가이드</a>를 참고하세요."),
        ("결제는 어떻게 하나요", "<a href='/reservation/payment/'>결제 안내</a> 페이지에서 확인하실 수 있습니다."),
        ("위생은 어떻게 관리되나요", "타월은 매회 교체하고 도구는 위생적으로 관리합니다. <a href='/guide/safety/'>위생 및 안전 기준</a> 참고."),
        ("심야에도 가능한가요", "네. 연중무휴 24시간 상담·예약이 가능합니다."),
    ]
    fbody = (lib.crumb([("/", "홈"), ("/seoul/", "서울 출장마사지"), (None, "자주 묻는 질문")])
             + lib.lux_hero("FAQ", "서울 출장마사지 자주 묻는 질문",
                "예약·지역·코스·요금·위생 등 자주 묻는 질문을 모았습니다.", actions=False)
             + lib.faq_block(faq) + lib.cta_band())
    add("/seoul/faq/", lib.document("서울 출장마사지 자주 묻는 질문",
        "서울 출장마사지 예약·지역·코스·요금·위생 관련 자주 묻는 질문 모음.",
        "/seoul/faq/", fbody, jsonld=lib.faq_jsonld(faq)), "0.6", "monthly")

    # /seoul/area/ (권역·자치구 허브)
    blocks = []
    toc_items = []
    for rk, rl, gus in data.REGIONS:
        gu_cards = "".join(
            f'<a class="card reveal" href="/seoul/{slug}/"><div class="k">{rl}</div>'
            f'<h3>{name} 출장마사지</h3><p>{name} 전역 방문 관리 안내</p>'
            f'<span class="more">자세히 →</span></a>' for slug, name in gus)
        blocks.append(f'<section class="lux-sec reveal" id="{rk}"><h2>{rl}</h2>'
                      f'<p>{rl}에 속한 자치구의 출장마사지 안내입니다.</p>'
                      f'<div class="grid g3">{gu_cards}</div></section>')
        toc_items.append(f'<li><a href="#{rk}">{rl}</a></li>')
    abody = (lib.crumb([("/", "홈"), ("/seoul/", "서울 출장마사지"), (None, "지역별 안내")])
             + lib.lux_hero("AREA", "서울 지역별 출장마사지 안내",
                "강남권부터 서북권까지 6개 권역 25개 자치구로 방문합니다. 가까운 지역을 선택하세요.")
             + '<section class="block lux-body" style="padding-top:34px"><div class="wrap"><div class="lux-grid">'
             + f'<aside class="toc"><div class="toc-inner"><span class="toc-label">권역</span><ul>{"".join(toc_items)}</ul></div></aside>'
             + f'<div class="lux-main">{"".join(blocks)}</div></div></div></section>'
             + lib.cta_band())
    add("/seoul/area/", lib.document("서울 지역별 출장마사지 안내",
        "서울 6개 권역 25개 자치구 출장마사지 안내. 강남권·강서권·서남권·동북권·도심권·서북권.",
        "/seoul/area/", abody), "0.8", "weekly")


# ────────────────────────── 자치구 25 ──────────────────────────
def build_districts():
    for slug, name in data.ALL_GU:
        _, rk, rl = data.GU_BY_SLUG[slug]
        areas = data.GU_AREAS.get(slug, [])
        area_txt = " · ".join(areas) if areas else f"{name} 전 지역"
        secs = [
            (f"{name} 출장마사지 안내", lib.P(
                f"웰니스센터는 {name} 전역으로 방문하는 출장마사지·홈타이 서비스입니다. "
                f"{area_txt} 등 어디든 관리사가 직접 방문해 익숙한 공간에서 편안하게 관리해 드립니다.",
                f"이동·대기 없이 예약한 시간에 바로 휴식할 수 있어 {name} 주민과 직장인분들께 특히 편리합니다.")),
            ("주요 생활권 방문", "<ul>" + "".join(f"<li>{a} 일대 방문 관리</li>" for a in (areas or [f'{name} 전역'])) + "</ul>"
                + lib.P(f"위 지역 외에도 {name} 전역으로 방문하니 편하게 문의해 주세요.")),
            ("추천 코스", lib.P(
                "업무·일상 피로엔 <a href='/course/fatigue/'>피로 회복 관리</a>, 긴장 완화엔 "
                "<a href='/theme/aroma-therapy/'>아로마테라피</a>, 근육 뭉침엔 "
                "<a href='/course/sports/'>스포츠 관리</a>를 권해 드립니다. 처음이라면 90분 스웨디시가 무난합니다.")),
            ("예약 안내", lib.P(
                f"전화 한 통이면 됩니다. {lib.PHONE_D}로 원하는 시간·코스·주소를 알려주세요. "
                "연중무휴 24시간 상담이 가능합니다.")),
        ]
        related = [(f"/seoul/area/#{rk}", f"{rl} 전체 보기"), ("/course/price/", "가격 안내"),
                   ("/theme/swedish/", "스웨디시 안내"), ("/reservation/", "예약 방법")]
        faq = [
            (f"{name} 전역 방문되나요", f"네. {name} 전 지역으로 방문하며 예약 시 정확한 위치를 확인합니다."),
            ("심야에도 가능한가요", "네. 24시간 예약이 가능합니다."),
            ("요금은 얼마인가요", "60분 90,000원, 90분 150,000원, 120분 180,000원 정찰 요금 기준입니다."),
        ]
        lux_page(f"{name} 출장마사지", f"{name} 출장마사지·홈타이 방문 안내. {area_txt} 전역 방문, 정찰 요금, 24시간 예약.",
                 f"/seoul/{slug}/", f"{rl} · {name}", f"{name} 출장마사지 안내",
                 f"{name} 전역으로 방문하는 출장마사지·홈타이. {area_txt} 어디든 예약한 시간에 편안하게.",
                 secs, [("/", "홈"), ("/seoul/area/", "지역별 안내"), (None, name)],
                 faq=faq, related=related, jsonld=lib.faq_jsonld(faq), prio="0.7")


# ────────────────────────── 지하철역 ──────────────────────────
def build_stations():
    allst = data.all_stations()
    # /seoul/stations/ 허브
    line_cards = "".join(
        f'<a class="card reveal" href="/seoul/stations/{ls}/"><div class="k">LINE</div>'
        f'<h3>{ll}</h3><p>{ll} 주요 역 인근 출장마사지 안내</p><span class="more">역 보기 →</span></a>'
        for ls, ll, _ in data.LINES)
    hbody = (lib.crumb([("/", "홈"), ("/seoul/", "서울 출장마사지"), (None, "지하철역별 안내")])
             + lib.lux_hero("STATION", "서울 지하철역별 출장마사지 안내",
                f"호선별로 주요 역 인근 출장마사지를 안내합니다. 총 {len(allst)}개 역 인근으로 방문합니다.")
             + '<section class="block"><div class="wrap"><div class="grid g3">' + line_cards + '</div></div></section>'
             + lib.cta_band())
    add("/seoul/stations/", lib.document("서울 지하철역별 출장마사지 안내",
        "서울 지하철 호선별 주요 역 인근 출장마사지 안내. 역세권 빠른 방문.",
        "/seoul/stations/", hbody), "0.8", "weekly")

    # 노선별 허브
    for ls, ll, _ in data.LINES:
        _, sts = data.line_stations(ls)
        st_cards = "".join(
            f'<a class="card reveal" href="/seoul/stations/{st}-station/"><div class="k">{ll}</div>'
            f'<h3>{data.station_name(st)}역</h3><p>{data.station_name(st)}역 인근 출장마사지</p>'
            f'<span class="more">자세히 →</span></a>' for st in sts)
        lbody = (lib.crumb([("/", "홈"), ("/seoul/stations/", "지하철역별 안내"), (None, ll)])
                 + lib.lux_hero(f"LINE · {ll}", f"{ll} 출장마사지 안내",
                    f"{ll} 주요 역 인근 출장마사지를 안내합니다. 역 인근 어디든 빠르게 방문합니다.")
                 + '<section class="block"><div class="wrap"><div class="grid g3">' + st_cards + '</div></div></section>'
                 + lib.cta_band())
        add(f"/seoul/stations/{ls}/", lib.document(f"{ll} 출장마사지 안내",
            f"{ll} 주요 역 인근 출장마사지·홈타이 방문 안내.", f"/seoul/stations/{ls}/", lbody), "0.6", "weekly")

    # 역별 페이지
    for st, sname, ls, ll in allst:
        secs = [
            (f"{sname}역 인근 출장마사지", lib.P(
                f"{sname}역 인근으로 방문하는 출장마사지·홈타이 안내입니다. 역세권은 도로 연결이 좋아 "
                f"예약 시간에 맞춘 빠른 방문이 가능합니다. {sname}역 주변 자택·오피스텔·숙소 어디든 방문합니다.")),
            ("이용 안내", lib.P(
                f"{sname}역 인근에서 받을 수 있는 코스는 스웨디시·아로마·타이·스포츠 등 다양합니다. "
                "오피스텔·호텔이라면 동·호수와 가까운 출구 번호를 알려주시면 더 빠릅니다.")),
            ("추천 코스·예약", lib.P(
                "처음이면 90분 스웨디시가 무난합니다. 깊은 이완을 원하면 120분 코스를 권합니다. "
                f"예약은 {lib.PHONE_D}로, 연중무휴 24시간 상담 가능합니다.")),
        ]
        related = [(f"/seoul/stations/{ls}/", f"{ll} 전체 역"), ("/theme/swedish/", "스웨디시 안내"),
                   ("/course/price/", "가격 안내"), ("/reservation/", "예약 방법")]
        faq = [
            (f"{sname}역에서 얼마나 걸리나요", "역 인근은 빠른 방문이 가능하며 출발·도착 시 연락드립니다."),
            ("호텔·오피스텔도 되나요", "네. 자택·호텔·오피스텔 모두 방문 가능합니다."),
        ]
        lux_page(f"{sname}역 출장마사지", f"{sname}역({ll}) 인근 출장마사지·홈타이 방문 안내. 역세권 빠른 방문, 24시간 예약.",
                 f"/seoul/stations/{st}-station/", f"{ll} · {sname}역", f"{sname}역 출장마사지 안내",
                 f"{sname}역 인근으로 방문하는 출장마사지·홈타이. 역세권 빠른 방문, 예약한 시간에 편안하게.",
                 secs, [("/", "홈"), ("/seoul/stations/", "지하철역별 안내"), (f"/seoul/stations/{ls}/", ll), (None, sname + "역")],
                 faq=faq, related=related, jsonld=lib.faq_jsonld(faq), prio="0.6")


# ────────────────────────── 테마 14 ──────────────────────────
def build_themes():
    t_cards = "".join(
        f'<a class="card reveal" href="/theme/{s}/"><div class="k">THEME</div>'
        f'<h3>{n}</h3><p>{d}</p><span class="more">자세히 →</span></a>' for s, n, d in data.THEMES)
    hbody = (lib.crumb([("/", "홈"), (None, "테마별 안내")])
             + lib.lux_hero("THEME", "테마별 출장마사지 안내",
                "컨디션과 목적에 맞춰 다양한 관리 테마를 제공합니다. 원하는 테마를 선택하세요.")
             + '<section class="block"><div class="wrap"><div class="grid g3">' + t_cards + '</div></div></section>'
             + lib.cta_band())
    add("/theme/", lib.document("테마별 출장마사지 안내", "스웨디시·아로마·타이·로미로미·스포츠 등 테마별 출장마사지 안내.",
        "/theme/", hbody), "0.8", "weekly")

    for s, n, d in data.THEMES:
        secs = [
            (f"{n}란?", lib.P(f"{n}는 {d}입니다. 웰니스센터에서는 고객의 컨디션에 맞춰 압과 시간을 조절해 진행합니다.")),
            ("이런 분께 추천", lib.P(
                f"{n}는 목적에 맞는 분께 특히 잘 맞습니다. 처음이라면 90분 코스로 부담 없이 체험해 보세요. "
                "압·집중 부위는 편하게 요청하실 수 있습니다.")),
            ("이용·예약 안내", lib.P(
                f"방문 관리로 자택·호텔·오피스텔 어디든 받으실 수 있습니다. 요금은 "
                "<a href='/course/price/'>가격 안내</a>를 참고하시고, 예약은 "
                f"{lib.PHONE_D}로 24시간 가능합니다.")),
        ]
        related = [("/theme/", "전체 테마"), ("/course/guide/", "코스 선택 가이드"),
                   ("/course/price/", "가격 안내"), ("/reservation/", "예약 방법")]
        faq = [
            (f"{n}는 처음도 괜찮나요", "네. 컨디션에 맞춰 진행하니 부담 없이 받으실 수 있습니다."),
            ("압 조절이 되나요", "네. 진행 중 편하게 요청하시면 조절해 드립니다."),
        ]
        lux_page(f"{n} 출장마사지", f"{n} 출장마사지 안내 — {d}. 방문 관리, 정찰 요금, 24시간 예약.",
                 f"/theme/{s}/", "THEME", f"{n} 안내", d + "입니다.",
                 secs, [("/", "홈"), ("/theme/", "테마별 안내"), (None, n)],
                 faq=faq, related=related, jsonld=lib.faq_jsonld(faq), prio="0.7")


# ────────────────────────── 코스 8 ──────────────────────────
def build_courses():
    c_cards = "".join(
        f'<a class="card reveal" href="/course/{s}/"><div class="k">COURSE</div>'
        f'<h3>{n}</h3><p>{d}</p><span class="more">자세히 →</span></a>' for s, n, d in data.COURSES)
    hbody = (lib.crumb([("/", "홈"), (None, "코스안내")])
             + lib.lux_hero("COURSE", "코스 안내", "목적에 맞는 다양한 코스를 제공합니다. 처음이라면 코스 선택 가이드를 참고하세요.")
             + '<section class="block"><div class="wrap"><div class="grid g3">' + c_cards + '</div></div></section>'
             + '<section class="block" style="padding-top:0"><div class="wrap">'
             + '<span class="eyebrow"><span class="pulse"></span>PRICE</span><h2 class="sec">코스별 기본 요금</h2>'
             + lib.pmenu() + '</div></section>'
             + lib.cta_band())
    add("/course/", lib.document("코스 안내", "피로 회복·아로마·스포츠·홈타이·커플·단체 등 출장마사지 코스 안내와 가격.",
        "/course/", hbody), "0.8", "weekly")

    for s, n, d in data.COURSES:
        if s == "price":
            secs = [
                ("코스별 기본 요금", lib.pmenu(note=False) + lib.P(
                    "표시 요금은 기본 정찰가입니다. 코스·인원·지역에 따라 달라질 수 있으며 예약 시 정확히 안내해 드립니다.")),
                ("시간별 차이", lib.P(
                    "60분은 핵심 부위 위주, 90분은 전신 균형, 120분은 머리부터 발끝까지 집중 관리에 적합합니다.")),
                ("결제 안내", lib.P("결제 방법은 <a href='/reservation/payment/'>결제 안내</a>에서 확인하실 수 있습니다.")),
            ]
        elif s == "guide":
            secs = [
                ("처음이라면", lib.P("어떤 코스가 맞을지 고민이라면 목적부터 정해 보세요. 피로 해소, 긴장 완화, 근육 뭉침 등 목적에 따라 추천이 달라집니다.")),
                ("목적별 추천", "<ul>"
                    "<li>전신 피로 해소 → <a href='/course/fatigue/'>피로 회복 관리</a></li>"
                    "<li>스트레스·불면 → <a href='/theme/aroma-therapy/'>아로마 관리</a></li>"
                    "<li>근육 뭉침 → <a href='/course/sports/'>스포츠 관리</a></li>"
                    "<li>활력·유연성 → <a href='/theme/thai-massage/'>타이마사지</a></li></ul>"),
                ("시간 선택", lib.P("처음이면 90분이 무난합니다. 충분한 이완을 원하면 120분을 권합니다.")),
            ]
        else:
            secs = [
                (f"{n}란?", lib.P(f"{n}는 {d}입니다. 고객의 컨디션에 맞춰 압과 범위를 조절해 진행합니다.")),
                ("이용 안내", lib.P(
                    "방문 관리로 자택·호텔·오피스텔 어디서든 받으실 수 있습니다. 집중하고 싶은 부위가 있으면 미리 말씀해 주세요.")),
                ("요금·예약", lib.P(
                    "요금은 <a href='/course/price/'>가격 안내</a>를 참고하세요. 예약은 "
                    f"{lib.PHONE_D}로 연중무휴 24시간 가능합니다.")),
            ]
        related = [("/course/", "전체 코스"), ("/course/price/", "가격 안내"),
                   ("/course/guide/", "코스 선택 가이드"), ("/reservation/", "예약 방법")]
        faq = [
            (f"{n}는 얼마인가요" if s not in ("price", "guide") else "요금이 궁금해요",
             "60분 90,000원, 90분 150,000원, 120분 180,000원 정찰 요금 기준입니다."),
            ("예약은 어떻게 하나요", f"{lib.PHONE_D}로 전화 주시면 24시간 안내해 드립니다."),
        ]
        lux_page(n, f"{n} — {d}. 출장마사지 방문 관리, 정찰 요금, 24시간 예약 안내.",
                 f"/course/{s}/", "COURSE", n, d + "입니다.",
                 secs, [("/", "홈"), ("/course/", "코스안내"), (None, n)],
                 faq=faq, related=related, jsonld=lib.faq_jsonld(faq), prio="0.7")


# ────────────────────────── 예약 / 가이드 / 후기 / 고객센터 ──────────────────────────
RES_CONTENT = {
    "": ("예약 방법", [
        ("예약 방법", lib.P(f"예약은 전화 한 통이면 됩니다. {lib.PHONE_D}로 원하는 날짜·시간, 방문 주소, 코스와 인원을 알려주세요. 연중무휴 24시간 상담이 가능합니다.")),
        ("예약 시 알려주실 정보", "<ul><li>희망 날짜·시간</li><li>방문 주소(동·호수, 가까운 출구)</li><li>코스·시간</li><li>인원</li><li>요청 사항(여성 관리사 등)</li></ul>"),
        ("진행 안내", lib.P("예약이 확정되면 관리사가 출발·도착 시 연락드립니다. 변경이 필요하면 가능한 빨리 알려주세요.")),
    ]),
    "hours/": ("예약 가능 시간", [
        ("운영 시간", lib.P("연중무휴 24시간 상담·예약이 가능합니다. 주말·공휴일에도 동일하게 운영합니다.")),
        ("추천 시간대", lib.P("저녁·심야 시간대는 예약이 몰리는 편입니다. 원하는 시간이 있으면 미리 문의해 주세요.")),
        ("당일 예약", lib.P("당일 예약도 시간대에 따라 가능합니다. 전화로 가능 여부를 확인해 드립니다.")),
    ]),
    "place/": ("방문 가능 장소", [
        ("방문 가능 장소", lib.P("자택·아파트·오피스텔·원룸·호텔·숙소 등 베드를 놓을 공간이 있으면 어디든 방문합니다.")),
        ("공간 안내", lib.P("약 2㎡ 정도의 평평한 공간이면 충분합니다. 주변 물건만 살짝 정리해 주세요.")),
        ("호텔 이용", lib.P("호텔은 객실 호수와 체류 일정을 알려주세요. <a href='/theme/hotel-massage/'>호텔식마사지</a>를 참고하세요.")),
    ]),
    "payment/": ("결제 안내", [
        ("요금 기준", lib.pmenu(note=False)),
        ("결제 안내", lib.P("결제 방법은 예약 시 안내해 드립니다. 표시 요금은 정찰가이며 코스·지역에 따른 차이는 사전에 안내해 임의 추가는 없습니다.")),
    ]),
    "change/": ("변경·취소 안내", [
        ("변경 안내", lib.P("일정 변경이 필요하면 가능한 빨리 연락해 주세요. 가능한 시간대로 다시 안내해 드립니다.")),
        ("취소 안내", lib.P("취소도 미리 알려주시면 원활합니다. 임박한 취소는 일정 조율이 어려울 수 있으니 양해 부탁드립니다.")),
    ]),
    "checklist/": ("예약 전 체크사항", [
        ("예약 전 확인", "<ul><li>코스·시간·요금 확인</li><li>방문 주소·출구 정리</li><li>방문 공간 확보</li><li>요청 사항 정리</li></ul>"),
        ("처음이라면", lib.P("처음이면 90분 스웨디시가 무난합니다. <a href='/course/guide/'>코스 선택 가이드</a>를 참고하세요.")),
    ]),
}

def build_reservation():
    cards_html = "".join(
        f'<a class="card reveal" href="/reservation/{p}"><div class="k">RESERVE</div><h3>{n}</h3>'
        f'<p>{n} 안내</p><span class="more">자세히 →</span></a>' for p, n in data.RESERVATION_PAGES if p)
    for p, n in data.RESERVATION_PAGES:
        title, secs = RES_CONTENT[p]
        related = [("/reservation/", "예약 방법"), ("/reservation/hours/", "예약 가능 시간"),
                   ("/reservation/payment/", "결제 안내"), ("/course/guide/", "코스 선택 가이드")]
        extra = ('<section class="block" style="padding-top:0"><div class="wrap"><div class="grid g3">'
                 + cards_html + '</div></div></section>') if p == "" else ""
        lux_page(title, f"{title} — 웰니스센터 출장마사지 예약 안내. 연중무휴 24시간.",
                 f"/reservation/{p}", "RESERVATION", title,
                 f"{title}를 안내합니다." if False else f"{title} 안내입니다.",
                 secs, [("/", "홈"), ("/reservation/", "예약안내")] + ([] if p == "" else [(None, n)]),
                 related=related, prio="0.7")
    # 허브에 카드 섹션을 덧붙이기 위해 별도 처리: 위 루프의 p=="" 페이지에 extra가 빠졌으므로 재생성
    title, secs = RES_CONTENT[""]
    body = (lib.crumb([("/", "홈"), (None, "예약안내")])
            + lib.lux_hero("RESERVATION", "예약 안내", "예약 방법부터 시간·장소·결제·변경까지 한 곳에서 안내합니다.")
            + '<section class="block lux-body" style="padding-top:34px"><div class="wrap"><div class="lux-grid">'
            + '<aside class="toc"><div class="toc-inner"><span class="toc-label">목차</span><ul>'
            + "".join(f'<li><a href="#sec-{i}">{esc(h)}</a></li>' for i,(h,_) in enumerate(secs,1))
            + '</ul></div></aside><div class="lux-main">' + lux_sections(secs) + '</div></div></div></section>'
            + '<section class="block" style="padding-top:0"><div class="wrap"><div class="grid g3">' + cards_html + '</div></div></section>'
            + lib.cta_band())
    write("/reservation/", lib.document("예약 안내", "웰니스센터 출장마사지 예약 방법·시간·장소·결제·변경 안내. 연중무휴 24시간.", "/reservation/", body))


GUIDE_CONTENT = {
    "": ("처음 이용하시는 분", [
        ("처음 이용 안내", lib.P("출장마사지가 처음이라도 걱정하지 마세요. 예약부터 관리, 마무리까지 관리사가 차근히 안내해 드립니다.")),
        ("진행 순서", lib.P("예약 → 방문 → 컨디션 확인 → 관리 → 마무리 순으로 진행됩니다. 압·집중 부위는 편하게 요청하세요.")),
        ("추천 코스", lib.P("처음이면 90분 스웨디시가 무난합니다. <a href='/course/guide/'>코스 선택 가이드</a> 참고.")),
    ]),
    "prepare/": ("방문 전 준비사항", [
        ("준비할 것", "<ul><li>샤워 후 편안한 상태</li><li>베드 놓을 공간(약 2㎡)</li><li>주소·출구 정리</li></ul>"),
        ("알려주실 점", lib.P("반려동물·주의 사항이 있으면 미리 알려주세요. 용품은 관리사가 준비해 옵니다.")),
    ]),
    "safety/": ("위생 및 안전 기준", [
        ("위생 기준", lib.P("타월은 매회 새것으로 교체하고 오일·도구는 위생적으로 관리합니다. 관리사는 손 위생을 철저히 한 뒤 시작합니다.")),
        ("안전 기준", lib.P("본 서비스는 만 19세 이상 성인 대상 건강관리 목적의 방문 관리이며 불법·퇴폐 행위는 일절 제공하지 않습니다.")),
        ("여성 고객 안내", lib.P("여성 관리사 배정을 원하면 예약 시 요청해 주세요.")),
    ]),
    "aftercare/": ("관리 후 주의사항", [
        ("관리 후", "<ul><li>따뜻한 물 충분히 섭취</li><li>격한 운동·음주 자제</li><li>충분한 휴식·수면</li></ul>"),
        ("효과 유지", lib.P("관리 후 숙면을 취하면 회복 효과가 더 좋습니다. 통증이 지속되면 의료기관 진료를 권해 드립니다.")),
    ]),
    "forbidden/": ("금지행위 안내", [
        ("금지행위", lib.P("본 서비스는 건강관리 목적의 방문 관리입니다. 불법·퇴폐 행위 요구는 일절 응대하지 않으며, 관리사 보호를 위해 부적절한 언행 시 관리가 중단될 수 있습니다.")),
        ("상호 존중", lib.P("관리사와 고객 모두의 안전과 존중을 위한 기준이니 양해 부탁드립니다.")),
    ]),
    "checklist/": ("이용 전 확인사항", [
        ("이용 전 확인", "<ul><li>코스·요금 확인</li><li>방문 공간 확보</li><li>요청 사항 정리</li><li>주소·출구 안내</li></ul>"),
        ("문의", lib.P(f"궁금한 점은 {lib.PHONE_D}로 24시간 문의하실 수 있습니다.")),
    ]),
    "faq/": ("이용 FAQ", None),  # FAQ 전용
}

def build_guide():
    cards_html = "".join(
        f'<a class="card reveal" href="/guide/{p}"><div class="k">GUIDE</div><h3>{n}</h3>'
        f'<p>{n} 안내</p><span class="more">자세히 →</span></a>' for p, n in data.GUIDE_PAGES if p)
    guide_faq = [
        ("관리 시간은 얼마나 걸리나요", "선택한 코스에 따라 60·90·120분입니다. 준비·정리 시간이 추가로 약간 소요됩니다."),
        ("준비물이 필요한가요", "거의 없습니다. 베드를 놓을 공간만 확보해 주세요."),
        ("압 조절이 가능한가요", "네. 진행 중 편하게 요청하시면 조절해 드립니다."),
        ("여성 관리사를 요청할 수 있나요", "네. 예약 시 요청하시면 가능 여부를 안내해 드립니다."),
        ("결제는 어떻게 하나요", "결제 방법은 <a href='/reservation/payment/'>결제 안내</a>에서 확인하실 수 있습니다."),
    ]
    for p, n in data.GUIDE_PAGES:
        if p == "faq/":
            fbody = (lib.crumb([("/", "홈"), ("/guide/", "이용가이드"), (None, "이용 FAQ")])
                     + lib.lux_hero("FAQ", "이용 FAQ", "이용과 관련해 자주 묻는 질문을 모았습니다.", actions=False)
                     + lib.faq_block(guide_faq) + lib.cta_band())
            add("/guide/faq/", lib.document("이용 FAQ", "웰니스센터 출장마사지 이용 관련 자주 묻는 질문.",
                "/guide/faq/", fbody, jsonld=lib.faq_jsonld(guide_faq)), "0.6", "monthly")
            continue
        title, secs = GUIDE_CONTENT[p]
        related = [("/guide/", "이용가이드 전체"), ("/guide/safety/", "위생 및 안전"),
                   ("/reservation/", "예약 방법"), ("/course/guide/", "코스 선택 가이드")]
        if p == "":
            body = (lib.crumb([("/", "홈"), (None, "이용가이드")])
                    + lib.lux_hero("GUIDE", "이용가이드", "처음 이용부터 준비·위생·관리 후 주의까지 한 곳에서 안내합니다.")
                    + '<section class="block lux-body" style="padding-top:34px"><div class="wrap"><div class="lux-grid">'
                    + '<aside class="toc"><div class="toc-inner"><span class="toc-label">목차</span><ul>'
                    + "".join(f'<li><a href="#sec-{i}">{esc(h)}</a></li>' for i,(h,_) in enumerate(secs,1))
                    + '</ul></div></aside><div class="lux-main">' + lux_sections(secs) + '</div></div></div></section>'
                    + '<section class="block" style="padding-top:0"><div class="wrap"><div class="grid g3">' + cards_html + '</div></div></section>'
                    + lib.cta_band())
            add("/guide/", lib.document("이용가이드", "웰니스센터 출장마사지 이용가이드 — 처음 이용·준비·위생·안전·관리 후 주의.",
                "/guide/", body), "0.8", "weekly")
        else:
            lux_page(title, f"{title} — 웰니스센터 출장마사지 이용가이드.",
                     f"/guide/{p}", "GUIDE", title, f"{title} 안내입니다.",
                     secs, [("/", "홈"), ("/guide/", "이용가이드"), (None, n)],
                     related=related, prio="0.6")


def build_reviews():
    revs = [
        ("강남구 · 30대 직장인", "퇴근 후 집에서 바로 받을 수 있어 편했어요. 어깨가 한결 가벼워졌습니다."),
        ("마포구 · 커플 이용", "기념일에 커플로 받았는데 둘 다 만족. 향도 좋고 압도 딱 맞았어요."),
        ("중구 · 출장 고객", "호텔에서 받았는데 여독이 풀렸어요. 시간 약속도 정확했습니다."),
        ("송파구 · 40대", "스포츠 관리로 뭉친 등을 풀었습니다. 시원하고 개운했어요."),
        ("영등포구 · 직장인", "야근 후 늦은 시간에 받았는데 친절하고 깔끔했습니다."),
        ("성동구 · 재택근무", "아로마 받고 그날 정말 푹 잤어요. 향이 은은해서 좋았습니다."),
        ("용산구 · 출장객", "외국 출장 전 호텔에서 받았어요. 컨디션 회복에 도움이 됐습니다."),
        ("노원구 · 부모님 선물", "부모님께 선물로 예약했는데 만족하셨어요. 압도 부드럽게 잘 맞춰주셨습니다."),
        ("서초구 · 30대", "120분 코스로 머리부터 발끝까지 받았네요. 깊게 이완됐습니다."),
    ]
    rh = "".join(
        f'<div class="review reveal"><div class="stars">★★★★★</div><p>"{t}"</p><div class="who">{w}</div></div>'
        for w, t in revs)
    body = (lib.crumb([("/", "홈"), (None, "후기")])
            + lib.lux_hero("REVIEW", "고객 후기", "웰니스센터를 이용하신 고객들의 후기입니다.", actions=False)
            + '<section class="block"><div class="wrap"><div class="grid g3">' + rh + '</div></div></section>'
            + lib.cta_band())
    add("/reviews/", lib.document("고객 후기", "웰니스센터 출장마사지 고객 후기 모음.", "/reviews/", body), "0.6", "weekly")


def build_customer():
    secs_html = (
        '<section class="lux-sec reveal" id="notice"><h2>공지사항</h2>'
        '<ul><li>연중무휴 24시간 상담·예약을 운영합니다.</li>'
        '<li>표시 요금은 정찰가이며 임의 추가 요금은 없습니다.</li>'
        '<li>건강관리 목적의 방문 관리만 제공하며 불법·퇴폐 행위는 일절 응대하지 않습니다.</li></ul></section>'
        '<section class="lux-sec reveal" id="qna"><h2>자주 묻는 질문</h2>'
        '<p>이용 관련 질문은 <a href="/guide/faq/">이용 FAQ</a>와 <a href="/seoul/faq/">서울 출장마사지 FAQ</a>에서 확인하실 수 있습니다.</p></section>'
        f'<section class="lux-sec reveal" id="inquiry"><h2>1:1 문의</h2>'
        f'<p>문의는 전화로 안내해 드립니다. <a href="tel:{lib.PHONE_T}">{lib.PHONE_D}</a>로 연락 주세요. 연중무휴 24시간 상담 가능합니다.</p></section>'
        '<section class="lux-sec reveal" id="partner"><h2>제휴·기업 문의</h2>'
        '<p>사무실·행사장 등 단체 방문은 <a href="/course/group/">기업·단체 방문</a>을 참고하시고, 제휴 문의도 전화로 안내해 드립니다.</p></section>')
    toc = ('<li><a href="#notice">공지사항</a></li><li><a href="#qna">자주 묻는 질문</a></li>'
           '<li><a href="#inquiry">1:1 문의</a></li><li><a href="#partner">제휴·기업 문의</a></li>')
    body = (lib.crumb([("/", "홈"), (None, "고객센터")])
            + lib.lux_hero("CUSTOMER", "고객센터", "공지·문의·제휴까지 고객 지원 정보를 안내합니다.", actions=False)
            + '<section class="block lux-body" style="padding-top:34px"><div class="wrap"><div class="lux-grid">'
            + f'<aside class="toc"><div class="toc-inner"><span class="toc-label">목차</span><ul>{toc}</ul></div></aside>'
            + f'<div class="lux-main">{secs_html}</div></div></div></section>' + lib.cta_band())
    add("/customer/", lib.document("고객센터", "웰니스센터 고객센터 — 공지사항·문의·제휴·기업 문의 안내.", "/customer/", body), "0.6", "monthly")


# ────────────────────────── 정책 페이지 ──────────────────────────
def policy_page(path, title, secs):
    sec_html = "".join(f'<section class="lux-sec reveal" id="sec-{i}"><h2>{esc(h)}</h2>{b}</section>'
                       for i,(h,b) in enumerate(secs,1))
    toc = "".join(f'<li><a href="#sec-{i}">{esc(h)}</a></li>' for i,(h,_) in enumerate(secs,1))
    body = (lib.crumb([("/", "홈"), (None, title)])
            + lib.lux_hero("POLICY", title, f"{title} 전문입니다.", actions=False)
            + '<section class="block lux-body" style="padding-top:34px"><div class="wrap"><div class="lux-grid">'
            + f'<aside class="toc"><div class="toc-inner"><span class="toc-label">목차</span><ul>{toc}</ul></div></aside>'
            + f'<div class="lux-main">{sec_html}</div></div></div></section>')
    add(path, lib.document(title, f"웰니스센터 {title}.", path, body), "0.3", "yearly")

def build_policies():
    policy_page("/privacy/", "개인정보처리방침", [
        ("수집하는 개인정보", lib.P("웰니스센터는 예약·상담을 위해 연락처, 방문 주소, 예약 정보를 수집합니다. 수집한 정보는 예약 이행 목적으로만 이용합니다.")),
        ("이용 및 보유 기간", lib.P("개인정보는 예약 서비스 제공 기간 동안 보유하며, 목적 달성 후 관련 법령에 따라 파기합니다.")),
        ("제3자 제공", lib.P("법령에 근거하거나 이용자 동의가 있는 경우를 제외하고 개인정보를 외부에 제공하지 않습니다.")),
        ("이용자 권리", lib.P("이용자는 본인의 개인정보 열람·정정·삭제를 요청할 수 있습니다.")),
        ("개인정보보호책임자", lib.P(f"개인정보보호책임자: {lib.PRIVACY_M} / 문의: <a href='tel:{lib.PHONE_T}'>{lib.PHONE_D}</a>")),
    ])
    policy_page("/terms/", "이용약관", [
        ("목적", lib.P("본 약관은 웰니스센터가 제공하는 방문 건강관리 서비스의 이용 조건을 규정합니다.")),
        ("서비스 내용", lib.P("본 서비스는 만 19세 이상 성인을 대상으로 한 이완·휴식 목적의 방문 관리이며, 의료 행위가 아닙니다.")),
        ("예약 및 취소", lib.P("예약·변경·취소는 전화로 진행하며, 자세한 내용은 <a href='/reservation/change/'>변경·취소 안내</a>를 따릅니다.")),
        ("금지행위", lib.P("불법·퇴폐 행위 요구는 일절 응대하지 않으며, 부적절한 언행 시 서비스가 중단될 수 있습니다.")),
        ("책임의 한계", lib.P("통증·질환이 있는 경우 의료기관 진료를 우선 권하며, 본 서비스는 치료를 대체하지 않습니다.")),
    ])
    policy_page("/youth/", "청소년보호정책", [
        ("기본 방침", lib.P("웰니스센터는 만 19세 이상 성인을 대상으로 서비스를 제공하며, 청소년 유해 정보로부터 청소년을 보호합니다.")),
        ("이용 제한", lib.P("미성년자의 서비스 이용은 제한되며, 모든 콘텐츠는 건강관리 목적의 정보만 제공합니다.")),
        ("책임자", lib.P(f"청소년보호책임자: {lib.PRIVACY_M} / 문의: <a href='tel:{lib.PHONE_T}'>{lib.PHONE_D}</a>")),
    ])


# ────────────────────────── 매거진 ──────────────────────────
BASE_DATE = datetime.date(2026, 6, 8)

def _article_meta():
    """각 글에 발행/수정일 부여(최신순). 반환: list of dict."""
    metas = []
    for i, a in enumerate(ARTICLES):
        slug, cat, title, lead, secs, faq = a
        pub = BASE_DATE - datetime.timedelta(days=i * 3)
        mod = pub + datetime.timedelta(days=1)
        metas.append({"slug": slug, "cat": cat, "title": title, "lead": lead,
                      "secs": secs, "faq": faq, "pub": pub, "mod": mod, "idx": i})
    return metas

def _card(m):
    catname = data.MAG_CAT_NAME.get(m["cat"], m["cat"])
    return (f'<a class="card reveal" href="/magazine/{m["slug"]}/"><div class="k">{esc(catname)}</div>'
            f'<h3>{esc(m["title"])}</h3><p>{esc(m["lead"][:90])}…</p>'
            f'<span class="more" style="color:var(--dim);font-weight:600">{m["pub"].strftime("%Y.%m.%d")}</span>'
            f'<span class="more">자세히 보기 →</span></a>')

def _pager(base, page, total_pages):
    if total_pages <= 1:
        return ""
    out = []
    for p in range(1, total_pages + 1):
        href = base if p == 1 else f"{base}page/{p}/"
        cls = " active" if p == page else ""
        out.append(f'<a class="pg{cls}" href="{href}">{p}</a>')
    return f'<div class="pager">{"".join(out)}</div>'

def _list_page(path, page, total_pages, metas_slice, h1, lead, crumb_items, base, blog_name, prio="0.6"):
    grid = '<div class="grid g3">' + "".join(_card(m) for m in metas_slice) + '</div>'
    pager = _pager(base, page, total_pages)
    body = (lib.crumb(crumb_items)
            + lib.lux_hero("MAGAZINE", h1, lead, actions=False)
            + f'<section class="block"><div class="wrap">{grid}{pager}</div></section>'
            + lib.cta_band())
    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "Blog", "name": blog_name, "url": lib.DOMAIN + base,
        "blogPost": [{"@type": "BlogPosting", "headline": m["title"],
                      "url": f'{lib.DOMAIN}/magazine/{m["slug"]}/',
                      "datePublished": m["pub"].isoformat()} for m in metas_slice]
    }, ensure_ascii=False)
    add(path, lib.document(h1, lead, path, body, jsonld=jsonld), prio, "weekly")

def build_magazine():
    metas = _article_meta()
    by_slug = {m["slug"]: m for m in metas}
    PER = 9

    # 전체 매거진 허브 + 페이지네이션
    total = len(metas)
    tp = (total + PER - 1) // PER
    for page in range(1, tp + 1):
        sl = metas[(page-1)*PER: page*PER]
        path = "/magazine/" if page == 1 else f"/magazine/page/{page}/"
        crumb_items = [("/", "홈"), (None, "매거진")] if page == 1 else [("/", "홈"), ("/magazine/", "매거진"), (None, f"{page}페이지")]
        _list_page(path, page, tp, sl, "웰니스센터 매거진",
                   "출장마사지·홈타이 이용가이드와 코스·지역·테마 이야기를 전합니다.",
                   crumb_items, "/magazine/", "웰니스센터 매거진", "0.8" if page == 1 else "0.5")

    # 카테고리별
    for cs, cn in data.MAG_CATS:
        cms = [m for m in metas if m["cat"] == cs]
        if not cms:
            continue
        ctp = (len(cms) + PER - 1) // PER
        base = f"/magazine/category/{cs}/"
        for page in range(1, ctp + 1):
            sl = cms[(page-1)*PER: page*PER]
            path = base if page == 1 else f"{base}page/{page}/"
            crumb_items = [("/", "홈"), ("/magazine/", "매거진"), (None, cn)]
            _list_page(path, page, ctp, sl, f"{cn} 매거진",
                       f"{cn} 관련 출장마사지 이야기와 안내를 모았습니다.",
                       crumb_items, base, f"{cn} 매거진", "0.6")

    # 글 60편
    for m in metas:
        slug, cat = m["slug"], m["cat"]
        catname = data.MAG_CAT_NAME.get(cat, cat)
        secs = list(m["secs"])
        # 함께 보면 좋은 안내: 같은 카테고리 다른 글 3개
        sib = [x for x in metas if x["cat"] == cat and x["slug"] != slug][:3]
        related = [(f'/magazine/{x["slug"]}/', x["title"]) for x in sib]
        related += [("/magazine/", "전체 매거진"), ("/reservation/", "예약 방법")]
        byline = (m["pub"].strftime("%Y.%m.%d"), m["mod"].strftime("%Y.%m.%d"))
        # JSON-LD: BreadcrumbList + BlogPosting
        crumb_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": lib.DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": "매거진", "item": lib.DOMAIN + "/magazine/"},
            {"@type": "ListItem", "position": 3, "name": catname, "item": f"{lib.DOMAIN}/magazine/category/{cat}/"},
            {"@type": "ListItem", "position": 4, "name": m["title"], "item": f'{lib.DOMAIN}/magazine/{slug}/'}]}
        post_ld = {"@context": "https://schema.org", "@type": "BlogPosting",
                   "headline": m["title"], "description": m["lead"],
                   "datePublished": m["pub"].isoformat(), "dateModified": m["mod"].isoformat(),
                   "author": {"@type": "Organization", "name": lib.SITE + " 운영팀"},
                   "publisher": {"@type": "Organization", "name": lib.SITE,
                                 "logo": {"@type": "ImageObject", "url": lib.OG_IMG}},
                   "mainEntityOfPage": f'{lib.DOMAIN}/magazine/{slug}/', "inLanguage": "ko-KR",
                   "image": lib.OG_IMG}
        jsonld = json.dumps(crumb_ld, ensure_ascii=False) + '</script><script type="application/ld+json">' + json.dumps(post_ld, ensure_ascii=False)
        lux_page(m["title"], m["lead"][:150], f"/magazine/{slug}/",
                 f"MAGAZINE · {catname}", m["title"], m["lead"],
                 secs, [("/", "홈"), ("/magazine/", "매거진"), (f"/magazine/category/{cat}/", catname), (None, m["title"])],
                 faq=m["faq"], byline=byline, related=related, og_type="article",
                 jsonld=jsonld, prio="0.8")


# ────────────────────────── 루트 파일 ──────────────────────────
FAVICON_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
    '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#f4d29c"/><stop offset="0.45" stop-color="#e9b8a7"/>'
    '<stop offset="1" stop-color="#c98a6b"/></linearGradient></defs>'
    '<rect width="64" height="64" rx="14" fill="#0b0b0e"/>'
    '<text x="32" y="44" font-family="Georgia,serif" font-style="italic" font-weight="700" '
    'font-size="38" text-anchor="middle" fill="url(#g)">W</text></svg>')

def build_root_files():
    # favicon.svg
    with open(os.path.join(ROOT, "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(FAVICON_SVG)
    # site.webmanifest
    manifest = {
        "name": lib.SITE, "short_name": lib.SITE, "lang": "ko",
        "start_url": "/", "display": "standalone",
        "background_color": "#0b0b0e", "theme_color": "#0b0b0e",
        "icons": [
            {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "/icon-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }
    with open(os.path.join(ROOT, "site.webmanifest"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    # robots.txt
    robots = (f"User-agent: *\nAllow: /\nDisallow: /tools/\n\n"
              "User-agent: GPTBot\nAllow: /\n\nUser-agent: ClaudeBot\nAllow: /\n\n"
              "User-agent: Google-Extended\nAllow: /\n\n"
              f"Sitemap: {lib.DOMAIN}/sitemap.xml\nHost: {lib.DOMAIN}\n")
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)
    # sitemap.xml
    lastmod = BASE_DATE.isoformat()
    urls = "".join(
        f"<url><loc>{lib.DOMAIN}{p}</loc><lastmod>{lastmod}</lastmod>"
        f"<changefreq>{freq}</changefreq><priority>{prio}</priority></url>"
        for p, prio, freq in PAGES)
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + "</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)


def main():
    build_home()
    build_seoul_hub()
    build_districts()
    build_stations()
    build_themes()
    build_courses()
    build_reservation()
    build_guide()
    build_reviews()
    build_customer()
    build_policies()
    build_magazine()
    build_root_files()
    print(f"생성 완료: {len(PAGES)} HTML 페이지 + sitemap/robots/manifest/favicon")


if __name__ == "__main__":
    main()
