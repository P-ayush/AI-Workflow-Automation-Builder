from app.llm import chat
from langchain_core.prompts import ChatPromptTemplate
from app.state import WorkflowState

   
def generate_dsl_node(state):
    entities = state["extracted_entities"]

    triggers = entities["triggers"]
    actions = entities["actions"]
    timeouts = entities["timeouts"]

    action_names = [a["name"] for a in actions]

    linked_triggers = []
    for t in triggers:
        linked_triggers.append({
            **t,
            "actions": action_names
        })

    dsl = {
        "triggers": linked_triggers,
        "actions": [
            {
                "name": a["name"],
                "type": "custom",
                "description": a["do"]
            }
            for a in actions
        ],
        "timeouts": timeouts
    }

    return {**state, "dsl": dsl}
