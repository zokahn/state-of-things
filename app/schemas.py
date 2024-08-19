from typing import List, Optional
from pydantic import BaseModel

from .schemas.project import Project, ProjectCreate, ProjectUpdate, ProjectBase
from .schemas.task import Task, TaskCreate, TaskUpdate, TaskBase
from .schemas.issue import Issue, IssueCreate, IssueBase
from .schemas.design_rule import DesignRule, DesignRuleCreate, DesignRuleBase
from .schemas.requirement import Requirement, RequirementCreate, RequirementBase
from .schemas.project_goal import ProjectGoal, ProjectGoalCreate, ProjectGoalBase
from .schemas.sbom import SBOM, SBOMCreate, SBOMBase

# Re-export all schemas
__all__ = [
    "Project", "ProjectCreate", "ProjectUpdate", "ProjectBase",
    "Task", "TaskCreate", "TaskUpdate", "TaskBase",
    "Issue", "IssueCreate", "IssueBase",
    "DesignRule", "DesignRuleCreate", "DesignRuleBase",
    "Requirement", "RequirementCreate", "RequirementBase",
    "ProjectGoal", "ProjectGoalCreate", "ProjectGoalBase",
    "SBOM", "SBOMCreate", "SBOMBase"
]

# Update ProjectRead to include tasks
class ProjectRead(ProjectBase):
    id: int
    tasks: List[Task] = []
    issues: List[Issue] = []
    design_rules: List[DesignRule] = []
    requirements: List[Requirement] = []
    goals: List[ProjectGoal] = []
    sbom: Optional[SBOM] = None

    class Config:
        orm_mode = True
