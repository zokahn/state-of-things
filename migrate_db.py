
from sqlalchemy import create_engine
from app.db.database import SQLALCHEMY_DATABASE_URL
from app.models.models import Base
from app.models.models import Project  # Make sure to import all model classes here

def run_migration():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(engine)
    print("Database schema updated successfully.")

if __name__ == "__main__":
    run_migration()
