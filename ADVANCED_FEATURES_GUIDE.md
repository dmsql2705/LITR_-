# 🚀 고급 기능 가이드

**LiTR 백엔드 고급 기능 3종 세트**

1. **이미지 생성** - AI로 게임 장면 시각화
2. **실시간 멀티플레이** - WebSocket 기반 동시 플레이
3. **음성 채팅** - Agora RTC 음성 통신

---

## 📦 **설치 및 설정**

### **1. 패키지 설치**

```bash
pip install -r requirements.txt
```

**새로 추가된 패키지:**
- `openai==1.12.0` - DALL-E 3 이미지 생성
- `websockets==12.0` - WebSocket 지원
- `pillow==10.2.0` - 이미지 처리
- `aiofiles==23.2.1` - 비동기 파일 처리
- `agora-token-builder==1.0.0` - Agora 토큰 생성

### **2. 환경 변수 설정**

`.env` 파일에 다음을 추가:

```env
# 이미지 생성 (DALL-E 3)
OPENAI_API_KEY=your-openai-api-key

# 음성 채팅 (Agora)
AGORA_APP_ID=your-agora-app-id
AGORA_APP_CERTIFICATE=your-agora-certificate
```

---

## 🎨 **1. 이미지 생성 (DALL-E 3)**

### **개요**

AI를 사용하여 게임 장면을 시각화하는 이미지를 자동 생성합니다.

### **API 엔드포인트**

#### **이미지 생성**

```
POST /api/image/generate
```

**요청:**
```json
{
  "prompt": "a dark abandoned school hallway at night",
  "style": "horror",
  "size": "1024x1024",
  "quality": "standard"
}
```

**응답:**
```json
{
  "success": true,
  "image_url": "https://...",
  "revised_prompt": "Enhanced prompt...",
  "local_path": "generated_images/scene_1737871234.png",
  "generation_time": 15.3
}
```

#### **게임 장면 이미지 생성**

```
POST /api/image/scene
```

**요청:**
```json
{
  "session_id": "game_1737871234",
  "scene_description": "어두운 학교 복도, 깜빡이는 형광등",
  "include_character": true,
  "style": "horror"
}
```

#### **이미지 목록 조회**

```
GET /api/image/list
```

#### **이미지 스타일 목록**

```
GET /api/image/styles
```

**지원 스타일:**
- `fantasy` - 에픽 판타지
- `horror` - 호러
- `realistic` - 사실적
- `anime` - 애니메이션
- `cyberpunk` - 사이버펑크
- `steampunk` - 스팀펑크

### **JavaScript 예시**

```javascript
// 이미지 생성
async function generateSceneImage(sessionId, sceneDescription) {
    const response = await fetch('/api/image/scene', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            session_id: sessionId,
            scene_description: sceneDescription,
            style: 'fantasy',
            include_character: true
        })
    });
    
    const result = await response.json();
    
    if (result.success) {
        // 이미지 표시
        document.getElementById('scene-image').src = result.image_url;
        console.log('생성 시간:', result.generation_time, '초');
    }
}
```

### **비용**

- DALL-E 3 Standard (1024x1024): $0.040/장
- DALL-E 3 HD (1024x1024): $0.080/장

---

## 👥 **2. 실시간 멀티플레이 (WebSocket)**

### **개요**

여러 플레이어가 동시에 같은 게임 세션에 접속하여 실시간으로 플레이합니다.

### **WebSocket 연결**

```
ws://localhost:8000/api/multiplayer/ws/{session_id}?player_name=PlayerName&user_id=1
```

### **메시지 형식**

#### **클라이언트 → 서버**

```javascript
// 플레이어 행동
{
  "type": "action",
  "content": "문을 연다"
}

// 일반 채팅
{
  "type": "chat",
  "content": "안녕하세요!"
}

// 타이핑 중 표시
{
  "type": "typing",
  "is_typing": true
}

// 다이스 굴림 공유
{
  "type": "dice_roll",
  "roll_type": "d20",
  "result": 15,
  "success": true
}
```

#### **서버 → 클라이언트**

```javascript
// 플레이어 입장
{
  "type": "player_joined",
  "player_name": "Player1",
  "timestamp": "2026-01-26T15:30:00",
  "total_players": 3
}

// 플레이어 퇴장
{
  "type": "player_left",
  "player_name": "Player1",
  "timestamp": "2026-01-26T16:00:00",
  "total_players": 2
}

// 플레이어 행동 브로드캐스트
{
  "type": "action",
  "player_name": "Player1",
  "content": "문을 연다",
  "timestamp": "2026-01-26T15:35:00"
}

// GM 응답
{
  "type": "gm_response",
  "content": "문이 삐걱거리며 열린다...",
  "timestamp": "2026-01-26T15:35:05"
}
```

### **JavaScript 클라이언트 예시**

