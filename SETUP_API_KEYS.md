# 🔑 API 키 설정 완벽 가이드

**OpenAI와 Agora API 키를 설정하는 방법**

---

## 📋 **목차**

1. [OpenAI API 키 설정](#1-openai-api-키-설정)
2. [Agora 계정 설정](#2-agora-계정-설정)
3. [.env 파일 설정](#3-env-파일-설정)
4. [설정 확인](#4-설정-확인)
5. [문제 해결](#5-문제-해결)

---

## 1. OpenAI API 키 설정

### **개요**
- **용도**: DALL-E 3 이미지 생성
- **비용**: $0.040/장 (Standard), $0.080/장 (HD)
- **필수 여부**: 선택 (이미지 생성 기능 사용 시 필요)

### **Step 1: 계정 생성**

1. **OpenAI Platform 접속**
   ```
   https://platform.openai.com/
   ```

2. **Sign Up 클릭**
   - 우측 상단 "Sign up" 버튼
   - 이메일 또는 Google/Microsoft 계정으로 가입

3. **이메일 인증**
   - 받은 이메일에서 "Verify email address" 클릭

### **Step 2: 결제 정보 등록**

⚠️ **중요**: API 사용을 위해서는 결제 정보 등록이 필수입니다.

1. **Billing 페이지 이동**
   ```
   https://platform.openai.com/account/billing/overview
   ```
   - 좌측 메뉴 "Settings" → "Billing"

2. **결제 수단 추가**
   - "Set up paid account" 클릭
   - 신용카드 정보 입력
   - 국내 카드 사용 가능 (Visa, Mastercard)

3. **크레딧 충전**
   - 최소 $5 권장
   - "Add to credit balance" 클릭
   - 금액 입력 ($5, $10, $20 등)

### **Step 3: API 키 생성**

1. **API Keys 페이지 이동**
   ```
   https://platform.openai.com/api-keys
   ```
   - 좌측 메뉴 "API keys"

2. **새 키 생성**
   - "Create new secret key" 버튼 클릭
   - 키 이름 입력 (예: "LiTR-Backend-Images")
   - "Create secret key" 클릭

3. **키 복사 및 저장**
   - ⚠️ **매우 중요**: 생성된 키는 한 번만 표시됩니다!
   - "Copy" 버튼 클릭
   - 안전한 곳에 저장 (메모장, 비밀번호 관리자 등)
   - 키 형식: `sk-proj-...` 또는 `sk-...`

### **Step 4: 사용량 제한 설정 (권장)**

1. **Usage limits 설정**
   ```
   https://platform.openai.com/account/limits
   ```
   - "Settings" → "Limits"

2. **월 사용 한도 설정**
   - "Set monthly budget" 클릭
   - 예: $10 (이미지 250장 생성 가능)
   - 초과 시 자동 중지

---

## 2. Agora 계정 설정

### **개요**
- **용도**: 실시간 음성 채팅
- **비용**: 무료 10,000분/월, 이후 $0.99/1,000분
- **필수 여부**: 선택 (음성 채팅 기능 사용 시 필요)

### **Step 1: 계정 생성**

1. **Agora 웹사이트 접속**
   ```
   https://www.agora.io/
   ```

2. **Sign Up 클릭**
   - 우측 상단 "Sign Up" 또는 "Get Started" 버튼
   - 이메일로 가입 (추천)
   - 또는 GitHub 계정 연동

3. **정보 입력**
   - Email: 이메일 주소
   - Password: 비밀번호 (8자 이상)
   - Country: South Korea 선택
   - "Sign Up" 클릭

4. **이메일 인증**
   - 받은 이메일에서 "Verify Email" 클릭

### **Step 2: Console 접속**

1. **로그인**
   ```
   https://console.agora.io/
   ```

2. **처음 로그인 시**
   - 간단한 설문 조사 (선택사항)
   - Use Case: "Social" 선택
   - "Continue" 클릭

### **Step 3: 프로젝트 생성**

1. **Project Management 이동**
   - 좌측 메뉴에서 "Project Management" 클릭
   - 또는 직접 접속: https://console.agora.io/projects

2. **새 프로젝트 생성**
   - 우측 상단 "Create" 버튼 클릭
   - 프로젝트 정보 입력:
     - **Project Name**: `LiTR-Voice` (또는 원하는 이름)
     - **Use Case**: `Social` 또는 `Live Broadcasting` 선택
     - **Authentication mechanism**: `App ID + Token` 선택 (보안)
   - "Submit" 클릭

3. **프로젝트 확인**
   - 생성된 프로젝트가 목록에 표시됨

### **Step 4: App ID & Certificate 확인**

1. **프로젝트 상세 보기**
   - 생성된 프로젝트의 이름 클릭
   - 또는 "View" 버튼 클릭

2. **App ID 복사**
   - "Project Information" 섹션
   - **App ID** 옆의 복사 아이콘 클릭
   - 예시: `12345678901234567890123456789012` (32자리 영숫자)

3. **Primary Certificate 확인**
   - **Primary Certificate** 옆의 "눈" 아이콘 클릭
   - Certificate가 표시됨
   - 복사 아이콘 클릭하여 복사
   - 예시: `abcdef1234567890abcdef1234567890` (32자리 영숫자)

### **Step 5: 무료 사용량 확인**

1. **Usage 페이지 이동**
   ```
   https://console.agora.io/usage
   ```
   - 좌측 메뉴 "Usage"

2. **무료 한도 확인**
   - **Free-tier**: 10,000분/월
   - 초과 시 자동 과금 (사전에 결제 정보 등록 필요)

---

## 3. .env 파일 설정

### **Step 1: .env 파일 생성**

1. **프로젝트 루트 디렉토리로 이동**
   ```bash
   cd c:\Users\lynlo\Downloads\01.26 LiTR\LiTR
   ```

2. **.env 파일 생성**
   - Windows: 메모장으로 `.env` 파일 생성
   - 또는 VS Code에서 새 파일 생성

### **Step 2: 환경 변수 입력**

**.env 파일 내용:**

```env
# ============================================
# LiTR 백엔드 환경 변수
# ============================================

# ============================================
# Claude API (필수)
# ============================================
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# ============================================
# JWT 인증 (필수)
# ============================================
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production-12345

# ============================================
# 데이터베이스 (선택, 기본값: SQLite)
# ============================================
DATABASE_URL=sqlite:///./litrpg.db

# ============================================
# OpenAI API - 이미지 생성 (선택)
# ============================================
# 여기에 OpenAI API 키 입력!
OPENAI_API_KEY=sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# ============================================
# Agora RTC - 음성 채팅 (선택)
# ============================================
# 여기에 Agora App ID 입력!
AGORA_APP_ID=12345678901234567890123456789012

# 여기에 Agora Certificate 입력!
AGORA_APP_CERTIFICATE=abcdef1234567890abcdef1234567890

# ============================================
# 소셜 로그인 (선택)
# ============================================
# Discord OAuth
DISCORD_CLIENT_ID=your-discord-client-id
DISCORD_CLIENT_SECRET=your-discord-client-secret
DISCORD_REDIRECT_URI=http://localhost:8000/api/auth/discord/callback

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback

# Apple Sign in with Apple
APPLE_CLIENT_ID=your-apple-services-id
APPLE_TEAM_ID=your-apple-team-id
APPLE_KEY_ID=your-apple-key-id
APPLE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\nYour Apple Private Key Here\n-----END PRIVATE KEY-----
APPLE_REDIRECT_URI=http://localhost:8000/api/auth/apple/callback
```

### **Step 3: 실제 키 입력**

**예시 (가상 값):**

```env
# OpenAI
OPENAI_API_KEY=sk-proj-1234567890abcdefghijklmnopqrstuvwxyz1234567890

# Agora
AGORA_APP_ID=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
AGORA_APP_CERTIFICATE=9876543210zyxwvutsrqponmlkjihgfe
```

### **Step 4: 파일 저장**

1. **.env 파일 저장**
   - `Ctrl + S` (Windows)
   - 파일 위치: `c:\Users\lynlo\Downloads\01.26 LiTR\LiTR\.env`

2. **보안 확인**
   - ⚠️ `.env` 파일은 절대 Git에 커밋하지 마세요!
   - `.gitignore`에 `.env`가 포함되어 있는지 확인

---

## 4. 설정 확인

### **Step 1: 서버 재시작**

```bash
# 기존 서버 중지 (Ctrl + C)

# 서버 재시작
uvicorn main:app --reload
```

### **Step 2: 자동 테스트 실행**

```bash
# 새 터미널 열기

# 테스트 실행
python test_advanced_features.py
```

**예상 출력:**

```
================================================================================
🚀 고급 기능 테스트 시작
================================================================================

💚 [테스트 0] 서버 상태 확인
✅ 서버 정상 작동 중

🎨 [테스트 1] 이미지 스타일 조회
✅ 사용 가능한 스타일: 6개

🖼️ [테스트 2] 이미지 생성
✅ 이미지 생성 성공!
   생성 시간: 12.34초

👥 [테스트 3] 멀티플레이 통계
✅ 통계 조회 성공!

🎤 [테스트 4] 음성 채팅 설정
✅ Agora 설정 완료!

🎤 [테스트 5] 음성 토큰 생성
✅ 토큰 생성 성공!
```

### **Step 3: Swagger UI로 확인**

```bash
# 브라우저에서 열기
http://localhost:8000/docs
```

**이미지 생성 테스트:**
1. "image" 섹션 펼치기
2. "POST /api/image/generate" 클릭
3. "Try it out" 클릭
4. Request body 입력:
   ```json
   {
     "prompt": "a fantasy castle",
     "style": "fantasy",
     "size": "1024x1024",
     "quality": "standard"
   }
   ```
5. "Execute" 클릭
6. 응답 확인 (약 20초 소요)

**음성 채팅 테스트:**
1. "voice" 섹션 펼치기
2. "GET /api/voice/config" 클릭
3. "Try it out" → "Execute"
4. 응답에서 `"agora_configured": true` 확인

---

## 5. 문제 해결

### **OpenAI 관련**

#### ❌ "OPENAI_API_KEY가 설정되지 않았습니다"

**원인:** API 키가 .env 파일에 없거나 잘못됨

**해결:**
1. `.env` 파일 확인
2. `OPENAI_API_KEY=sk-proj-...` 형식 확인
3. 키 앞뒤 공백 제거
4. 서버 재시작

#### ❌ "Incorrect API key provided"

**원인:** 잘못된 API 키

**해결:**
1. OpenAI Platform에서 키 재확인
2. 새 키 생성하여 교체
3. 키 전체가 복사되었는지 확인

#### ❌ "You exceeded your current quota"

**원인:** 크레딧 부족

**해결:**
1. https://platform.openai.com/account/billing 접속
2. "Add to credit balance" 클릭
3. $5-$10 충전

### **Agora 관련**

#### ❌ "Agora가 설정되지 않았습니다"

**원인:** App ID 또는 Certificate가 없음

**해결:**
1. `.env` 파일 확인
2. `AGORA_APP_ID`와 `AGORA_APP_CERTIFICATE` 확인
3. 32자리 영숫자인지 확인
4. 서버 재시작

#### ❌ "Invalid App ID"

**원인:** 잘못된 App ID

**해결:**
1. Agora Console에서 App ID 재확인
2. 프로젝트가 활성화되어 있는지 확인
3. 올바른 프로젝트의 App ID인지 확인

#### ❌ Token 생성은 되지만 음성이 안 들림

**원인:** 프론트엔드 Agora SDK 미구현

**참고:**
- 현재는 토큰 생성 API만 구현됨
- 실제 음성 통화는 프론트엔드에서 Agora SDK 연동 필요
- 가이드: `ADVANCED_FEATURES_GUIDE.md` 참고

### **일반 문제**

#### ❌ .env 파일을 찾을 수 없음

**해결:**
1. 파일이 프로젝트 루트에 있는지 확인
2. 파일 이름이 정확히 `.env`인지 확인 (`.env.txt` 아님)
3. 숨김 파일 표시 설정 확인

#### ❌ 서버가 .env를 읽지 않음

**해결:**
1. 서버 완전히 종료 후 재시작
2. `python-dotenv` 패키지 설치 확인:
   ```bash
   pip install python-dotenv
   ```

---

## 📊 **비용 요약**

### **OpenAI (DALL-E 3)**

| 품질 | 크기 | 비용/장 | $10으로 생성 가능 |
|------|------|---------|-------------------|
| Standard | 1024x1024 | $0.040 | 250장 |
| Standard | 1024x1792 | $0.080 | 125장 |
| HD | 1024x1024 | $0.080 | 125장 |
| HD | 1024x1792 | $0.120 | 83장 |

### **Agora RTC**

| 플랜 | 월 무료 시간 | 초과 시 비용 |
|------|--------------|--------------|
| Free | 10,000분 | $0.99/1,000분 |

**예시:**
- 4명이 동시에 1시간 음성 채팅 = 240분 사용
- 10,000분 = 약 41시간 (4명 기준)
- 월 $20 예산 = 약 20,000분 음성 가능

---

## ✅ **설정 완료 체크리스트**

### **OpenAI**
- [ ] OpenAI 계정 생성
- [ ] 결제 정보 등록
- [ ] 크레딧 충전 ($5 이상)
- [ ] API 키 생성
- [ ] .env 파일에 추가
- [ ] 테스트 성공

### **Agora**
- [ ] Agora 계정 생성
- [ ] 프로젝트 생성
- [ ] App ID 복사
- [ ] Certificate 복사
- [ ] .env 파일에 추가
- [ ] 테스트 성공

### **전체**
- [ ] .env 파일 저장
- [ ] 서버 재시작
- [ ] test_advanced_features.py 실행
- [ ] Swagger UI 확인
- [ ] 실제 기능 테스트

---

## 🎉 **완료!**

**모든 설정이 완료되었습니다!**

이제 다음 기능들을 사용할 수 있습니다:
- ✅ AI 이미지 생성 (DALL-E 3)
- ✅ 실시간 음성 채팅 (Agora RTC)
- ✅ 멀티플레이 (WebSocket)

---

## 💡 **다음 단계**

1. **프론트엔드 개발**
   - Vue.js 또는 React 선택
   - API 연동
   - Agora SDK 통합

2. **추가 기능**
   - 이미지 캐싱
   - 음성 녹음
   - 채팅 필터

3. **배포**
   - Docker 컨테이너화
   - HTTPS 설정
   - 프로덕션 환경 변수

---

**궁금한 점이 있으시면 언제든지 질문해 주세요!** 🚀
