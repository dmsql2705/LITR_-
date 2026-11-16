# 🎲 다이스 API 구현 완료!

## ✅ 완성된 것들

1. **routers/dice.py** - 다이스 롤 API (새로 생성)
2. **main.py** - 라우터 등록 완료
3. **test_dice_api.py** - 테스트 스크립트
4. **DICE_API_GUIDE.md** - 사용 가이드
5. **requirements.txt** - requests 패키지 추가

---

## 🚀 빠른 실행 가이드

### 1️⃣ 서버 실행

터미널을 열고 프로젝트 폴더로 이동한 후:

```bash
# Windows PowerShell
cd "C:\Users\lynlo\Downloads\01.26 LiTR\LiTR"
uvicorn main:app --reload
```

서버가 실행되면 이런 메시지가 보입니다:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

### 2️⃣ API 문서 확인

브라우저에서 열기:
```
http://localhost:8000/docs
```

여기서 모든 API를 테스트할 수 있습니다!

**새로 추가된 엔드포인트:**
- 🎲 POST `/api/dice/roll` - 다이스 굴리기
- ⚔️ POST `/api/dice/check` - 능력치 판정
- 📖 POST `/api/dice/coc-check` - CoC 7판 판정
- 💚 GET `/api/dice/test` - 테스트

---

### 3️⃣ 자동 테스트 실행

**새 터미널을 열고** (서버는 계속 실행 중):

```bash
cd "C:\Users\lynlo\Downloads\01.26 LiTR\LiTR"
python test_dice_api.py
```

테스트가 자동으로 실행되고 결과가 표시됩니다!

**예상 출력:**
```
==================================================
🎲 다이스 API 테스트 시작
==================================================

💚 [테스트 0] API 상태 확인
==================================================
✅ API 정상 작동 중
   메시지: 다이스 시스템이 정상 작동 중입니다!
   사용 가능한 주사위: d4, d6, d8, d10, d12, d20, d100

🎲 [테스트 1] 다이스 롤
==================================================
✅ 성공!
   굴린 주사위: ['d20', 'd6', 'd6']
   결과:
     - d20: 15
     - d6: 4
     - d6: 3
   수정치: +5
   최종 합계: 27
   이유: STR 판정

... (계속)
```

---

## 🧪 수동 테스트 방법

### Swagger UI 사용 (추천!)

1. 브라우저에서 `http://localhost:8000/docs` 열기
2. **POST /api/dice/roll** 클릭
3. "Try it out" 버튼 클릭
4. Request body에 입력:
```json
{
  "dice": ["d20", "d6"],
  "modifier": 5,
  "reason": "테스트"
}
```
5. "Execute" 버튼 클릭
6. 결과 확인!

### curl 사용

```bash
curl -X POST "http://localhost:8000/api/dice/roll" ^
  -H "Content-Type: application/json" ^
  -d "{\"dice\": [\"d20\", \"d6\"], \"modifier\": 5, \"reason\": \"테스트\"}"
```

---

## 🎯 프론트엔드 연동 예시

프론트엔드 담당자에게 전달할 내용:

### JavaScript에서 호출하기

```javascript
// API_BASE_URL은 이미 LiTR.html에 정의되어 있음
// const API_BASE_URL = 'http://localhost:8000';

async function rollDice() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/dice/roll`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                dice: ['d20', 'd6', 'd6'],
                modifier: 5,
                reason: '공격'
            })
        });

        const data = await response.json();
        console.log('결과:', data);
        
        // data.rolls = [{ die: "d20", result: 15 }, ...]
        // data.total = 27
        
    } catch (error) {
        console.error('에러:', error);
    }
}
```

---

## 📋 체크리스트

완료된 작업:
- ✅ `routers/dice.py` 생성
- ✅ 기본 다이스 롤 API
- ✅ 능력치 판정 API (d20 시스템)
- ✅ CoC 7판 판정 API
- ✅ 에러 처리
- ✅ 크리티컬 성공/실패 처리
- ✅ 보너스/페널티 주사위 지원
- ✅ main.py에 라우터 등록
- ✅ 테스트 스크립트 작성
- ✅ API 문서 작성

---

## 🔥 다음 단계

### 백엔드 (당신이 할 일)
1. ✅ **완료!** 다이스 롤 API
2. 🔜 **다음** 게임 상태 관리 API (routers/game.py)
3. 🔜 세션 저장/로드 API (routers/sessions.py)

### 프론트엔드 (팀원이 할 일)
1. 🔜 `rollMultipleDice()` 함수를 API 연동으로 수정
2. 🔜 GM 응답에서 `[판정 필요: DEX 15]` 패턴 감지
3. 🔜 판정 버튼 UI 추가
4. 🔜 판정 결과를 채팅에 표시

---

## 💡 팁

### API 주소 확인
- 로컬: `http://localhost:8000`
- 네트워크: `http://192.168.x.x:8000` (같은 WiFi면 접속 가능)

### 디버깅
- 서버 로그 확인: 터미널에 모든 요청이 표시됨
- Swagger UI에서 테스트: 가장 쉬운 방법!
- 브라우저 개발자 도구 (F12) → Network 탭

### 주의사항
1. **서버 실행 필수**: API를 호출하기 전에 서버가 실행 중이어야 함
2. **CORS 설정 완료**: 이미 main.py에 CORS 설정되어 있음
3. **캐릭터 ID**: 판정 API는 character_id가 필요함

---

## 🎉 완료!

다이스 롤 API 구현이 완료되었습니다!

**실행 순서:**
1. 서버 실행: `uvicorn main:app --reload`
2. 테스트 실행: `python test_dice_api.py`
3. Swagger 확인: `http://localhost:8000/docs`
4. 프론트엔드 연동!

궁금한 점이 있으면 언제든 물어보세요! 🚀
