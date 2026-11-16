"""
migrate_friend_tags.py - 기존 유저의 friend_code를 4자리 숫자 태그로 마이그레이션
실행: python migrate_friend_tags.py

순서:
1. 기존 유저 중 유효하지 않은 friend_code를 가진 유저에게 새 4자리 태그 할당
2. 모든 데이터 변환 후 ALTER TABLE로 컬럼 크기 축소
"""

import os
import sys
import re
import secrets
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def is_valid_tag(code) -> bool:
    """4자리 숫자 태그인지 검증"""
    if not code:
        return False
    return bool(re.match(r'^\d{4}$', str(code)))


def get_unique_tag(used_tags: set) -> str:
    """사용되지 않은 고유 4자리 숫자 태그 생성"""
    for _ in range(200):
        num = secrets.randbelow(9999) + 1
        tag = str(num).zfill(4)
        if tag not in used_tags:
            return tag
    raise RuntimeError("고유 태그 생성 실패 - 태그 풀이 소진되었습니다.")


def run_migration():
    from database import SessionLocal
    from models.user import User
    from sqlalchemy import text

    db = SessionLocal()
    try:
        # Step 1: 모든 유저 조회
        all_users = db.query(User).all()
        logger.info(f"전체 유저 수: {len(all_users)}")

        # 이미 유효한 태그를 가진 유저의 태그 수집
        used_tags = set()
        for u in all_users:
            if is_valid_tag(u.friend_code):
                used_tags.add(u.friend_code)

        logger.info(f"이미 유효한 태그 보유: {len(used_tags)}명")

        # Step 2: 유효하지 않은 태그를 가진 유저에게 새 태그 할당
        migrated = 0
        skipped = 0

        for user in all_users:
            if is_valid_tag(user.friend_code):
                skipped += 1
                continue

            old_code = user.friend_code
            new_tag = get_unique_tag(used_tags)
            used_tags.add(new_tag)
            user.friend_code = new_tag
            migrated += 1

            logger.info(f"  유저 #{user.id} ({user.nickname}): '{old_code}' → '{new_tag}'")

            if migrated % 100 == 0:
                db.commit()
                logger.info(f"  중간 커밋: {migrated}명 처리됨")

        db.commit()
        logger.info(f"마이그레이션 완료 - 변환: {migrated}명, 스킵: {skipped}명")

        # Step 3: 컬럼 크기 축소 (모든 데이터가 4자리 이하인 상태에서)
        try:
            db.execute(text("ALTER TABLE users ALTER COLUMN friend_code TYPE VARCHAR(4)"))
            db.commit()
            logger.info("ALTER TABLE 완료: friend_code VARCHAR(4)로 축소")
        except Exception as alter_err:
            db.rollback()
            logger.warning(f"ALTER TABLE 실패 (무시 가능): {alter_err}")

    except Exception as e:
        db.rollback()
        logger.error(f"마이그레이션 실패: {e}", exc_info=True)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    logger.info("=== 친구 태그 마이그레이션 시작 ===")
    run_migration()
    logger.info("=== 마이그레이션 완료 ===")
