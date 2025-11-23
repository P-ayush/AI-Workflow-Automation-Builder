from app.llm import chat
from langchain_core.prompts import ChatPromptTemplate

def normalize_instruction_node(state):
    instruction = state["instruction"]

    prompt = ChatPromptTemplate.from_messages([
        ("system", 
        "You rewrite user automation instructions into a clean, concise, "
        "numbered list without adding or removing meaning."),
        
        ("human",
        """
Normalize the automation instruction below.

RULES:
- Keep meaning EXACTLY the same.
- Convert to a clear numbered list.
- Do NOT add new logic.
- Do NOT explain anything.

Instruction:
{instruction}
        """
        )
    ])

    messages = prompt.format_messages(instruction=instruction)

    response = chat.invoke(messages)
    normalized = response.content.strip()

    return {
        **state,
        "normalized": normalized
    }
