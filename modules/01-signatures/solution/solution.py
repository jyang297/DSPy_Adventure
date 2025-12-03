"""
Module 01: Signatures - Complete Solution

This file contains production-ready implementations of all challenge tasks.
Study this code to understand best practices and compare with your solutions.

All signatures here are fully runnable and follow DSPy best practices.
"""

import dspy
from typing import Literal, Optional

# =============================================================================
# TASK 1 SOLUTION: Basic Signature
# =============================================================================


class BlogTitleGenerator(dspy.Signature):
    """Generate an engaging blog post title from a topic.

    Create titles that are attention-grabbing, clear, and relevant to the topic.
    """
    topic: str = dspy.InputField()
    title: str = dspy.OutputField()


# EXPLANATION:
# - Clear, single-sentence docstring states the task
# - Type hints (str) for clarity even though optional at this level
# - Minimal but complete - perfect for learning/prototyping


# =============================================================================
# TASK 2 SOLUTION: Multi-Field Signature
# =============================================================================


class ProductReviewAnalyzer(dspy.Signature):
    """Analyze product reviews for sentiment, rating, and key points.

    Extract structured insights from customer reviews to help product teams
    understand customer feedback at scale.
    """
    product_name: str = dspy.InputField(
        desc="Name of the product being reviewed"
    )
    review_text: str = dspy.InputField(
        desc="Customer review text (10-500 words)"
    )

    sentiment: Literal["positive", "negative", "neutral"] = dspy.OutputField(
        desc="Overall sentiment: positive (mostly praise), negative (mostly criticism), neutral (mixed/factual)"
    )
    rating: str = dspy.OutputField(
        desc="Predicted star rating (1-5 stars) based on review sentiment"
    )
    key_points: str = dspy.OutputField(
        desc="Comma-separated list of 3-5 main points from the review"
    )


# EXPLANATION:
# - Two inputs capture both product context and review
# - Literal type constrains sentiment to valid values
# - Field descriptions guide LM on format and expectations
# - Rating as str (could be "3-4 stars") for flexibility
# - key_points as comma-separated string (easier than List for LMs)


# =============================================================================
# TASK 3 SOLUTION: Production-Ready Signature
# =============================================================================


class MeetingNotesExtractor(dspy.Signature):
    """Extract structured information from meeting transcripts.

    Parse meeting transcripts to identify:
    - Key decisions that were made
    - Action items with responsible parties
    - Next steps for the team

    Edge Case Handling:
    - If no decisions were made, output "No formal decisions recorded"
    - If action items lack owners, note as "Owner: Unassigned"
    - If transcript is unclear/incomplete, set confidence to 'low'

    This signature supports both formal and casual meeting formats.
    """
    transcript: str = dspy.InputField(
        desc="Full meeting transcript or detailed notes (100-5000 words)"
    )
    meeting_type: str = dspy.InputField(
        desc="Type of meeting: formal, casual, standup, retrospective, etc. (optional context)"
    )

    decisions: str = dspy.OutputField(
        desc="Key decisions made, formatted as numbered list (1. Decision one, 2. Decision two, etc.). "
             "Use 'No formal decisions recorded' if none identified."
    )
    action_items: str = dspy.OutputField(
        desc="Action items with owners, formatted as: '- [Owner] Action description'. "
             "Use '[Unassigned]' if owner not mentioned. "
             "Example: '- [Alice] Update documentation by Friday'"
    )
    next_steps: str = dspy.OutputField(
        desc="Next steps for the team (3-5 bullet points). "
             "Each bullet should be actionable and specific."
    )
    confidence: Literal["high", "medium", "low"] = dspy.OutputField(
        desc="Extraction confidence: "
             "high = clear, detailed transcript; "
             "medium = some ambiguity or missing context; "
             "low = unclear, incomplete, or very short transcript"
    )


# EXPLANATION:
# - Comprehensive docstring documents edge cases
# - Field descriptions include format examples
# - Specifies fallback behavior ("No formal decisions recorded")
# - Confidence field enables quality assessment
# - meeting_type provides context but isn't strictly required
# - Output formats clearly specified (numbered list, bullet points, etc.)


# =============================================================================
# TASK 4 SOLUTION: Pattern Comparison
# =============================================================================

# VERSION 1: Official Docs Pattern (Minimal)
class EmailResponseV1(dspy.Signature):
    """Generate an email response."""
    email = dspy.InputField()
    response = dspy.OutputField()


# CHARACTERISTICS:
# - Minimal, quick to write
# - No guidance for LM
# - Unpredictable output format
# USE WHEN: Prototyping, learning, very simple tasks


# VERSION 2: Community Pattern (Descriptive)
class EmailResponseV2(dspy.Signature):
    """Generate a professional email response based on incoming email.

    Match the tone of the original email and be concise.
    """
    email: str = dspy.InputField(
        desc="Incoming email to respond to"
    )
    context: str = dspy.InputField(
        desc="Additional context or information to include in response"
    )

    response: str = dspy.OutputField(
        desc="Professional email response (2-4 paragraphs)"
    )
    tone: str = dspy.OutputField(
        desc="Tone of the response: formal, casual, friendly, business"
    )


