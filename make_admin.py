"""
유저를 관리자로 설정하는 스크립트
사용법: python make_admin.py <username>
"""

import sys
import logging
from database import SessionLocal
from models.user import User

logger = logging.getLogger("litr.make_admin")

def make_admin(username: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            logger.error("User '%s' not found", username)
            return

        if user.is_admin:
            logger.info("User '%s' is already an admin", username)
            return

        user.is_admin = True
        db.commit()
        logger.info("User '%s' (ID: %d) set as admin", username, user.id)
    finally:
        db.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    if len(sys.argv) < 2:
        logger.error("Usage: python make_admin.py <username>")
        sys.exit(1)

    make_admin(sys.argv[1])
