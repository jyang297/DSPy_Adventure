"""
Module 01: Signatures - Challenge Starter Code

Complete the tasks by filling in the commented sections below.
Remove the 'pass' statements and implement the signatures.

Test your code with:
    python starter_code.py

Compare your solution with ../solution/solution.py when done.
"""

import dspy
from typing import Literal

# =============================================================================
# TASK 1: Basic Signature (15 min)
# =============================================================================

# TODO: Create a signature for blog post title generation
# Requirements:
# - Input: topic (string)
# - Output: title (string)
# - Clear docstring
# - Use InputField and OutputField


class BlogTitleGenerator(dspy.Signature):
    # TODO: Add docstring describing the task
    pass
    # TODO: Define input field for 'topic'

    # TODO: Define output field for 'title'


# =============================================================================
# TASK 2: Multi-Field Signature (30 min)
# =============================================================================

# TODO: Create a signature for product review analysis
# Requirements:
# - Inputs: product_name (str), review_text (str)
# - Outputs: sentiment (Literal), rating (str or int), key_points (str)
# - Use type hints and field descriptions
# - Sentiment should be constrained to: positive, negative, neutral


class ProductReviewAnalyzer(dspy.Signature):
    # TODO: Add comprehensive docstring

    pass
    # TODO: Define input fields with descriptions
    # Hint: use dspy.InputField(desc="...")

    # TODO: Define output fields with descriptions
    # Hint: Use Literal["positive", "negative", "neutral"] for sentiment


# =============================================================================
# TASK 3: Production-Ready Signature (45 min)
# =============================================================================

# TODO: Create a production-ready signature for meeting notes extraction
# Requirements:
# - Inputs: transcript (str), meeting_type (str, optional)
# - Outputs: decisions (str), action_items (str), next_steps (str), confidence (Literal)
# - Comprehensive docstring with edge case handling
# - Detailed field descriptions with format specifications
# - Handle missing information gracefully


class MeetingNotesExtractor(dspy.Signature):
    # TODO: Add production-quality docstring
    # Include:
    # - Task description
    # - Edge case handling
    # - Format specifications
    # - Output structure expectations

    pass
    # TODO: Define input fields
    # Consider: What if transcript is unclear? What if meeting type matters?

    # TODO: Define output fields
    # Include:
    # - decisions: specify format (e.g., "numbered list")
    # - action_items: specify format (e.g., "with owners if mentioned")
    # - next_steps: specify format (e.g., "3-5 bullets")
    # - confidence: Literal["high", "medium", "low"]


# =============================================================================
# TASK 4: Pattern Comparison (30 min)
# =============================================================================

# TODO: Implement THREE versions of email response generation
# Show the evolution from simple to production-ready

# VERSION 1: Official Docs Pattern (Minimal)
class EmailResponseV1(dspy.Signature):
    # TODO: Minimal signature - just the basics
    # - Simple docstring
    # - No type hints
    # - No field descriptions
    pass


# VERSION 2: Community Pattern (Descriptive)
class EmailResponseV2(dspy.Signature):
    # TODO: Add clarity and guidance
    # - Better docstring
    # - Type hints
    # - Field descriptions
    # - Maybe add a second output (tone? length?)
    pass


# VERSION 3: Production Pattern (Validated)
class EmailResponseV3(dspy.Signature):
    # TODO: Production-ready
    # - Comprehensive docstring
    # - Type hints with Literal for categories
    # - Detailed field descriptions
    # - Multiple outputs (response, tone, length, confidence)
    # - Edge case handling
    pass


# =============================================================================
# BONUS TASK: Financial Report Analyzer (60 min)
# =============================================================================

# TODO: Design a signature for financial report analysis
# Requirements:
# - Multiple inputs (report_text, report_type, fiscal_period, etc.)
# - Structured outputs (metrics, red_flags, confidence, evidence)
# - Compliance-grade documentation
# - Audit trail support
# - Handle quarterly vs annual reports


class FinancialReportAnalyzer(dspy.Signature):
    # TODO: Design this signature thinking like a compliance officer
    # What information is critical?
    # What evidence do they need?
    # How should uncertainty be communicated?
    # What audit trail is required?

    pass


# =============================================================================
# TESTING SECTION (Optional - requires DSPy + LM setup)
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("DSPy Signatures Challenge - Starter Code")
    print("=" * 80)

    # Uncomment and configure when you're ready to test
    # You'll need an LM configured to actually run predictions

    # import os
    # lm = dspy.LM("openai/gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
    # dspy.configure(lm=lm)

    # # Test Task 1
    # print("\n[Testing Task 1: BlogTitleGenerator]")
    # try:
    #     predictor = dspy.Predict(BlogTitleGenerator)
    #     result = predictor(topic="artificial intelligence in healthcare")
    #     print(f"Generated title: {result.title}")
    # except Exception as e:
    #     print(f"Error: {e}")
    #     print("Make sure you've implemented BlogTitleGenerator")

    # # Test Task 2
    # print("\n[Testing Task 2: ProductReviewAnalyzer]")
    # try:
    #     predictor = dspy.Predict(ProductReviewAnalyzer)
    #     result = predictor(
    #         product_name="Wireless Headphones",
    #         review_text="Great sound quality but battery life could be better. Comfortable for long use."
    #     )
    #     print(f"Sentiment: {result.sentiment}")
    #     print(f"Rating: {result.rating}")
    #     print(f"Key points: {result.key_points}")
    # except Exception as e:
    #     print(f"Error: {e}")
    #     print("Make sure you've implemented ProductReviewAnalyzer")

    # # Add more tests for your other signatures

    print("\nComplete the TODOs above and uncomment the testing section to run.")
    print("Compare your implementation with ../solution/solution.py")
    print("=" * 80)

# =============================================================================
# REFLECTION QUESTIONS (Answer after completing tasks)
# =============================================================================

# 1. What's the main difference between your V1 and V3 email response signatures?
#
# YOUR ANSWER:
#

# 2. When would you use a simple signature vs. a production-ready one?
#
# YOUR ANSWER:
#

# 3. How do field descriptions affect LM behavior?
#
# YOUR ANSWER:
#

# 4. What role do Literal types play in signature design?
#
# YOUR ANSWER:
#

# 5. What was the hardest part of the financial analyzer signature? Why?
#
# YOUR ANSWER:
#
