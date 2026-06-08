# -*- coding: utf-8 -*-
"""웰니스센터 — 지역/테마/코스/역세권 데이터 + 내비게이션 생성."""

# ────────────────────────── 권역 6 / 자치구 25 ──────────────────────────
# region key -> (라벨, [(gu_slug, 한글명), ...])
REGIONS = [
    ("gangnam", "강남권", [
        ("gangnam-gu", "강남구"), ("seocho-gu", "서초구"),
        ("songpa-gu", "송파구"), ("gangdong-gu", "강동구")]),
    ("gangseo", "강서권", [
        ("gangseo-gu", "강서구"), ("yangcheon-gu", "양천구"),
        ("guro-gu", "구로구"), ("geumcheon-gu", "금천구")]),
    ("seonam", "서남권", [
        ("gwanak-gu", "관악구"), ("dongjak-gu", "동작구"),
        ("yeongdeungpo-gu", "영등포구")]),
    ("dongbuk", "동북권", [
        ("gwangjin-gu", "광진구"), ("seongdong-gu", "성동구"),
        ("dongdaemun-gu", "동대문구"), ("jungnang-gu", "중랑구"),
        ("seongbuk-gu", "성북구"), ("gangbuk-gu", "강북구"),
        ("dobong-gu", "도봉구"), ("nowon-gu", "노원구")]),
    ("dosim", "도심권", [
        ("jongno-gu", "종로구"), ("jung-gu", "중구"), ("yongsan-gu", "용산구")]),
    ("seobuk", "서북권", [
        ("mapo-gu", "마포구"), ("seodaemun-gu", "서대문구"), ("eunpyeong-gu", "은평구")]),
]

# 자치구별 대표 동·생활권 (콘텐츠 차별화용)
GU_AREAS = {
    "gangnam-gu": ["역삼동", "삼성동", "청담동", "논현동", "대치동", "신사동"],
    "seocho-gu": ["서초동", "반포동", "방배동", "잠원동", "양재동"],
    "songpa-gu": ["잠실동", "문정동", "가락동", "송파동", "방이동"],
    "gangdong-gu": ["천호동", "길동", "둔촌동", "성내동", "암사동"],
    "gangseo-gu": ["화곡동", "마곡동", "등촌동", "염창동", "가양동"],
    "yangcheon-gu": ["목동", "신정동", "신월동"],
    "guro-gu": ["구로동", "신도림동", "개봉동", "고척동"],
    "geumcheon-gu": ["가산동", "독산동", "시흥동"],
    "gwanak-gu": ["신림동", "봉천동", "서원동"],
    "dongjak-gu": ["사당동", "노량진동", "상도동", "흑석동"],
    "yeongdeungpo-gu": ["여의도동", "영등포동", "당산동", "문래동"],
    "gwangjin-gu": ["건대입구", "구의동", "자양동", "화양동"],
    "seongdong-gu": ["성수동", "왕십리", "옥수동", "금호동"],
    "dongdaemun-gu": ["회기동", "전농동", "이문동", "장안동"],
    "jungnang-gu": ["면목동", "상봉동", "중화동", "묵동"],
    "seongbuk-gu": ["성신여대", "정릉동", "길음동", "돈암동"],
    "gangbuk-gu": ["수유동", "미아동", "번동"],
    "dobong-gu": ["창동", "쌍문동", "방학동"],
    "nowon-gu": ["노원역", "상계동", "중계동", "공릉동"],
    "jongno-gu": ["종로", "혜화동", "삼청동", "평창동"],
    "jung-gu": ["명동", "을지로", "충무로", "동대문"],
    "yongsan-gu": ["이태원", "한남동", "용산", "삼각지"],
    "mapo-gu": ["홍대입구", "합정동", "상수동", "공덕동", "망원동"],
    "seodaemun-gu": ["신촌", "연희동", "홍제동", "북아현동"],
    "eunpyeong-gu": ["연신내", "응암동", "불광동", "녹번동"],
}

GU_BY_SLUG = {slug: (name, rk, rl) for rk, rl, gus in REGIONS for slug, name in gus}
ALL_GU = [(slug, name) for _, _, gus in REGIONS for slug, name in gus]

