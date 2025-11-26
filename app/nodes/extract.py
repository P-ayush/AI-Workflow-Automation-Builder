from langchain_core.prompts import ChatPromptTemplate
from app.llm import chat
from app.state import WorkflowState
from app.schema.workflow_entities import WorkflowEntities

def extract_entities_node(state: WorkflowState) -> WorkflowState:
    normalized = state["normalized"]

    structured_chat = chat.with_structured_output(WorkflowEntities)

    prompt = ChatPromptTemplate.from_template(
        """
Extract workflow entities from the text.

You MUST return JSON that EXACTLY follows this schema:

triggers: list of objects with:
- name (string)
- when (string)
- match (string)

actions: list of objects with:
- name (string)
- do (string)

timeouts: list of objects with:
- name (string)
- after_minutes (integer)
- action (string)

RULES:
- NEVER omit any required field.
- NEVER return null.
- If something is not present, return an EMPTY LIST [].
- ALWAYS return keys: triggers, actions, timeouts.

Text:
{input}
"""
    )

    text_prompt = prompt.format(input=normalized)

    result: WorkflowEntities = structured_chat.invoke(text_prompt)

    return {"extracted_entities": result.dict()}
