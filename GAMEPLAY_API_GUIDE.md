# 🎮 통합 게임 플레이 API 가이드

## 📌 개요

**통합 게임 플레이 API**는 다이스 판정, 게임 상태 관리, AI GM 응답을 **하나로 통합**한 API입니다.

### **장점**
- ✅ 프론트엔드에서 한 번의 API 호출로 모든 것 처리
- ✅ 자동 히스토리 관리
- ✅ 다이스 판정 결과가 AI GM에게 자동 전달
- ✅ 게임 상태 자동 저장
- ✅ 일관된 게임 플레이 경험

---

## 🚀 빠른 시작

### **1. 게임 시작**

```javascript
async function startGame() {
    const response = await fetch('http://localhost:8000/api/gameplay/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            scenario_id: "horror_school",
            character_id: "detective_k",
            user_id: 1  // 선택, 로그인한 회원의 ID
        })
    });
    
    const game = await response.json();
    
    console.log("세션 ID:", game.session_id);
    console.log("GM 오프닝:", game.gm_response);
    
    return game;
}
```

### **2. 플레이어 행동 (판정 없음)**

```javascript
async function performAction(sessionId, action) {
    const response = await fetch('http://localhost:8000/api/gameplay/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            session_id: sessionId,
            action: action,
            needs_roll: false
        })
    });
    
    const result = await response.json();
    
    console.log("GM 응답:", result.gm_response);
    console.log("현재 턴:", result.turn);
    
    return result;
}

// 사용 예시
await performAction(sessionId, "주변을 둘러본다");
```

### **3. 플레이어 행동 (능력치 판정)**

```javascript
async function performActionWithRoll(sessionId, action) {
    const response = await fetch('http://localhost:8000/api/gameplay/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            session_id: sessionId,
            action: action,
            needs_roll: true,
            roll_type: "ability",
            ability_name: "DEX",
            difficulty: 12
        })
    });
    
    const result = await response.json();
    
    console.log("판정 결과:", result.dice_result);
    console.log("성공 여부:", result.dice_result.success);
    console.log("GM 응답:", result.gm_response);
    
    return result;
}

// 사용 예시
await performActionWithRoll(sessionId, "문을 조용히 연다");
```

### **4. CoC 판정**

```javascript
async function performCoCCheck(sessionId, action, targetValue) {
    const response = await fetch('http://localhost:8000/api/gameplay/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            session_id: sessionId,
            action: action,
            needs_roll: true,
            roll_type: "coc",
            target_value: targetValue,
            bonus_penalty: 0  // -2~+2
        })
    });
    
    const result = await response.json();
    
    console.log("d100 결과:", result.dice_result.result);
    console.log("성공 등급:", result.dice_result.details.level);
    console.log("GM 응답:", result.gm_response);
    
    return result;
}

// 사용 예시
await performCoCCheck(sessionId, "숨겨진 단서를 찾는다", 65);
```

---

## 📡 API 엔드포인트

### **1️⃣ 게임 시작**

```
POST /api/gameplay/start
```

**요청:**
```json
{
  "scenario_id": "horror_school",
  "character_id": "detective_k",
  "user_id": 1  // 선택사항
}
```

**응답:**
```json
{
  "session_id": "game_1737871234",
  "turn": 0,
  "gm_response": "어둠이 깔린 학교...",
  "character_state": {
    "name": "탐정 K",
    "hp": 12,
    "maxHp": 12,
    "mp": 10,
    "san": 65
  },
  "game_state": {
    "location": "학교 정문",
    "flags": {},
    "combat_active": false
  },
  "history": [...]
}
```

---

### **2️⃣ 플레이어 행동**

```
POST /api/gameplay/action
```

**요청 (판정 없음):**
```json
{
  "session_id": "game_1737871234",
  "action": "주변을 둘러본다",
  "needs_roll": false
}
```

**요청 (능력치 판정):**
```json
{
  "session_id": "game_1737871234",
  "action": "문을 열려고 시도한다",
  "needs_roll": true,
  "roll_type": "ability",
  "ability_name": "DEX",
  "difficulty": 12
}
```

**요청 (CoC 판정):**
```json
{
  "session_id": "game_1737871234",
  "action": "단서를 찾는다",
  "needs_roll": true,
  "roll_type": "coc",
  "target_value": 65,
  "bonus_penalty": 1  // -2~+2
}
```

**응답:**
```json
{
  "session_id": "game_1737871234",
  "turn": 3,
  "player_action": "문을 열려고 시도한다",
  "dice_result": {
    "roll_type": "ability",
    "result": 15,
    "success": true,
    "details": {
      "ability": "DEX",
      "roll": 14,
      "modifier": 1,
      "difficulty": 12,
      "critical": false,
      "fumble": false
    }
  },
  "gm_response": "당신은 조심스럽게 문을 열었습니다...",
  "character_state": {...},
  "game_state": {...},
  "history": [...]
}
```

