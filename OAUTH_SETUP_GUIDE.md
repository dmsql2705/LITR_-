# 🌐 소셜 로그인 설정 가이드

## 📌 개요

디스코드, 구글, 애플 OAuth 2.0 연동을 위한 상세 설정 가이드입니다.

---

## 1️⃣ 디스코드 OAuth 설정

### **Step 1: 디스코드 앱 생성**

1. **디스코드 개발자 포털 접속**
   - https://discord.com/developers/applications

2. **New Application 클릭**
   - 앱 이름 입력: "LiTR TRPG"

3. **OAuth2 메뉴로 이동**
   - 왼쪽 메뉴에서 "OAuth2" 클릭

4. **Client ID & Secret 복사**
   - Client ID 복사
   - Client Secret 복사 (Reset Secret 클릭 시 새로 생성)

5. **Redirects 추가**
   - Add Redirect 클릭
   - 입력: `http://localhost:8000/api/auth/discord/callback`
   - 프로덕션: `https://yourdomain.com/api/auth/discord/callback`

6. **Scopes 선택**
   - `identify` (필수)
   - `email` (선택, 이메일 받기)

### **Step 2: .env 파일 설정**

```env
DISCORD_CLIENT_ID=1234567890123456789
DISCORD_CLIENT_SECRET=abcdefghijklmnopqrstuvwxyz123456
DISCORD_REDIRECT_URI=http://localhost:8000/api/auth/discord/callback
```

### **Step 3: 테스트**

브라우저에서 접속:
```
http://localhost:8000/api/auth/discord
```

---

## 2️⃣ 구글 OAuth 설정

### **Step 1: 구글 클라우드 프로젝트 생성**

1. **구글 클라우드 콘솔 접속**
   - https://console.cloud.google.com/

2. **새 프로젝트 생성**
   - 프로젝트 이름: "LiTR TRPG"

3. **OAuth 동의 화면 설정**
   - "APIs & Services" → "OAuth consent screen"
   - User Type: External
   - 앱 이름: "LiTR TRPG"
   - 사용자 지원 이메일: your@email.com
   - Scopes 추가: `email`, `profile`, `openid`

4. **사용자 인증 정보 만들기**
   - "Credentials" → "Create Credentials" → "OAuth client ID"
   - Application type: Web application
   - Name: "LiTR Web Client"

5. **승인된 리디렉션 URI 추가**
   - `http://localhost:8000/api/auth/google/callback`
   - `https://yourdomain.com/api/auth/google/callback`

6. **Client ID & Secret 복사**

### **Step 2: .env 파일 설정**

```env
GOOGLE_CLIENT_ID=123456789-abcdefghijklmnop.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnopqrstuvwx
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback
```

### **Step 3: 테스트**

브라우저에서 접속:
```
http://localhost:8000/api/auth/google
```

---

## 3️⃣ 애플 Sign in with Apple 설정

### **Step 1: 애플 개발자 계정 설정**

1. **애플 개발자 포털 접속**
   - https://developer.apple.com/account/

2. **Certificates, Identifiers & Profiles**
   - "Identifiers" 클릭

3. **Services ID 생성**
   - "+" 버튼 클릭
   - "Services IDs" 선택
   - Description: "LiTR TRPG"
   - Identifier: `com.yourcompany.litr` (역순 도메인)

4. **Sign in with Apple 설정**
   - Services ID 클릭
   - "Sign In with Apple" 체크
   - Configure 클릭
   - Domains and Subdomains: `localhost` (개발), `yourdomain.com` (프로덕션)
   - Return URLs: `http://localhost:8000/api/auth/apple/callback`

5. **Key 생성**
   - "Keys" 메뉴로 이동
   - "+" 버튼 클릭
   - Key Name: "LiTR Sign in with Apple Key"
   - "Sign in with Apple" 체크
   - Configure 클릭 → Services ID 선택
   - Continue → Register
   - **Download** 클릭 → `.p8` 파일 다운로드 (한 번만!)

6. **정보 수집**
   - Team ID: 개발자 계정 우측 상단
   - Key ID: 생성한 Key의 ID
   - Services ID: `com.yourcompany.litr`
   - Private Key: `.p8` 파일 내용

### **Step 2: .env 파일 설정**

