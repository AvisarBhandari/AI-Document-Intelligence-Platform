import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db

# In-memory SQLite database for fast, isolated test layers
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session", autouse=True)
def test_db_engine():
    """Creates the structural schema fields once per testing suite session."""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    # Generateing table from SQLAlchemy Base methadata
    Base.metadata.create_all(bind=engine)

    yield engine

    # Drop everything clean when all tests are finished
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_db_engine):
    """Provides a clean database transaction session for a single test case,

    then rolls back changes to prevent cross-test contamination.
    """
    connection = test_db_engine.connect()
    transaction = connection.begin()

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()

    # Override the FastAPI production dependency globally for this test
    def override_get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    yield session

    # Tear down session and rollback mutations safely
    session.close()
    transaction.rollback()
    connection.close()

    # Clear the override for safety
    app.dependency_overrides.pop(get_db, None)
