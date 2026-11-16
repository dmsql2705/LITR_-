from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse # 파일 응답 도구
from routers import chat, voice, pdf, dice, game, game_db, auth, gameplay, image_gen, multiplayer, session, materials, profile, friends, notifications, admin, payment
from dotenv import load_dotenv
import os
import json
import logging

# Security middleware imports
from middleware.security import (
    SecurityHeadersMiddleware,
    InputSanitizationMiddleware,
    SQLInjectionProtectionMiddleware
)
from middleware.csrf import CSRFMiddleware
from middleware.rate_limit import limiter
from slowapi.errors import RateLimitExceeded

# .env 파일 로드
load_dotenv()

# 구조화된 로깅 설정 (H6: print() → logging)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("litr")

# 데이터베이스 초기화
from database import init_db, SessionLocal
init_db()

# 프리셋 시나리오 시드 데이터
def seed_preset_scenarios():
    """프리셋 시나리오가 DB에 없으면 자동으로 생성합니다."""
    from models.scenario import Scenario

    PRESET_SCENARIOS = [
        {
            "id": "horror_school",
            "title": "폐교 심야 조사",
            "description": "10년 전 문을 닫은 고등학교. 밤마다 피아노 소리가 들린다는 소문을 확인하기 위해 당신은 학교로 향합니다.",
            "genre": ["공포", "미스터리"],
            "difficulty": "하",
            "playtime": "60분",
            "content": {
                "title": "폐교 심야 조사",
                "genre": ["공포", "미스터리"],
                "difficulty": "하",
                "playtime": "60분",
                "description": "10년 전 문을 닫은 고등학교. 밤마다 피아노 소리가 들린다는 소문을 확인하기 위해 당신은 학교로 향합니다. 어둠 속에서 들려오는 쇼팽의 녹턴... 이 학교에서 무슨 일이 있었던 걸까요?",
                "worldSetting": {
                    "era": "현대",
                    "location": "폐교된 고등학교",
                    "atmosphere": "으스스하고 음울한 분위기"
                },
                "backstory": "10년 전 이 학교에서 음악 교사 김수진이 의문의 죽음을 당했다. 공식적으로는 사고사로 처리되었지만, 그 이후로 밤마다 음악실에서 피아노 소리가 들린다는 소문이 퍼졌다. 학교는 결국 폐교되었고, 아무도 이 건물에 들어가려 하지 않는다.",
                "mainObjective": "학교에서 들리는 피아노 소리의 정체를 밝히고, 10년 전 김수진의 죽음에 숨겨진 진실을 파헤치세요.",
                "keyLocations": [
                    {"name": "음악실", "description": "김수진 교사가 마지막으로 목격된 곳. 피아노가 아직 남아있다."},
                    {"name": "교무실", "description": "당시 교사들의 기록이 남아있을 수 있다."},
                    {"name": "지하 보일러실", "description": "학생들 사이에서 금지 구역으로 알려진 곳."},
                    {"name": "옥상", "description": "김수진 교사의 사고 현장으로 알려진 곳."}
                ],
                "npcs": [
                    {"name": "관리인 박씨", "role": "정보 제공자", "description": "학교를 관리하는 노인. 10년 전 사건을 기억하고 있다.", "personality": "과묵하지만 진실을 알고 있는 듯한 눈빛"},
                    {"name": "김수진의 영혼", "role": "핵심 NPC", "description": "음악실에 머무는 존재. 진실을 전하려 한다.", "personality": "슬프고 원망에 찬 존재"}
                ],
                "openingText": "비가 그친 밤, 당신은 폐교 앞에 서 있습니다. 녹슨 철문 너머로 보이는 학교 건물은 10년의 세월만큼 낡아 있습니다. 그때, 어디선가 피아노 소리가 들려옵니다... 쇼팽의 녹턴. 당신은 손전등을 켜고 철문을 밀어 열었습니다.",
                "plotTwists": [],
                "clues": [],
                "endings": {"good": "진실을 밝히고 김수진의 영혼을 해방시킨다", "neutral": "일부 진실만 밝힌 채 학교를 떠난다", "bad": "학교에 갇혀 같은 운명을 맞이한다"}
            },
            "visibility": "public",
            "author": "LiTR",
        },
        {
            "id": "noir_detective",
            "title": "느와르 탐정 사무소",
            "description": "비 내리는 도시. 사라진 여가수를 찾아달라는 의뢰인이 찾아왔습니다. 단순 실종이 아님을 직감합니다.",
            "genre": ["수사", "느와르", "미스터리"],
            "difficulty": "중",
            "playtime": "120분",
            "content": {
                "title": "느와르 탐정 사무소",
                "genre": ["수사", "느와르", "미스터리"],
                "difficulty": "중",
                "playtime": "120분",
                "description": "비 내리는 도시. 사라진 여가수를 찾아달라는 의뢰인이 찾아왔습니다. 단순 실종이 아님을 직감합니다. 어둠의 도시에서 진실을 추적하세요.",
                "worldSetting": {
                    "era": "1940년대",
                    "location": "비 내리는 항구 도시",
                    "atmosphere": "어둡고 퇴폐적인 느와르 분위기"
                },
                "backstory": "재즈 가수 리나는 블루문 클럽의 스타였다. 일주일 전 마지막 공연을 마치고 사라졌다. 그녀의 매니저가 당신의 사무소를 찾아왔다. 경찰은 단순 가출로 처리했지만, 매니저는 그녀가 위험에 처했다고 확신한다.",
                "mainObjective": "실종된 재즈 가수 리나를 찾아내세요. 그녀가 마지막으로 목격된 장소들을 수사하고, 관련된 인물들을 심문하여 사건의 전모를 밝혀야 합니다.",
                "keyLocations": [
                    {"name": "탐정 사무소", "description": "당신의 사무실. 빗소리와 네온사인 불빛이 창문을 비춘다."},
                    {"name": "블루문 클럽", "description": "리나가 마지막으로 공연한 재즈 클럽."},
                    {"name": "항구 창고", "description": "수상한 거래가 이루어지는 곳이라는 제보가 있다."},
                    {"name": "리나의 아파트", "description": "리나가 살던 곳. 무언가 단서가 남아있을지 모른다."}
                ],
                "npcs": [
                    {"name": "매니저 톰", "role": "의뢰인", "description": "리나의 매니저. 그녀를 진심으로 걱정하는 듯하다.", "personality": "초조하고 불안한 모습"},
                    {"name": "바텐더 쟈크", "role": "정보 제공자", "description": "블루문 클럽의 바텐더. 모든 걸 알고 있지만 쉽게 말하지 않는다.", "personality": "과묵하고 신중함"},
                    {"name": "보스 카를로", "role": "적대자", "description": "도시의 어둠을 지배하는 마피아 보스.", "personality": "카리스마 있지만 위험한 인물"}
                ],
                "openingText": "빗줄기가 사무실 창문을 때립니다. 네온 불빛이 젖은 유리를 통해 방 안을 물들이고 있습니다. 문이 열리고, 비에 젖은 남자가 들어옵니다. '탐정님... 리나를 찾아주세요. 경찰은 믿을 수 없습니다.' 그가 당신 앞에 사진 한 장을 내밀었습니다.",
                "plotTwists": [],
                "clues": [],
                "endings": {"good": "리나를 구출하고 범인을 밝힌다", "neutral": "리나를 찾았지만 진실은 묻힌다", "bad": "모든 단서를 놓치고 사건은 미궁에 빠진다"}
            },
            "visibility": "public",
            "author": "LiTR",
        },
        {
            "id": "action_skygarden",
            "title": "공중정원 암살 작전",
            "description": "부유 도시의 펜트하우스 파티. 타겟은 삼엄한 경비 속에 있습니다. 당신의 임무는 조용하고 확실하게 처리하는 것입니다.",
            "genre": ["액션", "SF", "스릴러"],
            "difficulty": "중",
            "playtime": "90분",
            "content": {
                "title": "공중정원 암살 작전",
                "genre": ["액션", "SF", "스릴러"],
                "difficulty": "중",
                "playtime": "90분",
                "description": "부유 도시의 펜트하우스 파티. 타겟은 삼엄한 경비 속에 있습니다. 당신의 임무는 조용하고 확실하게 처리하는 것입니다.",
                "worldSetting": {
                    "era": "근미래 2045년",
                    "location": "부유 도시 스카이가든",
                    "atmosphere": "화려하지만 위험이 도사리는 긴장감"
                },
                "backstory": "무기 밀매상 빅터 모건이 스카이가든 펜트하우스에서 대규모 파티를 연다. 그는 전쟁 지역에 불법 무기를 공급하여 수천 명의 목숨을 앗아간 인물이다. 당신은 조직으로부터 그를 제거하라는 임무를 받았다.",
                "mainObjective": "무기 밀매상 빅터 모건을 제거하세요. 파티에 잠입하여 타겟에게 접근하고, 경비를 피해 임무를 완수해야 합니다.",
                "keyLocations": [
                    {"name": "파티 홀", "description": "수백 명의 손님이 모인 화려한 파티장."},
                    {"name": "빅터의 서재", "description": "빅터의 비밀이 숨겨진 개인 공간."},
                    {"name": "옥상 정원", "description": "도시를 한눈에 내려다볼 수 있는 공중정원."},
                    {"name": "보안 센터", "description": "건물 전체의 CCTV와 경비를 관할하는 곳."}
                ],
                "npcs": [
                    {"name": "빅터 모건", "role": "타겟", "description": "무기 밀매상. 파티의 주인공.", "personality": "자신만만하고 교활한 사업가"},
                    {"name": "경비대장 콜", "role": "장애물", "description": "빅터의 개인 경호원. 전직 특수부대원.", "personality": "냉철하고 경계심이 강함"},
                    {"name": "정보원 소피아", "role": "조력자", "description": "파티에 잠입한 당신의 연락책.", "personality": "침착하고 전문적인 스파이"}
                ],
                "openingText": "엘리베이터가 200층에 도착합니다. 문이 열리자 화려한 조명과 음악 소리가 쏟아져 나옵니다. 스카이가든 펜트하우스 파티. 당신은 초대받은 손님으로 위장하고 있습니다. 이어폰 속에서 소피아의 목소리가 들립니다. '타겟은 파티 홀 중앙에 있어요. 경비가 삼엄하니 조심하세요.'",
                "plotTwists": [],
                "clues": [],
                "endings": {"good": "임무를 완수하고 탈출에 성공한다", "neutral": "타겟을 제거했지만 정체가 발각된다", "bad": "임무에 실패하고 포위당한다"}
            },
            "visibility": "public",
            "author": "LiTR",
        },
    ]

    db = SessionLocal()
    try:
        for preset in PRESET_SCENARIOS:
            existing = db.query(Scenario).filter(Scenario.id == preset["id"]).first()
            if not existing:
                try:
                    scenario = Scenario(
                        id=preset["id"],
                        title=preset["title"],
                        description=preset["description"],
                        genre=preset["genre"],
                        difficulty=preset["difficulty"],
                        playtime=preset["playtime"],
                        content=preset["content"],
                        visibility=preset["visibility"],
                        author=preset["author"],
                    )
                    db.add(scenario)
                    db.flush()  # flush로 개별 에러 감지
                    logger.info("프리셋 시나리오 생성: %s", preset["title"])
                except Exception as e:
                    db.rollback()
                    logger.error("프리셋 시나리오 '%s' 생성 실패: %s", preset["title"], str(e), exc_info=True)
                    # 개별 실패 시 raw SQL로 재시도
                    try:
                        from sqlalchemy import text
                        db.execute(text("""
                            INSERT INTO scenarios (id, title, description, genre, difficulty, playtime, content, visibility, author, created_at, updated_at)
                            VALUES (:id, :title, :desc, :genre, :diff, :play, :content, :vis, :author, NOW(), NOW())
                            ON CONFLICT (id) DO NOTHING
                        """), {
                            "id": preset["id"],
                            "title": preset["title"],
                            "desc": preset["description"],
                            "genre": json.dumps(preset["genre"]),
                            "diff": preset["difficulty"],
                            "play": preset["playtime"],
                            "content": json.dumps(preset["content"]),
                            "vis": preset["visibility"],
                            "author": preset["author"],
                        })
                        db.commit()
                        logger.info("프리셋 시나리오 '%s' raw SQL로 생성 성공", preset["title"])
                    except Exception as e2:
                        db.rollback()
                        logger.error("프리셋 시나리오 '%s' raw SQL도 실패: %s", preset["title"], str(e2), exc_info=True)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error("프리셋 시나리오 시드 실패: %s", str(e), exc_info=True)
    finally:
        db.close()

