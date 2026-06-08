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

# 자치구별 지역 특성(차별화용 한 줄 설명) — 유사 페이지 방지
GU_DESC = {
    "gangnam-gu": "업무지구와 고급 주거가 밀집해 직장인·심야 이용 수요가 높은 지역입니다.",
    "seocho-gu": "법조·업무지구와 대단지 주거가 함께 있어 직장인과 가족 단위 이용이 고른 지역입니다.",
    "songpa-gu": "대규모 아파트 단지와 업무·상업 시설이 어우러진 생활권입니다.",
    "gangdong-gu": "한강 인접 주거지가 많아 가족 단위 방문 수요가 안정적인 지역입니다.",
    "gangseo-gu": "마곡 업무지구와 공항 인접 생활권으로 직장인·출장객 이용이 많습니다.",
    "yangcheon-gu": "목동을 중심으로 학군·주거가 발달한 정주형 생활권입니다.",
    "guro-gu": "구로디지털단지 등 IT 업무지구가 있어 야간·퇴근 후 이용이 많습니다.",
    "geumcheon-gu": "가산디지털단지를 중심으로 직장인 밀집도가 높은 지역입니다.",
    "gwanak-gu": "대학가와 1인 가구가 많아 합리적인 방문 관리 수요가 높은 지역입니다.",
    "dongjak-gu": "노량진·사당 등 교통 요지와 주거가 결합된 생활권입니다.",
    "yeongdeungpo-gu": "여의도 금융가와 영등포 상권이 있어 직장인 이용이 활발합니다.",
    "gwangjin-gu": "건대입구 상권과 대학가를 중심으로 활기가 있는 지역입니다.",
    "seongdong-gu": "성수동 오피스와 신축 주거가 늘며 방문 수요가 빠르게 증가한 지역입니다.",
    "dongdaemun-gu": "청량리·회기 등 교통 요지와 대학가가 있는 생활권입니다.",
    "jungnang-gu": "면목·상봉 등 안정적인 주거지가 넓게 분포한 지역입니다.",
    "seongbuk-gu": "대학가와 주거지가 어우러져 정주 인구가 많은 지역입니다.",
    "gangbuk-gu": "수유·미아를 중심으로 한 전통적인 주거 생활권입니다.",
    "dobong-gu": "창동·쌍문 등 대단지 주거가 많은 정주형 지역입니다.",
    "nowon-gu": "대규모 아파트 단지가 밀집해 가족 단위 수요가 고른 지역입니다.",
    "jongno-gu": "도심 업무지구와 관광·역사 지구가 함께 있는 중심권입니다.",
    "jung-gu": "명동·을지로 등 도심 상권과 호텔이 밀집한 지역입니다.",
    "yongsan-gu": "이태원·한남과 호텔이 많아 출장객·외국인 거주 수요가 높은 지역입니다.",
    "mapo-gu": "홍대·합정을 중심으로 1인 가구와 젊은 층이 많은 생활권입니다.",
    "seodaemun-gu": "신촌 대학가와 주거지가 결합된 활기 있는 지역입니다.",
    "eunpyeong-gu": "연신내·불광을 중심으로 한 대규모 주거 생활권입니다.",
}

