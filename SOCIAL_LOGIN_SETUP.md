# 🔐 JWT & 소셜 로그인 완벽 가이드

**JWT Secret, Discord, Google, Apple 로그인 설정 방법**

---

## 📋 **목차**

1. [JWT Secret Key 생성](#1-jwt-secret-key-생성)
2. [Discord OAuth 설정](#2-discord-oauth-설정)
3. [Google OAuth 설정](#3-google-oauth-설정)
4. [Apple Sign In 설정](#4-apple-sign-in-설정)
5. [.env 파일 완성](#5-env-파일-완성)

---

## 1. JWT Secret Key 생성

### **이건 직접 만듭니다!**

JWT Secret Key는 API 키가 아니라 **여러분이 직접 만드는 랜덤 문자열**입니다.

### **방법 1: 온라인 생성기 (추천)**

1. **브라우저에서 접속:**
   ```
   https://randomkeygen.com/
   ```

2. **"Fort Knox Passwords" 섹션에서 아무거나 복사**
   - 예시: `Kg7$mP9#nL2@qR5*tW8!yU4^iO1&aS6`

3. **.env 파일에 붙여넣기**

### **방법 2: Python으로 생성**

```bash
# 터미널에서 실행
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**출력 예시:**
```
xK9mP2nR5tW8yU4iO1aS6dF3gH7jL0qV
```

### **방법 3: 직접 입력 (개발용)**

```env
JWT_SECRET_KEY=my-super-secret-key-for-development-12345
```

⚠️ **보안 주의**:
- 최소 20자 이상
- 영문, 숫자, 특수문자 조합
- 프로덕션에서는 복잡한 키 사용 필수!

---

## 2. Discord OAuth 설정

### **개요**
- **시간**: 5분
- **비용**: 무료
- **계정**: Discord 계정 필요

### **Step 1: Discord Developer Portal**

1. **접속:**
   ```
   https://discord.com/developers/applications
   ```

2. **로그인**
   - Discord 계정으로 로그인

3. **새 애플리케이션 만들기**
   - 우측 상단 "New Application" 클릭
   - 이름 입력: `LiTR-Game` (또는 원하는 이름)
   - Terms of Service 동의
   - "Create" 클릭

### **Step 2: Client ID & Secret 복사**

1. **General Information 탭**
   - **Application ID** (=Client ID) 복사
   - 예시: `1234567890123456789`

2. **Client Secret 생성**
   - "CLIENT SECRET" 섹션
   - "Reset Secret" 클릭
   - 확인 팝업에서 "Yes, do it!" 클릭
   - 생성된 Secret 복사 (⚠️ 한 번만 표시됨!)
   - 예시: `abcdefghijklmnopqrstuvwxyz123456`

### **Step 3: OAuth2 설정**

1. **좌측 메뉴 "OAuth2" 클릭**

2. **Redirects 섹션**
   - "Add Redirect" 클릭
   - 입력:
     ```
     http://localhost:8000/api/auth/discord/callback
     ```
   - "Save Changes" 클릭

### **Step 4: .env 파일에 추가**

```env
# Discord OAuth
DISCORD_CLIENT_ID=1234567890123456789
DISCORD_CLIENT_SECRET=abcdefghijklmnopqrstuvwxyz123456
DISCORD_REDIRECT_URI=http://localhost:8000/api/auth/discord/callback
```

### **테스트**

```bash
# 서버 실행
uvicorn main:app --reload

# 브라우저에서
http://localhost:8000/api/auth/discord
```

---

## 3. Google OAuth 설정

### **개요**
- **시간**: 10분
- **비용**: 무료
- **계정**: Google 계정 필요

### **Step 1: Google Cloud Console 접속**

1. **접속:**
   ```
   https://console.cloud.google.com/
   ```

2. **로그인**
   - Google 계정으로 로그인

### **Step 2: 프로젝트 생성**

1. **상단 프로젝트 선택 드롭다운 클릭**
   - "새 프로젝트" 클릭

2. **프로젝트 정보 입력**
   - **프로젝트 이름**: `LiTR-Backend`
   - **조직**: 없음 (개인)
   - "만들기" 클릭

3. **프로젝트 선택**
   - 상단에서 방금 만든 프로젝트 선택

### **Step 3: OAuth 동의 화면 구성**

1. **좌측 메뉴**
   - "API 및 서비스" → "OAuth 동의 화면" 클릭

2. **User Type 선택**
   - **외부** 선택 (Internal은 G Suite 조직용)
   - "만들기" 클릭

3. **1단계: OAuth 동의 화면**
   - **앱 이름**: `LiTR`
   - **사용자 지원 이메일**: 본인 이메일
   - **앱 로고**: (선택사항)
   - **앱 도메인**: (선택사항, 나중에)
   - **승인된 도메인**: (선택사항)
   - **개발자 연락처 정보**: 본인 이메일
   - "저장 후 계속" 클릭

4. **2단계: 범위**
   - 기본 범위 자동 선택됨 (email, profile)
   - "저장 후 계속" 클릭

5. **3단계: 테스트 사용자**
   - (선택사항) 테스트할 이메일 추가
   - "저장 후 계속" 클릭

6. **4단계: 요약**
   - "대시보드로 돌아가기" 클릭

### **Step 4: OAuth 클라이언트 ID 만들기**

1. **좌측 메뉴 "사용자 인증 정보" 클릭**

2. **상단 "+ 사용자 인증 정보 만들기"**
   - "OAuth 클라이언트 ID" 선택

3. **애플리케이션 유형 선택**
   - "웹 애플리케이션" 선택

4. **설정 입력**
   - **이름**: `LiTR-Backend-Web`
   
   - **승인된 JavaScript 원본** (선택사항):
     - "+ URI 추가" 클릭
     - 입력: `http://localhost:8000`
   
   - **승인된 리디렉션 URI** (필수):
     - "+ URI 추가" 클릭
     - 입력: `http://localhost:8000/api/auth/google/callback`

5. **"만들기" 클릭**

### **Step 5: Client ID & Secret 복사**

팝업창이 나타나면:

- **클라이언트 ID** 복사
  - 예시: `123456789012-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com`

- **클라이언트 보안 비밀번호** 복사
  - 예시: `GOCSPX-abcdefghijklmnopqrstuvwxyz`

⚠️ 나중에 다시 보려면: "사용자 인증 정보" 목록에서 클릭

### **Step 6: .env 파일에 추가**

```env
# Google OAuth
GOOGLE_CLIENT_ID=123456789012-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnopqrstuvwxyz
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback
```

### **테스트**

```bash
# 서버 실행
uvicorn main:app --reload

# 브라우저에서
http://localhost:8000/api/auth/google
```

---

## 4. Apple Sign In 설정

### **⚠️ 중요 사항**

- **Apple Developer 계정 필요** (연 $99 USD)
- **설정이 복잡함** (인증서, 키 파일 등)
- **현재는 선택사항입니다!**

### **권장: 나중에 설정**

Apple 로그인은 **나중에 추가**하는 것을 권장합니다:

1. 먼저 Discord + Google로 소셜 로그인 테스트
2. 앱이 잘 작동하는지 확인
3. 실제 배포 단계에서 Apple 추가

### **.env 파일에서 Apple 비활성화**

```env
# Apple Sign in (나중에 설정)
# APPLE_CLIENT_ID=
# APPLE_TEAM_ID=
# APPLE_KEY_ID=
# APPLE_PRIVATE_KEY=
# APPLE_REDIRECT_URI=
```

### **Apple 설정이 필요하다면**

자세한 가이드: `OAUTH_SETUP_GUIDE.md` 파일 참고

간단 요약:
1. Apple Developer 계정 가입 ($99/년)
2. Identifiers 생성 (Services ID)
3. Keys 생성 (.p8 파일)
4. Certificates 생성
5. 복잡한 JWT 토큰 생성 로직

---

## 5. .env 파일 완성

### **최소 설정 (추천)**

```env
# ============================================
# 필수
# ============================================

# Claude API
ANTHROPIC_API_KEY=sk-ant-api03-여기에-클로드-키

# JWT (직접 생성!)
JWT_SECRET_KEY=xK9mP2nR5tW8yU4iO1aS6dF3gH7jL0qV

# ============================================
# 선택 (이미지 & 음성)
# ============================================

# OpenAI (이미지 생성)
OPENAI_API_KEY=sk-proj-여기에-오픈AI-키

# Agora (음성 채팅)
AGORA_APP_ID=12345678901234567890123456789012
AGORA_APP_CERTIFICATE=abcdef1234567890abcdef1234567890

# ============================================
# 소셜 로그인
# ============================================

# Discord
DISCORD_CLIENT_ID=1234567890123456789
DISCORD_CLIENT_SECRET=abcdefghijklmnopqrstuvwxyz123456
DISCORD_REDIRECT_URI=http://localhost:8000/api/auth/discord/callback

# Google
GOOGLE_CLIENT_ID=123456789012-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnopqrstuvwxyz
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback

# Apple (나중에)
# APPLE_CLIENT_ID=
# APPLE_TEAM_ID=
# APPLE_KEY_ID=
# APPLE_PRIVATE_KEY=
# APPLE_REDIRECT_URI=
```

---

## 📝 **설정 체크리스트**

### **필수 설정**
- [ ] JWT_SECRET_KEY 생성 (직접 만들기)
- [ ] ANTHROPIC_API_KEY (Claude)

### **이미지 & 음성 (선택)**
- [ ] OPENAI_API_KEY (OpenAI)
- [ ] AGORA_APP_ID + CERTIFICATE (Agora)

### **소셜 로그인 (선택)**
- [ ] Discord OAuth 설정
- [ ] Google OAuth 설정
- [ ] Apple Sign In (나중에)

---

## 🧪 **테스트 방법**

### **1. 서버 실행**

```bash
uvicorn main:app --reload
```

### **2. Discord 로그인 테스트**

브라우저에서:
```
http://localhost:8000/api/auth/discord
```

→ Discord 로그인 페이지로 리디렉션되면 성공!

### **3. Google 로그인 테스트**

브라우저에서:
```
http://localhost:8000/api/auth/google
```

→ Google 로그인 페이지로 리디렉션되면 성공!

### **4. Swagger UI 확인**

```
http://localhost:8000/docs
```

- "auth" 섹션 확인
- 모든 엔드포인트 테스트 가능

---

## ❓ **자주 묻는 질문**

### Q: JWT_SECRET_KEY는 어디서 발급받나요?

**A:** 발급받는 게 아니라 **직접 만듭니다**!
- https://randomkeygen.com/ 에서 복사
- 또는 `python -c "import secrets; print(secrets.token_urlsafe(32))"`

### Q: Discord/Google 설정이 너무 복잡해요

**A:** 소셜 로그인은 **선택사항**입니다!
- 일반 회원가입/로그인만으로도 충분히 작동
- 나중에 추가해도 됨

### Q: Apple 설정이 필수인가요?

**A:** 아니요! **선택사항**입니다.
- Apple Developer 계정 필요 ($99/년)
- Discord + Google만으로도 충분
- 실제 배포 단계에서 추가 권장

### Q: .env 파일이 안 읽혀요

**A:**
1. 파일 이름이 정확히 `.env`인지 확인 (`.env.txt` 아님)
2. 프로젝트 루트에 있는지 확인
3. 서버 완전히 재시작

### Q: 소셜 로그인 에러가 나요

**A:**
1. Redirect URI가 정확히 일치하는지 확인
2. Client Secret이 올바른지 확인
3. 브라우저 콘솔에서 에러 메시지 확인

---

## 🎉 **완료!**

**모든 설정이 완료되었습니다!**

### **최소 필요한 것**
- ✅ JWT_SECRET_KEY (직접 생성)
- ✅ ANTHROPIC_API_KEY (Claude)

### **추가로 설정하면 좋은 것**
- ✅ OpenAI API (이미지 생성)
- ✅ Agora (음성 채팅)
- ✅ Discord OAuth (소셜 로그인)
- ✅ Google OAuth (소셜 로그인)
- ⏸️ Apple Sign In (나중에)

---

## 💡 **다음 단계**

1. **서버 실행**
   ```bash
   uvicorn main:app --reload
   ```

2. **테스트 실행**
   ```bash
   python test_advanced_features.py
   python test_auth_api.py
   ```

3. **프론트엔드 개발**
   - 로그인 UI 구현
   - 소셜 로그인 버튼 추가

---

**궁금한 점이 있으시면 언제든지 질문해 주세요!** 🚀