```javascript
class MultiplayerClient {
    constructor(sessionId, playerName, userId = null) {
        this.sessionId = sessionId;
        this.playerName = playerName;
        this.userId = userId;
        this.ws = null;
    }
    
    connect() {
        const url = `ws://localhost:8000/api/multiplayer/ws/${this.sessionId}?player_name=${this.playerName}${this.userId ? '&user_id=' + this.userId : ''}`;
        
        this.ws = new WebSocket(url);
        
        this.ws.onopen = () => {
            console.log('멀티플레이 연결됨');
        };
        
        this.ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            this.handleMessage(message);
        };
        
        this.ws.onclose = () => {
            console.log('멀티플레이 연결 종료');
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket 오류:', error);
        };
    }
    
    handleMessage(message) {
        switch (message.type) {
            case 'connected':
                console.log('연결 성공:', message.message);
                this.updatePlayerList(message.players);
                break;
            
            case 'player_joined':
                console.log(`${message.player_name}님이 입장했습니다.`);
                this.showNotification(`${message.player_name} 입장`);
                break;
            
            case 'player_left':
                console.log(`${message.player_name}님이 퇴장했습니다.`);
                break;
            
            case 'action':
                this.displayPlayerAction(message.player_name, message.content);
                break;
            
            case 'chat':
                this.displayChatMessage(message.player_name, message.message);
                break;
            
            case 'gm_response':
                this.displayGmResponse(message.content);
                break;
            
            case 'typing':
                this.showTypingIndicator(message.player_name, message.is_typing);
                break;
        }
    }
    
    sendAction(action) {
        this.ws.send(JSON.stringify({
            type: 'action',
            content: action
        }));
    }
    
    sendChat(message) {
        this.ws.send(JSON.stringify({
            type: 'chat',
            content: message
        }));
    }
    
    sendTyping(isTyping) {
        this.ws.send(JSON.stringify({
            type: 'typing',
            is_typing: isTyping
        }));
    }
    
    disconnect() {
        if (this.ws) {
            this.ws.close();
        }
    }
    
    // UI 업데이트 메서드들
    updatePlayerList(players) { /* ... */ }
    showNotification(text) { /* ... */ }
    displayPlayerAction(player, action) { /* ... */ }
    displayChatMessage(player, message) { /* ... */ }
    displayGmResponse(response) { /* ... */ }
    showTypingIndicator(player, isTyping) { /* ... */ }
}

// 사용 예시
const client = new MultiplayerClient('game_1737871234', 'Player1', 1);
client.connect();

// 행동 전송
client.sendAction('문을 조심스럽게 연다');

// 채팅 전송
client.sendChat('여기 뭔가 있어!');
```

### **REST API 엔드포인트**

#### **활성 세션 목록**

```
GET /api/multiplayer/sessions
```

**응답:**
```json
{
  "total_sessions": 2,
  "total_players": 5,
  "sessions": [
    {
      "session_id": "game_1737871234",
      "player_count": 3,
      "players": [...]
    }
  ]
}
```

#### **세션 플레이어 목록**

```
GET /api/multiplayer/session/{session_id}/players
```

#### **서버에서 메시지 브로드캐스트**

```
POST /api/multiplayer/session/{session_id}/broadcast
```

---

## 🎤 **3. 음성 채팅 (Agora RTC)**

### **개요**

Agora RTC를 사용하여 게임 중 실시간 음성 통화를 제공합니다.

### **Agora 설정**

1. [Agora.io](https://www.agora.io/)에서 계정 생성
2. 프로젝트 생성
3. App ID와 App Certificate 복사
4. `.env` 파일에 추가

### **API 엔드포인트**

#### **음성 토큰 생성**

```
POST /api/voice/token
```

**요청:**
```json
{
  "channel_name": "game_1737871234",
  "user_id": "player_123",
  "role": 1
}
```

**응답:**
```json
{
  "token": "007eJxT...",
  "app_id": "your_app_id",
  "channel_name": "game_1737871234",
  "uid": "12345678",
  "expire_time": 86400,
  "expire_at": "2026-01-27T15:30:00"
}
```

#### **게임 세션 음성 채널 시작**

```
POST /api/voice/session/start?session_id=game_123&player_name=Player1
```

#### **Agora 설정 확인**

```
GET /api/voice/config
```

### **JavaScript 클라이언트 (Agora SDK)**

```html
<!-- Agora SDK -->
<script src="https://download.agora.io/sdk/release/AgoraRTC_N.js"></script>
```

```javascript
class VoiceChat {
    constructor() {
        this.client = null;
        this.localAudioTrack = null;
    }
    
