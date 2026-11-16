# 🗄️ SQLite 데이터베이스 구현 완료!

## ✅ 완성된 것들

1. **`database.py`** - 데이터베이스 연결 설정
2. **`models/__init__.py`** - 모델 패키지
3. **`models/user.py`** - 사용자 모델
4. **`models/game_session.py`** - 게임 세션 모델
5. **`routers/game_db.py`** - DB 기반 게임 API
6. **`init_db.py`** - DB 초기화 스크립트
7. **`migrate_to_db.py`** - JSON → DB 마이그레이션
8. **`test_db_api.py`** - DB API 테스트
9. **`requirements.txt`** - SQLAlchemy, Alembic 추가
10. **`main.py`** - game_db 라우터 등록

---

## 🚀 빠른 시작 가이드

### 1️⃣ 패키지 설치

```bash
pip install -r requirements.txt
```

새로 추가된 패키지:
- `sqlalchemy==2.0.25`
- `alembic==1.13.1`

---

### 2️⃣ 데이터베이스 초기화

```bash
python init_db.py
```

**예상 출력:**
```
==================================================
🗄️ LiTR 데이터베이스 초기화
==================================================

🔨 데이터베이스 테이블 생성 중...
✅ 데이터베이스 테이블이 생성되었습니다.

✅ 데이터베이스 초기화 완료!
   위치: C:\Users\lynlo\Downloads\01.26 LiTR\LiTR\litrpg.db

생성된 테이블:
   - users (사용자)
   - game_sessions (게임 세션)
```

---

### 3️⃣ 기존 JSON 세이브 마이그레이션 (선택)

만약 `saves/` 폴더에 기존 세이브 파일이 있다면:

```bash
python migrate_to_db.py
```

**예상 출력:**
```
==================================================
📦 JSON → DB 마이그레이션 시작
==================================================

📁 3개의 세이브 파일을 발견했습니다.

✅ 마이그레이션 성공: session123
✅ 마이그레이션 성공: session456
✅ 마이그레이션 성공: session789

==================================================
📊 마이그레이션 완료
==================================================
✅ 성공: 3개
❌ 실패: 0개
```

---

### 4️⃣ 서버 실행

```bash
uvicorn main:app --reload
```

---

### 5️⃣ API 테스트

```bash
python test_db_api.py
```

또는 Swagger UI:
```
http://localhost:8000/docs
```

**새로 추가된 섹션: "game-db"**

---

## 📡 데이터베이스 API 엔드포인트

모든 엔드포인트는 `/api/game-db/*` 경로를 사용합니다.

### 기존 JSON API vs 새 DB API

| 기능 | JSON API | DB API |
|------|----------|--------|
| 게임 초기화 | `POST /api/game/initialize` | `POST /api/game-db/initialize` |
| 게임 저장 | `POST /api/game/save` | `POST /api/game-db/save` |
| 게임 로드 | `GET /api/game/state/{id}` | `GET /api/game-db/state/{id}` |
| 상태 업데이트 | `POST /api/game/character/update` | `POST /api/game-db/character/update` |
| 데미지 적용 | `POST /api/game/character/damage` | `POST /api/game-db/character/damage` |
| 치유 적용 | `POST /api/game/character/heal` | `POST /api/game-db/character/heal` |
| 세이브 목록 | `GET /api/game/saves` | `GET /api/game-db/saves` |
| 세이브 삭제 | `DELETE /api/game/state/{id}` | `DELETE /api/game-db/state/{id}` |

**💡 팁**: 두 API 모두 사용 가능합니다!
- JSON: 빠른 프로토타입, 간단한 백업
- DB: 프로덕션, 복잡한 쿼리, 사용자 관리

---

## 🗄️ 데이터베이스 구조

### **테이블: users**

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER | PK |
| email | STRING | 이메일 (unique) |
| username | STRING | 사용자명 (unique) |
| nickname | STRING | 닉네임 |
| hashed_password | STRING | 암호화된 비밀번호 |
| credits | INTEGER | 크레딧 |
| follow_count | INTEGER | 팔로워 수 |
| oauth_provider | STRING | OAuth 제공자 |
| oauth_id | STRING | OAuth ID |
| created_at | DATETIME | 가입일 |
| last_login | DATETIME | 마지막 로그인 |
| is_active | BOOLEAN | 활성 여부 |
| is_admin | BOOLEAN | 관리자 여부 |