# CHARACTERISTICS:
# - Type hints added
# - Field descriptions provide guidance
# - Multiple outputs for richer data
# - Added context input for flexibility
# USE WHEN: Team development, moderate complexity, need some control


# VERSION 3: Production Pattern (Validated)
class EmailResponseV3(dspy.Signature):
    """Generate professional email responses with quality controls.

    Create responses that:
    - Match the urgency and tone of the incoming email
    - Are grammatically correct and professional
    - Include all necessary information from context
    - Are appropriately concise (no unnecessary verbosity)

    Edge Cases:
    - If email is unclear, ask clarifying questions in response
    - If context is insufficient, note what information is missing
    - If tone is difficult to determine, default to professional/formal
    """
    email: str = dspy.InputField(
        desc="Incoming email to respond to (with subject and body)"
    )
    context: str = dspy.InputField(
        desc="Background information, facts, or data to incorporate into response"
    )
    response_goal: str = dspy.InputField(
        desc="Primary goal of response: answer_question, schedule_meeting, provide_update, decline_request, etc."
    )

    response: str = dspy.OutputField(
        desc="Complete email response including greeting and signature. "
             "Length: 150-400 words. Must be professional and address all points from original email."
    )
    tone: Literal["formal", "professional", "friendly", "casual"] = dspy.OutputField(
        desc="Tone used in response, matching the incoming email's tone"
    )
    urgency: Literal["high", "medium", "low"] = dspy.OutputField(
        desc="Response urgency level based on original email"
    )
    confidence: Literal["high", "medium", "low"] = dspy.OutputField(
        desc="Confidence in response quality: "
             "high = all information available, clear request; "
             "medium = some ambiguity; "
             "low = insufficient context or unclear request"
    )
    flags: str = dspy.OutputField(
        desc="Any issues or notes for human review. Use 'None' if no issues. "
             "Example: 'Missing pricing information' or 'Legal review recommended'"
    )


# CHARACTERISTICS:
# - Comprehensive docstring with edge cases
# - Three inputs for full context
# - Five outputs for complete metadata
# - Literal types constrain categorical outputs
# - Length constraints specified
# - Flags field for human-in-the-loop workflow
# USE WHEN: Production systems, customer-facing, compliance requirements


# EVOLUTION SUMMARY:
# V1 → V2: Added type hints, field descriptions, multiple outputs
# V2 → V3: Added validation, edge case handling, metadata, constraints
# Complexity: Low → Medium → High
# Reliability: Variable → Good → Excellent


# =============================================================================
# BONUS SOLUTION: Financial Report Analyzer
# =============================================================================


class FinancialReportAnalyzer(dspy.Signature):
    """Analyze financial reports for compliance and risk assessment.

    Extract structured financial data and identify potential red flags from
    quarterly and annual financial reports. This signature is designed for
    compliance teams and auditors.

    Requirements:
    - Extract only explicitly stated metrics (no speculation)
    - Cite exact locations in report for all extracted data
    - Flag any anomalies or concerning patterns
    - Assess confidence based on report clarity and completeness

    Compliance Notes:
    - All metrics must be traceable to source document
    - Uncertainty must be explicitly communicated
    - Red flags should reference specific regulatory concerns
    - Evidence field is required for audit trail

    Supported Report Types: 10-K, 10-Q, 8-K, Annual Report, Quarterly Report
    """
    report_text: str = dspy.InputField(
        desc="Full text of financial report or relevant sections (500-10000 words)"
    )
    report_type: Literal["10-K", "10-Q", "8-K", "annual", "quarterly", "other"] = dspy.InputField(
        desc="Type of financial report being analyzed"
    )
    fiscal_period: str = dspy.InputField(
        desc="Fiscal period covered (e.g., 'Q3 2024', 'FY 2023')"
    )
    focus_areas: str = dspy.InputField(
        desc="Specific areas to focus on: revenue, expenses, cash_flow, debt, all (comma-separated)"
    )

    # Key Metrics
    revenue: str = dspy.OutputField(
        desc="Revenue figure with currency and period. Use 'Not stated' if not found. "
             "Example: '$45.2M for Q3 2024'"
    )
    net_income: str = dspy.OutputField(
        desc="Net income/loss with currency. Example: '$12.5M profit' or '$3.2M loss'"
    )
    cash_position: str = dspy.OutputField(
        desc="Cash and cash equivalents. Example: '$78.3M as of Sep 30, 2024'"
    )
    debt_level: str = dspy.OutputField(
        desc="Total debt or debt-to-equity ratio if stated. Use 'Not disclosed' if absent."
    )

    # Risk Assessment
    red_flags: str = dspy.OutputField(
        desc="Identified red flags or concerns as numbered list. "
             "Include: declining metrics, unusual patterns, missing disclosures, going concern warnings. "
             "Use 'None identified' if no concerns found. "
             "Example: '1. Revenue down 15% YoY, 2. Debt increased 40% QoQ'"
    )
    risk_level: Literal["low", "moderate", "high", "critical"] = dspy.OutputField(
        desc="Overall risk assessment: "
             "low = strong financials, no concerns; "
             "moderate = some weaknesses but manageable; "
             "high = significant concerns requiring attention; "
             "critical = going concern or severe issues"
    )

    # Quality & Audit
    confidence: Literal["high", "medium", "low"] = dspy.OutputField(
        desc="Confidence in analysis: "
             "high = complete report, clear metrics, detailed disclosures; "
             "medium = some missing data or ambiguity; "
             "low = incomplete report or unclear presentation"
    )
    evidence: str = dspy.OutputField(
        desc="Direct quotes from report supporting key findings. "
             "Format: '- [Metric]: \"exact quote from report\" (page X)'. "
             "Provide 3-5 key quotes for audit trail."
    )
    missing_data: str = dspy.OutputField(
        desc="List of expected data not found in report. "
             "Use 'All expected data present' if complete. "
             "Example: 'Cash flow statement, segment breakdowns'"
    )


