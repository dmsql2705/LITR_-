# 🗄️ 데이터베이스 관리 가이드

## 📍 데이터베이스 위치

```
c:\Users\lynlo\Downloads\01.26 LiTR\LiTR\litrpg.db
```

이 SQLite 파일에 **모든 데이터가 저장**됩니다!

---

## 📊 저장되는 데이터

### **1. users 테이블 (회원 정보)**

| 컬럼 | 설명 | 예시 |
|------|------|------|
| id | 회원 ID | 1, 2, 3... |
| email | 이메일 | user@example.com |
| username | 사용자명 | testuser |
| nickname | 닉네임 | 테스트유저 |
| hashed_password | 비밀번호 (해싱됨) | $2b$12$... |
| oauth_provider | 소셜 로그인 종류 | discord, google, apple, null |
| oauth_id | OAuth ID | 1234567890 |
| credits | 크레딧 | 0, 100, 500... |
| follow_count | 팔로워 수 | 0, 5, 10... |
| created_at | 가입일 | 2026-01-26 15:30:00 |
| last_login | 최근 로그인 | 2026-01-26 16:00:00 |
| is_active | 활성화 여부 | true, false |
| is_admin | 관리자 여부 | true, false |

### **2. game_sessions 테이블 (게임 세션)**

| 컬럼 | 설명 | 예시 |
|------|------|------|
| id | 세션 DB ID | 1, 2, 3... |
| session_id | 세션 고유 ID | game_1234567890 |
| user_id | 회원 ID (FK) | 1, 2, null (비회원) |
| scenario_id | 시나리오 ID | scenario_001 |
| scenario_title | 시나리오 제목 | 어둠의 저택 |
| character_id | 캐릭터 ID | char_001 |
| character_name | 캐릭터 이름 | 탐정 홍길동 |
| character_state | 캐릭터 상태 (JSON) | {"hp": 50, "mp": 30...} |
| story_progress | 스토리 진행 (JSON) | {"flags": {...}} |
| flags | 플래그 (JSON) | {"door_opened": true} |
| combat_state | 전투 상태 (JSON) | {"in_combat": false} |
| location | 현재 위치 | 저택 1층 |
| turn | 턴 수 | 0, 5, 10... |
| created_at | 생성일 | 2026-01-26 15:30:00 |
| updated_at | 수정일 | 2026-01-26 16:00:00 |
| last_played | 최근 플레이 | 2026-01-26 16:00:00 |

---

## 🛠️ 데이터베이스 관리 방법

### **방법 1: Python 스크립트 (추천!)** 🌟

**실행:**
```bash
python view_database.py
```

**기능:**
- ✅ 회원 목록 조회
- ✅ 게임 세션 조회
- ✅ 통계 확인
- ✅ 회원 삭제

**실행 예시:**
```
================================================================================
🗄️ LiTR 데이터베이스 관리 도구
================================================================================

선택하세요:
  1. 회원 목록 보기
  2. 게임 세션 목록 보기
  3. 통계 보기
  4. 회원 삭제
  0. 종료

번호 입력: 1

================================================================================
👥 회원 목록
================================================================================

총 2명의 회원
--------------------------------------------------------------------------------

[회원 ID: 1]
  📧 이메일: user@example.com
  👤 사용자명: testuser
  ✏️ 닉네임: 테스트유저
  💰 크레딧: 0
  👥 팔로워: 0
  🔐 로그인 방식: 이메일/비밀번호
  📅 가입일: 2026-01-26 15:30:00
  🕐 최근 로그인: 2026-01-26 16:00:00
  ✅ 활성화: 예
```

---

### **방법 2: DB Browser for SQLite (GUI)** 🖱️

**다운로드:**
```
https://sqlitebrowser.org/dl/
```

**사용법:**

1. **DB Browser 설치**
   - Windows: `.exe` 다운로드 후 설치

2. **데이터베이스 열기**
   - `Open Database` 클릭
   - `litrpg.db` 선택

3. **데이터 확인**
   - `Browse Data` 탭
   - Table 선택: `users` 또는 `game_sessions`
   - 모든 데이터가 표 형태로 표시됨

4. **데이터 편집**
   - 셀 더블클릭으로 수정 가능
   - `Write Changes` 클릭하여 저장

5. **SQL 쿼리**
   - `Execute SQL` 탭
   - 직접 SQL 작성 가능
   ```sql
   SELECT * FROM users WHERE is_active = 1;
   SELECT * FROM game_sessions WHERE user_id = 1;
   ```

---

### **방법 3: Python 대화형 쉘**

```bash
python
```

```python
from database import SessionLocal
from models.user import User
from models.game_session import GameSession

# 세션 생성
db = SessionLocal()

# 모든 회원 조회
users = db.query(User).all()
for user in users:
    print(f"{user.id}: {user.username} ({user.email})")

# 특정 회원 조회
user = db.query(User).filter(User.username == "testuser").first()
print(f"회원: {user.nickname}, 크레딧: {user.credits}")

# 회원 수정
user.credits = 100
db.commit()

# 게임 세션 조회
sessions = db.query(GameSession).filter(GameSession.user_id == user.id).all()
print(f"{user.username}의 게임 세션: {len(sessions)}개")

# 세션 종료
db.close()
```