---

### **3️⃣ 게임 상태 조회**

```
GET /api/gameplay/status/{session_id}
```

**응답:**
```json
{
  "session_id": "game_1737871234",
  "turn": 5,
  "scenario": {
    "id": "horror_school",
    "title": "폐교의 비밀"
  },
  "character": {
    "id": "detective_k",
    "name": "탐정 K",
    "hp": 10,
    "max_hp": 12,
    "mp": 8,
    "max_mp": 10,
    "san": 60
  },
  "location": "교실 3-A",
  "flags": {
    "door_opened": true,
    "key_found": false
  },
  "combat_active": false,
  "last_played": "2026-01-26T15:30:00"
}
```

---

### **4️⃣ 게임 히스토리 조회**

```
GET /api/gameplay/history/{session_id}
```

**응답:**
```json
{
  "session_id": "game_1737871234",
  "turn": 5,
  "history": [
    {
      "role": "assistant",
      "content": "어둠이 깔린 학교..."
    },
    {
      "role": "user",
      "content": "주변을 둘러본다"
    },
    {
      "role": "assistant",
      "content": "복도는 고요하고..."
    }
  ],
  "total_messages": 10
}
```

---

### **5️⃣ 게임 세션 삭제**

```
DELETE /api/gameplay/{session_id}
```

**응답:**
```json
{
  "success": true,
  "message": "게임 세션이 삭제되었습니다.",
  "session_id": "game_1737871234"
}
```

---

## 🎲 판정 시스템

### **판정 타입**

#### **1. ability (능력치 판정)**
- d20 + 수정치 vs 난이도
- 크리티컬 (20), 대실패 (1)

```json
{
  "roll_type": "ability",
  "ability_name": "STR",  // STR, DEX, INT, WIS, CON, CHA
  "difficulty": 12        // 8(쉬움), 12(보통), 15(어려움), 18(매우 어려움)
}
```

#### **2. coc (Call of Cthulhu 판정)**
- d100 vs 목표값
- 보너스/페널티 주사위 지원
- 성공 등급: 크리티컬, 극한 성공, 어려운 성공, 보통 성공, 실패, 대실패

```json
{
  "roll_type": "coc",
  "target_value": 65,     // 1-100
  "bonus_penalty": 1      // -2(큰 패널티), -1(패널티), 0(보통), 1(보너스), 2(큰 보너스)
}
```

#### **3. dice (일반 다이스)**
- 단순 d20
- 10 이상 성공

```json
{
  "roll_type": "dice"
}
```

---

## 💻 프론트엔드 완전 통합 예시

### **Vue.js 예시**

```vue
<template>
  <div class="game-container">
    <!-- 게임 화면 -->
    <div class="game-screen">
      <!-- GM 응답 -->
      <div class="gm-response">
        <p>{{ currentGmResponse }}</p>
      </div>
      
      <!-- 캐릭터 상태 -->
      <div class="character-status">
        <p>HP: {{ character.hp }}/{{ character.max_hp }}</p>
        <p>MP: {{ character.mp }}/{{ character.max_mp }}</p>
        <p>SAN: {{ character.san }}</p>
      </div>
      
      <!-- 플레이어 입력 -->
      <div class="player-input">
        <input v-model="playerAction" placeholder="행동을 입력하세요..." />
        <button @click="performAction">행동</button>
        
        <!-- 판정 옵션 -->
        <label>
          <input type="checkbox" v-model="needsRoll" />
          판정 필요
        </label>
        
        <select v-if="needsRoll" v-model="rollType">
          <option value="ability">능력치 판정</option>
          <option value="coc">CoC 판정</option>
        </select>
      </div>
      
      <!-- 히스토리 -->
      <div class="history">
        <div v-for="(msg, i) in history" :key="i" :class="msg.role">
          {{ msg.content }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sessionId: null,
      playerAction: '',
      needsRoll: false,
      rollType: 'ability',
      currentGmResponse: '',
      character: {},
      history: []
    };
  },
  
  async mounted() {
    // 게임 시작
    await this.startGame();
  },
  
  methods: {
    async startGame() {
      const response = await fetch('http://localhost:8000/api/gameplay/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          scenario_id: 'horror_school',
          character_id: 'detective_k'
        })
      });
      
      const game = await response.json();
      
      this.sessionId = game.session_id;
      this.currentGmResponse = game.gm_response;
      this.character = game.character_state;
      this.history.push({ role: 'assistant', content: game.gm_response });
    },
    
    async performAction() {
      if (!this.playerAction.trim()) return;
      
      // 플레이어 행동 추가
      this.history.push({ role: 'user', content: this.playerAction });
      
      // API 요청
      const requestData = {
        session_id: this.sessionId,
        action: this.playerAction,
        needs_roll: this.needsRoll
      };
      
      if (this.needsRoll) {
        requestData.roll_type = this.rollType;
        
        if (this.rollType === 'ability') {
          requestData.ability_name = 'DEX';
          requestData.difficulty = 12;
        } else if (this.rollType === 'coc') {
          requestData.target_value = 65;
          requestData.bonus_penalty = 0;
        }
      }
      
      const response = await fetch('http://localhost:8000/api/gameplay/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestData)
      });
      
      const result = await response.json();
      
      // 판정 결과 표시
      if (result.dice_result) {
        const diceMsg = `🎲 판정: ${result.dice_result.success ? '성공' : '실패'} (${result.dice_result.result})`;
        this.history.push({ role: 'system', content: diceMsg });
      }
      
      // GM 응답 추가
      this.currentGmResponse = result.gm_response;
      this.history.push({ role: 'assistant', content: result.gm_response });
      
      // 캐릭터 상태 업데이트
      this.character = result.character_state;
      
      // 입력 초기화
      this.playerAction = '';
    }
  }
};
</script>
```

