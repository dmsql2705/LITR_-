"""
데이터베이스 조회 스크립트
실행: python view_database.py
"""

import logging
from database import SessionLocal
from models.user import User
from models.game_session import GameSession
from datetime import datetime

logger = logging.getLogger("litr.view_database")


def view_users():
    """모든 회원 조회"""
    logger.info("=" * 80)
    logger.info("User List")
    logger.info("=" * 80)

    db = SessionLocal()
    users = db.query(User).all()

    if not users:
        logger.warning("No registered users found")
        db.close()
        return

    logger.info("Total %d users", len(users))

    for user in users:
        logger.info(
            "[User ID: %d] email=%s, username=%s, nickname=%s, credits=%s, followers=%s, oauth=%s, created=%s, last_login=%s, active=%s",
            user.id,
            user.email,
            user.username,
            user.nickname,
            user.credits,
            user.follow_count,
            user.oauth_provider or "email/password",
            user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else 'N/A',
            user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else 'N/A',
            'yes' if user.is_active else 'no',
        )

    db.close()


def view_game_sessions():
    """모든 게임 세션 조회"""
    logger.info("=" * 80)
    logger.info("Game Session List")
    logger.info("=" * 80)

    db = SessionLocal()
    sessions = db.query(GameSession).all()

    if not sessions:
        logger.warning("No saved game sessions found")
        db.close()
        return

    logger.info("Total %d game sessions", len(sessions))

    for session in sessions:
        player = "guest"
        if session.user:
            player = f"{session.user.username} ({session.user.nickname})"

        char = session.character_state or {}
        logger.info(
            "[Session: %s] player=%s, scenario=%s, character=%s, HP=%s/%s, MP=%s/%s, SAN=%s/%s, location=%s, turn=%d, created=%s, last_played=%s",
            session.session_id,
            player,
            session.scenario_title or session.scenario_id,
            session.character_name or session.character_id,
            char.get('hp', 'N/A'), char.get('max_hp', 'N/A'),
            char.get('mp', 'N/A'), char.get('max_mp', 'N/A'),
            char.get('san', 'N/A'), char.get('max_san', 'N/A'),
            session.location or 'N/A',
            session.turn,
            session.created_at.strftime('%Y-%m-%d %H:%M:%S') if session.created_at else 'N/A',
            session.last_played.strftime('%Y-%m-%d %H:%M:%S') if session.last_played else 'N/A',
        )

    db.close()


def view_stats():
    """통계 요약"""
    logger.info("=" * 80)
    logger.info("Database Statistics")
    logger.info("=" * 80)

    db = SessionLocal()

    # 회원 통계
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    oauth_users = db.query(User).filter(User.oauth_provider != None).count()
    jwt_users = total_users - oauth_users

    logger.info("Users: total=%d, active=%d, JWT=%d, OAuth=%d", total_users, active_users, jwt_users, oauth_users)

    # 게임 세션 통계
    total_sessions = db.query(GameSession).count()
    logger.info("Game sessions: total=%d", total_sessions)

    if total_users > 0:
        avg_sessions = total_sessions / total_users
        logger.info("Average sessions per user: %.1f", avg_sessions)

    db.close()


def delete_user(user_id: int):
    """회원 삭제 (주의!)"""
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        logger.error("User ID %d not found", user_id)
        db.close()
        return

    logger.warning("About to delete user: ID=%d, username=%s", user.id, user.username)

    confirm = input("\nAre you sure? (yes/no): ")

    if confirm.lower() == 'yes':
        db.delete(user)
        db.commit()
        logger.info("User deleted successfully")
    else:
        logger.info("Deletion cancelled")

    db.close()


def main():
    logger.info("=" * 80)
    logger.info("LiTR Database Management Tool")
    logger.info("=" * 80)

    while True:
        logger.info("Menu: 1=Users, 2=Sessions, 3=Stats, 4=Delete User, 0=Exit")

        choice = input("\nSelect: ").strip()

        if choice == "1":
            view_users()
        elif choice == "2":
            view_game_sessions()
        elif choice == "3":
            view_stats()
        elif choice == "4":
            user_id = input("User ID to delete: ").strip()
            try:
                delete_user(int(user_id))
            except ValueError:
                logger.error("Please enter a valid number")
        elif choice == "0":
            logger.info("Exiting")
            break
        else:
            logger.error("Please enter a valid option")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Exiting")
    except Exception as e:
        logger.error("Error: %s", str(e))
