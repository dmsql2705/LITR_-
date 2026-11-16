"""
데이터베이스 초기화 스크립트
PostgreSQL (Supabase) 연결을 확인하고 테이블을 생성합니다.
"""

import os
import logging
from dotenv import load_dotenv
from sqlalchemy import text

logger = logging.getLogger("litr.init_db")

load_dotenv()


def main():
    logger.info("=" * 50)
    logger.info("LiTR Database Initialization (PostgreSQL)")
    logger.info("=" * 50)

    # 환경변수 확인
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        logger.error("DATABASE_URL environment variable is not set.")
        logger.error("Set it in .env: DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres")
        return

    # 연결 문자열 마스킹 (보안)
    masked_url = database_url
    if "@" in database_url:
        parts = database_url.split("@")
        if ":" in parts[0]:
            prefix = parts[0].rsplit(":", 1)[0]
            masked_url = f"{prefix}:****@{parts[1]}"

    logger.info("Database URL: %s", masked_url)

    # 연결 테스트
    logger.info("Testing PostgreSQL connection...")

    try:
        from database import engine, init_db

        # 연결 테스트
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        logger.info("PostgreSQL connection successful")

    except Exception as e:
        logger.error("Database connection failed: %s", e)
        logger.error("Check: 1) DATABASE_URL is correct 2) Supabase project is active 3) Network connection")
        return

    # 테이블 생성 확인
    logger.info("Checking database tables...")

    try:
        init_db()
        logger.info("Database initialization complete")
        logger.info("Created tables: users, game_sessions")
        logger.info("Server is ready. Run: uvicorn main:app --reload")

    except Exception as e:
        logger.error("Table creation failed: %s", e)
        logger.info("Consider creating tables directly in Supabase SQL Editor")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    main()
