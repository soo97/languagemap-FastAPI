def build_youtube_keywords_prompt(
    final_feedback: str,
) -> str:
    role = """
You are an English learning content recommender.
You create YouTube search keywords for English learning videos.
"""

    instruction = """
Return ONLY valid JSON.
Do not include markdown.
Do not include extra explanation.

Rules:
- Create exactly 3 keywords.
- Keywords must be in English.
- Focus on speaking practice, pronunciation, or the learner's weak points.
"""

    context = f"""
[Final Feedback]
{final_feedback}
"""

    output_format = """
[Output JSON Format]
{
  "keywords": [
    "...",
    "...",
    "..."
  ]
}
"""

    return f"""
{role}

{instruction}

{context}

{output_format}
""".strip()