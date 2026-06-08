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
import content
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
             prio="0.6", freq="weekly", full_title=None):
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
    add(path, lib.document(title, desc, path, body, og_type=og_type, jsonld=jsonld,
        full_title=full_title), prio, freq)


# ────────────────────────── 홈 ──────────────────────────
HOME_STATIONS = [
    ("gangnam-station", "강남역"), ("seoul-station-station", "서울역"), ("jamsil-station", "잠실역"),
    ("hongik-univ-station", "홍대입구역"), ("konkuk-univ-station", "건대입구역"),
    ("sillim-station", "신림역"), ("yeouido-station", "여의도역"),
    ("express-bus-terminal-station", "고속터미널역"), ("gimpo-airport-station", "김포공항역"),
    ("wangsimni-station", "왕십리역"),
]


def _home_section(eyebrow, h2, inner, anchor=None, pad_top=True):
    aid = f' id="{anchor}"' if anchor else ""
    pt = "" if pad_top else ' style="padding-top:0"'
    return (f'<section class="block reveal"{pt}{aid}><div class="wrap">'
            f'<span class="eyebrow"><span class="pulse"></span>{eyebrow}</span>'
            f'<h2 class="sec">{h2}</h2>{inner}</div></section>')


def build_home():
    # 지역 카드: 자치구명만(키워드 접미사 없음), 부가설명은 대표 동
    region_cards = []
    for rk, rl, gus in data.REGIONS:
        for slug, name in gus:
            dongs = data.GU_AREAS.get(slug, [])
            desc = " · ".join(dongs[:3]) if dongs else f"{rl} 생활권"
            region_cards.append((rl, name, desc, f"/seoul/{slug}/", "안내 보기"))
    # 역 카드: 역명만
    station_cards = [("역세권", nm, "인근 생활권·예약 안내", f"/seoul/stations/{sl}/", "안내 보기")
                     for sl, nm in HOME_STATIONS]
    # 테마 카드: 테마명만
    theme_cards = [("테마", n, d, f"/theme/{s}/", "안내 보기") for s, n, d in data.THEMES]

    A = '<div class="article">'  # 가독성 본문 래퍼

    hero = f"""
<section class="hero"><div class="hero-inner">
  <div class="hero-text">
    <span class="eyebrow"><span class="pulse"></span>SEOUL · 방문 마사지 예약 안내</span>
    <h1>서울 출장마사지·홈타이 예약 안내</h1>
    <p class="lead">서울 전지역에서 방문 마사지와 홈타이 예약을 찾는 분들을 위해 지역별 가능 안내, 지하철역 인근 정보, 테마별 관리, 예약 전 확인사항을 한곳에 정리했습니다.</p>
    <div class="actions">
      <a class="btn btn-primary" href="tel:{lib.PHONE_T}">예약문의</a>
      <a class="btn btn-ghost" href="/seoul/area/">지역별 안내 보기</a>
      <a class="btn btn-ghost" href="/seoul/stations/">지하철역별 안내 보기</a>
      <a class="btn btn-ghost" href="/theme/">테마별 안내 보기</a>
    </div>
    <div class="trust">
      <span><b>연중무휴</b> 24시간 상담</span>
      <span><b>서울 25개 자치구</b> 안내</span>
      <span><b>정찰 요금</b> 사전 안내</span>
    </div>
  </div>
  <div class="hero-visual">
    <div class="glass">
      <h3>코스별 기본 요금<b>예약 시 안내</b></h3>
      <div class="book-row"><span>60분</span><span>90,000원</span></div>
      <div class="book-row"><span>90분</span><span>150,000원</span></div>
      <div class="book-row"><span>120분</span><span>180,000원</span></div>
      <a class="bk" href="tel:{lib.PHONE_T}">예약문의</a>
    </div>
    <div class="floating fl-1"><span class="dot"></span>예약 상담 가능</div>
    <div class="floating fl-2">서울 전지역 안내</div>
  </div>
</div></section>"""

    s_service = _home_section("SERVICE", "서울 출장마사지·홈타이 서비스 안내",
        A + lib.P(
        "서울 출장마사지·홈타이는 고객이 계신 장소로 관리사가 직접 방문해 편안하게 관리를 받는 방문형 서비스입니다. "
        "예약 시에는 희망 지역과 시간, 코스 정보를 먼저 확인한 뒤 방문 가능 여부를 안내해 드립니다. "
        "자택뿐 아니라 오피스텔, 호텔, 숙소 등 조용히 휴식할 수 있는 공간이라면 어디서든 이용할 수 있습니다.",
        "본 서비스는 만 19세 이상 성인을 대상으로 한 건강관리(이완·휴식) 목적의 방문 관리입니다. 이용 전에는 정확한 주소와 출입 방법, 예약 가능 시간을 함께 확인하면 더 원활하게 진행됩니다.") + "</div>",
        pad_top=False)

    s_allarea = _home_section("ALL AREA", "서울 전지역 방문 가능 안내",
        A + lib.P(
        "서울 25개 자치구를 강남권, 강서권, 서남권, 동북권, 도심권, 서북권 여섯 개 생활권으로 나누어 안내합니다. "
        "각 자치구 페이지에서는 대표 동을 기준으로 방문 가능 지역을 확인할 수 있으며, 1동·2동처럼 숫자로 나뉜 행정동은 별도 페이지 대신 대표 동 페이지에서 통합해 안내합니다.",
        "이렇게 구성하면 비슷한 페이지가 늘어나지 않아 원하는 지역을 더 쉽게 찾을 수 있습니다. 방문 가능 여부는 예약 시간과 위치, 배정 상황에 따라 달라질 수 있으므로 <a href='/seoul/area/'>지역별 안내</a>에서 권역과 자치구를 먼저 확인해 주세요.") + "</div>",
        pad_top=False)

    s_area = _home_section("AREA", "지역별 안내",
        A + lib.P(
        "지역별 안내는 서울 전체에서 자치구, 대표 동 순서로 구성됩니다. 아래에서 가까운 자치구를 선택하면 해당 지역의 대표 생활권과 예약 가능 시간, 방문 전 확인사항을 확인할 수 있습니다. "
        "숫자로 나뉜 행정동은 대표 동 페이지에서 함께 안내하여 더 쉽게 지역을 찾을 수 있도록 했습니다.") + "</div>"
        + f'<div style="margin-top:24px">{cards(region_cards)}</div>',
        anchor="area", pad_top=False)

    s_station = _home_section("STATION", "지하철역 인근 안내",
        A + lib.P(
        "지하철역별 안내는 노선별 역 목록과 역 상세 페이지로 구성됩니다. 강남역, 서울역, 잠실역, 홍대입구역처럼 이용 문의가 많은 역은 개별 안내 페이지에서 인근 생활권과 주변 대표 동, 예약 가능 시간, 방문 전 확인사항을 확인할 수 있습니다. "
        "노선과 역 이름으로 가까운 위치를 먼저 찾은 뒤, 정확한 방문 가능 여부는 예약 시 위치를 기준으로 안내해 드립니다.") + "</div>"
        + f'<div style="margin-top:24px">{cards(station_cards)}</div>'
        + '<div style="margin-top:18px"><a class="btn btn-ghost" href="/seoul/stations/">지하철역별 안내 전체 보기 →</a></div>',
        anchor="station", pad_top=False)

    s_theme = _home_section("THEME", "테마별 관리 안내",
        A + lib.P(
        "테마별 안내에서는 스웨디시, 타이마사지, 아로마테라피, 홈케어, 호텔식마사지 등 이용 목적에 따라 선택할 수 있는 관리 유형을 소개합니다. "
        "각 테마 페이지는 관리 특징과 추천 대상, 예약 전 확인사항을 중심으로 구성되어 처음 이용하시는 분도 자신에게 맞는 관리를 고르기 쉽습니다. 지역이나 역 이름과 조합한 중복 페이지는 만들지 않고, 테마 자체의 정보에 집중해 안내합니다.") + "</div>"
        + f'<div style="margin-top:24px">{cards(theme_cards)}</div>',
        anchor="theme", pad_top=False)

    s_course = _home_section("COURSE", "코스 선택 안내",
        A + lib.P(
        "코스는 이용 목적과 그날의 컨디션에 따라 선택하는 것이 좋습니다. 전반적인 피로 회복이 필요하다면 기본 관리, 편안한 휴식과 긴장 완화를 원한다면 아로마 관리, 뭉친 근육을 풀고 싶다면 스포츠 관리처럼 목적에 맞춰 확인할 수 있습니다.",
        "처음이라면 전신을 고르게 받을 수 있는 90분 코스가 무난합니다. 자세한 코스 구성과 정찰 요금은 <a href='/course/'>코스안내</a>와 <a href='/course/guide/'>코스 선택 가이드</a>에서 확인하세요.") + "</div>"
        + lib.pmenu(),
        pad_top=False)

    s_reserve = _home_section("RESERVATION", "예약 진행 방식",
        A + lib.P("예약은 다음 순서로 진행됩니다. 희망 지역과 시간을 먼저 확인한 뒤 코스와 인원, 방문 장소 정보를 기준으로 가능 여부를 안내해 드립니다.")
        + "<ol><li>지역 또는 역 인근 위치 확인</li><li>희망 시간 확인</li><li>코스와 인원 확인</li>"
          "<li>방문 가능 여부 안내</li><li>예약 확정</li></ol>"
        + lib.P("저녁 시간대와 주말은 문의가 몰릴 수 있으므로 여유 있게 예약하시는 것을 권장합니다.") + "</div>",
        pad_top=False)

    s_check = _home_section("CHECK", "이용 전 확인사항",
        A + lib.P("원활한 방문 관리를 위해 아래 항목을 미리 확인해 주세요. 숙소·오피스텔·주거지 방문 시에는 출입 안내와 연락 가능 여부를 함께 확인하면 예약 진행이 더 원활합니다.")
        + "<ul><li>정확한 주소</li><li>공동현관 출입 방법</li><li>주차 가능 여부</li>"
          "<li>조용한 공간 확보</li><li>예약자 연락 가능 여부</li><li>금지행위 안내 확인</li></ul></div>",
        pad_top=False)

    s_safety = _home_section("SAFETY", "위생 및 안전 안내",
        A + lib.P(
        "안전하고 건전한 방문 관리를 위해 예약 정보 확인, 위생 관리 기준, 개인정보 보호를 중요하게 운영합니다. "
        "타월은 매회 교체하고 도구는 위생적으로 관리하며, 관리사는 손 위생을 철저히 한 뒤 관리를 시작합니다.",
        "이용 전에는 서비스 범위와 <a href='/guide/forbidden/'>금지행위 안내</a>를 확인해 주세요. 무리한 요구나 불법적인 요청은 진행되지 않으며, 본 서비스는 의료 행위가 아닌 건강관리 목적의 방문 관리임을 명확히 안내합니다.") + "</div>",
        pad_top=False)

    body = hero + s_service + s_allarea + s_area + s_station + s_theme + s_course + s_reserve + s_check + s_safety

    faq = [
        ("서울 전지역 방문이 가능한가요",
         "예약 시간, 위치, 배정 상황에 따라 가능 여부가 달라질 수 있습니다. <a href='/seoul/area/'>지역별 안내</a> 페이지에서 자치구와 대표 동 기준으로 확인할 수 있습니다."),
        ("지하철역 근처도 예약할 수 있나요",
         "주요 지하철역 인근은 역 상세 페이지에서 주변 생활권과 함께 안내합니다. 정확한 가능 여부는 예약 시 위치를 기준으로 확인합니다."),
        ("당일 예약도 가능한가요",
         "당일 예약은 가능할 수 있지만 시간대와 배정 상황에 따라 달라집니다. 저녁 시간대와 주말은 사전 예약을 권장합니다."),
        ("테마별 관리는 어떻게 선택하나요",
         "스웨디시, 타이마사지, 아로마테라피, 홈케어 등 <a href='/theme/'>테마별 안내</a> 페이지에서 특징과 추천 대상을 확인할 수 있습니다."),
        ("예약 전 준비할 것이 있나요",
         "정확한 주소, 출입 방법, 주차 가능 여부, 조용한 공간을 미리 확인하면 원활한 이용에 도움이 됩니다."),
    ]
    body += lib.faq_block(faq)

    # 하단 예약문의 CTA
    body += (f'<section class="cta-band" id="contact"><div>'
             f'<span class="eyebrow"><span class="pulse"></span>RESERVE</span>'
             f'<h2>예약문의</h2>'
             f'<p style="max-width:680px;margin:12px auto 24px">서울 출장마사지·홈타이 예약은 희망 지역과 지하철역 인근 위치, 시간, 코스 정보를 기준으로 가능 여부를 안내합니다. '
             f'지역별 안내와 테마별 안내를 확인하신 뒤 문의하시면 더 빠른 상담이 가능합니다.</p>'
             f'<div class="actions" style="justify-content:center">'
             f'<a class="btn btn-primary" href="tel:{lib.PHONE_T}">예약문의 {lib.PHONE_D}</a>'
             f'<a class="btn btn-ghost" href="/seoul/area/">지역별 안내 보기</a>'
             f'<a class="btn btn-ghost" href="/seoul/stations/">지하철역별 안내 보기</a>'
             f'<a class="btn btn-ghost" href="/theme/">테마별 안내 보기</a>'
             f'</div></div></section>')

    biz_ld = {
        "@context": "https://schema.org", "@type": "LocalBusiness",
        "name": lib.SITE, "telephone": lib.PHONE_D, "url": lib.DOMAIN,
        "image": lib.OG_IMG, "areaServed": "서울특별시",
        "priceRange": "₩₩", "openingHours": "Mo-Su 00:00-24:00",
    }
    jsonld = (json.dumps(biz_ld, ensure_ascii=False)
              + '</script><script type="application/ld+json">'
              + lib.faq_jsonld(faq))
    desc = ("서울 출장마사지·홈타이 안내 페이지입니다. 서울 전지역 방문 가능 지역, 지하철역 인근, "
            "테마별 관리, 예약 전 확인사항을 한눈에 확인해보세요.")
    full_title = "서울 출장마사지·홈타이 | 서울 전지역 방문 마사지 예약 안내"
    naver = '<meta name="naver-site-verification" content="d162b05f213460e37758588567b7d1b03a7d8fe3" />\n'
    add("/", lib.document("서울 출장마사지·홈타이 예약 안내", desc, "/", body,
        jsonld=jsonld, full_title=full_title, head_extra=naver), "1.0", "daily")


