from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from adapters.database.models import UserRole
from adapters.database.repository import DatabaseUserRepository
from services.auth_service import AuthService
from core.config import config

engine = create_engine(config.DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_admin_user():
    """
    Create admin user if doesn't exist
    """

    # Use another session to create user
    db = SessionLocal()

    # Use auth service to create user
    user_repository = DatabaseUserRepository(db)
    auth_service = AuthService(user_repository)

    try:
        admin_username = config.ADMIN_USERNAME
        admin_password = config.ADMIN_PASSWORD

        # Check if admin exists
        if not auth_service.get_user(admin_username):
            auth_service.create_user(
                username=admin_username, password=admin_password, role=UserRole.ADMIN
            )
    except Exception as e:
        print(f"Error creating admin user: {e}")

    finally:
        db.close()
