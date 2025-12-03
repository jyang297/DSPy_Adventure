"""
Module 01: Signatures - Annotated Examples

This file demonstrates DSPy Signatures through heavily commented code.
Compare official docs patterns vs. community/production patterns.

Run this file to see signatures in action.
"""

import dspy
from typing import Literal, Optional

# =============================================================================
# SETUP: Configure DSPy with an LM
# =============================================================================

# In production, you'd use:
# lm = dspy.LM("openai/gpt-4o-mini", api_key="your-key")
# For this example, we'll show the pattern without requiring API keys

print("=" * 80)
print("DSPy Signatures: Annotated Examples")
print("=" * 80)

# =============================================================================
# EXAMPLE 1: Official Docs Pattern (Minimal)
# =============================================================================

print("\n[EXAMPLE 1] Official Docs Pattern: Minimal Signature\n")


class BasicQA(dspy.Signature):
    """Answer questions with short factoid answers."""
    # No type hints (they're optional in basic usage)
    # DSPy infers these should be strings
    question = dspy.InputField()  # What the user asks
    answer = dspy.OutputField()   # What LM should generate


# OFFICIAL DOCS SAY:
# - Keep it simple when learning
# - Types are optional (default to str)
# - Focus on core concept: input → output contract

# USAGE PATTERN (shown, not executed without API key):
# predictor = dspy.Predict(BasicQA)
# result = predictor(question="What is DSPy?")
# print(result.answer)

print("BasicQA Signature:")
print(f"  Docstring: {BasicQA.__doc__}")
print(f"  Input fields: question")
print(f"  Output fields: answer")
print(f"  Type hints: None (implied str)")
print("\n✅ Official docs use this for simplicity and teaching")

# =============================================================================
# EXAMPLE 2: Community Pattern (Descriptive)
# =============================================================================

print("\n[EXAMPLE 2] Community Pattern: With Descriptions\n")


class DescriptiveQA(dspy.Signature):
    """Answer questions using provided context.

    Focus on factual accuracy. Cite the context when possible.
    If the answer isn't in the context, say so clearly.
    """
    # Type hints make intent clear
    question: str = dspy.InputField(
        desc="The user's question to be answered"
    )
    # Additional input for context
    context: str = dspy.InputField(
        desc="Relevant background information retrieved for this question"
    )
    # Clear output expectations
    answer: str = dspy.OutputField(
        desc="A concise, factual answer (1-3 sentences) based on the context"
    )


# COMMUNITY PROJECTS DO:
# - Add type hints (better code clarity and IDE support)
# - Use desc parameter to guide LM behavior
# - Include multiple inputs when needed
# - Specify output format in description

print("DescriptiveQA Signature:")
print(f"  Docstring: Multi-line with constraints")
print(f"  Input fields: question, context (both with descriptions)")
print(f"  Output fields: answer (with format guidance)")
print(f"  Type hints: str (explicit)")
print("\n⚡ Community projects use this for better LM guidance")

# =============================================================================
# EXAMPLE 3: Production Pattern (Validated & Robust)
# =============================================================================

print("\n[EXAMPLE 3] Production Pattern: Full Validation\n")


class ProductionQA(dspy.Signature):
    """Answer questions with confidence assessment.

    Requirements:
    - Use only provided context for answers
    - Indicate confidence level based on evidence quality
    - Quote exact text from context to support answer
    - If context is insufficient, explicitly state "Insufficient information"

    This signature is designed for high-reliability QA systems.
    """
    # Input with clear length expectations
    question: str = dspy.InputField(
        desc="User's question (10-500 characters, well-formed)"
    )

    # Context with structure guidance
    context: str = dspy.InputField(
        desc="Retrieved context passages (1-5 paragraphs of relevant information)"
    )

    # Output with strict format
    answer: str = dspy.OutputField(
        desc="Direct answer (20-150 words). Must be based on context. "
             "Use 'Insufficient information' if context doesn't support an answer."
    )

    # Confidence as constrained enum using Literal
    confidence: Literal["high", "medium", "low"] = dspy.OutputField(
        desc="Confidence level: "
             "high = direct evidence in context; "
             "medium = inferential from context; "
             "low = speculative or weak evidence"
    )

    # Evidence tracking for auditing
    evidence: str = dspy.OutputField(
        desc="Direct quote from context supporting the answer (exact substring match)"
    )