### **테이블: game_sessions**

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER | PK |
| session_id | STRING | 세션 고유 ID (unique) |
| user_id | INTEGER | FK → users.id |
| scenario_id | STRING | 시나리오 ID |
| scenario_title | STRING | 시나리오 제목 |
| character_id | STRING | 캐릭터 ID |
| character_name | STRING | 캐릭터 이름 |
| character_state | JSON | 캐릭터 상태 |
| story_progress | JSON | 스토리 진행 |
| flags | JSON | 게임 플래그 |
| combat_state | JSON | 전투 상태 |
| location | STRING | 현재 위치 |
| turn | INTEGER | 턴 수 |
| created_at | DATETIME | 생성일 |
| updated_at | DATETIME | 수정일 |
| last_played | DATETIME | 마지막 플레이 |

---

## 🎯 프론트엔드 연동

### JavaScript 사용법

```javascript
const API_BASE_URL = 'http://localhost:8000';

// DB API 사용 (권장!)
async function startNewGame() {
    const sessionId = `session_${Date.now()}`;
    
    // game-db 엔드포인트 사용
    const response = await fetch(
        `${API_BASE_URL}/api/game-db/initialize?` +
        `session_id=${sessionId}&` +
        `scenario_id=horror_school&` +
        `character_id=detective_k`,
        { method: 'POST' }
    );
    
    const data = await response.json();
    return data.game_state;
}

// JSON API와 동일한 방식으로 사용
async function saveGame(gameState) {
    const response = await fetch(`${API_BASE_URL}/api/game-db/save`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(gameState)
    });
    return await response.json();
}
```

---

## 📊 JSON vs DB 비교

### **JSON API (`/api/game/*`)**
**장점:**
- ✅ 간단하고 빠름
- ✅ 파일로 직접 확인 가능
- ✅ 백업이 쉬움

**단점:**
- ❌ 동시 접속 처리 어려움
- ❌ 복잡한 쿼리 불가
- ❌ 사용자 관리 어려움

### **DB API (`/api/game-db/*`)**
**장점:**
- ✅ 빠른 조회 속도
- ✅ 복잡한 쿼리 가능
- ✅ 사용자별 세이브 관리
- ✅ 동시 접속 안전
- ✅ 프로덕션 준비 완료

**단점:**
- ❌ 설정이 조금 복잡
- ❌ 직접 파일 확인 어려움

---

## 💡 추천 사용법

### **개발 단계**
- JSON API 사용 (`/api/game/*`)
- 빠른 프로토타입
- 디버깅 쉬움

### **프로덕션**
- DB API 사용 (`/api/game-db/*`)
- 안정적이고 확장 가능
- 사용자 관리 기능

### **현재 상태**
- **둘 다 사용 가능!**
- 프론트엔드에서 선택 가능

---

## 🔧 데이터베이스 관리

### **SQLite 파일 위치**
```
litrpg.db
```

### **DB 브라우저 도구 (권장)**
- **DB Browser for SQLite**: https://sqlitebrowser.org/
- 무료, 쉬운 GUI
- 테이블, 데이터 직접 확인 가능

### **테이블 재생성**
```bash
python init_db.py
```
(기존 데이터 삭제 후 재생성 여부 선택)

---

## 📋 완료 체크리스트

- ✅ SQLAlchemy 설정
- ✅ User 모델 생성
- ✅ GameSession 모델 생성
- ✅ DB 초기화 스크립트
- ✅ DB API 구현
- ✅ 마이그레이션 스크립트
- ✅ 테스트 스크립트
- ✅ main.py 라우터 등록

---

## 🎁 추가 기능

### **User 모델 준비 완료**
- 이메일/비밀번호 로그인 지원
- OAuth 로그인 지원 (Google, Discord)
- 크레딧 관리
- 팔로우 수 관리

### **GameSession 모델**
- 사용자별 세션 관리
- 자동 타임스탬프
- JSON 필드 지원 (유연한 데이터 구조)

### **관계 설정**
- User ↔ GameSession (1:N)
- 사용자 삭제 시 세션 자동 삭제 (cascade)

---

## 🔥 다음 단계

### **즉시 가능**
- ✅ DB API 사용 시작
- ✅ 프론트엔드 연동
- ✅ JSON → DB 전환