```env
APPLE_CLIENT_ID=com.yourcompany.litr
APPLE_TEAM_ID=ABCD123456
APPLE_KEY_ID=EFGH789012
APPLE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQg...
(여러 줄)
-----END PRIVATE KEY-----
APPLE_REDIRECT_URI=http://localhost:8000/api/auth/apple/callback
```

**주의:** `.p8` 파일 내용을 한 줄로 만들고 `\n`으로 구분:
```env
APPLE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\nMIGTAgEA...\n-----END PRIVATE KEY-----
```

### **Step 3: 테스트**

브라우저에서 접속:
```
http://localhost:8000/api/auth/apple
```

---

## 🧪 테스트 체크리스트

### **JWT 자체 로그인**
- [ ] 회원가입 성공
- [ ] 중복 이메일 방지
- [ ] 중복 사용자명 방지
- [ ] 로그인 성공
- [ ] 토큰 발급
- [ ] 토큰 갱신
- [ ] 보호된 라우트 접근

### **디스코드**
- [ ] .env 설정 완료
- [ ] 로그인 페이지 리다이렉트
- [ ] 콜백 정상 작동
- [ ] 사용자 생성/로그인
- [ ] JWT 토큰 발급

### **구글**
- [ ] .env 설정 완료
- [ ] 로그인 페이지 리다이렉트
- [ ] 콜백 정상 작동
- [ ] 사용자 생성/로그인
- [ ] JWT 토큰 발급

### **애플**
- [ ] .env 설정 완료
- [ ] 로그인 페이지 리다이렉트
- [ ] 콜백 정상 작동 (POST)
- [ ] 사용자 생성/로그인
- [ ] JWT 토큰 발급

---

## 🐛 트러블슈팅

### **디스코드**

**문제:** "Invalid OAuth2 redirect_uri"
**해결:** 디스코드 앱 설정에서 Redirect URI가 정확히 일치하는지 확인

**문제:** "Invalid client_id"
**해결:** .env 파일의 CLIENT_ID 확인

### **구글**

**문제:** "redirect_uri_mismatch"
**해결:** 구글 클라우드 콘솔에서 승인된 리디렉션 URI 확인

**문제:** "Access blocked"
**해결:** OAuth 동의 화면에서 테스트 사용자 추가

### **애플**

**문제:** "invalid_client"
**해결:** 
- Services ID 확인
- Private Key가 올바른지 확인
- Team ID, Key ID 확인

**문제:** "invalid_grant"
**해결:** 
- 코드가 이미 사용되었거나 만료됨
- 다시 로그인 시도

---

## 📱 프로덕션 배포 시

### **1. HTTPS 필수**

소셜 로그인은 HTTPS가 필수입니다:
```env
# 프로덕션
DISCORD_REDIRECT_URI=https://yourdomain.com/api/auth/discord/callback
GOOGLE_REDIRECT_URI=https://yourdomain.com/api/auth/google/callback
APPLE_REDIRECT_URI=https://yourdomain.com/api/auth/apple/callback
```

### **2. JWT Secret 변경**

```env
# 강력한 랜덤 키 생성
JWT_SECRET_KEY=your-super-strong-random-key-at-least-32-characters-long
```

Python으로 생성:
```python
import secrets
print(secrets.token_urlsafe(32))
```

### **3. 각 플랫폼에서 프로덕션 URL 추가**

- 디스코드: Redirects에 프로덕션 URL 추가
- 구글: 승인된 리디렉션 URI에 추가
- 애플: Return URLs에 추가

---

## 🎁 추가 기능

### **이메일 인증 (선택)**

회원가입 시 이메일 인증:
```python
# 추후 추가 가능
POST /api/auth/verify-email
POST /api/auth/resend-verification
```

### **비밀번호 재설정 (선택)**

비밀번호 찾기:
```python
# 추후 추가 가능
POST /api/auth/forgot-password
POST /api/auth/reset-password
```

---

## 📝 요약

**설정 난이도:**
- 디스코드: ⭐ (쉬움)
- 구글: ⭐⭐ (보통)
- 애플: ⭐⭐⭐ (어려움, Private Key 필요)

**권장 순서:**
1. JWT 자체 로그인 먼저 테스트
2. 디스코드 OAuth 설정 (가장 쉬움)
3. 구글 OAuth 설정
4. 애플 OAuth 설정 (마지막)

**모든 설정이 완료되면 4가지 로그인 방식을 모두 사용할 수 있습니다!** 🎉
