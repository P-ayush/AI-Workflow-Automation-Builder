import json
import re
from app.llm import chat
from langchain_core.prompts import ChatPromptTemplate
from app.state import WorkflowState


def extract_entities_node(state: WorkflowState) -> WorkflowState:
    normalized = state["normalized"]

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Extract workflow entities from the text.\n"
            "Return ONLY valid JSON. No markdown, no explanation.\n\n"
            "STRICT RULES:\n"
            "- ALWAYS return keys: triggers, actions, timeouts\n"
            "- Each trigger MUST be an object with:\n"
            "    name: string\n"
            "    when: string\n"
            "    match: string ONLY\n"
            "- Each action MUST be an object with:\n"
            "    name: string\n"
            "    do: string ONLY\n"
            "- Each timeout MUST be an object with:\n"
            "    name: string\n"
            "    after_minutes: number\n"
            "    action: string\n"
            "- DO NOT return explanations.\n"
        ),
        ("human", "Text:\n{input}\n\nReturn ONLY JSON.")
    ])

    messages = prompt.format_messages(input=normalized)
    raw = chat.invoke(messages).content.strip()

    raw = raw.replace("```json", "").replace("```", "").strip()

    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if not match:
        raise ValueError(f"LLM did not return valid JSON:\n{raw}")

    json_str = match.group(0)

    try:
        parsed = json.loads(json_str)
    except Exception as e:
        raise ValueError(f"JSON parsing failed:\n{json_str}\nError: {e}")

    return {"extracted_entities": parsed}