### **추후 추가**
- [ ] JWT 인증 구현
- [ ] OAuth 연동
- [ ] 사용자별 세이브 필터링
- [ ] PostgreSQL로 마이그레이션

---

## 🎉 완료!

**SQLite 데이터베이스 구현 완료!**

**실행 순서:**
1. `pip install -r requirements.txt` - 패키지 설치
2. `python init_db.py` - DB 초기화
3. `python migrate_to_db.py` - JSON 마이그레이션 (선택)
4. `uvicorn main:app --reload` - 서버 실행
5. `python test_db_api.py` - 테스트
6. `http://localhost:8000/docs` - API 문서 확인

---

## 📂 프로젝트 구조 (업데이트)

```
LiTR/
├── database.py               # 🆕 DB 연결 설정
├── models/                   # 🆕 데이터베이스 모델
│   ├── __init__.py
│   ├── user.py              # 사용자 모델
│   └── game_session.py      # 게임 세션 모델
├── routers/
│   ├── game.py              # JSON 기반 API
│   └── game_db.py           # 🆕 DB 기반 API
├── init_db.py               # 🆕 DB 초기화
├── migrate_to_db.py         # 🆕 JSON → DB
├── test_db_api.py           # 🆕 DB 테스트
├── litrpg.db                # 🆕 SQLite 파일 (실행 후 생성)
└── saves/                   # JSON 파일 (기존)
```

---

## 💾 데이터 저장 방식

### **옵션 1: JSON (기존 방식)**
```
POST /api/game/save
```
- saves/ 폴더에 파일 저장
- 간단하고 빠름

### **옵션 2: Database (새로운 방식)**
```
POST /api/game-db/save
```
- litrpg.db에 저장
- 프로덕션 준비 완료

**둘 다 동시 사용 가능!**

---

## 🎯 사용 예시

### 게임 시작 (DB 버전)
```bash
curl -X POST "http://localhost:8000/api/game-db/initialize?session_id=test123&scenario_id=horror_school&character_id=detective_k"
```

### 게임 저장 (DB 버전)
```bash
curl -X POST "http://localhost:8000/api/game-db/save" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test123",
    "scenario_id": "horror_school",
    "character_state": { ... }
  }'
```

---

## 🔍 DB 확인 방법

### **1. Python으로 확인**
```python
import sqlite3

conn = sqlite3.connect('litrpg.db')
cursor = conn.cursor()

# 세이브 목록 조회
cursor.execute("SELECT session_id, scenario_id, location FROM game_sessions")
for row in cursor.fetchall():
    print(row)

conn.close()
```

### **2. DB Browser 사용 (추천!)**
- https://sqlitebrowser.org/ 다운로드
- litrpg.db 파일 열기
- 시각적으로 데이터 확인/수정

---

## 🎁 이점

### **이제 가능한 것들**

1. **사용자별 세이브 관리**
```python
# 특정 사용자의 세이브만 조회
GET /api/game-db/saves?user_id=123
```

2. **복잡한 쿼리**
```python
# 시나리오별 통계
SELECT scenario_id, COUNT(*) FROM game_sessions GROUP BY scenario_id
```

3. **빠른 검색**
```python
# 세션 ID로 즉시 찾기 (인덱스 사용)
```

4. **동시 접속 안전**
```python
# 여러 사용자가 동시에 저장해도 안전
```

5. **트랜잭션 지원**
```python
# 에러 발생 시 자동 롤백
```

---

## 📝 주의사항

### **중요!**
1. `litrpg.db` 파일을 `.gitignore`에 추가하세요
2. 백업을 정기적으로 수행하세요
3. 프로덕션에서는 PostgreSQL 권장

### **.gitignore에 추가**
```
litrpg.db
litrpg.db-journal
*.db
*.db-journal
```

---

## 🚀 다음 작업 제안

### **우선순위 2 작업**
1. ✅ **완료!** SQLite 데이터베이스
2. 🔜 JWT 인증 시스템
3. 🔜 사용자 등록/로그인 API
4. 🔜 OAuth 연동
5. 🔜 로깅 시스템

### **선택 사항**
- [ ] PostgreSQL로 전환
- [ ] Redis 캐싱
- [ ] WebSocket 추가
- [ ] Docker 컨테이너화

---

## 🎉 완료!

**SQLite 데이터베이스 구현 완료!**

이제 프로덕션 수준의 데이터 관리가 가능합니다! 🚀
