# 🔗 프론트엔드-백엔드 연동 가이드

**LiTR TRPG 플랫폼 통합 연동 완료!**

---

## ✅ **연동 완료 상태**

### **백엔드 복원 완료**
- ✅ 모든 라우터 복원
- ✅ 의존성 복원 (`requirements.txt`)
- ✅ 세션 API 추가

### **프론트엔드 파일**
- ✅ `LiTR.html` (메인 UI)
- ✅ `dice.js`, `teal.js` (3D 주사위)
- ✅ `libs/` (Three.js, Cannon.js)

---

## 📡 **API 연동 매핑**

### **프론트엔드 요구사항 → 백엔드 구현**

| 프론트엔드 API 요청 | 백엔드 라우터 | 파일 위치 | 상태 |
|-------------------|-------------|----------|------|
| `POST /api/session/create` | session.router | `routers/session.py` | ✅ |
| `POST /api/session/join` | session.router | `routers/session.py` | ✅ |
| `POST /api/session/message` | session.router | `routers/session.py` | ✅ |
| `GET /api/scenarios` | chat.router | `routers/chat.py` | ✅ |
| `GET /api/characters` | chat.router | `routers/chat.py` | ✅ |
| `GET /api/scenario/{id}` | chat.router | `routers/chat.py` | ✅ |
| `GET /api/character/{id}` | chat.router | `routers/chat.py` | ✅ |
| `POST /api/scenario` | chat.router | `routers/chat.py` | ✅ |
| `POST /api/character` | chat.router | `routers/chat.py` | ✅ |
| `POST /api/chat` | chat.router | `routers/chat.py` | ✅ |
| `POST /api/chat/continue` | chat.router | `routers/chat.py` | ✅ |
| `POST /api/voice/token` | voice.router | `routers/voice.py` | ✅ |
| `POST /api/pdf/convert-scenario` | pdf.router | `routers/pdf.py` | ✅ |

---

## 🚀 **실행 방법**

### **1. 백엔드 서버 시작**

```bash
# 프로젝트 디렉토리로 이동
cd "c:\Users\lynlo\Downloads\01.26 LiTR\LiTR"

# 가상환경 활성화 (있다면)
# venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 의존성 설치 (처음 한 번만)
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload
```

**예상 출력:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### **2. 프론트엔드 실행**

#### **방법 1: 직접 열기 (추천)**
```
파일 탐색기에서 LiTR.html 더블클릭
또는
브라우저 주소창에: file:///c:/Users/lynlo/Downloads/01.26%20LiTR/LiTR/LiTR.html
```

#### **방법 2: Live Server (VS Code)**
1. VS Code에서 `LiTR.html` 열기
2. 우클릭 → "Open with Live Server"

#### **방법 3: Python HTTP Server**
```bash
# 프로젝트 루트에서 실행
python -m http.server 3000

# 브라우저 열기
http://localhost:3000/LiTR.html
```

---

## 🔧 **환경 변수 설정**

### **.env 파일 필수 설정**

```env
# Claude API (필수)
ANTHROPIC_API_KEY=sk-ant-api03-실제-클로드-키

# JWT (필수)
JWT_SECRET_KEY=s7WBCel0iNBGdg-rWkfjGMvBIHuasLlinwvYFUd5KNk

# 데이터베이스
DATABASE_URL=sqlite:///./litrpg.db

# 선택 사항 (기능 사용 시 필요)
# OpenAI (이미지 생성)
# OPENAI_API_KEY=sk-proj-실제-오픈AI-키

# Agora (음성 채팅)
# AGORA_APP_ID=실제-App-ID
# AGORA_APP_CERTIFICATE=실제-Certificate

# Discord OAuth
# DISCORD_CLIENT_ID=1446523696107305995
# DISCORD_CLIENT_SECRET=실제-Secret
# DISCORD_REDIRECT_URI=http://localhost:8000/api/auth/discord/callback

# Google OAuth
# GOOGLE_CLIENT_ID=68570168053-f4v8svi47ts1p71fdua5srt7hmgoga0b.apps.googleusercontent.com
# GOOGLE_CLIENT_SECRET=실제-Secret
# GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback
```

---

## 🧪 **테스트**

### **1. 백엔드 API 테스트**

```bash
# 서버 상태 확인
curl http://localhost:8000

# Swagger UI 열기 (API 문서)
http://localhost:8000/docs

# ReDoc 열기 (대체 문서)
http://localhost:8000/redoc
```

### **2. 프론트엔드 기능 테스트**

**브라우저에서 `LiTR.html` 열고:**

