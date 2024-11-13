from passlib.context import CryptContext
from fastapi import HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from adapters.database.models import User, UserRole
from adapters.database.repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()


class AuthService:
    """
    AuthService is a service class that provides
    authentication and user management functionality.
    """

    def __init__(self, repository: UserRepository):
        """
        :param repository: UserRepository instance to
        interact with the database
        """
        self.repository = repository

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify the plain password against the hashed password
        :param plain_password: str - plain text password
        :param hashed_password: str - hashed password
        """
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        Generate a hashed password
        :param password: str - plain text password
        """
        return pwd_context.hash(password)

    def get_user(self, username: str) -> User:
        """
        Retrieve a user by username
        :param username: str - username
        """
        return self.repository.get(username)

    def create_user(
        self, username: str, password: str, role: UserRole = UserRole.USER
    ) -> User:
        """
        Create a new user
        :param username: str - username
        :param password: str - plain text password
        :param role: UserRole - user role
        """
        if self.get_user(username):
            raise HTTPException(status_code=400, detail="Username already registered")

        hashed_password = self.get_password_hash(password)
        user = User(username=username, hashed_password=hashed_password, role=role)
        self.repository.save(user)
        return user

    def authenticate_user(self, credentials: HTTPBasicCredentials) -> User:
        """
        Authenticate a user using HTTPBasic credentials
        :param credentials: HTTPBasicCredentials - username and password
        """

        user = self.get_user(credentials.username)
        if not user or not self.verify_password(
            credentials.password, user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
        return user