# ────────────────────────── 서울 허브 / 지역 ──────────────────────────
def build_seoul_hub():
    # /seoul/
    secs = [
        ("서울 출장마사지 안내", lib.P(
            "웰니스센터는 서울 25개 자치구 전역으로 방문하는 출장마사지·홈타이 서비스입니다. 관리사가 고객이 계신 자택·오피스텔·호텔로 직접 방문해, 매장을 찾아가거나 대기하지 않아도 익숙한 공간에서 편안하게 관리를 받을 수 있습니다.",
            "이동과 대기 없이 예약한 시간에 관리가 시작되므로 바쁜 일정 속에서도 온전히 휴식에 집중할 수 있고, 관리 후에는 외출 없이 그대로 쉴 수 있어 이완 효과가 오래 이어집니다.",
            "스웨디시·아로마테라피·타이마사지·스포츠·경락 등 목적에 맞는 다양한 코스를 제공하며, 만 19세 이상 성인을 대상으로 한 건강관리(이완·휴식) 목적의 방문 관리입니다.")),
        ("서울 홈타이 안내", lib.P(
            "홈타이는 집에서 받는 타이식 스트레칭·지압 관리입니다. 오일을 사용하는 일반 마사지와 달리 편한 복장을 입은 채 진행되며, 팔다리를 늘려주는 스트레칭과 지압을 결합해 활력과 유연성 회복에 초점을 둡니다.",
            "끈적임 없이 시원하게 받을 수 있어 오일 관리가 부담스러운 분이나 오래 앉아 몸이 굳은 분께 잘 맞습니다. 기법의 특징은 <a href='/theme/thai-massage/'>타이마사지</a>, 코스 구성은 <a href='/course/home/'>홈타이 코스</a>에서 자세히 확인할 수 있습니다.",
            "홈타이도 출장 방식과 동일하게 자택으로 방문해 진행하므로, 이동 없이 집에서 편하게 받을 수 있습니다.")),
        ("서울 전지역 출장 가능 안내", lib.P(
            "서울 전 지역을 강남권·강서권·서남권·동북권·도심권·서북권 여섯 개 생활권으로 나누어 안내하며, 25개 자치구 어디든 방문합니다. 각 자치구는 대표 동을 기준으로 구성되고, 숫자로 나뉜 행정동은 대표 동 페이지에서 통합해 안내합니다.",
            "이렇게 구성하면 비슷한 페이지가 늘어나지 않아 원하는 지역을 더 쉽게 찾을 수 있습니다. 가까운 지역은 <a href='/seoul/area/'>지역별 안내</a>에서 권역과 자치구를 선택해 확인하세요.",
            "방문 가능 여부는 예약 시간과 위치, 배정 상황에 따라 달라질 수 있어 정확한 가능 여부는 예약 시 위치를 기준으로 확인합니다.")),
        ("지하철역 인근 안내", lib.P(
            "지하철역 인근은 도로 연결이 좋아 예약 시간에 맞춘 방문이 수월한 편입니다. 강남역·서울역·잠실역·홍대입구역처럼 이용 문의가 많은 역은 개별 안내 페이지에서 인근 생활권과 예약 가능 시간을 확인할 수 있습니다.",
            "노선과 역 이름으로 가까운 위치를 먼저 찾고 싶다면 <a href='/seoul/stations/'>지하철역별 안내</a>에서 호선별 역 목록을 살펴보세요. 정확한 방문 가능 여부는 예약 시 위치를 기준으로 확인합니다.",
            "오피스텔·호텔이라면 동·호수와 가까운 출구 번호, 공동현관 출입 방법을 알려주시면 더 빠르게 방문할 수 있습니다.")),
        ("코스 선택과 예약 안내", lib.P(
            "처음 이용하신다면 전신을 고르게 받는 90분 코스가 무난합니다. 피로 회복·아로마·스포츠·홈타이 등 목적에 맞춰 선택할 수 있으며, 어떤 코스가 맞을지 고민된다면 <a href='/course/guide/'>코스 선택 가이드</a>를 참고하세요.",
            "예약은 전화로 진행하며 연중무휴 24시간 상담이 가능합니다. 희망 위치와 시간, 코스, 인원을 알려주시면 방문 가능 여부를 안내해 드리고, 저녁 시간대와 주말은 문의가 몰릴 수 있어 여유 있게 예약하는 것을 권합니다.",
            "이용 전에는 <a href='/guide/checklist/'>이용 전 확인사항</a>과 <a href='/guide/safety/'>위생 및 안전 안내</a>를 함께 살펴보시면 도움이 됩니다.")),
        ("이용 흐름과 준비", lib.P(
            "이용은 예약 → 방문 → 관리 → 마무리 순으로 진행됩니다. 예약이 확정되면 관리사가 출발·도착 시 연락드리며, 베드·오일·타월 등 용품은 모두 준비해 가므로 고객은 베드를 놓을 약 2㎡의 공간만 비워 주시면 됩니다.",
            "샤워 후 편안한 상태로 기다려 주시고, 관리 중 압이 강하거나 약하면 언제든 편하게 말씀해 주세요. 집중하고 싶은 부위가 있으면 그 부위에 시간을 더 할애해 드립니다.",
            "관리 후에는 따뜻한 물을 마시고 충분히 쉬면 이완 효과가 오래갑니다. 방문 직전 준비는 <a href='/guide/prepare/'>방문 전 준비사항</a>에서 자세히 확인할 수 있습니다.")),
    ]
    # id 매핑(메뉴 앵커용): home/allarea/station
    secs_html = (
        f'<section class="lux-sec reveal" id="sec-1"><h2>{secs[0][0]}</h2>{secs[0][1]}</section>'
        f'<section class="lux-sec reveal" id="home"><h2>{secs[1][0]}</h2>{secs[1][1]}</section>'
        f'<section class="lux-sec reveal" id="allarea"><h2>{secs[2][0]}</h2>{secs[2][1]}</section>'
        f'<section class="lux-sec reveal" id="station"><h2>{secs[3][0]}</h2>{secs[3][1]}</section>'
        f'<section class="lux-sec reveal" id="course"><h2>{secs[4][0]}</h2>{secs[4][1]}</section>'
        f'<section class="lux-sec reveal" id="flow"><h2>{secs[5][0]}</h2>{secs[5][1]}</section>')
    toc = ('<li><a href="#sec-1">서울 출장마사지 안내</a></li>'
           '<li><a href="#home">홈타이 안내</a></li>'
           '<li><a href="#allarea">전지역 출장</a></li>'
           '<li><a href="#station">지하철역 인근</a></li>'
           '<li><a href="#course">코스·예약 안내</a></li>'
           '<li><a href="#flow">이용 흐름</a></li>')
    body = (lib.crumb([("/", "홈"), (None, "서울 출장마사지")])
            + lib.lux_hero("SEOUL · 출장마사지", "서울 출장마사지·홈타이 안내",
                "서울 전역으로 방문하는 출장마사지·홈타이 안내입니다. 서비스 구성과 홈타이, 전지역 출장, 지하철역 인근, 코스·예약 안내를 한곳에 정리했습니다.")
            + '<section class="block lux-body" style="padding-top:34px"><div class="wrap"><div class="lux-grid">'
            + f'<aside class="toc"><div class="toc-inner"><span class="toc-label">목차</span><ul>{toc}</ul></div></aside>'
            + f'<div class="lux-main">{secs_html}</div></div></div></section>')
    body += lib.cta_band()
    add("/seoul/", lib.document("서울 출장마사지·홈타이 안내",
        "서울 25개 자치구 전역 출장마사지·홈타이 안내. 서비스 구성과 홈타이, 전지역 출장 가능 지역, 지하철역 인근, 코스 선택과 예약 방법을 확인하세요.",
        "/seoul/", body), "0.9", "weekly")

    # /seoul/faq/
    faq = [
        ("출장 지역은 어디까지인가요",
         "서울 25개 자치구 전역으로 방문합니다. 자치구별 대표 동을 기준으로 안내하며, 인근 지역도 예약 시 위치를 기준으로 가능 여부를 확인해 드립니다. 가까운 지역은 <a href='/seoul/area/'>지역별 안내</a>에서 확인할 수 있습니다."),
        ("출장마사지와 홈타이는 어떻게 다른가요",
         "출장마사지는 오일을 사용한 스웨디시·아로마 등 다양한 관리를 자택으로 방문해 받는 서비스이고, 홈타이는 옷을 입은 채 스트레칭과 지압으로 진행하는 타이식 관리입니다. 둘 다 방문 방식은 동일하며, 끈적임 없이 시원하게 받고 싶다면 홈타이가 잘 맞습니다."),
        ("예약은 얼마나 미리 해야 하나요",
         "당일 예약도 시간대와 배정 상황에 따라 가능합니다. 다만 저녁 시간대와 주말, 기념일은 문의가 몰릴 수 있어 원하는 시간이 있으면 여유 있게 예약하시는 것을 권합니다."),
        ("어떤 코스를 골라야 할지 모르겠어요",
         "처음이라면 전신을 고르게 받는 90분 코스가 무난합니다. 피로 회복이 목적이면 기본 관리, 스트레스·수면이 고민이면 아로마, 근육 뭉침이 심하면 스포츠 관리가 적합합니다. <a href='/course/guide/'>코스 선택 가이드</a>를 참고하세요."),
        ("요금은 어떻게 되나요",
         "60분 90,000원, 90분 150,000원, 120분 180,000원의 정찰 요금을 기준으로 안내합니다. 표시 요금 외 임의로 더해지는 비용은 없으며, 코스·인원·지역에 따른 차이는 예약 시 미리 안내해 드립니다. 자세한 내용은 <a href='/course/price/'>가격 안내</a>를 확인하세요."),
        ("결제는 어떻게 하나요",
         "결제 방법은 <a href='/reservation/payment/'>결제 안내</a> 페이지에서 확인하실 수 있으며, 예약 시 함께 안내해 드립니다."),
        ("준비물이 필요한가요",
         "거의 없습니다. 베드를 놓을 약 2㎡ 정도의 공간만 비워 주시면 되고, 베드·오일·타월 등 용품은 관리사가 준비해 갑니다. 샤워 후 편안한 상태로 기다려 주세요."),
        ("위생은 어떻게 관리되나요",
         "타월은 매회 새것으로 교체하고 도구는 위생적으로 관리하며, 관리사는 손 위생을 철저히 한 뒤 관리를 시작합니다. 자세한 기준은 <a href='/guide/safety/'>위생 및 안전 안내</a>에서 확인할 수 있습니다."),
        ("여성 관리사를 요청할 수 있나요",
         "네. 예약 시 요청하시면 가능 여부를 안내해 드립니다. 선호하는 진행 방식이 있으면 함께 말씀해 주세요."),
        ("심야에도 가능한가요",
         "네. 연중무휴 24시간 상담·예약이 가능해 야근 후나 새벽 시간에도 이용하실 수 있습니다. 취침 전에는 수면을 돕는 부드러운 이완 코스를 권합니다."),
        ("커플이나 가족이 함께 받을 수 있나요",
         "네. 두 분 이상이 같은 공간에서 동시에 받는 구성이 있습니다. 인원수에 맞춰 베드와 용품을 준비하며, 각자 다른 코스와 압으로 진행하는 것도 가능합니다. 자세한 내용은 <a href='/course/couple/'>커플·가족 방문</a>을 참고하세요."),
        ("호텔이나 오피스텔에서도 받을 수 있나요",
         "네. 자택뿐 아니라 호텔·숙소·오피스텔·원룸 등 베드를 놓을 공간이 있으면 어디서든 가능합니다. 건물 출입 방법과 객실 호수, 가까운 출구를 미리 알려주시면 방문이 매끄럽습니다."),
        ("관리 시간은 얼마나 걸리나요",
         "선택한 코스에 따라 60분·90분·120분입니다. 여기에 베드 설치와 마무리에 약간의 시간이 더 소요되므로, 다음 일정이 있다면 여유를 두고 예약하시는 것이 좋습니다."),
        ("관리사를 지정하거나 다시 요청할 수 있나요",
         "성별·기법 선호나 이전에 만족했던 관리사 재지정 요청은 예약 시 말씀해 주시면 가능 여부를 안내해 드립니다. 일정·지역에 따라 배정이 달라질 수 있어 미리 예약하면 수월합니다."),
        ("관리 후 주의할 점이 있나요",
         "관리 후에는 따뜻한 물을 충분히 마시고 당일 격한 운동·음주는 피하는 것이 좋습니다. 오일을 사용한 경우 1~2시간 뒤 샤워하면 보습 효과가 더 좋습니다. 자세한 내용은 <a href='/guide/aftercare/'>관리 후 주의사항</a>을 참고하세요."),
        ("처음이라 긴장되는데 괜찮을까요",
         "처음이라도 편히 누워 계시면 관리사가 진행 과정을 차근히 안내해 드립니다. 무엇을 입어야 할지 걱정하지 않으셔도 되며 타월로 가려 진행하고, 압이나 집중 부위는 진행 중 언제든 편하게 요청하실 수 있습니다."),
    ]
    fbody = (lib.crumb([("/", "홈"), ("/seoul/", "서울 출장마사지"), (None, "자주 묻는 질문")])
             + lib.lux_hero("FAQ", "서울 출장마사지 자주 묻는 질문",
                "서울 출장마사지·홈타이 이용과 관련해 지역·예약·코스·요금·준비물·위생 등 자주 묻는 질문을 모았습니다.", actions=False)
             + lib.faq_block(faq) + lib.cta_band())
    add("/seoul/faq/", lib.document("서울 출장마사지 자주 묻는 질문",
        "서울 출장마사지·홈타이 이용 관련 자주 묻는 질문 모음. 지역·예약·코스·요금·준비물·위생·심야 이용을 한눈에 확인하세요.",
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
# 자치구 유형(추천 코스/문구 차별화) — 유사 페이지 방지
GU_FOCUS = {
    "work": ["gangnam-gu", "seocho-gu", "yeongdeungpo-gu", "guro-gu", "geumcheon-gu",
             "jung-gu", "jongno-gu", "seongdong-gu"],
    "home": ["songpa-gu", "gangdong-gu", "yangcheon-gu", "nowon-gu", "dobong-gu",
             "gangbuk-gu", "jungnang-gu", "eunpyeong-gu", "seongbuk-gu", "dongdaemun-gu"],
    "univ": ["mapo-gu", "seodaemun-gu", "gwangjin-gu", "gwanak-gu", "dongjak-gu"],
    "hotel": ["yongsan-gu", "gangseo-gu"],
}
GU_FOCUS_OF = {g: k for k, gs in GU_FOCUS.items() for g in gs}

def _focus_intro(name, focus):
    return {
        "work": f"{name}는 직장인 이용이 많아 퇴근 후·심야 시간대 방문 수요가 높습니다.",
        "home": f"{name}는 주거 중심 생활권으로 가족 단위 이용과 낮 시간대 방문이 많습니다.",
        "univ": f"{name}는 대학가와 1인 가구가 많아 합리적인 방문 관리 수요가 높습니다.",
        "hotel": f"{name}는 호텔·숙소 이용이 많아 객실 방문 수요가 높습니다.",
    }.get(focus, f"{name}는 다양한 생활권이 어우러진 지역입니다.")

def _focus_course(name, focus):
    return {
        "work": ("업무로 뭉친 어깨·등에는 <a href='/course/sports/'>스포츠 관리</a>, 누적된 피로에는 "
                 "<a href='/course/fatigue/'>피로 회복 관리</a>가 적합합니다. 늦은 시간에는 "
                 "<a href='/theme/24hours/'>24시간</a> 예약을 활용할 수 있습니다."),
        "home": ("편안한 휴식과 숙면에는 <a href='/theme/aroma-therapy/'>아로마테라피</a>와 "
                 "<a href='/theme/sleep-available/'>수면 가능</a> 관리가, 가족·부모님께는 부드러운 "
                 "<a href='/theme/swedish/'>스웨디시</a>가 잘 맞습니다."),
        "univ": ("부담 없이 받기 좋은 <a href='/theme/swedish/'>스웨디시</a>와 긴장 완화를 위한 "
                 "<a href='/theme/aroma-therapy/'>아로마테라피</a>가 인기입니다. 귀가 후 이동 없이 받을 수 있어 편리합니다."),
        "hotel": ("객실에서 받는 <a href='/theme/hotel-massage/'>호텔식마사지</a>와 여독 해소를 위한 "
                  "<a href='/course/fatigue/'>피로 회복 관리</a>가 적합합니다. 출장·여행 일정에 맞춰 예약할 수 있습니다."),
    }.get(focus, "이용 목적에 따라 <a href='/theme/'>테마</a>와 <a href='/course/'>코스</a>를 선택할 수 있습니다.")


# 유형별 인기 테마 셋(역·동 페이지 공용)
THEME_SETS = {
    "work":  ["sports-massage", "swedish", "aroma-therapy", "24hours"],
    "home":  ["home-care", "aroma-therapy", "sleep-available", "swedish"],
    "univ":  ["home-care", "aroma-therapy", "sports-massage", "thai-massage"],
    "hotel": ["hotel-massage", "aroma-therapy", "swedish", "foot-massage"],
}
DEFAULT_THEMES = ["home-care", "aroma-therapy", "sports-massage", "thai-massage"]


def build_districts():
    valid_st = {s for s, *_ in data.all_stations()}
    for slug, name in data.ALL_GU:
        _, rk, rl = data.GU_BY_SLUG[slug]
        dong_list = data.DONGS.get(slug, [])   # [(slug, base)]
        gu_desc = data.GU_DESC.get(slug, f"{name}는 서울 {rl}에 속한 자치구입니다.")
        # 같은 권역의 다른 자치구(교차 내부링크)
        siblings = [(s, n) for _, rl2, gus in data.REGIONS if rl2 == rl
                    for s, n in gus if s != slug]
        # 인근 역 카드(존재하는 슬러그만)
        st_slugs = [s for s in data.GU_STATIONS.get(slug, []) if s in valid_st]
        st_names = [data.station_name(s) for s in st_slugs]
        focus = GU_FOCUS_OF.get(slug, "")

        A = '<div class="article">'
        # 1) 서비스 안내 (지역 특성 + 유형으로 차별화)
        s1 = _home_section("SERVICE", f"{name} 출장마사지·홈타이 서비스 안내",
            A + lib.P(
            f"{name}는 {gu_desc} {_focus_intro(name, focus)} 웰니스센터는 {name} 전역으로 관리사가 직접 방문하는 "
            "출장마사지·홈타이를 안내하며, 자택과 오피스텔, 호텔·숙소 등 조용히 휴식할 수 있는 공간이라면 어디서든 이용할 수 있습니다.",
            f"{name}에서는 예약 시 희망 위치와 시간, 코스 정보를 먼저 확인한 뒤 방문 가능 여부를 안내해 드립니다. "
            f"{name} 방문 관리는 만 19세 이상 성인을 대상으로 한 건강관리(이완·휴식) 목적의 서비스입니다.") + "</div>",
            pad_top=False)

        # 2) 방문 가능 지역 (대표 동을 동 페이지로 링크)
        if dong_list:
            chips = "".join(f'<a class="chip" href="/seoul/{slug}/{ds}/"><b>{b}동</b></a>'
                            for ds, b in dong_list)
        else:
            chips = f'<span class="chip">{name} 전역</span>'
        s2 = _home_section("AREA", f"{name} 방문 가능 지역 안내",
            A + lib.P(
            f"{name}의 방문 안내는 대표 동을 기준으로 구성됩니다. 아래 동 안내에서 {name} 전역을 확인할 수 있으며, "
            "1동·2동처럼 숫자로 나뉜 행정동은 대표 동 페이지에서 통합해 안내합니다.") + "</div>"
            + f'<div class="chips">{chips}</div>'
            + lib.P(f'정확한 방문 가능 여부는 예약 시 위치를 기준으로 확인하며, {rl} 전체는 '
                    f'<a href="/seoul/area/#{rk}">{rl} 안내</a>에서 확인할 수 있습니다.'),
            pad_top=False)

        # 3) 인근 지하철역
        if st_slugs:
            st_cards = cards([("역세권", nm, f"{nm}역 인근 {name} 생활권 안내",
                               f"/seoul/stations/{sl}-station/", "안내 보기")
                              for sl, nm in zip(st_slugs, st_names)])
            st_intro = (f"{name} 인근의 주요 지하철역을 기준으로도 위치를 확인할 수 있습니다. "
                        f"{', '.join(st_names)} 등 인근 역 상세 페이지에서 주변 생활권과 예약 가능 시간을 안내합니다.")
            s3 = _home_section("STATION", f"{name} 인근 지하철역 안내",
                A + lib.P(st_intro) + "</div>" + f'<div style="margin-top:24px">{st_cards}</div>',
                pad_top=False)
        else:
            s3 = ""

        # 4) 코스·테마 (자치구명·동·유형으로 차별화) + 가격표
        dong_txt = "·".join(b + "동" for _, b in dong_list[:3]) if dong_list else f"{name} 전역"
        s4 = _home_section("COURSE & THEME", f"{name} 추천 코스 및 테마",
            A + lib.P(
            f"{name}에서는 {_focus_intro(name, focus)} 이러한 특성에 맞춰 {_focus_course(name, focus)}",
            f"{name} {dong_txt} 등 주거·업무 생활권에서는 이동 없이 자택과 오피스텔에서 받는 방문 관리를 선호합니다. "
            f"처음이라면 전신을 고르게 받는 90분 코스가 무난하며, {name}에서 받을 수 있는 전체 코스와 정찰 요금은 "
            "<a href='/course/'>코스안내</a>와 <a href='/theme/'>테마별 안내</a>에서 확인할 수 있습니다.") + "</div>"
            + lib.pmenu(),
            pad_top=False)

        # 5) 예약·확인사항 (자치구명·인근역으로 차별화)
        s5 = _home_section("RESERVATION", f"{name} 예약 진행 및 이용 전 확인사항",
            A + lib.P(
            f"{name} 방문 예약은 희망 위치와 시간을 확인한 뒤 코스·인원·방문 장소 정보를 기준으로 진행됩니다. "
            f"{name} 내 주거지와 오피스텔, " + (f"{st_names[0]}역 인근 등 " if st_names else "") +
            "어디서든 원활한 방문을 위해 아래 항목을 미리 확인해 주세요.")
            + "<ul><li>정확한 주소와 공동현관 출입 방법</li><li>주차 가능 여부</li>"
              "<li>관리를 받을 조용한 공간</li><li>예약자 연락 가능 여부</li></ul>"
            + lib.P(f"{name} 방문 예약 절차와 변경·취소 안내는 <a href='/reservation/'>예약안내</a>에서 확인할 수 있습니다.") + "</div>",
            pad_top=False)

        # 6) 위생·안전 (자치구명으로 차별화)
        s6 = _home_section("SAFETY", "위생 및 안전 안내",
            A + lib.P(
            f"{name} 인근 방문 관리도 위생과 안전을 가장 우선으로 운영합니다. 타월은 매회 교체하고 도구는 위생적으로 관리하며, "
            "예약 정보 확인과 개인정보 보호를 중요하게 다룹니다. 관리사는 손 위생을 철저히 한 뒤 관리를 시작합니다.",
            f"{name}에서 진행되는 관리도 의료 행위가 아닌 건강관리(이완·휴식) 목적의 방문 관리이며, 무리한 요구나 불법적인 "
            "요청은 진행되지 않습니다. 이용 전 서비스 범위와 <a href='/guide/forbidden/'>금지행위 안내</a>를 확인해 주세요.") + "</div>",
            pad_top=False)

        body = (lib.crumb([("/", "홈"), ("/seoul/area/", "지역별 안내"), (None, name)])
                + lib.lux_hero(f"{rl} · {name}", f"{name} 출장마사지·홈타이 예약 안내",
                    f"{name} 전역 방문 마사지·홈타이 안내입니다. 대표 동과 인근 지하철역, 코스·테마, 예약 전 확인사항을 정리했습니다.")
                + s1 + s2 + s3 + s4 + s5 + s6)

        # 7) FAQ (지역명·인근역으로 차별화)
        near = st_names[0] if st_names else f"{name} 주요 지역"
        faq = [
            (f"{name} 전역 방문이 가능한가요",
             f"예약 시간과 위치, 배정 상황에 따라 가능 여부가 달라질 수 있습니다. {name}는 대표 동을 기준으로 안내하며 정확한 가능 여부는 예약 시 확인합니다."),
            (f"{name}에서 당일 예약도 되나요",
             f"{name}도 당일 예약은 시간대와 배정 상황에 따라 가능 여부가 달라집니다. 저녁 시간대와 주말은 사전 예약을 권장합니다."),
            (f"{name} 인근 지하철역에서도 안내받을 수 있나요",
             f"네. {near}역 등 {name} 인근 역은 <a href='/seoul/stations/'>지하철역별 안내</a>에서 주변 생활권과 함께 확인할 수 있습니다."),
            (f"{name} 요금은 어떻게 되나요",
             f"{name}도 코스·시간에 따라 안내되며 표시 요금은 정찰가입니다. 자세한 내용은 <a href='/course/price/'>가격 안내</a>를 확인하세요."),
        ]
        body += lib.faq_block(faq, title=f"{name} 출장마사지·홈타이 FAQ")

        # 8) 예약문의 CTA + 같은 권역 교차 링크
        sib_links = " · ".join(f'<a href="/seoul/{s}/" style="color:var(--gold)">{n}</a>' for s, n in siblings[:6])
        body += (f'<section class="cta-band"><div>'
                 f'<span class="eyebrow"><span class="pulse"></span>RESERVE</span>'
                 f'<h2>{name} 예약문의</h2>'
                 f'<p style="max-width:680px;margin:12px auto 20px">{name} 방문 마사지·홈타이 예약은 희망 위치와 시간, 코스 정보를 기준으로 안내합니다. '
                 f'대표 동과 인근 지하철역 안내를 확인하신 뒤 문의해 주세요.</p>'
                 + (f'<p style="color:var(--muted);font-size:13px;margin-bottom:20px">{rl} 다른 지역: {sib_links}</p>' if sib_links else '')
                 + f'<div class="actions" style="justify-content:center">'
                 f'<a class="btn btn-primary" href="tel:{lib.PHONE_T}">예약문의 {lib.PHONE_D}</a>'
                 f'<a class="btn btn-ghost" href="/seoul/area/#{rk}">{rl} 안내</a>'
                 f'<a class="btn btn-ghost" href="/theme/">테마별 안내</a>'
                 f'</div></div></section>')

        desc = (f"{name} 출장마사지·홈타이 예약 안내. {name} 대표 동과 인근 지하철역, 코스·테마, "
                "예약 전 확인사항을 한눈에 확인하세요.")
        full_title = f"{name} 출장마사지·홈타이 | {name} 방문 마사지 예약 안내"
        add(f"/seoul/{slug}/", lib.document(f"{name} 출장마사지·홈타이 예약 안내", desc,
            f"/seoul/{slug}/", body, jsonld=lib.faq_jsonld(faq), full_title=full_title), "0.7", "weekly")


# ────────────────────────── 동(洞) 상세 ──────────────────────────
def build_dongs():
    valid_st = {s for s, *_ in data.all_stations()}
    A = '<div class="article">'
    for gu_slug, dong_list in data.DONGS.items():
        gu_name, rk, rl = data.GU_BY_SLUG[gu_slug]
        focus = GU_FOCUS_OF.get(gu_slug, "")
        st_slugs = [s for s in data.GU_STATIONS.get(gu_slug, []) if s in valid_st][:4]
        st_named = [(s, data.station_name(s)) for s in st_slugs]
        th = THEME_SETS.get(focus, DEFAULT_THEMES)
        th_named = [(s, data.THEME_BY_SLUG[s][0]) for s in th]

        for dslug, base in dong_list:
            dn = base + "동"
            sibs = [(s, b + "동") for s, b in dong_list if s != dslug]

            # 1) 이용 안내
            s1 = _home_section("GUIDE", f"{dn} 출장마사지·홈타이 이용 안내",
                A + lib.P(
                f"{gu_name} {dn} 인근에서 방문 마사지와 홈타이 예약을 찾는 분들을 위해 이용 가능 지역과 코스 선택 기준, "
                f"예약 전 확인사항을 안내합니다. {dn}은 {gu_name}에 속한 생활권으로, 주거지와 오피스텔이 함께 형성되어 있습니다.",
                f"예약 시에는 정확한 위치와 희망 시간, 코스, 인원 정보를 기준으로 방문 가능 여부를 확인합니다. "
                f"{dn} 인근 자택과 오피스텔, 숙소 등 조용히 휴식할 수 있는 공간이라면 이용할 수 있으며, "
                "만 19세 이상 성인을 대상으로 한 건강관리(이완·휴식) 목적의 방문 관리입니다.") + "</div>",
                pad_top=False)

            # 2) 인근 방문 가능 생활권
            sib_txt = "·".join(n for _, n in sibs[:3]) if sibs else f"{gu_name} 인근"
            s2 = _home_section("AREA", f"{dn} 인근 방문 가능 생활권",
                A + lib.P(
                f"{dn}은 {gu_name} {sib_txt} 생활권과 가까운 지역입니다. 주변에는 주거지와 오피스텔, 상가가 함께 형성되어 있어, "
                "예약 시 정확한 주소와 공동현관 출입 방법을 기준으로 방문 가능 여부를 확인하는 것이 좋습니다.")
                + f"<ul><li>{dn} 주거지 방문 안내</li><li>{dn} 인근 오피스텔·숙소 방문 안내</li>"
                  f"<li>{dn} 조용한 공간 우선 안내</li></ul>"
                + lib.P(f"{dn} 일대는 도보 생활권이 넓어, 방문 위치와 시간을 미리 알려 주시면 더 정확히 안내해 드릴 수 있습니다.")
                + "</div>",
                pad_top=False)

            # 3) 주변 지역 함께 보기
            links = [(f"/seoul/{gu_slug}/", f"{gu_name} 출장마사지")]
            links += [(f"/seoul/{gu_slug}/{s}/", n) for s, n in sibs[:4]]
            links += [(f"/seoul/stations/{s}-station/", f"{n}역") for s, n in st_named]
            link_html = "".join(f'<li><a href="{h}">{esc(t)}</a></li>' for h, t in links)
            s3 = _home_section("NEARBY", f"{dn} 주변 지역 함께 보기",
                A + lib.P(
                f"{dn}과 함께 살펴보면 좋은 인근 동과 지하철역을 안내합니다. 인근 지역은 내부링크로 연결하며, "
                "지역과 테마를 조합한 별도 페이지는 만들지 않습니다.") + "</div>"
                + f'<ul style="max-width:760px;columns:2;color:#c8c8d0">{link_html}</ul>',
                pad_top=False)

            # 4) 많이 찾는 테마 + 가격표
            th_links = "".join(f'<li><a href="/theme/{s}/">{esc(n)}</a></li>' for s, n in th_named)
            s4 = _home_section("THEME", f"{dn}에서 많이 찾는 테마",
                A + lib.P(
                f"{dn} 인근에서는 {', '.join(n for _, n in th_named)} 등을 많이 찾습니다. "
                "이용 목적에 맞는 테마를 선택하면 만족도가 높으며, 각 테마의 특징과 추천 대상은 아래 안내 페이지에서 비교할 수 있습니다. "
                "지역이나 역과 조합한 별도 페이지 대신 테마 안내 페이지에서 정보를 확인하세요.") + "</div>"
                + f'<ul style="max-width:760px;color:#c8c8d0">{th_links}</ul>' + lib.pmenu(),
                pad_top=False)

            # 5) 예약 가능 시간
            s5 = _home_section("HOURS", "예약 가능 시간",
                A + lib.P(
                f"{dn} 인근 방문 예약은 연중무휴 24시간 상담으로 접수합니다. {gu_name} {dn} 일대는 저녁 시간대와 주말에 "
                "문의가 몰릴 수 있어, 원하는 시간이 있다면 여유 있게 예약하시는 것이 좋습니다.",
                f"{dn} 인근 당일 예약은 시간대와 배정 상황에 따라 달라지므로 전화로 확인해 주세요. 심야·새벽 시간대 이용도 가능하며, "
                "정확한 위치를 함께 알려 주시면 방문 시간을 더 정확히 안내해 드릴 수 있습니다.") + "</div>",
                pad_top=False)

            # 6) 방문 전 준비사항
            s6 = _home_section("PREPARE", "방문 전 준비사항",
                A + lib.P(f"{gu_name} {dn} 인근 방문 전에는 아래 사항을 미리 확인해 주시면 예약이 더 원활합니다.")
                + "<ul><li>정확한 주소와 공동현관 출입 방법</li><li>주차 가능 여부</li>"
                  "<li>관리를 받을 조용한 공간</li><li>예약자 연락 가능 여부</li></ul>"
                + lib.P(f"{dn}의 숙소나 오피스텔의 경우 건물 출입 방법과 호수를 함께 알려 주시면 방문이 수월합니다.") + "</div>",
                pad_top=False)

            # 7) 위생 및 안전
            s7 = _home_section("SAFETY", "위생 및 안전 안내",
                A + lib.P(
                f"{dn} 인근 방문 관리도 위생과 안전을 가장 우선으로 운영합니다. 타월은 매회 교체하고 도구는 위생적으로 관리하며, "
                "예약 정보 확인과 개인정보 보호를 중요하게 다룹니다.",
                f"{dn}에서 진행되는 관리도 의료 행위가 아닌 건강관리(이완·휴식) 목적의 방문 관리이며, 무리한 요구나 불법적인 요청은 "
                "진행되지 않습니다. 이용 전 서비스 범위와 <a href='/guide/forbidden/'>금지행위 안내</a>를 확인해 주세요.") + "</div>",
                pad_top=False)

            body = (lib.crumb([("/", "홈"), ("/seoul/area/", "지역별 안내"),
                               (f"/seoul/{gu_slug}/", gu_name), (None, dn)])
                    + lib.lux_hero(f"{gu_name} · {dn}", f"{dn} 출장마사지·홈타이 예약 안내",
                        f"{gu_name} {dn} 인근 출장마사지·홈타이 안내입니다. 방문 가능 생활권과 주변 지역, 예약 가능 시간, "
                        "이용 전 확인사항을 정리했습니다.")
                    + s1 + s2 + s3 + s4 + s5 + s6 + s7)

            # 8) FAQ
            faq = [
                (f"{dn} 인근 방문이 가능한가요",
                 f"예약 시간, 정확한 위치, 배정 상황에 따라 가능 여부가 달라질 수 있습니다. {gu_name} {dn} 인근 생활권을 기준으로 확인할 수 있습니다."),
                (f"{dn} 숙소나 오피스텔도 가능한가요",
                 f"{dn} 인근 숙소·오피스텔 방문 가능 여부는 건물 출입 방법과 예약 시간에 따라 달라질 수 있습니다. 공동현관 출입 방법과 정확한 주소를 미리 확인해 주세요."),
                (f"{dn}에서 당일 예약도 가능한가요",
                 f"당일 예약은 가능할 수 있지만 {dn} 일대도 저녁 시간대와 주말에는 문의가 몰릴 수 있습니다. 여유 있는 예약을 권장합니다."),
                (f"{dn}에서 어떤 테마를 선택하면 좋나요",
                 f"{dn} 인근에서는 {', '.join(n for _, n in th_named[:3])} 등을 많이 찾습니다. 휴식 목적이라면 "
                 "<a href='/theme/aroma-therapy/'>아로마테라피</a>, 근육 이완이 필요하다면 <a href='/theme/sports-massage/'>스포츠·경락</a> 안내를 참고할 수 있습니다."),
            ]
            body += lib.faq_block(faq, title=f"{dn} 출장마사지·홈타이 FAQ")

            # 9) 예약문의 CTA
            sib_links = " · ".join(f'<a href="/seoul/{gu_slug}/{s}/" style="color:var(--gold)">{n}</a>'
                                   for s, n in sibs[:5])
            body += (f'<section class="cta-band"><div>'
                     f'<span class="eyebrow"><span class="pulse"></span>RESERVE</span>'
                     f'<h2>{dn} 예약문의</h2>'
                     f'<p style="max-width:680px;margin:12px auto 20px">{gu_name} {dn} 인근 방문 마사지·홈타이 예약은 정확한 위치와 '
                     f'희망 시간, 코스 정보를 기준으로 안내합니다. 인근 생활권과 주변 지역 안내를 확인하신 뒤 문의해 주세요.</p>'
                     + (f'<p style="color:var(--muted);font-size:13px;margin-bottom:20px">{gu_name} 다른 동: {sib_links}</p>' if sib_links else '')
                     + f'<div class="actions" style="justify-content:center">'
                     f'<a class="btn btn-primary" href="tel:{lib.PHONE_T}">예약문의 {lib.PHONE_D}</a>'
                     f'<a class="btn btn-ghost" href="/seoul/{gu_slug}/">{gu_name} 안내</a>'
                     f'<a class="btn btn-ghost" href="/theme/">테마별 안내</a>'
                     f'</div></div></section>')

            full_title = f"{dn} 출장마사지·홈타이 | {gu_name} {dn} 방문 마사지 안내"
            desc = (f"{dn} 출장마사지·홈타이 안내 페이지입니다. {gu_name} {dn} 인근 생활권, 방문 가능 지역, "
                    "예약 가능 시간, 이용 전 확인사항을 확인해보세요.")
            add(f"/seoul/{gu_slug}/{dslug}/",
                lib.document(f"{dn} 출장마사지·홈타이 예약 안내", desc,
                             f"/seoul/{gu_slug}/{dslug}/", body,
                             jsonld=lib.faq_jsonld(faq), full_title=full_title), "0.6", "weekly")


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

    # 역별 페이지 — 노선·인근 자치구·생활권 기반 9섹션 구성
    A = '<div class="article">'

    for st, sname, ls, ll in allst:
        lines = data.station_lines(st)
        transfer = len(lines) >= 2
        gu_slug = data.STATION_GU.get(st)
        gu = data.GU_BY_SLUG.get(gu_slug) if gu_slug else None
        gu_name = gu[0] if gu else None
        focus = GU_FOCUS_OF.get(gu_slug, "") if gu_slug else ""
        dong_list = data.DONGS.get(gu_slug, []) if gu_slug else []   # [(slug, base)]
        dong_names = [b + "동" for _, b in dong_list]
        neighbors = [(n, data.station_name(n)) for n in data.station_neighbors(st)][:5]
        line_txt = "·".join(lines) if lines else ll

        if transfer:
            line_sentence = (f"{sname}역은 {line_txt}이 지나는 환승역으로 여러 방향에서 접근이 쉬워, "
                             "예약 시간에 맞춘 방문도 수월한 편입니다.")
        else:
            line_sentence = (f"{sname}역은 {line_txt} 구간에 위치한 역으로 인근 도로 연결이 좋아, "
                             "예약 시간에 맞춘 방문이 수월한 편입니다.")

        # 1) 이용 안내
        s1 = _home_section("GUIDE", f"{sname}역 출장마사지·홈타이 이용 안내",
            A + lib.P(
            f"{sname}역 인근에서 방문 마사지와 홈타이 예약을 찾는 분들을 위해 이용 가능 지역과 코스 선택 기준, "
            f"예약 전 확인사항을 안내합니다. {line_sentence}",
            f"예약 시에는 정확한 위치와 희망 시간, 코스, 인원 정보를 기준으로 방문 가능 여부를 확인합니다. "
            f"{sname}역 인근 자택과 오피스텔, 숙소 등 조용히 휴식할 수 있는 공간이라면 이용할 수 있으며, "
            "만 19세 이상 성인을 대상으로 한 건강관리(이완·휴식) 목적의 방문 관리입니다.") + "</div>",
            pad_top=False)

        # 2) 인근 방문 가능 생활권 (대표 동을 동 페이지로 링크)
        if gu_name and dong_list:
            life_lead = (f"{sname}역은 {gu_name} {'·'.join(dong_names[:3])} 생활권과 연결되는 역세권입니다. "
                         "주변에는 주거지와 오피스텔, 병원·공원 인근 생활권이 함께 형성되어 있어, "
                         "예약 시 정확한 주소와 공동현관 출입 방법을 기준으로 방문 가능 여부를 확인하는 것이 좋습니다.")
            life_items = [f'{sname}역 인근 <a href="/seoul/{gu_slug}/{ds}/">{b}동</a> 생활권'
                          for ds, b in dong_list[:4]] + [f"{sname}역 인근 주거지·숙소·오피스텔 방문 안내"]
        else:
            life_lead = (f"{sname}역 인근은 주거지와 오피스텔, 숙소가 함께 형성된 생활권입니다. "
                         "예약 시 정확한 주소와 공동현관 출입 방법을 기준으로 방문 가능 여부를 확인하는 것이 좋습니다.")
            life_items = [f"{sname}역 인근 주거지 방문 안내", f"{sname}역 인근 오피스텔·숙소 방문 안내", "조용한 공간 우선 안내"]
        s2 = _home_section("AREA", f"{sname}역 인근 방문 가능 생활권",
            A + lib.P(life_lead)
            + "<ul>" + "".join(f"<li>{x}</li>" for x in life_items) + "</ul>"
            + lib.P(f"{sname}역 인근은 도보 생활권이 넓게 분포해, 방문 위치와 시간을 미리 알려 주시면 "
                    "더 정확하게 안내해 드릴 수 있습니다.") + "</div>",
            pad_top=False)

        # 3) 주변 지역 함께 보기 (내부링크)
        links = []
        if gu_name:
            links.append((f"/seoul/{gu_slug}/", f"{gu_name} 출장마사지"))
        for nslug, nname in neighbors:
            links.append((f"/seoul/stations/{nslug}-station/", f"{nname}역"))
        for lsx, llx, _ in data.LINES:
            if llx in lines:
                links.append((f"/seoul/stations/{lsx}/", llx))
        link_html = "".join(f'<li><a href="{h}">{esc(t)}</a></li>' for h, t in links)
        s3 = _home_section("NEARBY", f"{sname}역 주변 지역 함께 보기",
            A + lib.P(
            f"{sname}역과 함께 살펴보면 좋은 인근 지역과 역을 안내합니다. 환승역이나 인근 역은 내부링크로 연결하며, "
            "역과 테마를 조합한 별도 페이지는 만들지 않습니다.") + "</div>"
            + f'<ul style="max-width:760px;columns:2;color:#c8c8d0">{link_html}</ul>',
            pad_top=False)

        # 4) 많이 찾는 테마 + 가격표
        th = THEME_SETS.get(focus, DEFAULT_THEMES)
        th_named = [(s, data.THEME_BY_SLUG[s][0]) for s in th]
        th_links = "".join(f'<li><a href="/theme/{s}/">{esc(n)}</a></li>' for s, n in th_named)
        s4 = _home_section("THEME", f"{sname}역에서 많이 찾는 테마",
            A + lib.P(
            f"{sname}역 인근에서는 {', '.join(n for _, n in th_named)} 등을 많이 찾습니다. "
            "이용 목적에 맞는 테마를 선택하면 만족도가 높으며, 각 테마의 특징과 추천 대상은 아래 안내 페이지에서 비교할 수 있습니다. "
            "지역이나 역과 조합한 별도 페이지 대신 테마 안내 페이지에서 정보를 확인하세요.") + "</div>"
            + f'<ul style="max-width:760px;color:#c8c8d0">{th_links}</ul>'
            + lib.pmenu(),
            pad_top=False)

        # 5) 예약 가능 시간 (역·노선 정보로 차별화)
        nb_first = neighbors[0][1] if neighbors else None
        s5 = _home_section("HOURS", "예약 가능 시간",
            A + lib.P(
            f"{sname}역({line_txt}) 인근 방문 예약은 연중무휴 24시간 상담으로 접수합니다. "
            + (f"{line_txt}이 만나는 환승역이라 여러 방향에서 이동이 가능하지만, " if transfer
               else f"{sname}역 일대는 ")
            + "저녁 시간대와 주말에는 문의가 몰릴 수 있어 원하는 시간이 있다면 여유 있게 예약하시는 것이 좋습니다.",
            f"{sname}역 인근 당일 예약은 시간대와 배정 상황에 따라 달라지므로 전화로 확인해 주세요. 심야·새벽 시간대 이용도 가능하며, "
            + (f"{gu_name} 내 정확한 위치" if gu_name else "정확한 위치")
            + "를 함께 알려 주시면 방문 시간을 더 정확히 안내해 드릴 수 있습니다.") + "</div>",
            pad_top=False)

        # 6) 방문 전 준비사항 (역·인근역으로 차별화)
        s6 = _home_section("PREPARE", "방문 전 준비사항",
            A + lib.P(
            f"{sname}역 인근"
            + (f" {gu_name} " if gu_name else " ")
            + "방문 전에는 아래 사항을 미리 확인해 주시면 예약이 더 원활합니다.")
            + "<ul><li>정확한 주소와 공동현관 출입 방법</li><li>주차 가능 여부</li>"
              "<li>관리를 받을 조용한 공간</li><li>예약자 연락 가능 여부</li></ul>"
            + lib.P(
            f"{sname}역 인근 숙소나 오피스텔의 경우 건물 출입 방법과 호수를 함께 알려 주시면 방문이 수월합니다."
            + (f" {nb_first}역 등 인근에서 이동해 머무는 경우에도 동일하게 위치를 확인합니다." if nb_first else "")) + "</div>",
            pad_top=False)

        # 7) 위생 및 안전 안내 (역명으로 차별화)
        s7 = _home_section("SAFETY", "위생 및 안전 안내",
            A + lib.P(
            f"{sname}역 인근 방문 관리도 위생과 안전을 가장 우선으로 운영합니다. 타월은 매회 교체하고 도구는 위생적으로 관리하며, "
            "예약 정보 확인과 개인정보 보호를 중요하게 다룹니다. 관리사는 손 위생을 철저히 한 뒤 관리를 시작합니다.",
            f"{sname}역 인근에서 진행되는 관리도 의료 행위가 아닌 건강관리(이완·휴식) 목적의 방문 관리이며, 무리한 요구나 불법적인 요청은 "
            "진행되지 않습니다. 이용 전 서비스 범위와 <a href='/guide/forbidden/'>금지행위 안내</a>를 확인해 주세요.") + "</div>",
            pad_top=False)

        body = (lib.crumb([("/", "홈"), ("/seoul/stations/", "지하철역별 안내"),
                           (f"/seoul/stations/{ls}/", ll), (None, sname + "역")])
                + lib.lux_hero(f"{line_txt} · {sname}역", f"{sname}역 출장마사지·홈타이 예약 안내",
                    f"{sname}역 인근 출장마사지·홈타이 안내입니다. 방문 가능 생활권과 주변 지역, 예약 가능 시간, "
                    "이용 전 확인사항을 정리했습니다.")
                + s1 + s2 + s3 + s4 + s5 + s6 + s7)

        # 8) FAQ
        d_txt = ", ".join(dong_names[:3]) if dong_names else f"{sname}역 인근 생활권"
        theme_a = th_named[1][1] if len(th_named) > 1 else "아로마테라피"
        nb_faq = ", ".join(f"{nm}역" for _, nm in neighbors[:3]) or "인근 역"
        th_faq = ", ".join(n for _, n in th_named[:3])
        faq = [
            (f"{sname}역 인근 방문이 가능한가요",
             f"예약 시간, 정확한 위치, 배정 상황에 따라 가능 여부가 달라질 수 있습니다. {sname}역 인근 {d_txt} 생활권을 기준으로 확인할 수 있습니다."),
            (f"{sname}역 근처 숙소나 오피스텔도 가능한가요",
             f"{sname}역 인근 숙소·오피스텔 방문 가능 여부는 건물 출입 방법과 예약 시간에 따라 달라질 수 있습니다. 공동현관 출입 방법과 정확한 주소를 미리 확인해 주세요."),
            (f"{sname}역에서 당일 예약도 가능한가요",
             f"당일 예약은 가능할 수 있지만 {sname}역 일대도 저녁 시간대와 주말에는 문의가 몰릴 수 있습니다. 여유 있는 예약을 권장합니다."),
            (f"{sname}역 인근에서 어떤 테마를 선택하면 좋나요",
             f"{sname}역 인근에서는 {th_faq} 등을 많이 찾습니다. 휴식 목적이라면 <a href='/theme/aroma-therapy/'>아로마테라피</a>, "
             "피로 회복 중심이라면 <a href='/theme/home-care/'>홈케어</a>, 근육 이완이 필요하다면 <a href='/theme/sports-massage/'>스포츠·경락</a> 안내를 참고할 수 있습니다."),
            (f"{sname}역 예약 전 준비할 것이 있나요",
             f"정확한 주소와 출입 방법, 주차 가능 여부, 조용한 공간을 미리 확인하면 {sname}역 인근 방문이 원활합니다. {nb_faq} 등 인근에서 이동하는 경우에도 동일합니다."),
        ]
        body += lib.faq_block(faq, title=f"{sname}역 출장마사지·홈타이 FAQ")

        # 9) 예약문의 CTA
        nb_links = " · ".join(f'<a href="/seoul/stations/{n}-station/" style="color:var(--gold)">{nm}역</a>'
                              for n, nm in neighbors[:4])
        body += (f'<section class="cta-band"><div>'
                 f'<span class="eyebrow"><span class="pulse"></span>RESERVE</span>'
                 f'<h2>{sname}역 예약문의</h2>'
                 f'<p style="max-width:680px;margin:12px auto 20px">{sname}역 인근 방문 마사지·홈타이 예약은 정확한 위치와 '
                 f'희망 시간, 코스 정보를 기준으로 안내합니다. 인근 생활권과 주변 역 안내를 확인하신 뒤 문의해 주세요.</p>'
                 + (f'<p style="color:var(--muted);font-size:13px;margin-bottom:20px">인근 역: {nb_links}</p>' if nb_links else '')
                 + f'<div class="actions" style="justify-content:center">'
                 f'<a class="btn btn-primary" href="tel:{lib.PHONE_T}">예약문의 {lib.PHONE_D}</a>'
                 + (f'<a class="btn btn-ghost" href="/seoul/{gu_slug}/">{gu_name} 안내</a>' if gu_name else '')
                 + f'<a class="btn btn-ghost" href="/theme/">테마별 안내</a>'
                 f'</div></div></section>')

        full_title = (f"{sname}역 출장마사지·홈타이 | {gu_name} {sname}역 방문 마사지 안내"
                      if gu_name else f"{sname}역 출장마사지·홈타이 | {sname}역 인근 방문 마사지 안내")
        desc = (f"{sname}역 출장마사지·홈타이 안내 페이지입니다. "
                + (f"{gu_name} " if gu_name else "") +
                f"{sname}역 인근 생활권, 방문 가능 지역, 예약 가능 시간, 이용 전 확인사항을 확인해보세요.")
        add(f"/seoul/stations/{st}-station/",
            lib.document(f"{sname}역 출장마사지·홈타이 예약 안내", desc,
                         f"/seoul/stations/{st}-station/", body,
                         jsonld=lib.faq_jsonld(faq), full_title=full_title), "0.6", "weekly")


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
        c = content.THEME_CONTENT.get(s)
        if c:
            lead, secs, faq = c
        else:
            lead = d + "입니다."
            secs = [(f"{n}란?", lib.P(f"{n}는 {d}입니다. 컨디션에 맞춰 압과 시간을 조절해 진행합니다.")),
                    ("이용·예약 안내", lib.P("방문 관리로 자택·호텔·오피스텔 어디든 받으실 수 있습니다."))]
            faq = [(f"{n}는 처음도 괜찮나요", "네. 컨디션에 맞춰 진행하니 부담 없이 받으실 수 있습니다.")]
        secs = secs + content.THEME_EXTRA.get(s, []) + content.THEME_EXTRA2.get(s, [])
        secs = secs + [(f"{n} 코스별 기본 요금", lib.P(
            f"{n}는 60분·90분·120분 코스 중 선택할 수 있습니다. 60분은 핵심 부위 위주로 가볍게, 90분은 전신을 고르게, "
            f"120분은 머리부터 발끝까지 충분히 다루기에 적합합니다. 처음 받으신다면 전신을 고르게 받는 90분 코스가 무난합니다.",
            f"표시 요금은 기본 정찰가이며 코스·인원·지역에 따라 달라질 수 있어 예약 시 정확히 안내해 드립니다. "
            f"{n}를 다른 테마나 특정 부위 집중 관리와 함께 구성하는 것도 가능하니, 원하는 구성이 있으면 예약 시 편하게 말씀해 주세요.")
            + lib.pmenu(note=False))]
        related = [("/theme/", "전체 테마 보기"), ("/course/guide/", "코스 선택 가이드"),
                   ("/course/price/", "가격 안내"), ("/reservation/", "예약 방법")]
        full_title = f"{n} 출장마사지·홈타이 | {n} 방문 관리 예약 안내"
        lux_page(f"{n} 안내", f"{n} 출장마사지·홈타이 방문 관리 안내. {lead[:80]}",
                 f"/theme/{s}/", f"THEME · {n}", f"{n} 방문 관리 안내", lead,
                 secs, [("/", "홈"), ("/theme/", "테마별 안내"), (None, n)],
                 faq=faq, related=related, jsonld=lib.faq_jsonld(faq), prio="0.7",
                 full_title=full_title)


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
                ("목적부터 정하세요", lib.P(
                    "어떤 코스가 맞을지 고민이라면 '무엇을 풀고 싶은지' 목적부터 정해 보세요. 전반적인 피로 해소인지, 스트레스와 수면 같은 마음의 긴장 완화인지, 특정 부위의 뭉침 해소인지에 따라 추천이 달라집니다.",
                    "목적이 분명하면 코스 선택이 쉬워지고, 같은 시간에도 더 만족스러운 관리를 받을 수 있습니다.")),
                ("목적별 추천", lib.P("아래는 목적에 따른 대표적인 선택입니다.")
                    + "<ul>"
                    "<li>전반적인 피로 해소 → <a href='/course/fatigue/'>피로 회복 관리</a></li>"
                    "<li>스트레스·불면 등 마음의 긴장 → <a href='/theme/aroma-therapy/'>아로마테라피</a></li>"
                    "<li>운동·자세로 인한 근육 뭉침 → <a href='/course/sports/'>스포츠 관리</a></li>"
                    "<li>활력·유연성 회복 → <a href='/theme/thai-massage/'>타이마사지</a> · <a href='/course/home/'>홈타이</a></li>"
                    "<li>깊은 휴식·숙면 → <a href='/theme/sleep-available/'>수면 가능</a> 관리</li></ul>"
                    + lib.P("두 가지 목적이 함께 있다면 전신은 부드럽게, 뭉친 부위는 집중해서 조합할 수도 있습니다.")),
                ("강도 선택", lib.P(
                    "강한 압이 효과가 좋은 것은 아닙니다. 시원하면서도 부담 없는 강도가 가장 효과적이며, 진행 중 '조금 약하게/강하게'처럼 편하게 요청할 수 있습니다.",
                    "마사지가 처음이라면 부드러운 <a href='/theme/swedish/'>스웨디시</a>부터 시작하는 것을 권합니다.")),
                ("시간 선택", lib.P(
                    "60분은 핵심 부위 위주로 가볍게, 90분은 전신을 고르게, 120분은 머리부터 발끝까지 충분히 다루기에 적합합니다. 처음이라면 전신을 고르게 받는 90분이 무난합니다.",
                    "집중하고 싶은 부위가 많거나 깊은 이완을 원하면 90분 이상을 권합니다.")),
                ("인원·상황별 선택", lib.P(
                    "혼자라면 목적에 맞는 단일 코스를, 두 분 이상이라면 같은 공간에서 함께 받는 <a href='/course/couple/'>커플·가족 방문</a>을 선택할 수 있습니다. 사무실·행사장 단체는 <a href='/course/group/'>기업·단체 방문</a>으로 안내합니다.",
                    "요금은 <a href='/course/price/'>가격 안내</a>에서 확인할 수 있습니다.")),
                ("정기 이용과 빈도", lib.P(
                    "한 번의 관리로도 컨디션이 가벼워지지만, 효과를 오래 유지하려면 정기적인 이용이 도움이 됩니다. 피로가 많이 쌓이는 분은 주 1회, 평소 관리 차원이라면 2~3주에 한 번 정도가 적당합니다.",
                    "정기적으로 받는다면 같은 코스만 고집하기보다 컨디션에 따라 바꿔 가며 받는 것이 좋습니다. 평소에는 전신 이완 위주로, 뭉침이 심한 주에는 부위 집중 관리로 조절하는 식입니다.")),
                ("이럴 땐 이렇게", lib.P(
                    "야근이 몰린 한 주에는 어깨·등을 풀어 주는 <a href='/course/sports/'>스포츠 관리</a>, 잠이 잘 오지 않는 시기에는 <a href='/theme/sleep-available/'>수면 가능</a> 관리나 아로마가 잘 맞습니다.",
                    "운동을 시작했거나 자세 교정 중이라면 유연성에 도움이 되는 <a href='/theme/thai-massage/'>타이마사지</a>를, 특별한 날에는 함께 받는 커플 관리를 선택하는 등 상황에 맞춰 고르면 만족도가 높습니다.")),
            ]
        cc = content.COURSE_CONTENT.get(s)
        if s in ("price", "guide"):
            lead = d + "입니다."
            faq = [
                ("요금이 궁금해요", "60분 90,000원, 90분 150,000원, 120분 180,000원 정찰 요금 기준입니다."),
                ("예약은 어떻게 하나요", f"{lib.PHONE_D}로 전화 주시면 24시간 안내해 드립니다."),
            ]
        elif cc:
            lead, secs, faq = cc
        else:
            lead = d + "입니다."
            secs = [(f"{n}란?", lib.P(f"{n}는 {d}입니다. 컨디션에 맞춰 진행합니다.")),
                    ("요금·예약", lib.P("요금은 <a href='/course/price/'>가격 안내</a>를 참고하세요."))]
            faq = [("예약은 어떻게 하나요", f"{lib.PHONE_D}로 전화 주시면 24시간 안내해 드립니다.")]
        if s != "price":
            secs = secs + content.COURSE_EXTRA.get(s, []) + content.COURSE_EXTRA2.get(s, [])
            secs = secs + [("코스별 기본 요금", lib.P(
                f"{n}는 60분·90분·120분 중 선택할 수 있습니다. 60분은 핵심 부위 위주로 가볍게, 90분은 전신을 고르게, "
                "120분은 머리부터 발끝까지 충분히 다루기에 적합합니다. 처음이라면 전신을 고르게 받는 90분이 무난합니다.",
                f"표시 요금은 기본 정찰가이며 코스·인원·지역에 따라 달라질 수 있어 예약 시 정확히 안내해 드립니다. "
                f"{n}를 다른 코스나 특정 부위 집중 관리와 함께 구성하는 것도 가능하니 원하는 구성을 예약 시 말씀해 주세요.")
                + lib.pmenu(note=False))]
        related = [("/course/", "전체 코스"), ("/course/price/", "가격 안내"),
                   ("/course/guide/", "코스 선택 가이드"), ("/reservation/", "예약 방법")]
        full_title = f"{n} | 출장마사지·홈타이 코스 안내"
        lux_page(f"{n}", f"{n} 안내 — {lead[:80]}", f"/course/{s}/", f"COURSE · {n}", n, lead,
                 secs, [("/", "홈"), ("/course/", "코스안내"), (None, n)],
                 faq=faq, related=related, jsonld=lib.faq_jsonld(faq), prio="0.7",
                 full_title=full_title)


# ────────────────────────── 예약 / 가이드 / 후기 / 고객센터 ──────────────────────────
RES_CONTENT = {
    "": ("예약 방법", [
        ("예약 방법", lib.P(f"예약은 전화 한 통이면 됩니다. {lib.PHONE_D}로 원하는 날짜·시간, 방문 주소, 코스와 인원을 알려주세요. 연중무휴 24시간 상담이 가능합니다.")),
        ("예약 시 알려주실 정보", "<ul><li>희망 날짜·시간</li><li>방문 주소(동·호수, 가까운 출구)</li><li>코스·시간</li><li>인원</li><li>요청 사항(여성 관리사 등)</li></ul>"),
        ("진행 안내", lib.P("예약이 확정되면 관리사가 출발·도착 시 연락드립니다. 변경이 필요하면 가능한 빨리 알려주세요.")),
    ]),
    "hours/": ("예약 가능 시간", [
        ("연중무휴 24시간 운영", lib.P(
            "웰니스센터는 연중무휴 24시간 상담·예약을 운영합니다. 평일과 주말, 공휴일 구분 없이 동일하게 접수하며, 정해진 영업시간에 얽매이지 않고 본인의 일정에 맞춰 이용할 수 있습니다.",
            "낮에 시간을 내기 어려운 분, 교대근무로 생활 패턴이 불규칙한 분도 원하는 시간대를 정해 예약할 수 있습니다.")),
        ("혼잡한 시간대 안내", lib.P(
            "퇴근 이후의 저녁 시간대와 주말, 기념일은 문의가 몰려 원하는 시간이 빠르게 마감될 수 있습니다. 특정 시간대를 꼭 이용하고 싶다면 며칠 전 미리 예약해 두는 것을 권합니다.",
            "커플·가족 방문이나 120분 같은 장시간 코스는 배정에 시간이 더 필요하므로 더 여유 있게 문의해 주세요.")),
        ("당일·사전 예약", lib.P(
            "당일 예약도 시간대와 관리사 배정 상황에 따라 가능합니다. 다만 원하는 시간에 바로 방문이 어려울 수 있으므로, 가능하면 하루 이틀 전 예약해 두면 일정을 잡기 수월합니다.",
            "예약 시 희망 위치와 시간, 코스, 인원을 함께 알려주시면 가능 여부를 더 빠르게 안내해 드립니다.")),
        ("심야·새벽 이용", lib.P(
            "야근 후나 늦은 밤, 새벽 시간에도 동일하게 예약할 수 있습니다. 심야에는 정확한 주소와 공동현관 출입 방법, 가까운 출구 번호를 함께 알려주시면 빠른 방문에 도움이 됩니다.",
            "취침 전 시간대라면 긴장을 낮춰 자연스러운 졸음을 유도하는 부드러운 이완 코스가 좋습니다.")),
        ("예약 시 알려주실 정보", lib.P(
            "원하는 시간에 정확히 방문하려면 예약 단계에서 몇 가지 정보를 함께 알려주시면 좋습니다. 정확한 주소와 공동현관 출입 방법, 가까운 출구 번호가 있으면 방문이 한결 빨라집니다.",
            "여기에 희망 코스와 시간, 인원, 그리고 여성 관리사 배정이나 선호 향 같은 요청 사항을 더해 주시면 가능 여부와 예상 방문 시간을 더 정확히 안내해 드릴 수 있습니다.")),
        ("시간대별 추천 코스", lib.P(
            "같은 코스라도 받는 시간대에 따라 잘 어울리는 구성이 조금씩 다릅니다. 낮이나 이른 저녁에는 전신을 고르게 받는 90분 코스가 무난하고, 취침 전 늦은 시간에는 긴장을 낮춰 자연스러운 졸음을 유도하는 부드러운 이완 코스가 좋습니다.",
            "야근 후라면 뭉친 어깨·등을 풀어 주는 관리가, 휴일 낮에는 충분히 시간을 들이는 120분 코스가 잘 맞습니다. 코스 선택이 고민이라면 <a href='/course/guide/'>코스 선택 가이드</a>를 참고하세요.")),
        ("예약이 몰리는 날 이용 팁", lib.P(
            "기념일이나 금요일 저녁처럼 예약이 집중되는 날은 원하는 시간이 빠르게 마감될 수 있습니다. 이런 날은 시간대를 조금 앞당기거나 늦추면 더 수월하게 예약할 수 있습니다.",
            "꼭 특정 시간이어야 한다면 며칠 전 미리 예약해 두는 것이 가장 확실합니다. 평일 낮이나 늦은 밤처럼 비교적 여유 있는 시간대를 활용하는 것도 방법입니다.")),
        ("코스별 소요 시간", lib.P(
            "예약 시간을 잡을 때는 코스 시간 외에 준비와 정리 시간을 함께 고려하면 좋습니다. 관리 자체는 60분·90분·120분 중 선택하지만, 베드 설치와 마무리에 약간의 시간이 더 소요됩니다.",
            "커플·가족 방문처럼 인원이 늘면 전체 소요 시간도 길어지므로, 다음 일정이 있다면 여유를 두고 예약하시는 것이 좋습니다.")),
        ("예약 확정·도착 안내", lib.P(
            "예약이 확정되면 희망 시간과 방문 위치를 다시 확인해 드립니다. 관리사는 출발과 도착 시점에 연락드리므로, 정확한 방문 시간을 미리 알 수 있습니다.",
            "교통 상황 등으로 시간이 조정될 경우에도 사전에 안내드리니, 예약자 본인이 연락 가능한 상태로 있어 주시면 진행이 매끄럽습니다.")),
        ("예약 변경·취소", lib.P(
            "일정 변경이나 취소가 필요하면 가능한 한 빨리 알려 주세요. 임박한 변경은 관리사 배정 조율이 어려울 수 있어 양해를 부탁드립니다.",
            "자세한 내용은 <a href='/reservation/change/'>변경·취소 안내</a>를 참고하시고, 예약 방법은 <a href='/reservation/'>예약안내</a>에서 확인할 수 있습니다.")),
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
        ("타월·도구 위생 기준", lib.P(
            "관리에 사용하는 타월은 매회 새것으로 교체하며, 1회 사용 후 위생적으로 세탁·관리합니다. 오일과 도구는 청결하게 보관하고, 소모품은 위생을 고려해 다룹니다.",
            "고객이 매번 깨끗한 용품으로 관리를 받을 수 있도록 하는 것이 방문 관리의 기본입니다. 위생은 한두 가지를 잘 지키는 것이 아니라 용품 준비부터 관리, 정리까지 전 과정에서 일관되게 유지되어야 의미가 있습니다.")),
        ("관리사 위생 관리", lib.P(
            "관리사는 방문 후 손 위생을 철저히 한 뒤 관리를 시작합니다. 컨디션 관리와 청결 유지를 기본으로 하며, 고객이 안심하고 받을 수 있는 환경을 우선합니다.")),
        ("건전한 서비스 운영", lib.P(
            "본 서비스는 만 19세 이상 성인을 대상으로 한 건강관리(이완·휴식) 목적의 방문 관리입니다. 불법·퇴폐 행위는 일절 제공하지 않으며, 관리사는 정해진 절차에 따라 정중하게 진행합니다.",
            "무리한 요구나 부적절한 언행 시에는 관리사 보호를 위해 관리가 중단될 수 있습니다. 자세한 내용은 <a href='/guide/forbidden/'>금지행위 안내</a>를 참고하세요.")),
        ("개인정보 보호", lib.P(
            "예약 과정에서 받은 연락처와 주소 등 개인정보는 예약 이행 목적으로만 이용하며, 목적 달성 후에는 관련 기준에 따라 관리합니다. 자세한 내용은 <a href='/privacy/'>개인정보처리방침</a>에서 확인할 수 있습니다.")),
        ("여성 고객·건강 안내", lib.P(
            "여성 관리사 배정을 원하면 예약 시 요청해 주시면 가능 여부를 안내해 드립니다. 정해진 절차에 따라 안전하게 진행되니 혼자 받으시더라도 안심하셔도 됩니다.",
            "임신 중이거나 질환·통증이 있는 경우 예약 시 미리 알려 주세요. 통증이 지속되는 경우에는 관리보다 의료기관 진료를 우선 권해 드립니다.")),
        ("신뢰할 수 있는 업체 확인 포인트", lib.P(
            "안심하고 이용하려면 예약 단계에서 코스와 요금, 진행 방식을 명확히 안내받는지 확인하는 것이 좋습니다. 투명한 정찰 요금과 사전 안내, 임의 추가 비용이 없는 운영은 신뢰할 수 있는 업체의 기본입니다.",
            "고객의 요청을 즉시 반영해 압과 부위를 조절하는지, 타월 교체와 도구 관리 같은 위생 기준을 지키는지도 함께 살펴보면 도움이 됩니다.")),
        ("관리 중 불편할 때", lib.P(
            "관리를 받는 동안 압이 부담스럽거나 자세가 불편하면 참지 말고 즉시 말씀해 주세요. 강도와 자세를 바로 조절해 드리며, 원하지 않는 부위는 다루지 않습니다.",
            "통증이 느껴지거나 컨디션이 좋지 않으면 관리를 잠시 멈추거나 마무리할 수 있습니다. 고객이 편안하게 이완하는 것이 가장 중요하므로 언제든 편하게 요청하시면 됩니다.")),
        ("안전한 환경 만들기", lib.P(
            "방문 관리는 고객의 공간에서 진행되는 만큼, 관리받을 공간을 정돈하고 충분히 밝혀 두면 더 안전하고 편안합니다. 미끄러운 바닥이나 걸리기 쉬운 물건은 미리 치워 주시면 좋습니다.",
            "예약자 본인이 연락 가능한 상태로 있어 주시고, 공동현관 출입 방법을 미리 전달해 두면 방문이 매끄럽게 진행됩니다.")),
        ("반려동물·동거인이 있을 때", lib.P(
            "집에 반려동물이 있거나 함께 거주하는 가족이 있는 경우, 예약 시 미리 알려 주시면 그에 맞춰 안내해 드립니다. 관리 중에는 조용히 이완할 수 있는 환경이 좋으므로, 반려동물은 별도 공간에 두시면 더 편안합니다.",
            "관리받을 공간과 동선이 안전하게 확보되도록 미리 정돈해 주시면, 관리사와 고객 모두 안심하고 진행할 수 있습니다.")),
        ("미성년자 이용 제한", lib.P(
            "본 서비스는 만 19세 이상 성인을 대상으로 하며, 미성년자의 이용은 제한됩니다. 사이트의 모든 안내는 건강관리 목적의 정보만을 제공합니다.",
            "관련 정책은 <a href='/youth/'>청소년보호정책</a>에서 확인할 수 있습니다.")),
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
        ("서비스 내용 이해하기", lib.P(
            "예약 전에 본 서비스가 어떤 관리인지 먼저 확인하는 것이 좋습니다. 웰니스센터는 만 19세 이상 성인을 대상으로 한 건강관리(이완·휴식) 목적의 방문 관리이며, 의료 행위가 아닙니다.",
            "받고 싶은 관리의 종류와 목적을 정해 두면 상담이 수월합니다. 어떤 코스가 맞을지 고민된다면 <a href='/course/guide/'>코스 선택 가이드</a>를 참고하세요.")),
        ("코스·요금 확인", lib.P(
            "예약 시 코스와 시간, 요금을 명확히 안내받는지 확인하세요. 표시 요금은 정찰가이며 임의로 더해지는 비용은 없습니다. 코스·인원·지역에 따른 차이는 예약 단계에서 미리 안내됩니다.",
            "요금 기준은 <a href='/course/price/'>가격 안내</a>, 결제 방법은 <a href='/reservation/payment/'>결제 안내</a>에서 확인할 수 있습니다.")),
        ("본인 컨디션 확인", lib.P(
            "임신 중이거나 질환·부상·통증이 있는 부위가 있으면 예약 시 미리 알려 주세요. 그에 맞춰 강도와 부위를 조절하며, 통증이 지속되는 경우에는 관리보다 진료를 우선 권해 드립니다.",
            "강한 압을 선호하지 않거나 특정 향에 민감하다면 함께 전달해 주시면 됩니다.")),
        ("위치·시간 확인", lib.P(
            "방문 가능 여부는 예약 시간과 위치, 배정 상황에 따라 달라질 수 있어, 정확한 주소와 희망 시간을 기준으로 확인합니다. 저녁·주말은 문의가 몰릴 수 있어 여유 있게 예약하는 것이 좋습니다.",
            "방문 장소 안내는 <a href='/reservation/place/'>방문 가능 장소</a>를 참고하세요.")),
        ("요청 사항 정리", lib.P(
            "여성 관리사 배정, 선호 향, 집중하고 싶은 부위 등 요청 사항이 있으면 예약 시 함께 전달하면 반영이 수월합니다. 방문 직전 준비는 <a href='/guide/prepare/'>방문 전 준비사항</a>에서 따로 안내합니다.",
            f"궁금한 점은 {lib.PHONE_D}로 24시간 문의하실 수 있습니다.")),
        ("예약 후 진행 미리 알아두기", lib.P(
            "예약을 마쳤다면 이용이 어떤 순서로 진행되는지 미리 알아두면 첫 이용도 편안합니다. 예약 확정 후 관리사가 출발·도착 시 연락드리고, 방문해 베드를 설치한 뒤 선택한 코스대로 관리하고 정리까지 마칩니다.",
            "진행 흐름과 준비 사항은 <a href='/seoul/'>서울 출장마사지 안내</a>의 이용 흐름 항목과 <a href='/guide/'>이용가이드</a>에서도 확인할 수 있습니다.")),
        ("방문 장소별 확인", lib.P(
            "방문 장소에 따라 미리 확인하면 좋은 점이 조금씩 다릅니다. 자택·아파트라면 베드를 놓을 공간과 주차 가능 여부를, 오피스텔·원룸이라면 공동현관 출입 방법과 동·호수를 정리해 두면 좋습니다.",
            "호텔·숙소라면 객실 호수와 체류 일정을 알려주시고, 일부 호텔은 외부 인원 방문에 사전 확인이 필요할 수 있어 함께 확인하면 매끄럽습니다. 방문 가능 장소는 <a href='/reservation/place/'>방문 가능 장소</a>에서 확인할 수 있습니다.")),
        ("결제·취소 정책 확인", lib.P(
            "이용 전에 결제 방법과 변경·취소 기준을 확인해 두면 당일 혼선이 줄어듭니다. 결제 방법은 <a href='/reservation/payment/'>결제 안내</a>에서, 일정 변경과 취소는 <a href='/reservation/change/'>변경·취소 안내</a>에서 확인할 수 있습니다.",
            "임박한 변경·취소는 관리사 배정 조율이 어려울 수 있으므로, 일정이 바뀔 가능성이 있다면 미리 알려 주시는 것이 좋습니다.")),
        ("한눈에 보는 확인 체크리스트", lib.P("예약 전 아래 항목을 가볍게 점검하면 이용이 한결 매끄럽습니다.")
            + "<ul><li>건강관리 목적의 방문 관리임을 이해했는가</li>"
              "<li>받고 싶은 코스와 시간, 요금을 확인했는가</li>"
              "<li>질환·임신·통증 등 알릴 사항을 정리했는가</li>"
              "<li>정확한 주소와 희망 시간을 정했는가</li>"
              "<li>방문 장소별 출입 방법을 확인했는가</li>"
              "<li>여성 관리사·선호 향 등 요청 사항을 준비했는가</li></ul>"
            + lib.P("위 내용이 정리되면 전화 한 통으로 빠르게 예약을 진행할 수 있습니다. 항목이 많아 보여도 대부분 한 번 확인해 두면 다음 이용부터는 훨씬 간단해지며, 빠진 부분이 있어도 예약 상담 과정에서 함께 확인할 수 있으니 부담 없이 문의해 주세요.")),
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
    cat_tip = {
        "guide": "방문 관리는 예약 시 희망 지역과 시간, 코스, 인원을 먼저 확인한 뒤 가능 여부를 안내합니다. 처음이라면 전신을 고르게 받는 90분 코스가 무난하며, 이용 전 <a href='/guide/checklist/'>이용 전 확인사항</a>을 살펴보면 도움이 됩니다.",
        "course-theme": "코스와 테마는 이용 목적과 컨디션에 따라 고르는 것이 좋습니다. 특징과 추천 대상은 <a href='/theme/'>테마별 안내</a>와 <a href='/course/'>코스안내</a>에서 비교할 수 있으며, 두 가지를 조합해 받는 것도 가능합니다.",
        "tips": "일상에서의 작은 습관과 정기적인 관리를 함께 활용하면 컨디션 유지에 도움이 됩니다. 방문 관리는 이동 없이 받을 수 있어, 바쁜 일정 속에서도 꾸준히 이어가기 좋습니다.",
        "area-station": "지역과 역세권은 대표 동과 인근 역을 기준으로 안내합니다. 가까운 위치는 <a href='/seoul/area/'>지역별 안내</a>와 <a href='/seoul/stations/'>지하철역별 안내</a>에서 확인할 수 있으며, 정확한 방문 가능 여부는 예약 시 위치를 기준으로 확인합니다.",
        "region": "서울 자치구별 안내는 대표 동을 기준으로 구성됩니다. 가까운 지역은 <a href='/seoul/area/'>지역별 안내</a>에서 확인할 수 있으며, 같은 지역이라도 예약 시간과 위치에 따라 가능 여부가 달라질 수 있습니다.",
        "swedish": "스웨디시는 부드러운 압의 대표적인 이완 관리로, 처음 받는 분께도 부담이 적습니다. 압과 시간은 컨디션에 맞춰 조절할 수 있으며, 자세한 내용은 <a href='/theme/swedish/'>스웨디시 안내</a>에서 확인할 수 있습니다.",
        "visiting": "출장마사지는 관리사가 직접 방문해 익숙한 공간에서 받는 방문형 서비스입니다. 자택·오피스텔·호텔 어디서든 가능하며, 예약 방법은 <a href='/reservation/'>예약안내</a>에서 확인할 수 있습니다.",
        "korean-therapist": "한국인 관리사 관리는 한국어로 압과 부위를 편하게 소통할 수 있어 세밀한 요청 반영이 쉽습니다. 성별·기법 선호가 있으면 예약 시 요청할 수 있습니다.",
        "thai-therapist": "태국 관리사 관리는 전통 타이 기법에 강점이 있어 스트레칭과 지압을 결합한 시원한 관리를 받을 수 있습니다. 자세한 내용은 <a href='/theme/thai-massage/'>타이마사지 안내</a>를 참고할 수 있습니다.",
    }
    for m in metas:
        slug, cat = m["slug"], m["cat"]
        catname = data.MAG_CAT_NAME.get(cat, cat)
        secs = list(m["secs"])
        # 이용 시 알아두면 좋은 점(카테고리별 안내) — 글 주제와 함께 제공
        secs = secs + [("이용 시 알아두면 좋은 점", lib.P(
            f"{m['title']}와 함께 알아두면 좋은 이용 정보입니다. "
            + cat_tip.get(cat, "방문 관리는 예약 시 희망 지역과 시간, 코스를 기준으로 가능 여부를 안내합니다."),
            "본 안내는 의료 행위가 아닌 건강관리(이완·휴식) 목적의 방문 관리에 대한 정보이며, 만 19세 이상 성인을 대상으로 합니다. "
            "통증이나 질환이 있는 경우에는 관리보다 의료기관 진료를 우선 권해 드립니다."))]
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
    build_dongs()
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