---

## 📋 자주 사용하는 관리 작업

### **1. 모든 회원 조회**

```bash
python view_database.py
# → 1번 선택
```

또는

```python
from database import SessionLocal
from models.user import User

db = SessionLocal()
users = db.query(User).all()
for user in users:
    print(f"{user.username}: {user.email}")
db.close()
```

### **2. 특정 회원의 게임 세션 조회**

```python
from database import SessionLocal
from models.user import User

db = SessionLocal()
user = db.query(User).filter(User.username == "testuser").first()

print(f"게임 세션 {len(user.game_sessions)}개:")
for session in user.game_sessions:
    print(f"  - {session.scenario_title}")

db.close()
```

### **3. 회원 크레딧 수정**

```python
from database import SessionLocal
from models.user import User

db = SessionLocal()
user = db.query(User).filter(User.username == "testuser").first()

user.credits = 500  # 크레딧 변경
db.commit()

print(f"✅ {user.username}의 크레딧: {user.credits}")
db.close()
```

### **4. 비활성화된 회원 조회**

```python
from database import SessionLocal
from models.user import User

db = SessionLocal()
inactive_users = db.query(User).filter(User.is_active == False).all()

print(f"비활성 회원: {len(inactive_users)}명")
for user in inactive_users:
    print(f"  - {user.username}")

db.close()
```

### **5. 게임 세션 삭제**

```python
from database import SessionLocal
from models.game_session import GameSession

db = SessionLocal()
session = db.query(GameSession).filter(
    GameSession.session_id == "game_1234567890"
).first()

if session:
    db.delete(session)
    db.commit()
    print("✅ 세션 삭제 완료")

db.close()
```

---

## 💾 백업 및 복원

### **백업 만들기**

**방법 1: 파일 복사**
```bash
copy litrpg.db litrpg_backup_20260126.db
```

**방법 2: Python 스크립트**
```python
import shutil
from datetime import datetime

backup_name = f"litrpg_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
shutil.copy("litrpg.db", backup_name)
print(f"✅ 백업 완료: {backup_name}")
```

### **복원하기**

```bash
copy litrpg_backup_20260126.db litrpg.db
```

---

## 🔒 데이터베이스 초기화

**주의: 모든 데이터가 삭제됩니다!**

```bash
python init_db.py
```

프롬프트에서 `y` 입력 시 기존 DB 삭제 후 새로 생성

---

## 📊 데이터베이스 마이그레이션

### **JSON → DB로 기존 세이브 가져오기**

```bash
python migrate_to_db.py
```

`saves/` 폴더의 모든 JSON 파일을 DB로 이동합니다.

---

## 🚀 프로덕션 환경

### **SQLite → PostgreSQL 전환 (추후)**

현재는 SQLite를 사용하지만, 나중에 PostgreSQL로 쉽게 전환 가능:

1. `requirements.txt`에 `psycopg2-binary` 추가
2. `database.py`의 `DATABASE_URL` 변경
3. 환경 변수로 관리

```python
# database.py
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./litrpg.db"  # 기본값
)

# 프로덕션 .env
DATABASE_URL=postgresql://user:pass@localhost/litrpg
```

---

## 📞 자주 묻는 질문

### **Q1: 데이터베이스 파일을 옮기면?**

A: `litrpg.db` 파일을 다른 곳으로 옮기면 안 됩니다. 
프로젝트 루트(`LiTR/`)에 있어야 합니다.

### **Q2: 데이터베이스가 커지면?**

A: SQLite는 약 140TB까지 지원하므로 걱정 없습니다.
수백만 개의 레코드도 문제없습니다.

### **Q3: 여러 사람이 동시에 접속하면?**

A: SQLite는 동시 쓰기가 제한적입니다. 
사용자가 많아지면 PostgreSQL로 전환하세요.

### **Q4: 데이터베이스가 손상되면?**

A: 정기적으로 백업하세요!
```bash
copy litrpg.db backup/litrpg_$(date +%Y%m%d).db
```

### **Q5: 관리자 계정 만들기?**

```python
from database import SessionLocal
from models.user import User

db = SessionLocal()
user = db.query(User).filter(User.username == "admin").first()
user.is_admin = True
db.commit()
db.close()
```

---

## 📌 요약

### **데이터베이스 위치**
```
c:\Users\lynlo\Downloads\01.26 LiTR\LiTR\litrpg.db
```

### **관리 방법**
1. ✅ **Python 스크립트**: `python view_database.py` (가장 쉬움!)
2. ✅ **DB Browser**: GUI 도구
3. ✅ **Python 쉘**: 고급 작업

### **저장되는 데이터**
- ✅ 회원 정보 (`users` 테이블)
- ✅ 게임 세션 (`game_sessions` 테이블)
- ✅ 캐릭터 상태, 인벤토리, 스토리 진행

### **백업**
```bash
copy litrpg.db litrpg_backup.db
```

---

**작성일**: 2026년 1월 26일  
**프로젝트**: LiTR - AI 기반 TRPG 플랫폼
