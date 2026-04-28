OPTION_TYPE_WORD = "WORD"
OPTION_TYPE_GRAMMAR = "GRAMMAR"
OPTION_TYPE_DIALOGUE = "DIALOGUE"

OPTION_TYPE_INSTRUCTIONS = {
    "WORD": """
Upgrade only selected vocabulary in the previous dialogue.
Keep the same dialogue flow, roles, order, and meaning.
Do not create a completely new scenario.
Replace simple words or phrases with more advanced but still natural spoken English.
Keep grammar structure mostly the same.
""",
    "GRAMMAR": """
Upgrade the sentence grammar in the previous dialogue.
Keep the same dialogue flow, roles, order, and meaning.
Do not create a completely new scenario.
Make the sentences slightly more complex and natural.
""",
    "DIALOGUE": """
Expand the previous dialogue with more turn-taking.
Keep the same place and scenario.
Add more natural ASSISTANT and USER exchanges.
"""
}

ALLOWED_FEEDBACK_LEVELS = ["EXCELLENT", "NORMAL", "INSUFFICIENT"]