# ────────────────────────── 테마 14 ──────────────────────────
THEMES = [
    ("swedish", "스웨디시", "부드러운 오일 압으로 전신 순환과 이완을 돕는 대표 코스"),
    ("aroma-therapy", "아로마테라피", "천연 에센셜 오일 향으로 심신 안정을 더하는 관리"),
    ("thai-massage", "타이마사지", "스트레칭과 지압을 결합한 활력 회복 관리"),
    ("lomi-lomi", "로미로미", "하와이안 전통 기법의 리드미컬한 전신 이완"),
    ("chinese-massage", "중국마사지", "경혈 지압 중심의 깊은 근육 이완"),
    ("sports-massage", "스포츠·경락", "운동 후 근육 피로와 뭉침을 풀어주는 집중 관리"),
    ("foot-massage", "발마사지", "발 반사구를 자극해 전신 피로를 더는 관리"),
    ("home-care", "홈케어", "집에서 받는 1:1 맞춤 방문 관리"),
    ("hotel-massage", "호텔식마사지", "호텔·숙소에서 받는 프리미엄 방문 관리"),
    ("skin-care", "스킨케어", "피부 결과 컨디션을 가다듬는 페이셜·바디 관리"),
    ("waxing", "왁싱", "위생적인 도구로 진행하는 제모 관리"),
    ("couple", "커플 관리", "두 분이 함께 받는 동시 방문 관리"),
    ("24hours", "24시간", "심야·새벽에도 가능한 24시간 예약 관리"),
    ("sleep-available", "수면 가능", "관리 중 편안히 잠들 수 있는 깊은 이완 관리"),
]
THEME_BY_SLUG = {s: (n, d) for s, n, d in THEMES}

# ────────────────────────── 코스 8 ──────────────────────────
COURSES = [
    ("fatigue", "피로 회복 관리", "쌓인 전신 피로와 뭉침을 푸는 기본 회복 코스"),
    ("aroma", "아로마 관리", "아로마 오일로 긴장과 스트레스를 완화하는 코스"),
    ("sports", "스포츠 관리", "운동·자세로 인한 근육 피로를 집중 관리하는 코스"),
    ("home", "홈타이 코스", "집에서 받는 타이식 스트레칭·지압 코스"),
    ("couple", "커플·가족 방문", "두 분 이상 동시에 받는 방문 관리 코스"),
    ("group", "기업·단체 방문", "사무실·행사장 등 단체 방문 관리 코스"),
    ("price", "가격 안내", "코스·시간별 정찰 요금 안내"),
    ("guide", "코스 선택 가이드", "처음이라면 어떤 코스가 맞는지 안내"),
]
COURSE_BY_SLUG = {s: (n, d) for s, n, d in COURSES}

# ────────────────────────── 예약 / 가이드 하위 ──────────────────────────
RESERVATION_PAGES = [
    ("", "예약 방법"), ("hours/", "예약 가능 시간"), ("place/", "방문 가능 장소"),
    ("payment/", "결제 안내"), ("change/", "변경·취소 안내"), ("checklist/", "예약 전 체크사항"),
]
GUIDE_PAGES = [
    ("", "처음 이용하시는 분"), ("prepare/", "방문 전 준비사항"), ("safety/", "위생 및 안전 기준"),
    ("aftercare/", "관리 후 주의사항"), ("forbidden/", "금지행위 안내"), ("checklist/", "이용 전 확인사항"),
    ("faq/", "이용 FAQ"),
]

# ────────────────────────── 매거진 카테고리 9 ──────────────────────────
MAG_CATS = [
    ("guide", "이용가이드"), ("course-theme", "코스·테마"), ("tips", "활용팁"),
    ("area-station", "지역·역세권"), ("region", "지역별 마사지"), ("swedish", "스웨디시"),
    ("visiting", "출장마사지"), ("korean-therapist", "한국인 관리사"), ("thai-therapist", "태국 관리사"),
]
MAG_CAT_NAME = {s: n for s, n in MAG_CATS}

