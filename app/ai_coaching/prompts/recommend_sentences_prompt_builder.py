def build_recommend_sentences_prompt(
    final_feedback: str,
) -> str:
    role = """
You are an English speaking coach.
You create reusable English practice sentences based on final feedback.
"""

    instruction = """
Return ONLY valid JSON.
Do not include markdown.
Do not include extra explanation.

Rules:
- Create 3 to 5 sentences.
- Sentences must be in English.
- Sentences should be practical and short.
- Focus on expressions the learner can reuse.
- Match the learner's weak points from the final feedback.
"""

    context = f"""
[Final Feedback]
{final_feedback}
"""

    output_format = """
[Output JSON Format]
{
  "sentences": [
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