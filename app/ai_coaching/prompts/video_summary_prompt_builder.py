def build_video_summary_prompt(
    title: str,
    channel_title: str,
    description: str,
) -> str:
    role = """
You are an English learning content recommender.
You explain why a YouTube video is useful for the learner.
"""

    instruction = """
Return ONLY valid JSON.
Do not include markdown.
Do not include extra explanation.

Rules:
- Write in Korean.
- Keep it under 2 sentences.
- Explain why this video helps English speaking practice.
"""

    context = f"""
[Video Title]
{title}

[Channel Title]
{channel_title}

[Description]
{description}
"""

    output_format = """
[Output JSON Format]
{
  "summary": "..."
}
"""

    return f"""
{role}

{instruction}

{context}

{output_format}
""".strip()