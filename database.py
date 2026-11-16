"""
데이터베이스 설정 및 연결
PostgreSQL (Supabase) 데이터베이스를 사용합니다.
"""

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("litr.database")

# 데이터베이스 URL (환경변수에서 가져오기)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL 환경변수가 설정되지 않았습니다.")

# 커넥션 풀 설정 (Supabase 무료 티어: 총 60 연결 제한, 환경변수로 조정 가능)
POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))
MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))
POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))
POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "1800"))  # 30분

# SQLAlchemy 엔진 생성
if DATABASE_URL.startswith("sqlite"):
    # SQLite는 커넥션 풀 설정이 다름
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False,
    )
else:
    # PostgreSQL (Supabase) 설정
    engine = create_engine(
        DATABASE_URL,
        pool_size=POOL_SIZE,
        max_overflow=MAX_OVERFLOW,
        pool_timeout=POOL_TIMEOUT,
        pool_recycle=POOL_RECYCLE,
        pool_pre_ping=True,
        echo=False,
    )

# 세션 팩토리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 (모든 모델의 부모)
Base = declarative_base()


# 데이터베이스 세션 의존성
def get_db():
    """
    데이터베이스 세션을 생성하고 요청 종료 시 닫습니다.
    FastAPI의 Depends()와 함께 사용됩니다.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# 데이터베이스 초기화
def init_db():
    """
    모든 테이블을 생성합니다. (이미 존재하는 테이블은 건너뜁니다)
    프로덕션에서는 Alembic 마이그레이션을 사용하세요:
        alembic upgrade head
    """
    from models import user, game_session, friendship, notification  # 모델 import
    from models import analytics, transaction  # 활동 분석 + 크레딧 트랜잭션 모델
    from models.scenario import Scenario  # 시나리오 모델
    from models.character import Character  # 캐릭터 모델
    Base.metadata.create_all(bind=engine, checkfirst=True)

    # 누락 컬럼 자동 마이그레이션
    _migrate_missing_columns()

    logger.info("데이터베이스 테이블 초기화 완료 (pool_size=%d, max_overflow=%d)", POOL_SIZE, MAX_OVERFLOW)


def _migrate_missing_columns():
    """기존 테이블에 누락된 컬럼이 있으면 ALTER TABLE로 추가합니다."""
    migrations = [
        ("users", "follower_count", "INTEGER DEFAULT 0"),
        ("users", "deleted_at", "TIMESTAMP"),
    ]

    # 컬럼 타입 변경 마이그레이션 (table, column, new_type)
    type_migrations = [
        ("characters", "image_url", "TEXT"),  # varchar(500) → TEXT (data URL 지원)
    ]

    inspector = inspect(engine)
    with engine.begin() as conn:
        for table_name, col_name, col_type in migrations:
            if not inspector.has_table(table_name):
                continue
            existing = [c["name"] for c in inspector.get_columns(table_name)]
            if col_name not in existing:
                conn.execute(text(f'ALTER TABLE "{table_name}" ADD COLUMN "{col_name}" {col_type}'))
                logger.info("마이그레이션: %s.%s 컬럼 추가됨", table_name, col_name)

        # 컬럼 타입 변경 (SQLite는 ALTER COLUMN TYPE 미지원이므로 건너뜀)
        if not DATABASE_URL.startswith("sqlite"):
            for table_name, col_name, new_type in type_migrations:
                if not inspector.has_table(table_name):
                    continue
                columns = inspector.get_columns(table_name)
                for col in columns:
                    if col["name"] == col_name:
                        col_type_str = str(col["type"])
                        # VARCHAR → TEXT 변경이 필요한 경우
                        if "VARCHAR" in col_type_str.upper() and new_type.upper() == "TEXT":
                            conn.execute(text(
                                f'ALTER TABLE "{table_name}" ALTER COLUMN "{col_name}" TYPE {new_type}'
                            ))
                            logger.info("마이그레이션: %s.%s 타입 변경 %s → %s", table_name, col_name, col_type_str, new_type)
                        break


# 데이터베이스 삭제 (개발용)
def drop_db():
    """
    모든 테이블을 삭제합니다. (주의!)
    """
    Base.metadata.drop_all(bind=engine)
    logger.warning("모든 데이터베이스 테이블이 삭제되었습니다.")
