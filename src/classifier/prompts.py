from typesafe_sdk import Choice

CATEGORY_QUESTION = Choice(
    instructions="What is the primary category and intent of this user query?",
    criteria={
        "general": "General knowledge, factual questions, conceptual explanations, or basic summaries",
        "coding": "Programming, code generation, debugging, syntax questions, or software architecture",
        "reasoning": "Complex logic puzzles, multi-step mathematical problems, deep analysis, or deductions",
        "creative": "Creative writing, storytelling, poetry, brainstorms, or open-ended ideation",
    },
)

COMPLEXITY_QUESTION = Choice(
    instructions="What is the complexity and effort required to answer this query accurately?",
    criteria={
        "low": "Simple, direct, concise answer needed with minimal computation or reasoning",
        "medium": "Moderate difficulty, requiring a multi-part answer, explanation, or typical code snippet",
        "high": "High difficulty, requiring intricate multi-step reasoning, advanced algorithms, or deep domain expertise",
    },
)

CLASSIFIER_QUESTIONS = {
    "category": CATEGORY_QUESTION,
    "complexity": COMPLEXITY_QUESTION,
}