# PRODUCTION BEST PRACTICES:
# - Literal types for categorical outputs (enforces valid values)
# - Detailed descriptions with examples
# - Length constraints specified
# - Fallback behavior documented ("Insufficient information")
# - Audit fields (evidence) for explainability

print("ProductionQA Signature:")
print(f"  Docstring: Comprehensive with requirements")
print(f"  Input fields: question, context (with length/structure guidance)")
print(f"  Output fields: answer, confidence (Literal enum), evidence")
print(f"  Type hints: str + Literal (strict types)")
print(f"  Special features: Audit trail, fallback behavior, constrained categories")
print("\n🎯 Production systems use this for reliability and auditability")

# =============================================================================
# EXAMPLE 4: Classification Signature
# =============================================================================

print("\n[EXAMPLE 4] Classification Pattern\n")


class EmailClassifier(dspy.Signature):
    """Classify emails as spam or legitimate.

    Consider: suspicious links, urgent language, grammar quality,
    sender reputation indicators, promotional content.
    """
    email_subject: str = dspy.InputField(
        desc="Email subject line"
    )
    email_body: str = dspy.InputField(
        desc="Email body content (up to 1000 chars)"
    )

    # Literal constrains output to valid categories only
    classification: Literal["spam", "legitimate"] = dspy.OutputField(
        desc="Classification: spam or legitimate"
    )

    # Reasoning helps debugging and builds trust
    reasoning: str = dspy.OutputField(
        desc="Brief explanation of classification decision (1-2 sentences)"
    )


# WHY THIS PATTERN:
# - Classification tasks benefit from Literal types
# - Reasoning field enables debugging
# - Multiple inputs capture different aspects

print("EmailClassifier Signature:")
print(f"  Task: Binary classification")
print(f"  Inputs: email_subject, email_body")
print(f"  Outputs: classification (Literal), reasoning")
print(f"  Key feature: Literal['spam', 'legitimate'] prevents invalid outputs")

# =============================================================================
# EXAMPLE 5: Multi-Output Structured Extraction
# =============================================================================

print("\n[EXAMPLE 5] Structured Extraction Pattern\n")


class ArticleExtractor(dspy.Signature):
    """Extract structured information from news articles.

    Parse article text and identify key components.
    Be precise - only extract what's explicitly stated.
    """
    article_text: str = dspy.InputField(
        desc="Full article text"
    )

    # Multiple outputs create structured data
    title: str = dspy.OutputField(
        desc="Article title or headline (5-15 words)"
    )

    author: str = dspy.OutputField(
        desc="Author name, or 'Unknown' if not mentioned"
    )

    publication_date: str = dspy.OutputField(
        desc="Publication date in YYYY-MM-DD format, or 'Unknown'"
    )

    summary: str = dspy.OutputField(
        desc="Three-sentence summary of main points"
    )

    category: Literal["politics", "technology", "sports", "business", "other"] = dspy.OutputField(
        desc="Primary article category"
    )

    sentiment: Literal["positive", "negative", "neutral"] = dspy.OutputField(
        desc="Overall article sentiment/tone"
    )


# WHY MULTIPLE OUTPUTS:
# - Creates structured data in one LM call
# - Each field has specific format/constraints
# - Better than parsing unstructured output
# - Enables downstream processing

print("ArticleExtractor Signature:")
print(f"  Task: Extract 6 structured fields")
print(f"  Inputs: article_text")
print(f"  Outputs: title, author, date, summary, category, sentiment")
print(f"  Key feature: Single LM call → structured data object")

# =============================================================================
# EXAMPLE 6: Comparison - Evolution of a Signature
# =============================================================================

print("\n[EXAMPLE 6] Signature Evolution: V1 → V2 → V3\n")

# VERSION 1: Learning (official docs style)
class SentimentV1(dspy.Signature):
    """Analyze sentiment."""
    text = dspy.InputField()
    sentiment = dspy.OutputField()


print("SentimentV1 (Learning):")
print("  ✅ Simple, easy to understand")
print("  ❌ Vague output format")
print("  ❌ No guidance on edge cases")

# VERSION 2: Development (community style)
class SentimentV2(dspy.Signature):
    """Classify text sentiment as positive, negative, or neutral."""
    text: str = dspy.InputField(desc="Text to analyze for sentiment")
    sentiment: str = dspy.OutputField(desc="Sentiment: positive, negative, or neutral")


