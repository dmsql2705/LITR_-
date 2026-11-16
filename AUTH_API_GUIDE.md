# 🔐 인증 API 가이드

## 📌 개요

LiTR 백엔드의 인증 시스템은 **2가지 방식**을 지원합니다:

1. **JWT 자체 로그인** - 이메일/비밀번호로 회원가입/로그인
2. **소셜 로그인** - 디스코드, 구글, 애플 계정으로 로그인

---

## 🎯 JWT 자체 로그인

### **1. 회원가입**

**엔드포인트:** `POST /api/auth/register`

**요청:**
```json
{
  "email": "user@example.com",
  "username": "testuser",
  "password": "password123",
  "nickname": "테스트유저"
}
```

**응답:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "username": "testuser",
  "nickname": "테스트유저"
}
```

**JavaScript 예시:**
```javascript
async function register(email, username, password, nickname) {
    const response = await fetch('http://localhost:8000/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, username, password, nickname })
    });
    
    const data = await response.json();
    
    // 토큰 저장
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    
    return data;
}
```

---

### **2. 로그인**

**엔드포인트:** `POST /api/auth/login`

**요청:**
```json
{
  "username": "testuser",
  "password": "password123"
}
```

**응답:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "username": "testuser",
  "nickname": "테스트유저"
}
```

**JavaScript 예시:**
```javascript
async function login(username, password) {
    const response = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    
    if (!response.ok) {
        throw new Error('로그인 실패');
    }
    
    const data = await response.json();
    
    // 토큰 저장
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    
    return data;
}
```

---

### **3. 현재 사용자 정보**

**엔드포인트:** `GET /api/auth/me`

**헤더:**
```
Authorization: Bearer <access_token>
```

**응답:**
```json
{
  "user_id": 1,
  "username": "testuser",
  "nickname": "테스트유저",
  "email": "user@example.com",
  "credits": 0,
  "follow_count": 0,
  "oauth_provider": null,
  "created_at": "2026-01-26T10:00:00"
}
```

**JavaScript 예시:**
```javascript
async function getMe() {
    const token = localStorage.getItem('access_token');
    
    const response = await fetch('http://localhost:8000/api/auth/me', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    return await response.json();
}
```

---

### **4. 토큰 갱신**

**엔드포인트:** `POST /api/auth/refresh`

**요청:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**응답:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "username": "testuser",
  "nickname": "테스트유저"
}
```

**JavaScript 예시:**
```javascript
async function refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    
    const response = await fetch('http://localhost:8000/api/auth/refresh', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken })
    });
    
    const data = await response.json();
    
    // 새 토큰 저장
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    
    return data;
}
```

---

## 🌐 소셜 로그인

### **1. 디스코드 로그인**

#### **Step 1: 로그인 시작**

**브라우저에서 접속:**
```
http://localhost:8000/api/auth/discord
```

디스코드 로그인 페이지로 리다이렉트됩니다.

#### **Step 2: 콜백 처리**

사용자가 디스코드에서 로그인하면 자동으로 콜백 URL로 돌아옵니다:
```
http://localhost:8000/api/auth/discord/callback?code=...
```

**응답:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 2,
  "username": "discord_1234567890",
  "nickname": "DiscordUser"
}
```

#### **프론트엔드 연동:**
```javascript
// 디스코드 로그인 버튼 클릭 시
function loginWithDiscord() {
    // 디스코드 로그인 페이지로 이동
    window.location.href = 'http://localhost:8000/api/auth/discord';
}

// 콜백 페이지에서 토큰 받기
// URL: http://yourfrontend.com/callback?access_token=...&refresh_token=...
const urlParams = new URLSearchParams(window.location.search);
const accessToken = urlParams.get('access_token');
const refreshToken = urlParams.get('refresh_token');

if (accessToken) {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
    // 메인 페이지로 이동
}
```

---

### **2. 구글 로그인**

#### **Step 1: 로그인 시작**

**브라우저에서 접속:**
```
http://localhost:8000/api/auth/google
```

#### **Step 2: 콜백 처리**

```
http://localhost:8000/api/auth/google/callback?code=...
```

**응답:** 디스코드와 동일한 형식

#### **프론트엔드 연동:**
```javascript
function loginWithGoogle() {
    window.location.href = 'http://localhost:8000/api/auth/google';
}
```

---

### **3. 애플 로그인**

#### **Step 1: 로그인 시작**

