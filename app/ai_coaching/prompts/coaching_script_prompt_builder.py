from app.ai_coaching.prompts.prompt_constants import OPTION_TYPE_INSTRUCTIONS
from typing import Protocol, Sequence

class MessageLike(Protocol):
    role: str
    message: str

def build_coaching_script_prompt(
    option_type: str,
    place_name: str,
    country: str,
    city: str,
    place_address: str,
    scenario_prompt: str,
    evaluation: str,
    previous_messages: Sequence[MessageLike],
) -> str:
    option_instruction = OPTION_TYPE_INSTRUCTIONS.get(
        option_type,
        "Create a practical coaching dialogue.",
    )

    previous_message_text = "\n".join(
        [f"{message.role}: {message.message}" for message in previous_messages]
    ) or "No previous messages."

    role = """
You are an English speaking coach for a language learning app.
You create short, practical speaking practice scripts based on place and scenario context.
"""

    instruction = """
Return ONLY valid JSON.
Do not include markdown.
Do not include extra explanation.

Rules:
- Create 4 to 6 messages.
- The first message must be ASSISTANT.
- Alternate ASSISTANT and USER.
- USER messages are sample answers for the learner.
- Use natural spoken English.
- Keep each message short.
- Keep the dialogue related to the given place and scenario.
"""

    context = f"""
[Option Type]
{option_type}

[Option Instruction]
{option_instruction}

[Place Context]
placeName: {place_name}
country: {country}
city: {city}
placeAddress: {place_address}

[Scenario Prompt]
{scenario_prompt}

[Previous Map Learning Evaluation]
{evaluation}

[Previous Map Learning Messages]
{previous_message_text}
"""

    output_format = """
[Output JSON Format]
{
  "messages": [
  {"role":"ASSISTANT","message":"..."},
  {"role":"USER","message":"..."},
  {"role":"ASSISTANT","message":"..."},
  {"role":"USER","message":"..."}
]
}
"""

    return f"""
{role}

{instruction}

{context}

{output_format}
""".strip()