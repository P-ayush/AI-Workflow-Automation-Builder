from pydantic import BaseModel
from typing import List, Optional

class Trigger(BaseModel):
    name: str
    when: str
    match: str

class Action(BaseModel):
    name: str
    do: str

class Timeout(BaseModel):
    name: str
    after_minutes: int
    action: str

class WorkflowEntities(BaseModel):
    triggers: List[Trigger]
    actions: List[Action]
    timeouts: List[Timeout]