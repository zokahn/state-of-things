
from sqlalchemy import create_engine
from app.models.models import Base
from app.db.database import SQLALCHEMY_DATABASE_URL

def run_migration():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(engine)
    print("Database schema updated successfully.")

if __name__ == "__main__":
    run_migration()