print("\nSentimentV2 (Development):")
print("  ✅ Clear task definition")
print("  ✅ Type hints added")
print("  ✅ Field descriptions")
print("  ❌ Still allows invalid outputs (str not constrained)")

# VERSION 3: Production (enterprise style)
class SentimentV3(dspy.Signature):
    """Classify sentiment with confidence assessment.

    Analyze emotional tone. Return neutral for ambiguous text.
    Consider word choice, punctuation, context.
    """
    text: str = dspy.InputField(
        desc="Input text for sentiment analysis (10-1000 characters)"
    )

    sentiment: Literal["positive", "negative", "neutral"] = dspy.OutputField(
        desc="Overall emotional tone classification"
    )

    confidence: Literal["high", "medium", "low"] = dspy.OutputField(
        desc="Classification confidence: high = clear indicators, "
             "medium = mixed signals, low = ambiguous"
    )

    key_phrases: str = dspy.OutputField(
        desc="Comma-separated phrases that influenced classification (3-5 phrases)"
    )


print("\nSentimentV3 (Production):")
print("  ✅ Constrained outputs (Literal types)")
print("  ✅ Confidence tracking")
print("  ✅ Explainability (key_phrases)")
print("  ✅ Edge case handling (ambiguous → neutral)")
print("  ✅ Length constraints specified")

# =============================================================================
# PATTERN COMPARISON SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("PATTERN COMPARISON SUMMARY")
print("=" * 80)

print("""
┌────────────────┬─────────────────────┬──────────────────────┬──────────────────────┐
│ Aspect         │ Official Docs       │ Community Projects   │ Production Systems   │
├────────────────┼─────────────────────┼──────────────────────┼──────────────────────┤
│ Type Hints     │ Optional            │ Recommended          │ Required             │
│ Field Desc     │ Minimal             │ Descriptive          │ Comprehensive        │
│ Docstring      │ 1 line              │ 2-3 lines            │ Multi-line + rules   │
│ Output Fields  │ 1-2                 │ 2-3                  │ 3-5 (with metadata)  │
│ Validation     │ None                │ Type-based           │ Literal + length     │
│ Complexity     │ Low                 │ Medium               │ High                 │
│ Flexibility    │ High                │ Medium               │ Lower (more rigid)   │
│ Reliability    │ Variable            │ Good                 │ Excellent            │
└────────────────┴─────────────────────┴──────────────────────┴──────────────────────┘

WHEN TO USE EACH:

Official Docs Pattern:
  ✓ Learning DSPy
  ✓ Prototyping quickly
  ✓ Simple, one-off tasks
  ✓ Tutorial/demo code

Community Pattern:
  ✓ Development phase
  ✓ Team collaboration
  ✓ Moderate complexity tasks
  ✓ When you need some guidance but not strict control

Production Pattern:
  ✓ User-facing applications
  ✓ High-stakes decisions
  ✓ Compliance/audit requirements
  ✓ When consistency is critical
  ✓ Enterprise deployments
""")

# =============================================================================
# KEY TAKEAWAYS
# =============================================================================

print("=" * 80)
print("KEY TAKEAWAYS")
print("=" * 80)

print("""
1. SIGNATURES ARE CONTRACTS
   - Define what, not how
   - Separate specification from implementation
   - Enable LM-agnostic programming

2. EVOLUTION IS NATURAL
   - Start simple (official docs pattern)
   - Add detail as requirements emerge (community pattern)
   - Harden for production (enterprise pattern)

3. DESCRIPTIONS MATTER
   - They become part of the prompt
   - Clear descriptions → better LM behavior
   - Specify formats, constraints, examples

4. TYPE HINTS ENABLE VALIDATION
   - Literal types constrain outputs
   - Catch errors before they reach users
   - Better IDE support and documentation

5. MULTIPLE OUTPUTS CREATE STRUCTURE
   - One LM call → rich data object
   - Better than parsing unstructured text
   - Enable metadata capture (confidence, reasoning, evidence)

6. TRADE-OFFS ARE REAL
   - Simple = flexible but unpredictable
   - Detailed = reliable but rigid
   - Choose based on your use case

7. OFFICIAL DOCS VS REALITY
   - Docs optimize for learning
   - Production optimizes for reliability
   - Both are "correct" for different goals
""")

print("\n" + "=" * 80)
print("Next: Try ../challenge/tasks.md to practice these patterns!")
print("=" * 80)
