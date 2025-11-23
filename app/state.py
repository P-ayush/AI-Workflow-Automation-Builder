from typing import TypedDict, Optional, Dict, Any

class WorkflowState(TypedDict, total=False):
    instruction: str               
    normalized: str               
    extracted_entities: Dict[str, Any] 
    dsl: Dict[str, Any]           
    errors: Optional[str]           
