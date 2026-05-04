from typing import Protocol, Sequence
from app.ai_coaching.prompts.prompt_constants import ALLOWED_FEEDBACK_LEVELS

class MessageLike(Protocol):
    role: str
    message: str

class PronunciationResultLike(Protocol):
    expectedText: str
    recognizedText: str
    accuracyScore: float
    fluencyScore: float
    completenessScore: float

def build_final_feedback_prompt(
    messages: Sequence[MessageLike],
    pronunciation_results: Sequence[PronunciationResultLike],
) -> str:
    conversation = "\n".join(
        [f"{message.role}: {message.message}" for message in messages]
    ) or "No conversation messages."

    pronunciation_text = "\n".join(
        [
            f"Expected: {result.expectedText} / "
            f"Recognized: {result.recognizedText} / "
            f"Accuracy: {result.accuracyScore} / "
            f"Fluency: {result.fluencyScore} / "
            f"Completeness: {result.completenessScore}"
            for result in pronunciation_results
        ]
    ) or "No pronunciation results."

    allowed_levels = ", ".join(ALLOWED_FEEDBACK_LEVELS)

    role = """
You are an English speaking evaluator for a language learning app.
You evaluate the learner's conversation and provide practical feedback in Korean.
"""

    instruction = f"""
Return ONLY valid JSON.
Do not include markdown.
Do not include extra explanation.

Rules:
- Write feedback in Korean.
- totalScore must be an integer from 0 to 100.
- level must be one of: {allowed_levels}.
- problemWords should include 0 to 5 words.
- Use pronunciation results when writing pronunciation feedback.
- If pronunciation results are missing, focus on conversation naturalness and flow.
- Focus on naturalness, response flow, and pronunciation hints.
"""

    context = f"""
[Conversation]
{conversation}

[Pronunciation Results]
{pronunciation_text}
"""

    output_format = """
[Output JSON Format]
{
  "totalScore": 87,
  "summaryFeedback": "...",
  "naturalness": {
    "level": "GOOD",
    "comment": "..."
  },
  "flow": {
    "level": "GOOD",
    "comment": "..."
  },
  "pronunciation": {
    "level": "CHECK",
    "comment": "...",
    "problemWords": [
      {
        "word": "preferably"
      },
      {
        "word": "almond"
      }
    ]
  }
}
"""

    return f"""
{role}

{instruction}

{context}

{output_format}
""".strip()