seed_preset_scenarios()


# 프리셋 캐릭터 시드 데이터
def seed_preset_characters():
    """프리셋 캐릭터가 DB에 없으면 자동으로 생성합니다."""
    from models.character import Character

    PRESET_CHARACTERS = [
        {
            "id": "default_detective",
            "name": "사립 탐정 K",
            "description": "예리한 관찰력과 추리력을 가졌습니다. 전직 형사 출신으로 싸움 실력도 나쁘지 않습니다.",
            "background": "전직 형사 출신의 사립 탐정. 본명은 '김경호'. 5년 전 파트너였던 동료가 미제 사건을 수사하다 의문의 죽음을 당했다. 경찰 내부의 부패와 무관심에 환멸을 느끼고 사표를 던진 뒤, 홀로 탐정 사무소를 열었다. 동료의 죽음에 대한 진실을 여전히 찾고 있다.",
            "stats": {
                "icon": "🕵️",
                "occupation": "수사 전문가",
                "age": 35,
                "base_stats": {"STR": 45, "CON": 50, "SIZ": 55, "DEX": 65, "APP": 60, "INT": 90, "POW": 80, "EDU": 85, "LUK": 55},
                "hp": 12,
                "maxHp": 12,
                "mp": 12,
                "maxMp": 12,
                "san": 60,
                "maxSan": 99,
                "mov": 7,
                "personality": "냉철하고 분석적이지만, 약자에 대한 연민이 있다.",
                "speechStyle": "차분하고 논리적인 말투",
                "skills": [
                    {"name": "증거 분석", "description": "현장의 단서를 분석합니다", "bonus": "+20"},
                    {"name": "심문 기술", "description": "대상을 심문합니다", "bonus": "+15"},
                    {"name": "은밀 행동", "description": "은밀하게 행동합니다", "bonus": "+10"},
                    {"name": "격투술", "description": "근접 전투 기술", "bonus": "+10"}
                ],
                "equipment": [
                    {"name": "손전등", "description": "어두운 곳을 비추는 강력한 손전등"},
                    {"name": "수첩과 펜", "description": "단서를 기록하는 수첩"},
                    {"name": "돋보기", "description": "미세한 흔적을 관찰하는 도구"}
                ],
                "weaknesses": ["과거의 트라우마", "고소공포증"],
                "occupationPoints": 340,
                "interestPoints": 180,
            },
        },
        {
            "id": "default_warrior",
            "name": "용병 아르텐",
            "description": "묵직한 대검을 사용하는 베테랑 전사. 말보다는 행동이 앞서는 타입입니다.",
            "background": "폭풍 벼락이 치는 마을 출신. 10살 때 마을이 신적에게 습격당해 가족을 모두 잃었다. 이후 마을이 결계에게 거두어져 검술을 배웠다. 20년간 여러 전장터와 분쟁 지역을 떠돌며 용병으로 살아왔다. 수많은 전투에서 살아남아 '불사의 아르텐'이라는 별명을 얻었다. 지금은 특별한 소속 없이 의뢰를 받아 일하고 있다.",
            "stats": {
                "icon": "⚔️",
                "occupation": "전투 전문가",
                "age": 32,
                "base_stats": {"STR": 80, "CON": 75, "SIZ": 70, "DEX": 60, "APP": 45, "INT": 50, "POW": 55, "EDU": 40, "LUK": 55},
                "hp": 15,
                "maxHp": 15,
                "mp": 11,
                "maxMp": 11,
                "san": 55,
                "maxSan": 99,
                "mov": 7,
                "personality": "과묵하지만 의리가 있다. 약속을 반드시 지킨다.",
                "speechStyle": "짧고 단호한 말투",
                "skills": [
                    {"name": "대검 숙련", "description": "대검 전투에 능숙합니다", "bonus": "+25"},
                    {"name": "방어 태세", "description": "방어 자세를 취합니다", "bonus": "+15"},
                    {"name": "전장 감각", "description": "전장의 위험을 감지합니다", "bonus": "+10"},
                    {"name": "응급 처치", "description": "간단한 치료를 합니다", "bonus": "+5"}
                ],
                "equipment": [
                    {"name": "대검", "description": "묵직하지만 강력한 양손검"},
                    {"name": "가죽 갑옷", "description": "이동이 자유로운 경장갑"},
                    {"name": "치료 키트", "description": "간단한 응급 처치 도구"}
                ],
                "weaknesses": ["마법에 대한 불신", "수영 불가"],
                "occupationPoints": 160,
                "interestPoints": 100,
            },
        },
    ]

    db = SessionLocal()
    try:
        for preset in PRESET_CHARACTERS:
            existing = db.query(Character).filter(Character.id == preset["id"]).first()
            if not existing:
                try:
                    character = Character(
                        id=preset["id"],
                        user_id=None,
                        name=preset["name"],
                        description=preset["description"],
                        stats=preset["stats"],
                        background=preset["background"],
                        is_public=True,
                    )
                    db.add(character)
                    db.flush()
                    logger.info("프리셋 캐릭터 생성: %s", preset["name"])
                except Exception as e:
                    db.rollback()
                    logger.error("프리셋 캐릭터 '%s' 생성 실패: %s", preset["name"], str(e), exc_info=True)
                    # raw SQL 폴백
                    try:
                        from sqlalchemy import text
                        db.execute(text("""
                            INSERT INTO characters (id, user_id, name, description, stats, background, is_public, created_at, updated_at)
                            VALUES (:id, NULL, :name, :desc, :stats, :bg, true, NOW(), NOW())
                            ON CONFLICT (id) DO NOTHING
                        """), {
                            "id": preset["id"],
                            "name": preset["name"],
                            "desc": preset["description"],
                            "stats": json.dumps(preset["stats"]),
                            "bg": preset["background"],
                        })
                        db.commit()
                        logger.info("프리셋 캐릭터 '%s' raw SQL로 생성 성공", preset["name"])
                    except Exception as e2:
                        db.rollback()
                        logger.error("프리셋 캐릭터 '%s' raw SQL도 실패: %s", preset["name"], str(e2), exc_info=True)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error("프리셋 캐릭터 시드 실패: %s", str(e), exc_info=True)
    finally:
        db.close()

