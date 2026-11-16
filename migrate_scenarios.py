"""
시나리오 마이그레이션 스크립트
로컬 JSON 파일의 시나리오를 Supabase DB로 마이그레이션합니다.
"""

import json
import logging
from pathlib import Path
from datetime import datetime, timezone

# 프로젝트 루트 설정
import sys
sys.path.insert(0, str(Path(__file__).parent))

logger = logging.getLogger("litr.migrate_scenarios")

from database import SessionLocal
from models.scenario import Scenario


def migrate_scenarios():
    """scenarios 폴더의 JSON 파일들을 DB로 마이그레이션"""
    scenarios_dir = Path(__file__).parent / "scenarios"

    if not scenarios_dir.exists():
        logger.warning("scenarios directory does not exist")
        return

    db = SessionLocal()
    migrated = 0
    skipped = 0
    errors = 0

    try:
        for file_path in scenarios_dir.glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                scenario_id = data.get("id")
                if not scenario_id:
                    logger.warning("Skipping %s: no ID", file_path.name)
                    skipped += 1
                    continue

                # 이미 DB에 있는지 확인
                existing = db.query(Scenario).filter(Scenario.id == scenario_id).first()
                if existing:
                    logger.info("Skipping %s: already exists in DB", scenario_id)
                    skipped += 1
                    continue

                # Scenario 객체 생성
                now = datetime.now(timezone.utc)
                scenario = Scenario(
                    id=scenario_id,
                    user_id=data.get("user_id"),
                    title=data.get("title", "제목 없음"),
                    description=data.get("description", ""),
                    genre=data.get("genre", []),
                    difficulty=data.get("difficulty", "보통"),
                    playtime=data.get("playtime", ""),
                    content=data,  # 전체 JSON 저장
                    visibility=data.get("visibility", "public"),
                    author=data.get("author", ""),
                    created_at=now,
                    updated_at=now,
                )

                db.add(scenario)
                db.commit()
                logger.info("Migrated: %s", scenario_id)
                migrated += 1

            except json.JSONDecodeError as e:
                logger.error("JSON parse error in %s: %s", file_path.name, e)
                errors += 1
            except Exception as e:
                logger.error("Error in %s: %s", file_path.name, e)
                db.rollback()
                errors += 1

    finally:
        db.close()

    logger.info("Migration complete: %d migrated, %d skipped, %d errors", migrated, skipped, errors)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    logger.info("Starting scenario migration...")
    migrate_scenarios()
