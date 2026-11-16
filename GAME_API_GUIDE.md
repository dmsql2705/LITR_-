# 🎮 게임 상태 관리 API - 완성!

## ✅ 2단계 완료!

게임 상태 관리 API가 완성되었습니다. HP, MP, 인벤토리, 전투 등 모든 게임 메카닉을 관리할 수 있습니다!

---

## 📡 사용 가능한 엔드포인트

### 1. 게임 초기화
```http
POST /api/game/initialize
```

새 게임을 시작할 때 사용합니다.

**파라미터:**
- `session_id`: 세션 ID
- `scenario_id`: 시나리오 ID
- `character_id`: 캐릭터 ID

**예시:**
```
POST /api/game/initialize?session_id=session123&scenario_id=horror_school&character_id=detective_k
```

---

### 2. 게임 저장
```http
POST /api/game/save
```

**요청 예시:**
```json
{
  "session_id": "session123",
  "scenario_id": "horror_school",
  "character_state": {
    "character_id": "detective_k",
    "hp": 10,
    "max_hp": 12,
    "mp": 12,
    "max_mp": 15,
    "san": 70,
    "max_san": 99,
    "inventory": [
      {
        "name": "손전등",
        "description": "밝은 손전등",
        "quantity": 1,
        "type": "tool"
      }
    ],
    "conditions": ["출혈"],
    "notes": "폐교에 들어갔다."
  },
  "story_progress": {
    "entered_school": true,
    "found_music_room": false
  },
  "flags": {
    "met_ghost": false
  },
  "location": "1층 복도",
  "turn": 5
}
```

---

### 3. 게임 로드
```http
GET /api/game/state/{session_id}
```

저장된 게임 상태를 불러옵니다.

**예시:**
```
GET /api/game/state/session123
```

**응답 예시:**
```json
{
  "success": true,
  "game_state": {
    "session_id": "session123",
    "scenario_id": "horror_school",
    "character_state": { ... },
    "location": "1층 복도",
    "turn": 5
  }
}
```

---

### 4. 캐릭터 상태 업데이트
```http
POST /api/game/character/update
```

HP, MP, 인벤토리, 상태 이상을 업데이트합니다.

**요청 예시:**
```json
{
  "session_id": "session123",
  "hp": 8,
  "mp": 10,
  "san": 65,
  "add_items": [
    {
      "name": "열쇠",
      "description": "녹슨 열쇠",
      "quantity": 1,
      "type": "key"
    }
  ],
  "remove_items": ["손전등"],
  "add_conditions": ["독"],
  "remove_conditions": ["출혈"]
}
```

---

### 5. 데미지 적용
```http
POST /api/game/character/damage
```

캐릭터에게 데미지를 입힙니다.

**파라미터:**
- `session_id`: 세션 ID
- `damage`: 데미지 양
- `damage_type`: 데미지 타입 (physical, magical, psychic)

**예시:**
```
POST /api/game/character/damage?session_id=session123&damage=5&damage_type=physical
```

**응답 예시:**
```json
{
  "success": true,
  "message": "5 데미지를 입었습니다!",
  "damage": 5,
  "old_hp": 10,
  "new_hp": 5,
  "is_dead": false
}
```

---

### 6. 치유 적용
```http
POST /api/game/character/heal
```

캐릭터를 치유합니다.

**파라미터:**
- `session_id`: 세션 ID
- `heal_amount`: 회복량

**예시:**
```
POST /api/game/character/heal?session_id=session123&heal_amount=5
```

---

### 7. 전투 시작
```http
POST /api/game/combat/start
```

**요청 예시:**
```json
{
  "session_id": "session123",
  "enemies": [
    {
      "name": "좀비",
      "hp": 15,
      "max_hp": 15,
      "attack": 5,
      "defense": 2
    },
    {
      "name": "해골",
      "hp": 10,
      "max_hp": 10,
      "attack": 3,
      "defense": 1
    }
  ]
}
```

---

### 8. 전투 종료
```http
POST /api/game/combat/end
```

**파라미터:**
- `session_id`: 세션 ID
- `victory`: 승리 여부 (true/false)

---

### 9. 세이브 목록 조회
```http
GET /api/game/saves
```

모든 게임 세이브를 조회합니다.

**응답 예시:**
```json
{
  "success": true,
  "count": 3,
  "saves": [
    {
      "session_id": "session123",
      "scenario_id": "horror_school",
      "character_id": "detective_k",
      "last_saved": "2026-01-26T12:00:00",
      "turn": 5,
      "location": "1층 복도"
    }
  ]
}
```

---

### 10. 세이브 삭제
```http
DELETE /api/game/state/{session_id}
```