---

## 🎯 사용 시나리오

### **시나리오 1: 간단한 탐험**

```javascript
// 1. 게임 시작
const game = await startGame();

// 2. 주변 관찰 (판정 없음)
await performAction(game.session_id, "주변을 둘러본다");

// 3. 문 열기 (민첩 판정)
await performActionWithRoll(game.session_id, "문을 연다", "DEX", 12);

// 4. 단서 찾기 (CoC 판정)
await performCoCCheck(game.session_id, "단서를 찾는다", 65);
```

### **시나리오 2: 전투**

```javascript
// 1. 적 발견 (판정 없음)
await performAction(sessionId, "복도 끝에 무언가를 발견한다");

// 2. 선제 공격 (민첩 판정)
await performActionWithRoll(sessionId, "재빨리 공격한다", "DEX", 15);

// 3. 회피 (CoC 판정)
await performCoCCheck(sessionId, "적의 공격을 피한다", 70);
```

---

## 📊 응답 데이터 구조

### **GamePlayResponse**

```typescript
interface GamePlayResponse {
  session_id: string;
  turn: number;
  player_action?: string;
  dice_result?: DiceRollResult;
  gm_response: string;
  character_state: {
    name: string;
    hp: number;
    maxHp: number;
    mp: number;
    maxMp: number;
    san: number;
    // ... 기타 캐릭터 정보
  };
  game_state: {
    location: string;
    flags: Record<string, any>;
    combat_active: boolean;
  };
  history: GameHistory[];
}
```

### **DiceRollResult**

```typescript
interface DiceRollResult {
  roll_type: "ability" | "coc" | "dice";
  result: number;
  success: boolean;
  details: Record<string, any>;
}
```

---

## 🧪 테스트

### **자동 테스트 실행**

```bash
python test_gameplay_api.py
```

### **Swagger UI**

```
http://localhost:8000/docs
```

**"gameplay" 섹션에서:**
- POST /api/gameplay/start
- POST /api/gameplay/action
- GET /api/gameplay/status/{session_id}
- GET /api/gameplay/history/{session_id}
- DELETE /api/gameplay/{session_id}

---

## 💡 팁

### **1. 히스토리 관리**

히스토리는 자동으로 저장됩니다. 별도로 관리할 필요 없음!

### **2. 판정 자동 인식**

AI GM이 "[판정 필요: DEX 12]" 같은 힌트를 주면, 프론트엔드에서 자동으로 판정 요청!

### **3. 에러 처리**

```javascript
try {
  const result = await performAction(sessionId, action);
} catch (error) {
  if (error.status === 404) {
    console.error("세션을 찾을 수 없습니다");
  } else if (error.status === 500) {
    console.error("서버 오류:", error.message);
  }
}
```

### **4. 실시간 업데이트**

WebSocket을 추가하면 여러 플레이어가 실시간으로 같은 게임을 플레이할 수 있습니다!

---

## 🎊 완료!

**통합 게임 플레이 API 사용 준비 완료!**

**다음 단계:**
1. 프론트엔드 UI 구현
2. 실시간 멀티플레이 (WebSocket)
3. 이미지 생성 추가
4. 음성 채팅 통합

---

**작성일**: 2026년 1월 26일  
**프로젝트**: LiTR - AI 기반 TRPG 플랫폼