# EXPLANATION:
# - Comprehensive compliance-focused docstring
# - Four inputs provide full context (report, type, period, focus)
# - Nine outputs cover metrics, risk, and audit requirements
# - Literal types for categorical data (report_type, risk_level)
# - Evidence field provides audit trail
# - missing_data field tracks gaps
# - All outputs specify fallback values ("Not stated", "None identified")
# - Format examples in every field description
# - Confidence tracking for downstream risk management


# DESIGN PRINCIPLES DEMONSTRATED:
# 1. Traceability: evidence field enables audit
# 2. Transparency: confidence and missing_data communicate uncertainty
# 3. Structure: Multiple focused outputs vs. one blob
# 4. Constraints: Literal types prevent invalid categories
# 5. Flexibility: Handles multiple report types
# 6. Documentation: Compliance requirements in docstring


# =============================================================================
# TESTING & DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("DSPy Signatures - Complete Solutions")
    print("=" * 80)

    # Display signature information without requiring LM
    signatures = [
        ("Task 1: Blog Title Generator", BlogTitleGenerator),
        ("Task 2: Product Review Analyzer", ProductReviewAnalyzer),
        ("Task 3: Meeting Notes Extractor", MeetingNotesExtractor),
        ("Task 4 V1: Email Response (Simple)", EmailResponseV1),
        ("Task 4 V2: Email Response (Descriptive)", EmailResponseV2),
        ("Task 4 V3: Email Response (Production)", EmailResponseV3),
        ("Bonus: Financial Report Analyzer", FinancialReportAnalyzer),
    ]

    for name, sig_class in signatures:
        print(f"\n{name}")
        print("-" * 40)
        print(f"Docstring: {sig_class.__doc__[:100]}...")

        # Count fields
        input_fields = [f for f in sig_class.__annotations__ if hasattr(sig_class, f) and
                       isinstance(getattr(sig_class, f), dspy.InputField)]
        output_fields = [f for f in sig_class.__annotations__ if hasattr(sig_class, f) and
                        isinstance(getattr(sig_class, f), dspy.OutputField)]

        print(f"Inputs: {len(input_fields)}")
        print(f"Outputs: {len(output_fields)}")

    print("\n" + "=" * 80)
    print("Pattern Evolution Comparison")
    print("=" * 80)
    print("""
EmailResponse Evolution:

V1 (Official Docs):
  - 1 input, 1 output
  - No type hints
  - Minimal docstring
  - ~5 lines of code
  → Use for: Learning, prototyping

V2 (Community):
  - 2 inputs, 2 outputs
  - Type hints added
  - Field descriptions
  - ~15 lines of code
  → Use for: Development, team projects

V3 (Production):
  - 3 inputs, 5 outputs
  - Literal types for validation
  - Comprehensive docstring with edge cases
  - ~40 lines of code
  → Use for: Production, compliance, customer-facing

Key Insight: Start with V1, evolve to V3 as requirements clarify.
    """)

    print("=" * 80)
    print("\nTo test with actual LM calls, uncomment the testing section below")
    print("and configure your LM provider.")
    print("=" * 80)

    # UNCOMMENT TO TEST WITH REAL LM
    # import os
    # lm = dspy.LM("openai/gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
    # dspy.configure(lm=lm)
    #
    # # Test Blog Title Generator
    # print("\n[Live Test: Blog Title Generator]")
    # predictor = dspy.Predict(BlogTitleGenerator)
    # result = predictor(topic="machine learning in climate science")
    # print(f"Topic: machine learning in climate science")
    # print(f"Generated Title: {result.title}")
    #
    # # Test Product Review Analyzer
    # print("\n[Live Test: Product Review Analyzer]")
    # predictor = dspy.Predict(ProductReviewAnalyzer)
    # result = predictor(
    #     product_name="Bluetooth Speaker",
    #     review_text="Amazing sound quality and battery lasts forever. A bit pricey but worth it."
    # )
    # print(f"Sentiment: {result.sentiment}")
    # print(f"Rating: {result.rating}")
    # print(f"Key Points: {result.key_points}")