    async initialize(appId, channel, token, uid) {
        // Agora 클라이언트 생성
        this.client = AgoraRTC.createClient({ 
            mode: "rtc", 
            codec: "vp8" 
        });
        
        // 채널 참가
        await this.client.join(appId, channel, token, uid);
        
        // 마이크 활성화
        this.localAudioTrack = await AgoraRTC.createMicrophoneAudioTrack();
        await this.client.publish([this.localAudioTrack]);
        
        // 다른 사용자 구독
        this.client.on("user-published", async (user, mediaType) => {
            await this.client.subscribe(user, mediaType);
            if (mediaType === "audio") {
                user.audioTrack.play();
            }
        });
        
        console.log('음성 채팅 연결됨');
    }
    
    async mute() {
        if (this.localAudioTrack) {
            await this.localAudioTrack.setEnabled(false);
        }
    }
    
    async unmute() {
        if (this.localAudioTrack) {
            await this.localAudioTrack.setEnabled(true);
        }
    }
    
    async leave() {
        if (this.localAudioTrack) {
            this.localAudioTrack.close();
        }
        if (this.client) {
            await this.client.leave();
        }
    }
}

// 사용 예시
async function startVoiceChat(sessionId, playerName) {
    // 1. 백엔드에서 토큰 받기
    const response = await fetch('/api/voice/session/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            session_id: sessionId,
            player_name: playerName
        })
    });
    
    const { app_id, channel_name, token, uid } = await response.json();
    
    // 2. Agora 연결
    const voiceChat = new VoiceChat();
    await voiceChat.initialize(app_id, channel_name, token, uid);
    
    return voiceChat;
}

// 음성 채팅 시작
const voiceChat = await startVoiceChat('game_1737871234', 'Player1');

// 음소거
await voiceChat.mute();

// 음소거 해제
await voiceChat.unmute();

// 퇴장
await voiceChat.leave();
```

---

## 🧪 **테스트**

### **자동 테스트 실행**

```bash
# 서버 실행
uvicorn main:app --reload

# 새 터미널에서 테스트
python test_advanced_features.py
```

### **Swagger UI**

```
http://localhost:8000/docs
```

**새로 추가된 섹션:**
- `image` - 이미지 생성
- `multiplayer` - 멀티플레이
- `voice` - 음성 채팅

---

## 📊 **비용 및 제한사항**

### **이미지 생성 (OpenAI)**
- DALL-E 3: $0.040 ~ $0.120/장
- 생성 시간: 10-30초
- 동시 요청 제한: 계정별 상이

### **음성 채팅 (Agora)**
- 무료: 10,000분/월
- 이후: $0.99/1,000분
- 동시 접속: 무제한

### **멀티플레이 (WebSocket)**
- 무료 (자체 서버)
- 동시 접속: 서버 성능에 따라

---

## 🎯 **통합 예시**

### **완전한 멀티플레이 게임 세션**

```javascript
// 1. 게임 시작
const game = await startGame('horror_school', 'detective_k');
const sessionId = game.session_id;

// 2. 멀티플레이 연결
const mp = new MultiplayerClient(sessionId, 'Player1', userId);
mp.connect();

// 3. 음성 채팅 시작
const voice = await startVoiceChat(sessionId, 'Player1');

// 4. 플레이어 행동
mp.sendAction('문을 연다');

// 5. 이미지 생성 (장면 시각화)
const image = await generateSceneImage(sessionId, game.gm_response);
document.getElementById('scene').src = image.image_url;

// 6. 채팅
mp.sendChat('와, 여기 무섭다!');

// 7. 종료
mp.disconnect();
await voice.leave();
```

---

## 🚀 **프로덕션 배포**

### **환경 변수 설정**

```env
# API Keys
OPENAI_API_KEY=sk-...
AGORA_APP_ID=...
AGORA_APP_CERTIFICATE=...

# 보안
JWT_SECRET_KEY=super-secret-key
```

### **서버 설정**

```bash
# HTTPS 필수 (WebSocket + 음성 채팅)
uvicorn main:app --host 0.0.0.0 --port 443 --ssl-keyfile key.pem --ssl-certfile cert.pem
```

### **CORS 설정**

```python
# main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📝 **FAQ**

### **Q: 이미지 생성이 느립니다**
A: DALL-E 3는 10-30초 소요됩니다. 백그라운드 처리나 캐싱을 고려하세요.

### **Q: WebSocket이 자주 끊깁니다**
A: 네트워크 안정성을 확인하고, 재연결 로직을 추가하세요.

### **Q: 음성이 안 들립니다**
A: 브라우저 마이크 권한과 Agora 설정을 확인하세요.

### **Q: 비용이 걱정됩니다**
A: 이미지는 필요할 때만 생성하고, Agora 무료 티어를 활용하세요.

---

## 🎊 **완료!**

**3가지 고급 기능이 모두 구현되었습니다!**

- ✅ AI 이미지 생성
- ✅ 실시간 멀티플레이
- ✅ 음성 채팅

---

**작성일**: 2026년 1월 26일  
**프로젝트**: LiTR - AI 기반 TRPG 플랫폼
