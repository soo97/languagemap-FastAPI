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
    - Write the summary in Korean.
    - Do not translate the video title literally.
    - Summarize the learning value of this video.
    - Explain why this video helps English speaking practice.
    - Keep it short, within 3 sentences.
    - Use a friendly but clear tone for Korean learners.
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