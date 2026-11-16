# 🎮 LiTR - TRPG Game Backend Server

FastAPI 기반 TRPG 게임 백엔드 서버 (Powered by Claude Sonnet 4)

---

## ✨ 주요 기능

- 🤖 **Claude Sonnet 4** - 숙련된 TRPG GM 역할 수행
- ⚡ **FastAPI** - 빠르고 안정적인 백엔드
- 🎭 **실시간 대화** - 자연스러운 TRPG 세션 진행
- 💾 **대화 히스토리** - 컨텍스트 유지
- 🌐 **CORS 지원** - 프론트엔드 연동 완벽 지원

---

## 🚀 빠른 시작

### 1️⃣ 의존성 설치

```bash
pip install -r requirements.txt
```

### 2️⃣ 환경변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 Anthropic API 키를 입력하세요:

**`.env` 파일 내용:**
```env
ANTHROPIC_API_KEY=sk-ant-api03-your_api_key_here
```

> 💡 **API 키 발급**: https://console.anthropic.com/ → "API Keys" → "Create Key"

### 3️⃣ 서버 실행

```bash
uvicorn main:app --reload
```

서버 실행 확인:
```
INFO: Uvicorn running on http://127.0.0.1:8000
```

### 4️⃣ 프론트엔드 실행

- `LiTR.html` 파일을 브라우저로 열기
- 또는 `test_api.html`로 API 테스트

---

## 📡 API 엔드포인트

### 1. 헬스 체크
```http
GET /
```

**응답:**
```json
{
  "message": "Hello TRPG"
}
```

### 2. TRPG GM 채팅
```http
POST /api/chat
```

**요청:**
```json
{
  "message": "던전에 들어갔습니다. 무엇이 보이나요?",
  "history": []
}
```

**응답:**
```json
{
  "response": "당신은 어두운 던전에 발을 들여놓습니다...",
  "usage": {
    "input_tokens": 45,
    "output_tokens": 120
  }
}
```

### 3. API 상태 확인
```http
GET /api/health
```

**응답:**
```json
{
  "status": "healthy",
  "anthropic_api_key_set": true,
  "model": "Claude Sonnet 4"
}
```

---

## 📚 API 문서

서버 실행 후 자동 생성된 문서를 확인할 수 있습니다:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🛠️ 기술 스택

| 분류 | 기술 |
|------|------|
| 언어 | Python 3.10+ |
| 프레임워크 | FastAPI |
| AI 모델 | Claude Sonnet 4 (Anthropic) |
| 환경변수 | python-dotenv |
| 프론트엔드 | HTML/JavaScript |

---

## 📁 프로젝트 구조

```
LiTR/
├── main.py                 # FastAPI 앱 진입점
├── routers/
│   └── chat.py            # TRPG GM 채팅 API
├── requirements.txt       # Python 패키지
├── .env                   # API 키 설정 (직접 생성)
├── .gitignore            # Git 제외 파일
├── README.md             # 이 문서
├── LiTR.html             # 메인 게임 UI
├── LiTR_SUB.html         # 서브 페이지
└── test_api.html         # API 테스트 페이지
```

---

## 💰 비용 안내

### Claude Sonnet 4 가격

| 항목 | 가격 |
|------|------|
| 입력 토큰 | $3 / 100만 토큰 |
| 출력 토큰 | $15 / 100만 토큰 |

### 예상 사용량

| 시나리오 | 예상 비용 |
|----------|----------|
| TRPG 한 세션 (30분) | 약 $0.04 |
| 하루 10세션 | 약 $0.40 |
| 월간 (300세션) | 약 $12 |

**💡 팁:** $5 크레딧으로 약 125세션 플레이 가능!

---

## ⚙️ 설정

### CORS 설정

프로덕션 환경에서는 `main.py`의 CORS 설정을 수정하세요:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # 특정 도메인만
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 시스템 프롬프트 커스터마이징

`routers/chat.py`에서 GM 스타일을 변경할 수 있습니다:

```python
SYSTEM_PROMPT = "당신은 TRPG 게임의 숙련된 GM입니다."
```

---

## 🧪 테스트

### 방법 1: test_api.html

1. `test_api.html` 파일을 브라우저로 열기
2. 자동으로 서버 상태 확인
3. "메시지 전송" 버튼으로 테스트

### 방법 2: Swagger UI

1. http://localhost:8000/docs 접속
2. `POST /api/chat` 엔드포인트 선택
3. "Try it out" 클릭 후 테스트

### 방법 3: curl

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "던전에 들어갔습니다",
    "history": []
  }'
```

---

## 🔒 보안

### 중요!

- ❌ `.env` 파일을 Git에 커밋하지 마세요
- ❌ API 키를 공개하지 마세요
- ✅ `.gitignore`에 `.env` 포함 (이미 설정됨)
- ✅ 프로덕션에서는 CORS 제한 설정

---

## 🐛 문제 해결

### API 키 오류

**증상:** "ANTHROPIC_API_KEY가 설정되지 않았습니다"

**해결:**
1. `.env` 파일이 프로젝트 루트에 있는지 확인
2. API 키가 올바르게 입력되었는지 확인
3. 서버 재시작

### 서버 연결 오류

**증상:** "백엔드 서버가 실행 중인지 확인하세요"

**해결:**
1. 서버가 실행 중인지 확인: `uvicorn main:app --reload`
2. 포트 8000이 사용 중인지 확인
3. 방화벽 설정 확인

### CORS 오류

**증상:** "CORS policy blocked"

**해결:**
1. 브라우저 캐시 삭제 (Ctrl + Shift + R)
2. `main.py`의 CORS 설정 확인
3. 브라우저를 완전히 재시작

---

## 📝 라이센스

이 프로젝트는 교육 및 개인 프로젝트 용도로 제작되었습니다.

---

## 🙏 크레딧

- **AI 모델**: Claude Sonnet 4 by Anthropic
- **프레임워크**: FastAPI
- **프론트엔드**: Vanilla HTML/CSS/JavaScript

---

## 📞 지원

문제가 발생하거나 질문이 있으시면:

- **Anthropic 문서**: https://docs.anthropic.com/
- **FastAPI 문서**: https://fastapi.tiangolo.com/
- **GitHub Issues**: 프로젝트 이슈 탭

---

**즐거운 TRPG 게임 되세요!** 🎲✨