**브라우저에서 접속:**
```
http://localhost:8000/api/auth/apple
```

#### **Step 2: 콜백 처리 (POST)**

**주의:** 애플은 POST 방식으로 콜백을 보냅니다!

```
POST http://localhost:8000/api/auth/apple/callback
```

**응답:** 디스코드와 동일한 형식

#### **프론트엔드 연동:**
```javascript
function loginWithApple() {
    window.location.href = 'http://localhost:8000/api/auth/apple';
}
```

---

## 🔑 토큰 사용 방법

### **액세스 토큰**
- **만료 시간**: 7일
- **용도**: API 요청 시 사용
- **헤더**: `Authorization: Bearer <access_token>`

### **리프레시 토큰**
- **만료 시간**: 30일
- **용도**: 액세스 토큰 갱신
- **사용**: `/api/auth/refresh` 엔드포인트

---

## 🛡️ 보호된 API 사용

### **인증이 필요한 API 호출**

```javascript
async function callProtectedAPI() {
    const token = localStorage.getItem('access_token');
    
    const response = await fetch('http://localhost:8000/api/auth/me', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    if (response.status === 401) {
        // 토큰 만료 → 갱신 시도
        await refreshToken();
        // 재시도...
    }
    
    return await response.json();
}
```

---

## ⚙️ 환경 변수 설정

### **필수 설정**

`.env` 파일에 다음을 추가하세요:

```env
# JWT 시크릿 키 (필수!)
JWT_SECRET_KEY=your-super-secret-key-change-this

# Claude API
ANTHROPIC_API_KEY=your-anthropic-key
```

### **소셜 로그인 설정 (선택)**

#### **디스코드**
1. https://discord.com/developers/applications 에서 앱 생성
2. OAuth2 설정:
   - Redirect URI: `http://localhost:8000/api/auth/discord/callback`
   - Scopes: `identify`, `email`

```env
DISCORD_CLIENT_ID=your-client-id
DISCORD_CLIENT_SECRET=your-client-secret
DISCORD_REDIRECT_URI=http://localhost:8000/api/auth/discord/callback
```

#### **구글**
1. https://console.cloud.google.com/ 에서 프로젝트 생성
2. OAuth 2.0 클라이언트 ID 생성
3. 승인된 리디렉션 URI: `http://localhost:8000/api/auth/google/callback`

```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback
```

#### **애플**
1. https://developer.apple.com/ 에서 Services ID 생성
2. Sign in with Apple 설정
3. Private Key (.p8) 다운로드

```env
APPLE_CLIENT_ID=com.yourcompany.serviceid
APPLE_TEAM_ID=YOUR_TEAM_ID
APPLE_KEY_ID=YOUR_KEY_ID
APPLE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----
APPLE_REDIRECT_URI=http://localhost:8000/api/auth/apple/callback
```

---

## 📋 API 엔드포인트 정리

### **JWT 자체 로그인 (5개)**
```
POST /api/auth/register          - 회원가입
POST /api/auth/login             - 로그인
POST /api/auth/refresh           - 토큰 갱신
POST /api/auth/logout            - 로그아웃
GET  /api/auth/me                - 현재 사용자 정보
```

### **소셜 로그인 (6개)**
```
GET  /api/auth/discord           - 디스코드 로그인 시작
GET  /api/auth/discord/callback  - 디스코드 콜백
GET  /api/auth/google            - 구글 로그인 시작
GET  /api/auth/google/callback   - 구글 콜백
GET  /api/auth/apple             - 애플 로그인 시작
POST /api/auth/apple/callback    - 애플 콜백
```

### **테스트 (1개)**
```
GET  /api/auth/test-protected    - 보호된 라우트 테스트
```

**총 12개 엔드포인트**

---

## 💻 프론트엔드 통합 예시

### **완전한 로그인 시스템**

