# Security Policy

## 🔒 보안 개요

LiTR 프로젝트는 사용자 데이터 보호와 시스템 보안을 최우선으로 합니다. 이 문서는 보안 정책, 구현된 보안 기능, 그리고 취약점 보고 절차를 설명합니다.

---

## 🛡️ 구현된 보안 기능

### 1. 인증 및 권한 관리
- **JWT 기반 인증**: 액세스 토큰 + 리프레시 토큰 시스템
- **OAuth 통합**: Discord, Google, Apple 소셜 로그인 지원
- **비밀번호 해싱**: bcrypt를 사용한 안전한 비밀번호 저장
- **비밀번호 정책**:
  - 최소 8자 이상
  - 대문자, 소문자, 숫자 포함 필수

### 2. API 보안

#### 보안 헤더 (Security Headers Middleware)
```python
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
Referrer-Policy: strict-origin-when-cross-origin
```

#### 입력 검증
- **Pydantic 스키마**: 모든 API 엔드포인트에서 입력 데이터 검증
- **XSS 방어**: HTML/스크립트 태그 필터링
- **SQL 인젝션 방어**: Parameterized queries (SQLAlchemy ORM)
- **입력 Sanitization**: 위험한 패턴 감지 및 차단

#### Rate Limiting
엔드포인트별 요청 제한:
- 인증 엔드포인트: 10 req/분
- 일반 API: 60 req/분
- AI 작업: 5 req/분
- 파일 업로드: 10 req/5분
- 읽기 작업: 120 req/분

### 3. 데이터베이스 보안

#### Row Level Security (RLS)
Supabase PostgreSQL RLS 정책:
```sql
-- 사용자는 자신의 데이터만 접근 가능
CREATE POLICY "Users can view own data"
  ON users FOR SELECT
  USING (auth.uid() = id);

-- 게임 세션은 참가자만 접근 가능
CREATE POLICY "Players can view their games"
  ON game_sessions FOR SELECT
  USING (auth.uid() = user_id);
```

#### 데이터 암호화
- **전송 중 암호화**: HTTPS/TLS
- **저장 시 암호화**: Supabase의 저장 시 암호화 사용
- **민감 정보**: JWT 시크릿, API 키는 환경 변수로 관리

### 4. 환경 변수 보안

**절대 커밋하지 말 것**:
- `.env` 파일 (`.gitignore`에 명시)
- API 키, 데이터베이스 비밀번호
- JWT 시크릿 키
- OAuth 클라이언트 시크릿

**안전한 관리 방법**:
1. 로컬 개발: `.env` 파일 사용 (git 추적 제외)
2. 프로덕션: Railway 환경 변수로 설정
3. `.env.example` 템플릿 제공 (실제 값 없음)

### 5. CORS 설정

**개발 환경**:
```python
allow_origins=["*"]  # 로컬 테스트용
```

**프로덕션** (TODO):
```python
allow_origins=[os.getenv("FRONTEND_URL")]  # 특정 도메인만 허용
```

---

## 🚨 알려진 제한사항

### 현재 구현되지 않은 기능
1. ~~이메일 인증~~ (향후 구현 예정)
2. ~~2FA (Two-Factor Authentication)~~ (향후 구현 예정)
3. ~~세션 관리 (동시 로그인 제한)~~ (향후 구현 예정)
4. ~~감사 로그 (Audit Logging)~~ (향후 구현 예정)

---

## 🔐 환경 변수 보안 가이드

### 필수 환경 변수

```bash
# 데이터베이스
DATABASE_URL=postgresql://user:password@host:port/database

# API 키
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-proj-...

# JWT 인증
JWT_SECRET_KEY=<32자 이상의 안전한 랜덤 문자열>
JWT_ALGORITHM=HS256

# OAuth
DISCORD_CLIENT_SECRET=<Discord OAuth 시크릿>
GOOGLE_CLIENT_SECRET=<Google OAuth 시크릿>
```

### JWT_SECRET_KEY 생성 방법

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Railway 환경 변수 설정

1. Railway 대시보드 → 프로젝트 → Variables 탭
2. 각 환경 변수를 개별적으로 추가
3. ⚠️ **절대 GitHub에 커밋하지 말 것**

---

## 🚨 취약점 보고 절차

보안 취약점을 발견하셨나요? 아래 절차를 따라주세요:

### 1. 보고 방법

**이메일**: [security@your-domain.com] (TODO: 실제 이메일 추가)

**포함 사항**:
- 취약점 설명
- 재현 단계 (Step-by-step)
- 영향 범위 (Critical/High/Medium/Low)
- 가능한 경우 PoC (Proof of Concept)
- 제안하는 해결 방법 (선택)

### 2. 대응 절차

1. **접수 확인**: 24시간 이내
2. **심각도 평가**: 48시간 이내
3. **패치 개발**: 심각도에 따라 1-14일
4. **패치 배포**: 테스트 후 즉시
5. **공개**: 패치 배포 후 30일

### 3. 보상 프로그램

현재 공식 버그 바운티 프로그램은 없지만, 기여자는 CONTRIBUTORS.md에 기록됩니다.

---

## 🔄 보안 업데이트

### 의존성 업데이트

**백엔드**:
```bash
pip list --outdated
pip install --upgrade <package>
```

**프론트엔드**:
```bash
npm outdated
npm update
```

### 보안 스캔

**Python**:
```bash
pip install safety
safety check
```

**Node.js**:
```bash
npm audit
npm audit fix
```

---

## 📋 보안 체크리스트

배포 전 확인 사항:

### 백엔드
- [ ] `.env` 파일이 `.gitignore`에 추가되었는가?
- [ ] 모든 환경 변수가 Railway에 설정되었는가?
- [ ] JWT_SECRET_KEY가 강력한가? (32자 이상)
- [ ] CORS가 프로덕션 도메인으로 제한되었는가?
- [ ] Rate limiting이 활성화되었는가?
- [ ] 보안 헤더 미들웨어가 등록되었는가?
- [ ] Pydantic 스키마가 모든 엔드포인트에 적용되었는가?

### 프론트엔드
- [ ] API 키가 환경 변수로 관리되는가?
- [ ] `console.log`가 제거되었는가?
- [ ] ErrorBoundary가 구현되었는가?
- [ ] HTTPS가 강제되는가?

### 데이터베이스
- [ ] RLS 정책이 활성화되었는가?
- [ ] 인덱스가 생성되었는가?
- [ ] 백업이 설정되었는가?

---

## 📞 연락처

보안 관련 문의:
- **이메일**: [security@your-domain.com] (TODO: 추가)
- **GitHub Issues**: 공개 이슈로 보고하지 마세요
- **긴급 상황**: 이메일로 [URGENT] 태그와 함께 연락

---

## 🔖 참고 자료

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Next.js Security Headers](https://nextjs.org/docs/advanced-features/security-headers)
- [Supabase RLS](https://supabase.com/docs/guides/auth/row-level-security)

---

**마지막 업데이트**: 2026-02-02
**버전**: 1.0.0