# 자치구 인근 대표 지하철역(역 슬러그) — 존재하는 슬러그만 사용
GU_STATIONS = {
    "gangnam-gu": ["gangnam", "yeoksam", "seolleung", "samseong", "apgujeong"],
    "seocho-gu": ["gyodae", "express-bus-terminal", "yangjae", "nambu-terminal", "bangbae"],
    "songpa-gu": ["jamsil", "garak-market", "munjeong", "mongchontoseong"],
    "gangdong-gu": ["cheonho", "gangdong", "gildong", "amsa"],
    "gangseo-gu": ["gimpo-airport", "magongnaru", "hwagok", "gayang"],
    "yangcheon-gu": ["omokgyo", "mokdong", "sinjeong", "kkachisan"],
    "guro-gu": ["sindorim", "guro-digital-complex", "daerim"],
    "geumcheon-gu": ["gasan-digital-complex", "doksan", "geumcheon-gu-office"],
    "gwanak-gu": ["sillim", "nakseongdae", "seoul-nat-univ", "bongcheon"],
    "dongjak-gu": ["sadang", "noryangjin", "isu", "dongjak"],
    "yeongdeungpo-gu": ["yeouido", "yeongdeungpo", "dangsan", "mullae"],
    "gwangjin-gu": ["konkuk-univ", "gunja", "children-grand-park", "achasan"],
    "seongdong-gu": ["wangsimni", "seongsu", "ttukseom", "majang"],
    "dongdaemun-gu": ["cheongnyangni", "hoegi", "jegi-dong", "sinseol-dong"],
    "jungnang-gu": ["sangbong", "mangu", "myeonmok", "junghwa"],
    "seongbuk-gu": ["sungshin-womens-univ", "hansung-univ", "bomun", "korea-univ"],
    "gangbuk-gu": ["suyu", "mia", "miasageori"],
    "dobong-gu": ["chang-dong", "ssangmun", "banghak", "dobong"],
    "nowon-gu": ["nowon", "junggye", "hagye", "gongneung", "madeul"],
    "jongno-gu": ["jongno-3ga", "jonggak", "gwanghwamun", "anguk", "gyeongbokgung"],
    "jung-gu": ["city-hall", "euljiro-3ga", "myeong-dong", "chungmuro"],
    "yongsan-gu": ["yongsan", "itaewon", "samgakji", "ichon", "hangangjin"],
    "mapo-gu": ["hongik-univ", "hapjeong", "mangwon", "gongdeok", "sangsu"],
    "seodaemun-gu": ["sinchon", "ewha-womans-univ", "hongje", "muakjae"],
    "eunpyeong-gu": ["yeonsinnae", "bulgwang", "gupabal", "nokbeon"],
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
    ("line-4", "4호선", "danggogae sanggye nowon chang-dong ssangmun suyu mia "
        "miasageori gireum sungshin-womens-univ hansung-univ hyehwa dongdaemun "
        "dongdaemun-history-park chungmuro myeong-dong hoehyeon seoul-station sukdae-ipgu "
        "samgakji sinyongsan ichon dongjak chongsin-univ isu sadang namtaeryeong seoul-racecourse"),
    ("line-5", "5호선", "banghwa gaehwasan gimpo-airport songjeong magongnaru balsan ujangsan "
        "hwagok kkachisan sinjeong mokdong omokgyo yangpyeong yeongdeungpo-market "
        "yeouinaru yeouido mapo gongdeok aeogae chungjeongno seodaemun gwanghwamun "
        "jongno-3ga euljiro-4ga dongdaemun-history-park cheonggu sindang sangwangsimni wangsimni "
        "majang dapsimni janghanpyeong gunja achasan gwangnaru cheonho gangdong gildong"),
    ("line-6", "6호선", "eungam yeokchon bulgwang dokbawi yeonsinnae gusan saejeol "
        "jeungsan digital-media-city worldcup-stadium mangwon hapjeong sangsu gwangheungchang "
        "daeheung gongdeok hyochang-park samgakji noksapyeong itaewon hangangjin "
        "beotigogae yaksu cheonggu sindang dongmyo changsin bomun anam korea-univ wolgok sangwolgok"),
    ("line-7", "7호선", "jangam dobongsan suraksan madeul nowon junggye hagye gongneung "
        "taereung meokgol junghwa sangbong myeonmok sagajeong yongmasan junggok gunja "
        "children-grand-park ttukseom-resort konkuk-univ cheongdam gangnam-gu-office "
        "hak-dong nonhyeon banpo express-bus-terminal naebang isu namseong sadang "
        "boramae sindaebang-samgeori jangseungbaegi sindaebang"),
    ("line-8", "8호선", "amsa cheonho gangdong-guoffice mongchontoseong jamsil "
        "seokchon songpa garak-market munjeong jangji bokjeong sanseong namhansanseong"),
    ("line-9", "9호선", "gaehwa airport-market sinbanghwa magongnaru yangcheon-hyanggyo "
        "gayang jeungmi deungchon yeomchang sinmokdong seonyudo dangsan gukhoe "
        "yeouido saetgang nodeul noryangjin heukseok dongjak gubanpo sinbanpo express-bus-terminal "
        "sapyeong sinnonhyeon eonju seonjeongneung samseong-jungang bongeunsa sports-complex"),
    ("sinbundang", "신분당선", "gangnam yangjae yangjae-citizens-forest cheonggyesan pangyo "
        "jeongja migeum dongcheon suji-guuni sanghyeon"),
    ("suin-bundang", "수인분당선", "wangsimni seoulforest apgujeong-rodeo gangnam-gu-office "
        "seonjeongneung seolleung hanti dogok guryong gaepo-dong daemosan suseo bokjeong"),
    ("gyeongui-jungang", "경의중앙선", "munsan seoul-station gajwa digital-media-city "
        "hongik-univ gongdeok wangsimni cheongnyangni hoegi jungnang sangbong mangu"),
    ("gyeongchun", "경춘선", "cheongnyangni hoegi jungnang sangbong mangu galmae byeollae "
        "toegyewon sareung geumgok pyeongnae-hopyeong"),
    ("airport", "공항철도", "seoul-station gongdeok hongik-univ digital-media-city "
        "magongnaru gimpo-airport gyeyang geomam"),
    ("sillim", "신림선", "saetgang daebang seoul-national-univ-venture boramae "
        "sillim gwanaksan seowon"),
    ("ui-sinseol", "우이신설선", "bukhansan-ui solbat 4-19-democracy gaori hwagye "
        "samyang samyang-sageori solsaem bomun sinseol-dong"),
    ("seohae", "서해선", "sosa soraepogu siheung-daeya siheung-neunggok"),
]