# ────────────────────────── 지하철 노선 / 역 ──────────────────────────
# line slug -> (라벨, [(station_slug, 한글역명), ...])  (서울 구간 중심)
LINES = [
    ("line-1", "1호선", "dobongsan dobong banghak chang-dong nokcheon wolgye gwangun-univ "
        "seokgye sinimun hufs-front hoegi cheongnyangni jegi-dong sinseol-dong dongmyo "
        "dongdaemun jongno-5ga jongno-3ga jonggak city-hall seoul-station namyeong yongsan "
        "noryangjin daebang singil yeongdeungpo sindorim guro gasan-digital-complex doksan geumcheon-gu-office"),
    ("line-2", "2호선", "city-hall euljiro-1ga euljiro-3ga euljiro-4ga dongdaemun-history-park "
        "sindang sangwangsimni wangsimni hanyang-univ ttukseom seongsu konkuk-univ "
        "guui gangbyeon jamsillaru jamsil jamsilsaenae sports-complex samseong seolleung "
        "yeoksam gangnam gyodae seocho bangbae sadang nakseongdae seoul-nat-univ bongcheon "
        "sillim sindaebang guro-digital-complex daerim sindorim mullae yeongdeungpo-gu-office "
        "dangsan hapjeong hongik-univ sinchon ewha-womans-univ ahyeon chungjeongno"),
    ("line-3", "3호선", "gupabal yeonsinnae bulgwang nokbeon hongje muakjae "
        "dongnimmun gyeongbokgung anguk jongno-3ga euljiro-3ga chungmuro dongguk-univ "
        "yaksu geumho oksu apgujeong sinsa jamwon express-bus-terminal gyodae nambu-terminal "
        "yangjae maebong dogok daechi hangnyeoul daecheong irwon suseo"),
    ("line-4", "4호선", "danggogae sanggye nogang changdong ssangmun suyu mia "
        "miasageori gireum sungshin-womens-univ hansung-univ hyehwa dongdaemun "
        "dongdaemun-history-park chungmuro myeong-dong hoehyeon seoul-station sukdae-ipgu "
        "samgakji sinyongsan ichon dongjak chongsin-univ isu sadang namtaeryeong seoul-racecourse"),
    ("line-5", "5호선", "banghwa gaehwasan gimpo-airport songjeong magongnaru sinbanghwa "
        "gaehwasan-r hwagok kkachisan sinjeong mokdong omokgyo yangpyeong yeongdeungpo-market "
        "yeouinaru yeouido yeoui-yeouido mapo gongdeok aeogae chungjeongno seodaemun gwanghwamun "
        "jongno-3ga euljiro-4ga dongdaemun-history-park cheonggu sindang sangwangsimni wangsimni "
        "majang dapsimni janghanpyeong gunja achasan gwangnaru cheonho gangdong gildong"),
    ("line-6", "6호선", "eungam yeokchon bulgwang dokbawi yeonsinnae gusan saejeol "
        "jeungsan digital-media-city worldcup-stadium mangwon hapjeong sangsu gwangheungchang "
        "daeheung gongdeok hyochang-park samgakji noksapyeong itaewon hangangjin "
        "beotigogae yaksu cheonggu sindang dongmyo changsin bomun anam korea-univ wolgok sangwolgok"),
    ("line-7", "7호선", "jangam dobongsan-7 suraksan madeul nowon junggye hagye gongneung "
        "taereung meokgol junghwa sangbong myeonmok sagajeong yongmasan junggok gunja "
        "children-grand-park ttukseom-resort konkuk-univ cheongdam gangnam-gu-office "
        "hak-dong nonhyeon banpo express-bus-terminal naebang isu namseong sadang "
        "sasang-r boramae sindaebang-samgeori jangseungbaegi sindaebang"),
    ("line-8", "8호선", "amsa cheonho gangdong-guoffice mongchontoseong jamsil "
        "seoknchon songpa garak-market munjeong jangji bokjeong sanseong namhansanseong"),
    ("line-9", "9호선", "gaehwa airport-market sinbanghwa magongnaru yangcheon-hyanggyo "
        "gayang jeungmi deungchon yeomchang sinmokdong seonyudo dangsan gukhoe "
        "yeouido saetgang nodeul noryangjin heukseok dongjak gubanpo sinbanpo express-bus-terminal "
        "sapyeong sinnonhyeon eonju seonjeongneung samseong-jungang bongeunsa sports-complex"),
    ("sinbundang", "신분당선", "gangnam yangjae yangjae-citizens-forest cheonggyesan pangyo "
        "jeongja migeum dongcheon suji-guuni sanghyeon"),
    ("suin-bundang", "수인분당선", "wangsimni seoulforest apgujeong-rodeo gangnam-gu-office "
        "seonjeongneung seolleung hanti dogok guryong gaepo-dong daemosan suseo bokjeong"),
    ("gyeongui-jungang", "경의중앙선", "munsan-r seoul-station sinchon-g gajwa digital-media-city "
        "hongdae-r gongdeok seoulforest-g wangsimni cheongnyangni hoegi jungnang sangbong mangu"),
    ("gyeongchun", "경춘선", "cheongnyangni hoegi jungnang sangbong mangu galmae byeollae "
        "toegyewon sareung geumgok pyeongnae-hopyeong"),
    ("airport", "공항철도", "seoul-station gongdeok hongik-univ-a digital-media-city-a "
        "magongnaru gimpo-airport-a gyeyang geomam"),
    ("sillim", "신림선", "saetgang-s daebang-s seoul-national-univ-venture boramae-s "
        "sillim-s gwanaksan seowon"),
    ("ui-sinseol", "우이신설선", "bukhansan-ui solbat 4-19-democracy gaeunsa hwagye "
        "samyang samyang-sageori solsaem bomun sinseol-dong"),
    ("seohae", "서해선", "sosa-r soraepogu siheung-daeya siheung-neunggok"),
]


