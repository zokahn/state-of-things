#!/bin/bash

fix_file() {
    file_path=$1
    # Fix syntax errors and add missing imports
    if [[ $file_path == *"database.py" ]]; then
        sed -i '1ifrom sqlalchemy import create_engine\nfrom sqlalchemy.orm import sessionmaker\nfrom sqlalchemy.ext.declarative import declarative_base' "$file_path"
        sed -i '/^from/d' "$file_path"
    fi
    if [[ $file_path == *"models.py" ]]; then
        sed -i '1ifrom sqlalchemy import Column, Integer, String, DateTime, func\nfrom sqlalchemy.ext.declarative import declarative_base\n\nBase = declarative_base()' "$file_path"
        sed -i 's/Project(Base):/class Project(Base):/' "$file_path"
    fi
    if [[ $file_path == *"schemas.py" ]]; then
        sed -i '1ifrom pydantic import BaseModel\nfrom typing import Optional' "$file_path"
        sed -i 's/ProjectBase(BaseModel):/class ProjectBase(BaseModel):/' "$file_path"
    fi
    if [[ $file_path == *"test_fastapi.py" ]]; then
        sed -i '1ifrom fastapi import FastAPI\n' "$file_path"
    fi
    if [[ $file_path == *"main.py" ]]; then
        sed -i '1ifrom fastapi import FastAPI, Depends, HTTPException\nfrom sqlalchemy.orm import Session\nfrom . import crud, models, schemas\nfrom .database import SessionLocal, engine\n\nmodels.Base.metadata.create_all(bind=engine)\n\napp = FastAPI()' "$file_path"
        sed -i '/^Task as TaskModel/d' "$file_path"
        sed -i '/^Issue as IssueModel/d' "$file_path"
        sed -i '/^DesignRule as DesignRuleModel/d' "$file_path"
        sed -i '/^Requirement as RequirementModel/d' "$file_path"
        sed -i '/^ProjectGoal as ProjectGoalModel/d' "$file_path"
        sed -i '/^SBOM as SBOMModel/d' "$file_path"
        sed -i '/^Project as ProjectModel/d' "$file_path"
    fi

    # Fix indentation and add proper spacing
    sed -i 's/^[[:space:]]*//' "$file_path"
    sed -i 's/^class/\n\nclass/' "$file_path"
    sed -i 's/^def/\n\ndef/' "$file_path"

    # Remove unused imports
    sed -i '/^from.*import.*$/d' "$file_path"

    # Ensure file ends with a newline
    sed -i -e '$a\' "$file_path"
} \
# @@==>> SSHInteractiveSession End-of-Command  <<==@@
# Fix database.py
cat << 'EOF' > /root/project_notes_api/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./project_notes.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
