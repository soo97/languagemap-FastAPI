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
    - The output must be based on the previous map learning messages.
    - Do not ignore the previous dialogue.
    - Keep the dialogue related to the given place and scenario.
    - The first message must be ASSISTANT.
    - Alternate ASSISTANT and USER.
    - USER messages are sample answers for the learner.
    - Use natural spoken English.
    - Keep each message short.

    Important:
    - USER messages are not fixed answers.
    - USER messages must also be rewritten according to the selected optionType.
    - For WORD option, every USER message should contain at least one vocabulary upgrade.
    - Do not copy previous USER messages with only tiny changes.
    
    Option-specific rules:
    - If optionType is WORD:
      - Keep the same dialogue flow, roles, and message order.
      - Rewrite BOTH ASSISTANT and USER messages.
      - Each USER message must include at least one upgraded vocabulary word or phrase.
      - Do not keep USER messages almost identical to the previous messages.
      - Replace basic expressions with slightly more advanced spoken English.
      - Keep the grammar structure mostly the same.
      - Keep the meaning almost the same.
      - Do not create a completely new conversation.
      - Do not add unnecessary new turns.
    
      Vocabulary upgrade examples:
      - would like -> would prefer
      - order -> get / have / purchase
      - size -> cup size
      - medium -> regular-sized / medium-sized
      - also -> additionally
      - muffin -> pastry

    - If optionType is GRAMMAR:
      - Keep the original dialogue flow.
      - Improve sentence structure and grammar.
      - Do not mainly change vocabulary.

    - If optionType is DIALOGUE:
      - Add more turns to the conversation.
      - Keep the same scenario and place context.
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