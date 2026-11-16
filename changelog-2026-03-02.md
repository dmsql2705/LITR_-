# 변경사항 정리 — 2026-03-02

## 수정 파일
- `litr-frontend/src/components/game/GameView.tsx`
- `litr-frontend/src/components/game/GameModals.tsx`
- `litr-frontend/src/styles/game.module.css`

---

## 1. TT모드 이모티콘 바 제거 → 캐릭터 추가로 교체

### 제거
- `ttEmoteBar` (😊, 😱, 🤔, 😡, 😢, 🎉, 💀, ⚔️ 이모지 퀵 버튼) 삭제

### 변경
- 캐릭터 칩 바(`vnCharChipBar`) 표시 조건을 `ttTab === 'main' && selectedCharacter` → `ttTab === 'main'`으로 변경
- 캐릭터가 선택되지 않아도 **캐릭터 추가(+) 버튼**이 항상 노출되도록 수정

---

## 2. 툴바 툴팁 위치 수정

### 문제
- ✋(선택/이동), 👁(FOW) 등 툴바 버튼의 `data-tip` 툴팁이 오른쪽으로 나와 잘림

### 수정 (game.module.css)
- 툴팁 위치를 **버튼 오른쪽 → 버튼 아래쪽**으로 변경
  - `left: calc(100% + 8px)` → `left: 50%`
  - `top: 50%` → `top: calc(100% + 8px)`
  - `transform: translateY(-50%)` → `transform: translateX(-50%)`

---

## 3. 전장 안개(FOW) 기능 전체 삭제

### 제거된 항목
- **상태 변수**: `ttFowEnabled`, `ttFowDataRef`, `ttFogSettingsOpen`, `ttFogMode`, `ttFogVisionRadius`
- **캔버스 렌더링**: `drawTtGrid` 내 FOW 오버레이 코드 (수동 안개 + 자동 시야)
- **이벤트 핸들러**: Shift+클릭 FOW 브러시 로직
- **툴바 버튼**: Eye/EyeOff 전장 안개 토글 버튼
- **"+" 메뉴 항목**: 전장 안개 설정 메뉴
- **모달**: `FogSettingsModal` (안개/자동 시야 설정 창) — GameModals.tsx에 코드는 남아있으나 사용처 없음
- **CSS**: `.ttFowOverlay` 스타일
- **미사용 import**: `Eye`, `EyeOff` (lucide-react)

---

## 4. 손(✋) 버튼 제거

### 제거
- 툴바의 ✋ 선택/이동 버튼 삭제

### 수정
- `ttToolBar`가 빈 상태로 렌더되어 빈 박스가 보이던 문제 수정
- 💬(대사창 열기) 버튼이 있을 때만 `ttToolBar` 자체가 렌더되도록 조건 변경
