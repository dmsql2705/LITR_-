# Railway 배포 가이드

LiTR TRPG 플랫폼을 Railway에 배포하는 전체 가이드입니다.

---

## 📋 목차
1. [사전 준비](#사전-준비)
2. [백엔드 배포](#백엔드-배포)
3. [프론트엔드 배포](#프론트엔드-배포)
4. [환경 변수 설정](#환경-변수-설정)
5. [배포 확인](#배포-확인)
6. [트러블슈팅](#트러블슈팅)

---

## 🔧 사전 준비

### 1. 필수 계정 생성
- [Railway](https://railway.app/) 계정
- [Supabase](https://supabase.com/) 프로젝트
- [Anthropic](https://console.anthropic.com/) API 키
- [OpenAI](https://platform.openai.com/) API 키 (DALL-E 사용 시)

### 2. Railway CLI 설치

```bash
# npm을 통한 설치
npm install -g @railway/cli

# 로그인
railway login
```

### 3. 자격증명 로테이션

⚠️ **중요**: `.env` 파일에 노출된 모든 자격증명을 로테이션하세요!

1. **Supabase 데이터베이스 비밀번호**
   - Supabase Dashboard → Settings → Database → Reset password

2. **Anthropic API 키**
   - [Anthropic Console](https://console.anthropic.com/) → API Keys → Create new

3. **JWT 시크릿 키**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

4. **OAuth 시크릿**
   - Discord: [Discord Developer Portal](https://discord.com/developers/applications)
   - Google: [Google Cloud Console](https://console.cloud.google.com/)

---

## 🚀 백엔드 배포

### 1. 프로젝트 생성

```bash
cd C:\LiTR-master\01.31LiTR-master
railway init
railway link
```

### 2. 환경 변수 설정

Railway 대시보드 → 프로젝트 → Variables 탭에서 설정:

```bash
# 데이터베이스 (Supabase)
DATABASE_URL=postgresql://postgres:<NEW_PASSWORD>@db.xxxxx.supabase.co:5432/postgres

# API 키
ANTHROPIC_API_KEY=sk-ant-api03-<NEW_KEY>
OPENAI_API_KEY=sk-proj-<NEW_KEY>

# JWT 인증
JWT_SECRET_KEY=<NEW_32_CHAR_SECRET>
JWT_ALGORITHM=HS256

# Discord OAuth
DISCORD_CLIENT_ID=<YOUR_CLIENT_ID>
DISCORD_CLIENT_SECRET=<NEW_SECRET>
DISCORD_REDIRECT_URI=https://your-backend.railway.app/api/auth/discord/callback

# Google OAuth
GOOGLE_CLIENT_ID=<YOUR_CLIENT_ID>
GOOGLE_CLIENT_SECRET=<NEW_SECRET>
GOOGLE_REDIRECT_URI=https://your-backend.railway.app/api/auth/google/callback

# Agora (음성 채팅)
AGORA_APP_ID=<YOUR_APP_ID>
AGORA_APP_CERTIFICATE=<YOUR_CERTIFICATE>

# 프론트엔드 URL (CORS)
FRONTEND_URL=https://your-frontend.railway.app

# Python 버전
PYTHON_VERSION=3.11.8
```

### 3. 배포 실행

```bash
railway up
```

### 4. 도메인 생성

```bash
railway domain
```

또는 Railway 대시보드에서 Settings → Generate Domain

---

## 🎨 프론트엔드 배포

### 1. 프로젝트 생성

```bash
cd C:\LiTR-master\01.31LiTR-master\litr-frontend
railway init
railway link
```

### 2. 환경 변수 설정

Railway 대시보드 → 프로젝트 → Variables 탭:

```bash
# 백엔드 API URL (백엔드 배포 후 생성된 URL)
NEXT_PUBLIC_API_URL=https://your-backend.railway.app

# Socket.IO URL (백엔드와 동일)
NEXT_PUBLIC_SOCKET_URL=https://your-backend.railway.app

# Node.js 환경
NODE_ENV=production

# Supabase (선택)
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<YOUR_ANON_KEY>
```

### 3. 배포 실행

```bash
railway up
```

### 4. 도메인 생성

```bash
railway domain
```

---

## 🔗 서비스 연결

### 1. CORS 업데이트

백엔드 `main.py`에서 CORS 설정 업데이트:

```python
# 프론트엔드 URL로 변경
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],  # "*" 대신 실제 도메인 사용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. OAuth Redirect URI 업데이트

각 OAuth 프로바이더 콘솔에서 Redirect URI 추가:

**Discord**:
- `https://your-backend.railway.app/api/auth/discord/callback`

**Google**:
- `https://your-backend.railway.app/api/auth/google/callback`

---

## ✅ 배포 확인

### 1. 백엔드 Health Check

```bash
curl https://your-backend.railway.app/health
```

**예상 응답**:
```json
{
  "status": "healthy",
  "service": "LiTR TRPG Backend",
  "version": "1.0.0",
  "timestamp": "2026-02-02T12:00:00.000000"
}
```

### 2. API 문서 확인

브라우저에서 접속:
- Swagger UI: `https://your-backend.railway.app/docs`
- ReDoc: `https://your-backend.railway.app/redoc`

### 3. 프론트엔드 접속

브라우저에서 프론트엔드 URL 접속:
- `https://your-frontend.railway.app`

### 4. 기능 테스트

1. **회원가입**: 새 계정 생성
2. **로그인**: JWT 토큰 발급 확인
3. **캐릭터 생성**: 데이터베이스 저장 확인
4. **게임 시작**: AI GM 응답 확인

---

## 🐛 트러블슈팅

### 문제 1: "Failed to connect to database"

**원인**: DATABASE_URL이 잘못되었거나 Supabase 접근 권한 없음

**해결**:
1. Supabase 대시보드에서 Connection String 확인
2. Railway 환경 변수에서 DATABASE_URL 업데이트
3. 비밀번호에 특수문자가 있다면 URL 인코딩 필요

```python
# 예: 비밀번호에 @가 있는 경우
password = "pass@word"
encoded = urllib.parse.quote(password)  # "pass%40word"
```

### 문제 2: "CORS policy error"

**원인**: 프론트엔드 도메인이 백엔드 CORS 설정에 없음

**해결**:
1. 백엔드 환경 변수 `FRONTEND_URL` 확인
2. `main.py`의 CORS 설정 확인
3. Railway 재배포: `railway up`

### 문제 3: "Module not found" 에러

**원인**: 의존성이 설치되지 않음

**해결**:

**백엔드**:
```bash
# requirements.txt 확인
pip install -r requirements.txt
```

**프론트엔드**:
```bash
# package.json 확인
npm install
```

### 문제 4: Health check 실패

**원인**: 앱이 시작되지 않거나 /health 엔드포인트 없음

**해결**:
1. Railway 로그 확인: 대시보드 → Deployments → View logs
2. `main.py`에 `/health` 엔드포인트 있는지 확인
3. PORT 환경 변수 확인 (Railway가 자동 설정)

### 문제 5: 빌드 실패

**백엔드**:
- Python 버전 확인: `runtime.txt`에 `python-3.11.8`
- `requirements.txt` 형식 확인

**프론트엔드**:
- Node.js 버전 확인: `package.json`의 engines 설정
- 빌드 명령어 확인: `npm run build`

---

## 📊 모니터링

### Railway 대시보드

**확인 사항**:
- CPU/메모리 사용량
- 배포 로그
- 에러 로그
- 요청 지표

### 로그 확인

```bash
# Railway CLI로 실시간 로그
railway logs

# 특정 서비스 로그
railway logs --service backend
```

---

## 🔄 업데이트 배포

### 백엔드 업데이트

```bash
cd C:\LiTR-master\01.31LiTR-master
git add .
git commit -m "Update backend"
railway up
```

### 프론트엔드 업데이트

```bash
cd C:\LiTR-master\01.31LiTR-master\litr-frontend
git add .
git commit -m "Update frontend"
railway up
```

### 자동 배포 (GitHub 연동)

Railway 대시보드 → Settings → Deploy Triggers:
- GitHub 저장소 연결
- 브랜치 선택 (예: `main`)
- Push 시 자동 배포

---

## 📝 배포 후 체크리스트

백엔드:
- [ ] Health check 응답 확인
- [ ] API 문서 접근 가능 (/docs)
- [ ] 데이터베이스 연결 확인
- [ ] JWT 인증 작동 확인
- [ ] Rate limiting 작동 확인
- [ ] CORS 설정 확인

프론트엔드:
- [ ] 홈페이지 로드 확인
- [ ] 로그인/회원가입 확인
- [ ] API 통신 확인
- [ ] 이미지 로딩 확인
- [ ] 에러 처리 확인

보안:
- [ ] HTTPS 강제 확인
- [ ] 환경 변수 보안 확인
- [ ] RLS 정책 활성화 확인
- [ ] API 키 로테이션 완료

---

## 🆘 도움 받기

- Railway 문서: https://docs.railway.app/
- Supabase 문서: https://supabase.com/docs
- FastAPI 문서: https://fastapi.tiangolo.com/
- Next.js 문서: https://nextjs.org/docs

---

**마지막 업데이트**: 2026-02-02