def _stations(blob):
    return [s for s in blob.split() if s]


def station_name(slug):
    """역 슬러그를 한글 표기로(간단 변환). 슬러그가 이미 충분히 식별 가능하므로 보기용."""
    return STATION_NAMES.get(slug, slug.replace("-", " ").title())


# 슬러그→한글 역명 (주요 역; 없는 경우 슬러그 표기 사용)
STATION_NAMES = {
    "city-hall": "시청", "seoul-station": "서울역", "gangnam": "강남", "jamsil": "잠실",
    "hongik-univ": "홍대입구", "konkuk-univ": "건대입구", "samseong": "삼성", "yeoksam": "역삼",
    "seolleung": "선릉", "gyodae": "교대", "sadang": "사당", "sillim": "신림", "sinchon": "신촌",
    "ewha-womans-univ": "이대", "wangsimni": "왕십리", "seongsu": "성수", "itaewon": "이태원",
    "yongsan": "용산", "yeouido": "여의도", "express-bus-terminal": "고속터미널", "sinsa": "신사",
    "apgujeong": "압구정", "cheongnyangni": "청량리", "nowon": "노원", "chang-dong": "창동",
    "gangbyeon": "강변", "cheonho": "천호", "myeong-dong": "명동", "gwanghwamun": "광화문",
    "jongno-3ga": "종로3가", "gongdeok": "공덕", "mapo": "마포", "yangjae": "양재",
    "pangyo": "판교", "jeongja": "정자", "seoulforest": "서울숲", "dangsan": "당산",
    "hapjeong": "합정", "mangwon": "망원", "noryangjin": "노량진", "dongjak": "동작",
    "yeonsinnae": "연신내", "bulgwang": "불광", "suyu": "수유", "mia": "미아",
    "hyehwa": "혜화", "anguk": "안국", "gyeongbokgung": "경복궁", "chungmuro": "충무로",
    "dongdaemun": "동대문", "gupabal": "구파발", "suseo": "수서", "garak-market": "가락시장",
    "mongchontoseong": "몽촌토성", "gimpo-airport": "김포공항", "magongnaru": "마곡나루",
}