def _stations(blob):
    return [s for s in blob.split() if s]


def station_name(slug):
    """역 슬러그를 한글 표기로(간단 변환). 슬러그가 이미 충분히 식별 가능하므로 보기용."""
    return STATION_NAMES.get(slug, slug.replace("-", " ").title())


# 슬러그→한글 역명 (전 노선)
STATION_NAMES = {
    # 1호선
    "dobongsan": "도봉산", "dobong": "도봉", "banghak": "방학", "chang-dong": "창동",
    "nokcheon": "녹천", "wolgye": "월계", "gwangun-univ": "광운대", "seokgye": "석계",
    "sinimun": "신이문", "hufs-front": "외대앞", "hoegi": "회기", "cheongnyangni": "청량리",
    "jegi-dong": "제기동", "sinseol-dong": "신설동", "dongmyo": "동묘앞", "dongdaemun": "동대문",
    "jongno-5ga": "종로5가", "jongno-3ga": "종로3가", "jonggak": "종각", "city-hall": "시청",
    "seoul-station": "서울역", "namyeong": "남영", "yongsan": "용산", "noryangjin": "노량진",
    "daebang": "대방", "singil": "신길", "yeongdeungpo": "영등포", "sindorim": "신도림",
    "guro": "구로", "gasan-digital-complex": "가산디지털단지", "doksan": "독산",
    "geumcheon-gu-office": "금천구청",
    # 2호선
    "euljiro-1ga": "을지로입구", "euljiro-3ga": "을지로3가", "euljiro-4ga": "을지로4가",
    "dongdaemun-history-park": "동대문역사문화공원", "sindang": "신당", "sangwangsimni": "상왕십리",
    "wangsimni": "왕십리", "hanyang-univ": "한양대", "ttukseom": "뚝섬", "seongsu": "성수",
    "konkuk-univ": "건대입구", "guui": "구의", "gangbyeon": "강변", "jamsillaru": "잠실나루",
    "jamsil": "잠실", "jamsilsaenae": "잠실새내", "sports-complex": "종합운동장", "samseong": "삼성",
    "seolleung": "선릉", "yeoksam": "역삼", "gangnam": "강남", "gyodae": "교대", "seocho": "서초",
    "bangbae": "방배", "sadang": "사당", "nakseongdae": "낙성대", "seoul-nat-univ": "서울대입구",
    "bongcheon": "봉천", "sillim": "신림", "sindaebang": "신대방",
    "guro-digital-complex": "구로디지털단지", "daerim": "대림", "mullae": "문래",
    "yeongdeungpo-gu-office": "영등포구청", "dangsan": "당산", "hapjeong": "합정",
    "hongik-univ": "홍대입구", "sinchon": "신촌", "ewha-womans-univ": "이대",
    "ahyeon": "아현", "chungjeongno": "충정로",
    # 3호선
    "gupabal": "구파발", "yeonsinnae": "연신내", "bulgwang": "불광", "nokbeon": "녹번",
    "hongje": "홍제", "muakjae": "무악재", "dongnimmun": "독립문", "gyeongbokgung": "경복궁",
    "anguk": "안국", "chungmuro": "충무로", "dongguk-univ": "동대입구", "yaksu": "약수",
    "geumho": "금호", "oksu": "옥수", "apgujeong": "압구정", "sinsa": "신사", "jamwon": "잠원",
    "express-bus-terminal": "고속터미널", "nambu-terminal": "남부터미널", "yangjae": "양재",
    "maebong": "매봉", "dogok": "도곡", "daechi": "대치", "hangnyeoul": "학여울",
    "daecheong": "대청", "irwon": "일원", "suseo": "수서",
    # 4호선
    "danggogae": "당고개", "sanggye": "상계", "nowon": "노원", "ssangmun": "쌍문", "suyu": "수유",
    "mia": "미아", "miasageori": "미아사거리", "gireum": "길음", "sungshin-womens-univ": "성신여대입구",
    "hansung-univ": "한성대입구", "hyehwa": "혜화", "myeong-dong": "명동", "hoehyeon": "회현",
    "sukdae-ipgu": "숙대입구", "samgakji": "삼각지", "sinyongsan": "신용산", "ichon": "이촌",
    "dongjak": "동작", "chongsin-univ": "총신대입구", "isu": "이수", "namtaeryeong": "남태령",
    "seoul-racecourse": "경마공원",
    # 5호선
    "banghwa": "방화", "gaehwasan": "개화산", "gimpo-airport": "김포공항", "songjeong": "송정",
    "magongnaru": "마곡나루", "balsan": "발산", "ujangsan": "우장산", "hwagok": "화곡",
    "kkachisan": "까치산", "sinjeong": "신정", "mokdong": "목동", "omokgyo": "오목교",
    "yangpyeong": "양평", "yeongdeungpo-market": "영등포시장", "yeouinaru": "여의나루",
    "yeouido": "여의도", "mapo": "마포", "gongdeok": "공덕", "aeogae": "애오개",
    "seodaemun": "서대문", "gwanghwamun": "광화문", "cheonggu": "청구", "majang": "마장",
    "dapsimni": "답십리", "janghanpyeong": "장한평", "gunja": "군자", "achasan": "아차산",
    "gwangnaru": "광나루", "cheonho": "천호", "gangdong": "강동", "gildong": "길동",
    # 6호선
    "eungam": "응암", "yeokchon": "역촌", "dokbawi": "독바위", "gusan": "구산", "saejeol": "새절",
    "jeungsan": "증산", "digital-media-city": "디지털미디어시티", "worldcup-stadium": "월드컵경기장",
    "mangwon": "망원", "sangsu": "상수", "gwangheungchang": "광흥창", "daeheung": "대흥",
    "hyochang-park": "효창공원앞", "noksapyeong": "녹사평", "itaewon": "이태원",
    "hangangjin": "한강진", "beotigogae": "버티고개", "changsin": "창신", "bomun": "보문",
    "anam": "안암", "korea-univ": "고려대", "wolgok": "월곡", "sangwolgok": "상월곡",
    # 7호선
    "jangam": "장암", "suraksan": "수락산", "madeul": "마들", "junggye": "중계", "hagye": "하계",
    "gongneung": "공릉", "taereung": "태릉입구", "meokgol": "먹골", "junghwa": "중화",
    "myeonmok": "면목", "sagajeong": "사가정", "yongmasan": "용마산", "junggok": "중곡",
    "children-grand-park": "어린이대공원", "ttukseom-resort": "뚝섬유원지", "cheongdam": "청담",
    "gangnam-gu-office": "강남구청", "hak-dong": "학동", "nonhyeon": "논현", "banpo": "반포",
    "naebang": "내방", "namseong": "남성", "boramae": "보라매",
    "sindaebang-samgeori": "신대방삼거리", "jangseungbaegi": "장승배기",
    # 8호선
    "amsa": "암사", "gangdong-guoffice": "강동구청", "mongchontoseong": "몽촌토성",
    "seokchon": "석촌", "songpa": "송파", "garak-market": "가락시장", "munjeong": "문정",
    "jangji": "장지", "bokjeong": "복정", "sanseong": "산성", "namhansanseong": "남한산성입구",
    # 9호선
    "gaehwa": "개화", "airport-market": "공항시장", "sinbanghwa": "신방화",
    "yangcheon-hyanggyo": "양천향교", "gayang": "가양", "jeungmi": "증미", "deungchon": "등촌",
    "yeomchang": "염창", "sinmokdong": "신목동", "seonyudo": "선유도", "gukhoe": "국회의사당",
    "saetgang": "샛강", "nodeul": "노들", "heukseok": "흑석", "gubanpo": "구반포",
    "sinbanpo": "신반포", "sapyeong": "사평", "sinnonhyeon": "신논현", "eonju": "언주",
    "seonjeongneung": "선정릉", "samseong-jungang": "삼성중앙", "bongeunsa": "봉은사",
    # 신분당선
    "yangjae-citizens-forest": "양재시민의숲", "cheonggyesan": "청계산입구", "pangyo": "판교",
    "jeongja": "정자", "migeum": "미금", "dongcheon": "동천", "suji-guuni": "수지구청",
    "sanghyeon": "상현",
    # 수인분당선
    "seoulforest": "서울숲", "apgujeong-rodeo": "압구정로데오", "hanti": "한티",
    "guryong": "구룡", "gaepo-dong": "개포동", "daemosan": "대모산입구",
    # 경의중앙선
    "munsan": "문산", "gajwa": "가좌", "jungnang": "중랑", "mangu": "망우", "sangbong": "상봉",
    # 경춘선
    "galmae": "갈매", "byeollae": "별내", "toegyewon": "퇴계원", "sareung": "사릉",
    "geumgok": "금곡", "pyeongnae-hopyeong": "평내호평",
    # 공항철도
    "gyeyang": "계양", "geomam": "검암",
    # 신림선
    "seoul-national-univ-venture": "서울대벤처타운", "gwanaksan": "관악산", "seowon": "서원",
    # 우이신설선
    "bukhansan-ui": "북한산우이", "solbat": "솔밭공원", "4-19-democracy": "4·19민주묘지",
    "gaori": "가오리", "hwagye": "화계", "samyang": "삼양", "samyang-sageori": "삼양사거리",
    "solsaem": "솔샘",
    # 서해선
    "sosa": "소사", "soraepogu": "소래포구", "siheung-daeya": "시흥대야",
    "siheung-neunggok": "시흥능곡",
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


def station_lines(slug):
    """해당 역을 지나는 모든 노선 라벨(환승 정보)."""
    out = []
    for ls, ll, blob in LINES:
        if slug in _stations(blob):
            out.append(ll)
    return out


def station_neighbors(slug):
    """노선 순서 기준 인접역(앞/뒤) 슬러그 목록(중복 제거, 자기 제외)."""
    out = []
    for ls, ll, blob in LINES:
        sts = _stations(blob)
        if slug in sts:
            i = sts.index(slug)
            for j in (i - 1, i + 1):
                if 0 <= j < len(sts):
                    out.append(sts[j])
    seen, res = set(), []
    for s in out:
        if s != slug and s not in seen:
            seen.add(s)
            res.append(s)
    return res


# 역 슬러그 → 자치구 슬러그 (전 역; 서울 외 역은 미포함)
STATION_GU = {
    # 1호선
    "dobongsan": "dobong-gu", "dobong": "dobong-gu", "banghak": "dobong-gu", "chang-dong": "dobong-gu",
    "nokcheon": "nowon-gu", "wolgye": "nowon-gu", "gwangun-univ": "nowon-gu", "seokgye": "nowon-gu",
    "sinimun": "dongdaemun-gu", "hufs-front": "dongdaemun-gu", "hoegi": "dongdaemun-gu",
    "cheongnyangni": "dongdaemun-gu", "jegi-dong": "dongdaemun-gu", "sinseol-dong": "dongdaemun-gu",
    "dongmyo": "jongno-gu", "dongdaemun": "jongno-gu", "jongno-5ga": "jongno-gu",
    "jongno-3ga": "jongno-gu", "jonggak": "jongno-gu", "city-hall": "jung-gu", "seoul-station": "jung-gu",
    "namyeong": "yongsan-gu", "yongsan": "yongsan-gu", "noryangjin": "dongjak-gu",
    "daebang": "yeongdeungpo-gu", "singil": "yeongdeungpo-gu", "yeongdeungpo": "yeongdeungpo-gu",
    "sindorim": "guro-gu", "guro": "guro-gu", "gasan-digital-complex": "geumcheon-gu",
    "doksan": "geumcheon-gu", "geumcheon-gu-office": "geumcheon-gu",
    # 2호선
    "euljiro-1ga": "jung-gu", "euljiro-3ga": "jung-gu", "euljiro-4ga": "jung-gu",
    "dongdaemun-history-park": "jung-gu", "sindang": "jung-gu", "sangwangsimni": "seongdong-gu",
    "wangsimni": "seongdong-gu", "hanyang-univ": "seongdong-gu", "ttukseom": "seongdong-gu",
    "seongsu": "seongdong-gu", "konkuk-univ": "gwangjin-gu", "guui": "gwangjin-gu",
    "gangbyeon": "gwangjin-gu", "jamsillaru": "songpa-gu", "jamsil": "songpa-gu",
    "jamsilsaenae": "songpa-gu", "sports-complex": "songpa-gu", "samseong": "gangnam-gu",
    "seolleung": "gangnam-gu", "yeoksam": "gangnam-gu", "gangnam": "gangnam-gu", "gyodae": "seocho-gu",
    "seocho": "seocho-gu", "bangbae": "seocho-gu", "sadang": "dongjak-gu", "nakseongdae": "gwanak-gu",
    "seoul-nat-univ": "gwanak-gu", "bongcheon": "gwanak-gu", "sillim": "gwanak-gu",
    "sindaebang": "dongjak-gu", "guro-digital-complex": "guro-gu", "daerim": "yeongdeungpo-gu",
    "mullae": "yeongdeungpo-gu", "yeongdeungpo-gu-office": "yeongdeungpo-gu", "dangsan": "yeongdeungpo-gu",
    "hapjeong": "mapo-gu", "hongik-univ": "mapo-gu", "sinchon": "seodaemun-gu",
    "ewha-womans-univ": "seodaemun-gu", "ahyeon": "mapo-gu", "chungjeongno": "seodaemun-gu",
    # 3호선
    "gupabal": "eunpyeong-gu", "yeonsinnae": "eunpyeong-gu", "bulgwang": "eunpyeong-gu",
    "nokbeon": "eunpyeong-gu", "hongje": "seodaemun-gu", "muakjae": "seodaemun-gu",
    "dongnimmun": "seodaemun-gu", "gyeongbokgung": "jongno-gu", "anguk": "jongno-gu",
    "chungmuro": "jung-gu", "dongguk-univ": "jung-gu", "yaksu": "jung-gu", "geumho": "seongdong-gu",
    "oksu": "seongdong-gu", "apgujeong": "gangnam-gu", "sinsa": "gangnam-gu", "jamwon": "seocho-gu",
    "express-bus-terminal": "seocho-gu", "nambu-terminal": "seocho-gu", "yangjae": "seocho-gu",
    "maebong": "gangnam-gu", "dogok": "gangnam-gu", "daechi": "gangnam-gu", "hangnyeoul": "gangnam-gu",
    "daecheong": "gangnam-gu", "irwon": "gangnam-gu", "suseo": "gangnam-gu",
    # 4호선
    "danggogae": "nowon-gu", "sanggye": "nowon-gu", "nowon": "nowon-gu", "ssangmun": "dobong-gu",
    "suyu": "gangbuk-gu", "mia": "gangbuk-gu", "miasageori": "gangbuk-gu", "gireum": "seongbuk-gu",
    "sungshin-womens-univ": "seongbuk-gu", "hansung-univ": "seongbuk-gu", "hyehwa": "jongno-gu",
    "myeong-dong": "jung-gu", "hoehyeon": "jung-gu", "sukdae-ipgu": "yongsan-gu", "samgakji": "yongsan-gu",
    "sinyongsan": "yongsan-gu", "ichon": "yongsan-gu", "dongjak": "dongjak-gu",
    "chongsin-univ": "dongjak-gu", "isu": "dongjak-gu", "namtaeryeong": "gwanak-gu",
    # 5호선
    "banghwa": "gangseo-gu", "gaehwasan": "gangseo-gu", "gimpo-airport": "gangseo-gu",
    "songjeong": "gangseo-gu", "magongnaru": "gangseo-gu", "balsan": "gangseo-gu",
    "ujangsan": "gangseo-gu", "hwagok": "gangseo-gu", "kkachisan": "yangcheon-gu",
    "sinjeong": "yangcheon-gu", "mokdong": "yangcheon-gu", "omokgyo": "yangcheon-gu",
    "yangpyeong": "yeongdeungpo-gu", "yeongdeungpo-market": "yeongdeungpo-gu",
    "yeouinaru": "yeongdeungpo-gu", "yeouido": "yeongdeungpo-gu", "mapo": "mapo-gu",
    "gongdeok": "mapo-gu", "aeogae": "mapo-gu", "seodaemun": "jongno-gu", "gwanghwamun": "jongno-gu",
    "cheonggu": "jung-gu", "majang": "seongdong-gu", "dapsimni": "dongdaemun-gu",
    "janghanpyeong": "dongdaemun-gu", "gunja": "gwangjin-gu", "achasan": "gwangjin-gu",
    "gwangnaru": "gwangjin-gu", "cheonho": "gangdong-gu", "gangdong": "gangdong-gu", "gildong": "gangdong-gu",
    # 6호선
    "eungam": "eunpyeong-gu", "yeokchon": "eunpyeong-gu", "dokbawi": "eunpyeong-gu",
    "gusan": "eunpyeong-gu", "saejeol": "eunpyeong-gu", "jeungsan": "eunpyeong-gu",
    "digital-media-city": "mapo-gu", "worldcup-stadium": "mapo-gu", "mangwon": "mapo-gu",
    "sangsu": "mapo-gu", "gwangheungchang": "mapo-gu", "daeheung": "mapo-gu",
    "hyochang-park": "yongsan-gu", "noksapyeong": "yongsan-gu", "itaewon": "yongsan-gu",
    "hangangjin": "yongsan-gu", "beotigogae": "jung-gu", "changsin": "jongno-gu", "bomun": "seongbuk-gu",
    "anam": "seongbuk-gu", "korea-univ": "seongbuk-gu", "wolgok": "seongbuk-gu", "sangwolgok": "seongbuk-gu",
    # 7호선
    "suraksan": "nowon-gu", "madeul": "nowon-gu", "junggye": "nowon-gu", "hagye": "nowon-gu",
    "gongneung": "nowon-gu", "taereung": "nowon-gu", "meokgol": "jungnang-gu", "junghwa": "jungnang-gu",
    "sangbong": "jungnang-gu", "myeonmok": "jungnang-gu", "sagajeong": "jungnang-gu",
    "yongmasan": "jungnang-gu", "junggok": "gwangjin-gu", "children-grand-park": "gwangjin-gu",
    "ttukseom-resort": "gwangjin-gu", "cheongdam": "gangnam-gu", "gangnam-gu-office": "gangnam-gu",
    "hak-dong": "gangnam-gu", "nonhyeon": "gangnam-gu", "banpo": "seocho-gu", "naebang": "seocho-gu",
    "namseong": "dongjak-gu", "boramae": "dongjak-gu", "sindaebang-samgeori": "dongjak-gu",
    "jangseungbaegi": "dongjak-gu",
    # 8호선
    "amsa": "gangdong-gu", "gangdong-guoffice": "gangdong-gu", "mongchontoseong": "songpa-gu",
    "seokchon": "songpa-gu", "songpa": "songpa-gu", "garak-market": "songpa-gu",
    "munjeong": "songpa-gu", "jangji": "songpa-gu", "bokjeong": "songpa-gu",
    # 9호선
    "gaehwa": "gangseo-gu", "airport-market": "gangseo-gu", "sinbanghwa": "gangseo-gu",
    "yangcheon-hyanggyo": "gangseo-gu", "gayang": "gangseo-gu", "jeungmi": "gangseo-gu",
    "deungchon": "gangseo-gu", "yeomchang": "gangseo-gu", "sinmokdong": "yangcheon-gu",
    "seonyudo": "yeongdeungpo-gu", "gukhoe": "yeongdeungpo-gu", "saetgang": "yeongdeungpo-gu",
    "nodeul": "dongjak-gu", "heukseok": "dongjak-gu", "gubanpo": "seocho-gu", "sinbanpo": "seocho-gu",
    "sapyeong": "seocho-gu", "sinnonhyeon": "gangnam-gu", "eonju": "gangnam-gu",
    "seonjeongneung": "gangnam-gu", "samseong-jungang": "gangnam-gu", "bongeunsa": "gangnam-gu",
    # 신분당선(서울 구간)
    "yangjae-citizens-forest": "seocho-gu", "cheonggyesan": "seocho-gu",
    # 수인분당선(서울 구간)
    "seoulforest": "seongdong-gu", "apgujeong-rodeo": "gangnam-gu", "hanti": "gangnam-gu",
    "guryong": "gangnam-gu", "gaepo-dong": "gangnam-gu", "daemosan": "gangnam-gu",
    # 경의중앙선·경춘선(서울 구간)
    "gajwa": "seodaemun-gu", "jungnang": "jungnang-gu", "mangu": "jungnang-gu",
    # 신림선
    "seoul-national-univ-venture": "gwanak-gu", "gwanaksan": "gwanak-gu", "seowon": "gwanak-gu",
    # 우이신설선
    "bukhansan-ui": "gangbuk-gu", "solbat": "gangbuk-gu", "4-19-democracy": "gangbuk-gu",
    "gaori": "gangbuk-gu", "hwagye": "gangbuk-gu", "samyang": "gangbuk-gu",
    "samyang-sageori": "gangbuk-gu", "solsaem": "seongbuk-gu",
}
