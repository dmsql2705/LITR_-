"""
JSON 세이브 파일을 데이터베이스로 마이그레이션
saves/ 폴더의 모든 JSON 파일을 DB로 이전합니다.
"""

from pathlib import Path
import json
import logging
from database import SessionLocal, init_db
from models.game_session import GameSession
from datetime import datetime

logger = logging.getLogger("litr.migrate_to_db")


def migrate_json_to_db():
    """JSON 세이브 파일을 데이터베이스로 마이그레이션"""
    
    logger.info("JSON -> DB migration starting")

    # saves 폴더 확인
    saves_dir = Path(__file__).parent / "saves"

    if not saves_dir.exists():
        logger.error("saves/ directory does not exist. Nothing to migrate.")
        return

    json_files = list(saves_dir.glob("*.json"))

    if not json_files:
        logger.error("No JSON files in saves/ directory. Nothing to migrate.")
        return

    logger.info("Found %d save files", len(json_files))
    
    # 데이터베이스 세션 생성
    db = SessionLocal()
    
    success_count = 0
    error_count = 0
    
    try:
        for json_file in json_files:
            try:
                # JSON 파일 읽기
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                session_id = data.get("session_id")
                
                # 이미 DB에 있는지 확인
                existing = db.query(GameSession).filter(
                    GameSession.session_id == session_id
                ).first()
                
                if existing:
                    logger.info("Skipping %s: already exists in DB", session_id)
                    continue
                
                # 게임 세션 생성
                game_session = GameSession(
                    session_id=session_id,
                    scenario_id=data.get("scenario_id", "unknown"),
                    character_id=data.get("character_state", {}).get("character_id", "unknown"),
                    character_state=data.get("character_state", {}),
                    story_progress=data.get("story_progress", {}),
                    flags=data.get("flags", {}),
                    combat_state=data.get("combat_state"),
                    location=data.get("location", ""),
                    turn=data.get("turn", 0)
                )
                
                # 타임스탬프 설정
                if "last_saved" in data:
                    try:
                        game_session.last_played = datetime.fromisoformat(data["last_saved"])
                        game_session.updated_at = datetime.fromisoformat(data["last_saved"])
                    except:
                        pass
                
                db.add(game_session)
                db.commit()
                
                logger.info("Migration success: %s", session_id)
                success_count += 1
                
            except Exception as e:
                logger.error("Migration failed for %s: %s", json_file.name, str(e))
                error_count += 1
                db.rollback()
                continue
        
        logger.info("Migration complete: %d success, %d failed, %d total", success_count, error_count, len(json_files))

        if success_count > 0:
            logger.info("Database file: %s", Path(__file__).parent / "litrpg.db")
            logger.info("You can now use /api/game-db/* endpoints")
        
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    # 데이터베이스 초기화 (테이블 생성)
    logger.info("Creating database tables...")
    init_db()

    # 마이그레이션 실행
    migrate_json_to_db()