# ────────────────────────── 내비게이션 생성 ──────────────────────────
def build_nav():
    li = []
    li.append('<li><a href="/">홈</a></li>')

    # 서울 출장마사지
    li.append("""<li><a href="/seoul/" aria-haspopup="true">서울 출장마사지</a>
      <ul class="submenu">
        <li><a href="/seoul/">서울 출장마사지 안내</a></li>
        <li><a href="/seoul/#home">서울 홈타이 안내</a></li>
        <li><a href="/seoul/#allarea">서울 전지역 출장 안내</a></li>
        <li><a href="/seoul/#station">지하철역 인근 안내</a></li>
        <li><a href="/reservation/hours/">예약 가능 시간</a></li>
        <li><a href="/course/guide/">코스 선택 안내</a></li>
        <li><a href="/guide/checklist/">이용 전 확인사항</a></li>
        <li><a href="/guide/safety/">위생 및 안전 안내</a></li>
        <li><a href="/seoul/faq/">자주 묻는 질문</a></li>
      </ul></li>""")

    # 지역별 안내 (2뎁스: 권역 → 자치구)
    regs = ['<li><a href="/seoul/area/">서울 전체</a></li>']
    for rk, rl, gus in REGIONS:
        subs = "".join(f'<li><a href="/seoul/{slug}/">{name}</a></li>' for slug, name in gus)
        regs.append(f'<li class="has-sub"><a href="/seoul/area/#{rk}" aria-haspopup="true">{rl}</a>'
                    f'<ul class="submenu sub2">{subs}</ul></li>')
    li.append(f'<li><a href="/seoul/area/" aria-haspopup="true">지역별 안내</a>'
              f'<ul class="submenu">{"".join(regs)}</ul></li>')

    # 지하철역별 안내 (2뎁스: 노선 → 노선 허브)
    lns = ['<li><a href="/seoul/stations/">서울 지하철역 전체</a></li>']
    for ls, ll, _ in LINES:
        lns.append(f'<li><a href="/seoul/stations/{ls}/">{ll}</a></li>')
    li.append(f'<li><a href="/seoul/stations/" aria-haspopup="true">지하철역별 안내</a>'
              f'<ul class="submenu">{"".join(lns)}</ul></li>')

    # 테마별
    th = ['<li><a href="/theme/">전체 테마</a></li>']
    th += [f'<li><a href="/theme/{s}/">{n}</a></li>' for s, n, _ in THEMES]
    li.append(f'<li><a href="/theme/" aria-haspopup="true">테마별 안내</a>'
              f'<ul class="submenu">{"".join(th)}</ul></li>')

    # 코스
    co = ['<li><a href="/course/">전체 코스</a></li>']
    co += [f'<li><a href="/course/{s}/">{n}</a></li>' for s, n, _ in COURSES]
    li.append(f'<li><a href="/course/" aria-haspopup="true">코스안내</a>'
              f'<ul class="submenu">{"".join(co)}</ul></li>')

    # 예약
    rv = [f'<li><a href="/reservation/{p}">{n}</a></li>' for p, n in RESERVATION_PAGES]
    li.append(f'<li><a href="/reservation/" aria-haspopup="true">예약안내</a>'
              f'<ul class="submenu">{"".join(rv)}</ul></li>')

    # 가이드
    gd = [f'<li><a href="/guide/{p}">{n}</a></li>' for p, n in GUIDE_PAGES]
    li.append(f'<li><a href="/guide/" aria-haspopup="true">이용가이드</a>'
              f'<ul class="submenu">{"".join(gd)}</ul></li>')

    li.append('<li><a href="/reviews/">후기</a></li>')

    # 매거진
    mg = ['<li><a href="/magazine/">전체 매거진</a></li>']
    mg += [f'<li><a href="/magazine/category/{s}/">{n}</a></li>' for s, n in MAG_CATS]
    li.append(f'<li><a href="/magazine/" aria-haspopup="true">매거진</a>'
              f'<ul class="submenu">{"".join(mg)}</ul></li>')

    # 고객센터
    li.append("""<li><a href="/customer/" aria-haspopup="true">고객센터</a>
      <ul class="submenu">
        <li><a href="/customer/#notice">공지사항</a></li>
        <li><a href="/customer/#qna">자주 묻는 질문</a></li>
        <li><a href="/customer/#inquiry">1:1 문의</a></li>
        <li><a href="/customer/#partner">제휴·기업 문의</a></li>
        <li><a href="/privacy/">개인정보처리방침</a></li>
        <li><a href="/terms/">이용약관</a></li>
      </ul></li>""")

    li.append('<li><a class="cta-pill" href="tel:+825082024743">24시 예약</a></li>')

    return '<ul id="primary-menu" class="menu">' + "\n".join(li) + "</ul>"


# 노선별 역 리스트 헬퍼
def line_stations(line_slug):
    for ls, ll, blob in LINES:
        if ls == line_slug:
            return ll, _stations(blob)
    return None, []


def all_stations():
    """(station_slug, 한글명, line_slug, line_label) 중복 제거(첫 등장 노선 기준)."""
    seen = {}
    out = []
    for ls, ll, blob in LINES:
        for st in _stations(blob):
            if st in seen:
                continue
            seen[st] = True
            out.append((st, station_name(st), ls, ll))
    return out