---

## 🎯 프론트엔드 연동 예시

### JavaScript 사용법

```javascript
const API_BASE_URL = 'http://localhost:8000';

// 1. 게임 초기화
async function initializeGame(sessionId, scenarioId, characterId) {
    const response = await fetch(
        `${API_BASE_URL}/api/game/initialize?` +
        `session_id=${sessionId}&` +
        `scenario_id=${scenarioId}&` +
        `character_id=${characterId}`,
        { method: 'POST' }
    );
    const data = await response.json();
    return data.game_state;
}

// 2. 게임 저장
async function saveGame(gameState) {
    const response = await fetch(`${API_BASE_URL}/api/game/save`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(gameState)
    });
    return await response.json();
}

// 3. 게임 로드
async function loadGame(sessionId) {
    const response = await fetch(`${API_BASE_URL}/api/game/state/${sessionId}`);
    const data = await response.json();
    return data.game_state;
}

// 4. HP 감소
async function takeDamage(sessionId, damage) {
    const response = await fetch(
        `${API_BASE_URL}/api/game/character/damage?` +
        `session_id=${sessionId}&damage=${damage}`,
        { method: 'POST' }
    );
    return await response.json();
}

// 5. 아이템 획득
async function addItem(sessionId, item) {
    const response = await fetch(`${API_BASE_URL}/api/game/character/update`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            session_id: sessionId,
            add_items: [item]
        })
    });
    return await response.json();
}

// 6. 전투 시작
async function startCombat(sessionId, enemies) {
    const response = await fetch(`${API_BASE_URL}/api/game/combat/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            session_id: sessionId,
            enemies: enemies
        })
    });
    return await response.json();
}
```

---

## 💾 세이브 파일 구조

세이브 파일은 `saves/` 폴더에 JSON 형식으로 저장됩니다:

```
saves/
├── session123.json
├── session456.json
└── session789.json
```

**세이브 파일 예시:**
```json
{
  "session_id": "session123",
  "scenario_id": "horror_school",
  "character_state": {
    "character_id": "detective_k",
    "hp": 10,
    "max_hp": 12,
    "inventory": [ ... ],
    "conditions": [ ... ]
  },
  "story_progress": { ... },
  "flags": { ... },
  "location": "1층 복도",
  "turn": 5,
  "last_saved": "2026-01-26T12:00:00"
}
```

---

## 🧪 테스트 방법

### 1. 자동 테스트
```bash
python test_game_api.py
```

### 2. Swagger UI
```
http://localhost:8000/docs
```

"game" 섹션에서 모든 API를 테스트할 수 있습니다!

---

## 📋 주요 기능

### ✅ 캐릭터 상태 관리
- HP, MP, SAN 관리
- 최대값 자동 제한
- 사망 체크

### ✅ 인벤토리 시스템
- 아이템 추가/제거
- 수량 관리
- 아이템 타입 분류

### ✅ 상태 이상 시스템
- 독, 출혈, 기절 등
- 중복 방지
- 쉬운 추가/제거

### ✅ 전투 시스템
- 턴 순서 관리
- 적 정보 저장
- 전투 시작/종료

### ✅ 스토리 진행 관리
- 진행 상황 플래그
- 위치 추적
- 턴 카운트

### ✅ 자동 저장
- 상태 변경 시 자동 저장
- 타임스탬프 기록
- JSON 포맷

---

## 🔥 다음 단계

### 백엔드 (당신이 할 일)
1. ✅ **완료!** 다이스 롤 API
2. ✅ **완료!** 게임 상태 관리 API
3. 🔜 **다음** 세션 저장/로드 고도화 (이미 기본 구현됨!)

이제 **우선순위 1 작업이 거의 완료**되었습니다!

### 추가 개선 사항 (선택)
- [ ] 전투 AI 로직
- [ ] 자동 저장 주기 설정
- [ ] 세이브 슬롯 제한
- [ ] 클라우드 저장 (DB)

---

## 💡 팁

### 게임 흐름
1. `initialize` → 게임 시작
2. `save` → 주기적 저장
3. `update` → 상태 변경
4. `damage/heal` → HP 관리
5. `combat/start` → 전투 시작
6. `combat/end` → 전투 종료
7. `load` → 이어하기

### 주의사항
- 세션 ID는 유니크해야 함
- HP는 0 이하로 떨어지지 않음
- 인벤토리 아이템은 이름으로 식별
- 모든 상태 변경은 자동 저장됨

---

## 🎉 완료!

게임 상태 관리 API 구현이 완료되었습니다!

**다음은?**
- 프론트엔드와 연동하기
- 또는 다음 단계(세션 관리 고도화)로 진행
