"""Initialize database with admin user and sample data."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session

from app.config.database import SessionLocal, engine, Base
from app.models.user import User
from app.utils.security import get_password_hash


def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully")


def init_admin_user(db: Session) -> None:
    """Create initial admin user.

    Args:
        db: Database session
    """
    # Check if admin user already exists
    existing_admin = db.query(User).filter(User.username == "admin").first()

    if existing_admin:
        print("⚠ Admin user already exists, skipping...")
        return

    # Create admin user
    admin_user = User(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("admin123"),
        full_name="系统管理员",
        role="admin",
        is_active=True,
    )

    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    print(f"✓ Admin user created successfully")
    print(f"  Username: admin")
    print(f"  Password: admin123")
    print(f"  Role: admin")


def init_db():
    """Initialize database with tables and initial data."""
    print("\n" + "=" * 50)
    print("Database Initialization")
    print("=" * 50 + "\n")

    # Create tables
    create_tables()

    # Create database session
    db = SessionLocal()

    try:
        # Initialize admin user
        print("\nInitializing admin user...")
        init_admin_user(db)

        print("\n" + "=" * 50)
        print("Database initialization completed successfully!")
        print("=" * 50 + "\n")

    except Exception as e:
        print(f"\n✗ Error during initialization: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