1. **시나리오 불러오기 테스트**
   - 콘솔(F12) 확인: `GET http://localhost:8000/api/scenarios`
   - 성공: 시나리오 목록 표시
   - 실패: CORS 오류 또는 백엔드 미실행

2. **캐릭터 불러오기 테스트**
   - 콘솔 확인: `GET http://localhost:8000/api/characters`
   - 성공: 캐릭터 목록 표시

3. **세션 생성 테스트**
   - 시나리오 선택 후 "게임 시작"
   - 콘솔 확인: `POST http://localhost:8000/api/session/create`
   - 성공: 6자리 세션 코드 생성

4. **AI 채팅 테스트**
   - 게임 중 메시지 입력
   - 콘솔 확인: `POST http://localhost:8000/api/chat`
   - 성공: AI GM 응답 받기

### **3. 통합 테스트 스크립트**

```bash
# 백엔드 테스트 (서버 실행 상태에서)
python test_auth_api.py
python test_gameplay_api.py
python test_advanced_features.py
```

---

## 🐛 **문제 해결**

### **❌ "CORS policy" 오류**

**증상:**
```
Access to fetch at 'http://localhost:8000/api/...' from origin 'file://' 
has been blocked by CORS policy
```

**해결:**
1. 백엔드 서버가 실행 중인지 확인
2. `main.py`에 CORS 설정 확인 (이미 설정됨)
3. `file://` 대신 `http://localhost:3000`로 프론트엔드 열기

### **❌ "502 Bad Gateway" 또는 연결 거부**

**원인:** 백엔드 서버가 실행되지 않음

**해결:**
```bash
uvicorn main:app --reload
```

### **❌ "Module not found" 오류**

**원인:** 의존성 미설치

**해결:**
```bash
pip install -r requirements.txt
```

### **❌ ".env 파일을 찾을 수 없음"**

**해결:**
1. 프로젝트 루트에 `.env` 파일 생성
2. 최소한 `ANTHROPIC_API_KEY`와 `JWT_SECRET_KEY` 입력

### **❌ "Scenarios not loading"**

**해결:**
1. `scenarios/` 폴더에 JSON 파일 있는지 확인
2. 백엔드 콘솔에서 오류 메시지 확인
3. Swagger UI에서 직접 API 테스트

---

## 📂 **프로젝트 구조**

```
LiTR/
├── main.py                    # FastAPI 앱 (백엔드 진입점)
├── requirements.txt           # Python 의존성
├── .env                       # 환경 변수 (중요! Git에 커밋 금지)
├── .gitignore                # Git 제외 파일
│
├── routers/                   # API 라우터
│   ├── auth.py               # 인증 (JWT, OAuth)
│   ├── session.py            # 세션 관리 ⭐ 프론트엔드 연동
│   ├── chat.py               # AI 채팅, 시나리오/캐릭터 API ⭐
│   ├── voice.py              # 음성 채팅
│   ├── pdf.py                # PDF 변환
│   ├── dice.py               # 주사위
│   ├── game.py               # 게임 상태 (JSON)
│   ├── game_db.py            # 게임 상태 (DB)
│   ├── gameplay.py           # 통합 플레이
│   ├── image_gen.py          # 이미지 생성
│   └── multiplayer.py        # 멀티플레이
│
├── models/                    # 데이터베이스 모델
│   ├── user.py               # 사용자 모델
│   └── game_session.py       # 게임 세션 모델
│
├── utils/                     # 유틸리티
│   ├── auth.py               # JWT 토큰
│   └── oauth.py              # OAuth 헬퍼
│
├── scenarios/                 # 시나리오 파일
│   ├── horror_school.json
│   ├── noir_detective.json
│   └── action_skygarden.json
│
├── characters/                # 캐릭터 파일
│   ├── detective_k.json
│   └── mercenary_arten.json
│
├── LiTR.html                 # 프론트엔드 메인 ⭐
├── dice.js                   # 3D 주사위 라이브러리
├── teal.js                   # 유틸리티 라이브러리
├── libs/                     # 외부 라이브러리
│   ├── three.min.js          # 3D 엔진
│   └── cannon.min.js         # 물리 엔진
│
├── saves/                    # 게임 저장 파일 (JSON)
├── images/                   # 생성된 이미지
├── litrpg.db                 # SQLite 데이터베이스
└── sessions_data.json        # 세션 데이터
```

---

## 🎮 **실행 흐름**

### **1. 사용자 접속**
```
사용자가 LiTR.html 열기
  ↓
프론트엔드 JavaScript 로드
  ↓
API_BASE_URL = 'http://localhost:8000' 설정
```