```javascript
class AuthService {
    constructor() {
        this.API_BASE = 'http://localhost:8000';
    }
    
    // JWT 자체 로그인
    async register(email, username, password, nickname) {
        const response = await fetch(`${this.API_BASE}/api/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, username, password, nickname })
        });
        
        const data = await response.json();
        this.saveTokens(data.access_token, data.refresh_token);
        return data;
    }
    
    async login(username, password) {
        const response = await fetch(`${this.API_BASE}/api/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        this.saveTokens(data.access_token, data.refresh_token);
        return data;
    }
    
    // 소셜 로그인
    loginWithDiscord() {
        window.location.href = `${this.API_BASE}/api/auth/discord`;
    }
    
    loginWithGoogle() {
        window.location.href = `${this.API_BASE}/api/auth/google`;
    }
    
    loginWithApple() {
        window.location.href = `${this.API_BASE}/api/auth/apple`;
    }
    
    // 토큰 관리
    saveTokens(accessToken, refreshToken) {
        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);
    }
    
    getAccessToken() {
        return localStorage.getItem('access_token');
    }
    
    async refreshToken() {
        const refreshToken = localStorage.getItem('refresh_token');
        
        const response = await fetch(`${this.API_BASE}/api/auth/refresh`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh_token: refreshToken })
        });
        
        const data = await response.json();
        this.saveTokens(data.access_token, data.refresh_token);
        return data;
    }
    
    // 인증된 요청
    async fetchWithAuth(url, options = {}) {
        const token = this.getAccessToken();
        
        const response = await fetch(url, {
            ...options,
            headers: {
                ...options.headers,
                'Authorization': `Bearer ${token}`
            }
        });
        
        // 토큰 만료 시 자동 갱신
        if (response.status === 401) {
            await this.refreshToken();
            // 재시도
            return this.fetchWithAuth(url, options);
        }
        
        return response;
    }
    
    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    }
}

// 사용 예시
const auth = new AuthService();

// 회원가입
await auth.register('user@example.com', 'username', 'password123', '닉네임');

// 로그인
await auth.login('username', 'password123');

// 소셜 로그인
auth.loginWithDiscord();
auth.loginWithGoogle();
auth.loginWithApple();

// 인증된 API 호출
const response = await auth.fetchWithAuth('http://localhost:8000/api/auth/me');
const user = await response.json();
```

---

## 🔒 보안 기능

### **구현된 보안**
- ✅ 비밀번호 해싱 (bcrypt)
- ✅ JWT 토큰 (HS256)
- ✅ 토큰 만료 시간 (7일)
- ✅ 리프레시 토큰 (30일)
- ✅ CSRF 방지 (state 파라미터)
- ✅ 중복 가입 방지
- ✅ 계정 활성화 체크

### **권장 보안 강화**
- 🔜 Rate Limiting
- 🔜 2단계 인증 (2FA)
- 🔜 비밀번호 정책 (대소문자, 숫자, 특수문자)
- 🔜 이메일 인증

---

## ❗ 에러 코드

| 코드 | 의미 | 해결 방법 |
|------|------|-----------|
| 400 | 잘못된 요청 | 요청 데이터 확인 |
| 401 | 인증 실패 | 토큰 확인 또는 재로그인 |
| 403 | 권한 없음 | 계정 활성화 상태 확인 |
| 404 | 찾을 수 없음 | 사용자 존재 여부 확인 |
| 500 | 서버 오류 | 서버 로그 확인 |

---

## 🧪 테스트 방법

### **자동 테스트**
```bash
python test_auth_api.py
```

### **수동 테스트 (Swagger UI)**
```
http://localhost:8000/docs
```

**Auth 섹션에서:**
1. `/auth/register` - 회원가입 테스트
2. `/auth/login` - 로그인 테스트
3. `/auth/me` - 사용자 정보 조회 (토큰 필요)
4. Authorize 버튼 - 토큰 입력

---

## 💡 사용 시나리오

### **시나리오 1: 신규 사용자**
1. 회원가입 (`/auth/register`)
2. 토큰 저장
3. 게임 시작

### **시나리오 2: 기존 사용자**
1. 로그인 (`/auth/login`)
2. 토큰 저장
3. 게임 이어하기

### **시나리오 3: 소셜 로그인**
1. 디스코드/구글/애플 버튼 클릭
2. 외부 사이트에서 인증
3. 자동으로 토큰 받음
4. 게임 시작

### **시나리오 4: 토큰 만료**
1. API 호출 → 401 에러
2. 리프레시 토큰으로 갱신 (`/auth/refresh`)
3. 새 토큰으로 재시도

---

## 🎯 완료!

**인증 시스템 100% 구현 완료!**

**지원 기능:**
- ✅ JWT 자체 로그인
- ✅ 회원가입/로그인
- ✅ 토큰 갱신
- ✅ 디스코드 OAuth
- ✅ 구글 OAuth
- ✅ 애플 OAuth
- ✅ 보호된 라우트

**다음 단계:**
- 프론트엔드 연동
- 소셜 로그인 설정
- 프로덕션 배포