seed_preset_characters()

# FastAPI 앱 생성 — 프로덕션에서는 Swagger/ReDoc 비활성화
_is_production = os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("ENVIRONMENT") == "production"
app = FastAPI(
    title="TRPG Game Backend",
    version="1.0.0",
    description="AI-powered TRPG game platform",
    docs_url=None if _is_production else "/docs",
    redoc_url=None if _is_production else "/redoc",
)

# CORS 설정 - 환경 변수에서 허용할 도메인 읽기 (rate limit handler보다 먼저 정의)
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
if allowed_origins_env:
    # 쉼표로 구분된 도메인 목록 (예: "https://app.example.com,https://admin.example.com")
    allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]
else:
    # 환경 변수 없으면 로컬 개발 환경 허용
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    allowed_origins = [frontend_url, "http://localhost:3000"]

# Rate limiter state + 커스텀 핸들러 (CORS 헤더 포함)
app.state.limiter = limiter

def _custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Rate limit 초과 시 CORS 헤더를 포함한 429 응답 반환"""
    response = JSONResponse(
        status_code=429,
        content={"detail": f"요청 한도를 초과했습니다. 잠시 후 다시 시도해주세요. ({exc.detail})"},
    )
    origin = request.headers.get("origin", "")
    if origin in allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

app.add_exception_handler(RateLimitExceeded, _custom_rate_limit_handler)

# Security middleware (order matters!)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(InputSanitizationMiddleware)
app.add_middleware(SQLInjectionProtectionMiddleware)
app.add_middleware(CSRFMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "X-Requested-With", "X-CSRF-Token"],
)

# 👇 [핵심 수정] 메인 화면 강제 연결 (순서가 제일 중요함!)
# 파일 이름이 index.html 이든 LiTR.html 이든 있는 놈을 찾아서 보여줍니다.
@app.get("/")
async def read_root():
    # 1순위: index.html 찾기
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    # 2순위: LiTR.html 찾기
    elif os.path.exists("LiTR.html"):
        return FileResponse("LiTR.html")
    # 3순위: API 전용 모드 (프론트엔드 별도 배포)
    else:
        return JSONResponse(
            content={
                "service": "LiTR TRPG Backend API",
                "version": "1.0.0",
                "docs": "/docs",
            }
        )

# 라우터 등록
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(session.router, prefix="/api", tags=["session"])
app.include_router(gameplay.router, prefix="/api", tags=["gameplay"])
app.include_router(multiplayer.router, prefix="/api", tags=["multiplayer"])
app.include_router(image_gen.router, prefix="/api", tags=["image"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(voice.router, prefix="/api", tags=["voice"])
app.include_router(pdf.router, prefix="/api", tags=["pdf"])
app.include_router(dice.router, prefix="/api", tags=["dice"])
app.include_router(game.router, prefix="/api", tags=["game"])
app.include_router(game_db.router, prefix="/api", tags=["game-db"])
app.include_router(materials.router, prefix="/api", tags=["materials"])
app.include_router(profile.router, prefix="/api", tags=["profile"])
app.include_router(friends.router, prefix="/api", tags=["friends"])
app.include_router(notifications.router, prefix="/api", tags=["notifications"])
app.include_router(admin.router, prefix="/api", tags=["admin"])
app.include_router(payment.router, prefix="/api", tags=["payment"])

# 헬스 체크 (Railway deployment)
@app.get("/health")
async def health_check():
    """
    Health check endpoint for Railway and monitoring services.
    환경변수 설정 상태를 확인합니다 (값 자체는 노출하지 않음).
    """
    from datetime import datetime, timezone

    env_status = {
        "DATABASE_URL": bool(os.getenv("DATABASE_URL")),
        "GOOGLE_AI_API_KEY": bool(os.getenv("GOOGLE_AI_API_KEY")),
        "JWT_SECRET_KEY": bool(os.getenv("JWT_SECRET_KEY")),
        "FRONTEND_URL": os.getenv("FRONTEND_URL", "(not set)"),
        "ALLOWED_ORIGINS": os.getenv("ALLOWED_ORIGINS", "(not set)"),
        "SUPABASE_URL": bool(os.getenv("SUPABASE_URL")),
        "SUPABASE_SERVICE_KEY": bool(os.getenv("SUPABASE_SERVICE_KEY")),
        "OPENAI_API_KEY": bool(os.getenv("OPENAI_API_KEY")),
    }

    return {
        "status": "healthy",
        "service": "LiTR TRPG Backend",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "env_configured": env_status,
    }

# 정적 파일 서빙 (images)
if os.path.exists("images"):
    app.mount("/images", StaticFiles(directory="images"), name="images")

# 정적 파일 서빙 (프론트엔드 파일이 있을 경우만)
# Railway 배포 시에는 백엔드만 배포되므로 프론트엔드 파일이 없을 수 있음
# 프론트엔드 정적 파일 서빙 — 전체 디렉토리 노출 방지를 위해 static/ 디렉토리만 서빙
_static_dir = "static"
if os.path.exists(_static_dir):
    app.mount("/", StaticFiles(directory=_static_dir, html=True), name="static")
elif os.path.exists("LiTR.html") or os.path.exists("index.html"):
    # Legacy fallback: HTML 파일이 루트에 있는 경우 (개발 환경만)
    if not _is_production:
        app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
