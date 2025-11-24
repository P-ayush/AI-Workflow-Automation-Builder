from app.llm import chat
from langchain_core.prompts import ChatPromptTemplate
from app.state import WorkflowState

   
def generate_dsl_node(state: WorkflowState):
    entities = state["extracted_entities"]

    workflow = {
        "triggers": [],
        "actions": [],
        "timeouts": []
    }

    for t in entities.get("triggers", []):
        workflow["triggers"].append({
            "name": t.get("name", "trigger_1"),
            "when": t.get("when", ""),
            "match": t.get("match", ""),
            "actions": []   
        })

    for a in entities.get("actions", []):
        workflow["actions"].append({
            "name": a.get("name", "action_1"),
            "type": "custom",
            "description": a.get("do", "")
        })

    for tm in entities.get("timeouts", []):
        workflow["timeouts"].append({
            "name": tm.get("name", "timeout_1"),
            "after_minutes": tm.get("after_minutes", 0),
            "action": tm.get("action", "")
        })

    return {
        **state,
        "dsl": workflow
    }