### **2. 시나리오 불러오기**
```
프론트엔드: GET /api/scenarios
  ↓
백엔드 (chat.py): scenarios/ 폴더 읽기
  ↓
JSON 파일 목록 반환
  ↓
프론트엔드: 시나리오 카드 렌더링
```

### **3. 게임 시작**
```
사용자: 시나리오 + 캐릭터 선택
  ↓
프론트엔드: POST /api/session/create
  ↓
백엔드 (session.py): 6자리 코드 생성
  ↓
세션 데이터 저장 (sessions_data.json)
  ↓
프론트엔드: 게임 화면으로 전환
```

### **4. AI 상호작용**
```
사용자: 메시지 입력
  ↓
프론트엔드: POST /api/chat
  ↓
백엔드 (chat.py): Anthropic API 호출
  ↓
Claude Sonnet 4 응답 생성
  ↓
프론트엔드: AI GM 응답 표시
  ↓
프론트엔드: POST /api/session/message
  ↓
백엔드 (session.py): 메시지 히스토리 저장
```

---

## 🔐 **보안 사항**

### **필수 체크리스트**

- ✅ `.env` 파일 Git 제외 (`.gitignore`에 포함)
- ✅ API 키 노출 금지
- ✅ CORS 설정 (프로덕션에서는 특정 도메인만 허용)
- ⚠️ JWT Secret 강력하게 설정
- ⚠️ OAuth Redirect URI 검증
- ⚠️ HTTPS 사용 (프로덕션)

---

## 📊 **모니터링**

### **로그 확인**

```bash
# 백엔드 로그 (터미널에 실시간 표시)
uvicorn main:app --reload --log-level info

# 특정 로그만 확인
uvicorn main:app --reload --log-level debug
```

### **데이터베이스 확인**

```bash
# SQLite DB 보기
python view_database.py

# 세션 데이터 확인
cat sessions_data.json  # Mac/Linux
type sessions_data.json  # Windows
```

---

## 🚀 **다음 단계**

### **개발 환경 (현재)**
- ✅ 백엔드: `http://localhost:8000`
- ✅ 프론트엔드: `file://` 또는 `http://localhost:3000`

### **프로덕션 배포**

1. **프론트엔드 빌드**
   - 프론트엔드 프레임워크 사용 시 빌드
   - 정적 파일 최적화

2. **백엔드 배포**
   - Docker 컨테이너화
   - Railway, Render, AWS 등

3. **도메인 연결**
   - HTTPS 적용
   - CORS origin 수정
   - OAuth Redirect URI 업데이트

---

## 📚 **추가 문서**

- `SETUP_API_KEYS.md`: OpenAI & Agora 설정
- `SOCIAL_LOGIN_SETUP.md`: Discord, Google, Apple 로그인
- `ADVANCED_FEATURES_GUIDE.md`: 고급 기능 (이미지, 멀티, 음성)
- `DATABASE_MANAGEMENT_GUIDE.md`: 데이터베이스 관리
- `AUTH_API_GUIDE.md`: 인증 API
- `GAMEPLAY_API_GUIDE.md`: 통합 게임플레이 API

---

## ✅ **체크리스트**

### **백엔드 준비**
- [ ] Python 3.10+ 설치
- [ ] 의존성 설치 (`pip install -r requirements.txt`)
- [ ] `.env` 파일 생성
- [ ] `ANTHROPIC_API_KEY` 설정
- [ ] `JWT_SECRET_KEY` 생성
- [ ] 서버 실행 (`uvicorn main:app --reload`)
- [ ] Swagger UI 확인 (`http://localhost:8000/docs`)

### **프론트엔드 준비**
- [ ] `LiTR.html` 파일 확인
- [ ] 브라우저에서 열기
- [ ] 개발자 도구 (F12) 열기
- [ ] Network 탭에서 API 호출 확인

### **통합 테스트**
- [ ] 시나리오 목록 불러오기
- [ ] 캐릭터 목록 불러오기
- [ ] 세션 생성
- [ ] AI 채팅 테스트
- [ ] 주사위 굴리기 (3D 주사위)
- [ ] 음성 채팅 (선택)

---

## 🎉 **완료!**

**모든 프론트엔드-백엔드 연동이 완료되었습니다!**

문제가 발생하면:
1. 백엔드 콘솔 로그 확인
2. 프론트엔드 브라우저 콘솔 (F12) 확인
3. Swagger UI에서 API 직접 테스트
4. 이 문서의 "문제 해결" 섹션 참고

**Happy Gaming!** 🎲🎮
