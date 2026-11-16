# 다이스 롤 API 사용 가이드

## 🎲 백엔드 API 완성!

다이스 롤 API가 완성되었습니다. 이제 프론트엔드에서 연동하면 됩니다.

---

## 📡 사용 가능한 엔드포인트

### 1. 기본 다이스 롤
```http
POST /api/dice/roll
```

**요청 예시:**
```json
{
  "dice": ["d20", "d6", "d6"],
  "modifier": 5,
  "reason": "STR 판정"
}
```

**응답 예시:**
```json
{
  "rolls": [
    {"die": "d20", "result": 15},
    {"die": "d6", "result": 4},
    {"die": "d6", "result": 3}
  ],
  "modifier": 5,
  "total": 27,
  "reason": "STR 판정"
}
```

---

### 2. 능력치 판정 (d20 시스템)
```http
POST /api/dice/check
```

**요청 예시:**
```json
{
  "stat": "DEX",
  "difficulty": 15,
  "character_id": "detective_k",
  "modifier": 0
}
```

**응답 예시:**
```json
{
  "stat": "DEX",
  "stat_value": 70,
  "roll": 18,
  "difficulty": 15,
  "modifier": 2,
  "success": true,
  "critical": false,
  "result_text": "✅ 성공! (18 + 2 = 20 ≥ 15)"
}
```

---

### 3. CoC 7판 기능 판정
```http
POST /api/dice/coc-check
```

**요청 예시:**
```json
{
  "skill_value": 75,
  "character_id": "detective_k",
  "bonus_dice": 0,
  "penalty_dice": 0
}
```

**응답 예시:**
```json
{
  "skill_value": 75,
  "roll": 42,
  "success": true,
  "success_level": "보통성공",
  "result_text": "🎲 42 / 75 - 성공했습니다!"
}
```

---

### 4. 테스트 엔드포인트
```http
GET /api/dice/test
```

---

## 🔗 프론트엔드 연동 예시 (JavaScript)

### LiTR.html에 추가할 코드

```javascript
// 다이스 롤 함수 (기존 rollMultipleDice 함수 수정)
async function rollMultipleDice() {
    const selectedDice = state.selectedDice;
    
    if (selectedDice.length === 0) {
        alert('굴릴 주사위를 선택해주세요!');
        return;
    }

    try {
        // 백엔드 API 호출
        const response = await fetch(`${API_BASE_URL}/api/dice/roll`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                dice: selectedDice,
                modifier: 0,
                reason: "주사위 굴리기"
            })
        });

        if (!response.ok) {
            throw new Error('주사위 롤 실패');
        }

        const data = await response.json();
        
        // 결과 표시
        console.log('다이스 롤 결과:', data);
        
        // UI 업데이트
        updateMultiDiceHistory(data.rolls, data.total);
        
        // 채팅에 결과 추가
        addChatMessage('system', `🎲 ${data.rolls.map(r => `${r.die}: ${r.result}`).join(', ')} = 총합: ${data.total}`);
        
        // 3D 애니메이션 (기존 로직)
        // ... 기존 3D 애니메이션 코드 ...
        
    } catch (error) {
        console.error('다이스 롤 오류:', error);
        alert('주사위를 굴리는 중 오류가 발생했습니다.');
    }
}

// 능력치 판정 함수 (새로 추가)
async function performAbilityCheck(stat, difficulty) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/dice/check`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                stat: stat,
                difficulty: difficulty,
                character_id: state.selectedCharacterId,
                modifier: 0
            })
        });

        if (!response.ok) {
            throw new Error('능력치 판정 실패');
        }

        const data = await response.json();
        
        // 결과를 채팅에 표시
        addChatMessage('system', data.result_text);
        
        return data;
        
    } catch (error) {
        console.error('능력치 판정 오류:', error);
        alert('능력치 판정 중 오류가 발생했습니다.');
    }
}

// GM이 판정을 요청했을 때 처리 (AI 응답 파싱)
function processAIResponse(response) {
    // 기존 코드...
    
    // [판정 필요: DEX 15] 형식 감지
    const checkPattern = /\[판정 필요: ([A-Z]+) (\d+)\]/g;
    let match;
    
    while ((match = checkPattern.exec(response)) !== null) {
        const stat = match[1];  // DEX
        const difficulty = parseInt(match[2]);  // 15
        
        // 판정 버튼 표시
        showAbilityCheckButton(stat, difficulty);
    }
}

// 판정 버튼 UI (새로 추가)
function showAbilityCheckButton(stat, difficulty) {
    const buttonHtml = `
        <div class="ability-check-prompt">
            <p>GM이 <strong>${stat} ${difficulty}</strong> 판정을 요청했습니다.</p>
            <button onclick="performAbilityCheck('${stat}', ${difficulty})" class="btn btn-primary">
                판정하기
            </button>
        </div>
    `;
    
    const chatBox = document.getElementById('chatBox');
    const div = document.createElement('div');
    div.innerHTML = buttonHtml;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}
```

---

## 🧪 테스트 방법

### 1. 서버 실행
```bash
uvicorn main:app --reload
```

### 2. Swagger UI로 테스트
브라우저에서 열기:
```
http://localhost:8000/docs
```

### 3. 다이스 롤 테스트
1. `/api/dice/test` 엔드포인트로 이동
2. "Try it out" 클릭
3. "Execute" 클릭
4. 응답 확인

### 4. 실제 롤 테스트
1. `/api/dice/roll` 엔드포인트로 이동
2. "Try it out" 클릭
3. Request body에 입력:
```json
{
  "dice": ["d20", "d6"],
  "modifier": 5,
  "reason": "테스트"
}
```
4. "Execute" 클릭
5. 결과 확인

---

## 📝 다음 단계

이제 프론트엔드 담당자에게 전달하세요:

1. ✅ 다이스 롤 API 완성 (`/api/dice/roll`)
2. ✅ 능력치 판정 API 완성 (`/api/dice/check`)
3. ✅ CoC 판정 API 완성 (`/api/dice/coc-check`)

프론트엔드에서 해야 할 일:
- `rollMultipleDice()` 함수를 API 호출로 수정
- GM 응답에서 `[판정 필요: DEX 15]` 패턴 감지
- 판정 버튼 UI 추가
- 판정 결과를 채팅에 표시

---

## 🎯 지원하는 주사위 종류

- d4 (4면)
- d6 (6면)
- d8 (8면)
- d10 (10면)
- d12 (12면)
- d20 (20면)
- d100 (100면)

**여러 개 동시 굴리기 가능!**
예: `["d20", "d6", "d6", "d4"]`

---

## ⚠️ 주의사항

1. **캐릭터 ID 필수**: 능력치 판정 시 `character_id`가 필요합니다.
2. **난이도 가이드**:
   - 8: 쉬움
   - 12: 보통
   - 15: 어려움
   - 18: 매우 어려움
3. **CoC 7판**: `coc-check` 엔드포인트는 Call of Cthulhu 룰 사용

---

## 🚀 완료!

백엔드 다이스 롤 API가 완성되었습니다!
이제 프론트엔드와 연동하면 실제로 게임을 플레이할 수 있습니다.
