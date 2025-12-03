# Module 01: Signatures - Guide Overview

## What Are Signatures?

**Signatures are declarative specifications of what your LM should do.**

Instead of writing string prompts:
```python
# Old way: brittle string prompts
prompt = "Given a question, provide a short answer: " + question
response = llm.generate(prompt)
```

You define contracts:
```python
# DSPy way: declarative signatures
class QA(dspy.Signature):
    """Answer questions with short factoid answers."""
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()
```

---

## The Three-Pattern Comparison

### Pattern 1: Official Docs (Simple & Clean)

**Philosophy**: Focus on learning core concepts

```python
class BasicQA(dspy.Signature):
    """Answer the question."""
    question = dspy.InputField()
    answer = dspy.OutputField()
```

**Characteristics**:
- Minimal code
- No type hints (implied str)
- Simple docstring
- Great for tutorials

**When Official Uses This**:
- Documentation examples
- Quick demonstrations
- Teaching core concepts

---

### Pattern 2: Community Projects (Descriptive & Robust)

**Philosophy**: Production systems need guidance

```python
class ProductionQA(dspy.Signature):
    """Answer questions accurately using provided context.

    Focus on factual accuracy. If uncertain, indicate that.
    """
    question: str = dspy.InputField(
        desc="User's question requiring a factual answer"
    )
    context: str = dspy.InputField(
        desc="Background information to use for answering"
    )
    answer: str = dspy.OutputField(
        desc="Concise answer (1-2 sentences) based on context"
    )
    confidence: str = dspy.OutputField(
        desc="High/Medium/Low confidence level"
    )
```

**Characteristics**:
- Explicit type hints
- Detailed field descriptions
- Multiple output fields for metadata
- Clear constraints

**When Community Uses This**:
- Production applications
- Multi-stage pipelines
- Systems requiring reliability
- When LM behavior must be predictable

---

### Pattern 3: Production Best Practice (Validated & Scalable)

**Philosophy**: Fail fast, validate early

```python
from typing import Literal
from pydantic import Field, validator

class EnterpriseQA(dspy.Signature):
    """Answer questions with confidence scoring.

    Use provided context only. Do not speculate beyond given information.
    Confidence must reflect answer quality.
    """
    question: str = dspy.InputField(
        desc="Well-formed question from user (max 500 chars)"
    )
    context: str = dspy.InputField(
        desc="Retrieved context paragraphs (1-5 passages)"
    )

    answer: str = dspy.OutputField(
        desc="Direct answer (20-100 words). State 'Insufficient information' if context inadequate."
    )
    confidence: Literal["high", "medium", "low"] = dspy.OutputField(
        desc="high: direct evidence; medium: inferential; low: speculative"
    )
    evidence_used: str = dspy.OutputField(
        desc="Quote from context supporting answer (exact substring)"
    )
```

**Characteristics**:
- Strict types (Literal for enums)
- Length constraints in descriptions
- Fallback behavior specified
- Evidence tracking
- Production-ready

**When to Use This**:
- High-stakes applications
- Regulated industries
- Systems requiring auditing
- Enterprise deployments

---

## Why These Patterns Differ

### Official Docs Optimize For:
✅ **Learning speed** - Get started fast
✅ **Concept clarity** - Understand core ideas
✅ **Minimal friction** - Don't overwhelm beginners

### Production Code Optimizes For:
✅ **Reliability** - Consistent LM behavior
✅ **Debuggability** - Clear failure modes
✅ **Maintainability** - Team can understand intent
✅ **Observability** - Track what LM actually does

### The Trade-off:
- **Official**: Simple but may require trial-and-error
- **Production**: Verbose but predictable

**Best Practice**: Start with official pattern, evolve to production pattern as requirements clarify.

---

## Core Signature Components

### 1. Class Definition
```python
class TaskName(dspy.Signature):
    # Inherits from dspy.Signature
```

**Purpose**: Declares this is a DSPy task contract

---

### 2. Docstring
```python
class TaskName(dspy.Signature):
    """This is the task-level instruction to the LM."""
```

**What It Does**:
- Becomes part of the prompt
- Sets overall task context
- Guides LM behavior at high level

**Best Practices**:
- Be specific about task goal
- Include tone/style guidance
- Mention key constraints
- Keep it 1-3 sentences

**Examples**:
```python
# ❌ Too vague
"""Do the task."""

# ✅ Clear and actionable
"""Classify emails as spam or not spam based on content patterns."""

# ✅ With constraints
"""Summarize text in exactly 3 bullet points, each under 20 words."""

# ✅ With tone
"""Answer questions in a friendly, conversational tone suitable for beginners."""
```

---

### 3. InputField
```python
question: str = dspy.InputField()
# or with description
question: str = dspy.InputField(desc="The user's question")
```

**What It Does**:
- Marks data as input to LM
- Description becomes part of prompt
- Type hint helps validation

**Best Practices**:
- Always include type hints in production
- Add `desc` for non-obvious inputs
- Describe format expectations
- Mention constraints (length, format)

**Examples**:
```python
# Basic (official docs style)
query = dspy.InputField()

# With type (better)
query: str = dspy.InputField()

# With description (production)
query: str = dspy.InputField(
    desc="User search query (2-100 words)"
)

# Multiple inputs
class MultiInput(dspy.Signature):
    """Combine information from multiple sources."""
    source_a: str = dspy.InputField(desc="First information source")
    source_b: str = dspy.InputField(desc="Second information source")
    output: str = dspy.OutputField(desc="Synthesized output")
```

---

### 4. OutputField
```python
answer: str = dspy.OutputField()
# or with description
answer: str = dspy.OutputField(desc="A concise answer")
```

**What It Does**:
- Marks data as expected output from LM
- Description guides generation
- Type hint helps parsing

**Best Practices**:
- Describe format clearly
- Specify length/structure
- Include example format in description
- Use multiple outputs for structured data

**Examples**:
```python
# Basic
answer = dspy.OutputField()

# With constraints
answer: str = dspy.OutputField(
    desc="Answer in 1-2 complete sentences"
)

# Multiple outputs for structure
class StructuredOutput(dspy.Signature):
    """Extract structured information."""
    text: str = dspy.InputField()

    title: str = dspy.OutputField(desc="Main title (5-10 words)")
    summary: str = dspy.OutputField(desc="Brief summary (2-3 sentences)")
    sentiment: str = dspy.OutputField(desc="positive/negative/neutral")
    key_points: str = dspy.OutputField(desc="Comma-separated list of 3-5 key points")
```

---

## Type Hints in Signatures

### Basic Types
```python
class TypeExamples(dspy.Signature):
    """Demonstrate type usage."""
    text: str = dspy.InputField()  # String
    count: int = dspy.OutputField()  # Integer
    score: float = dspy.OutputField()  # Float
    flag: bool = dspy.OutputField()  # Boolean
```

### Advanced Types
```python
from typing import List, Literal

class AdvancedTypes(dspy.Signature):
    """Advanced type usage."""
    # Enum-like (recommended for categories)
    category: Literal["spam", "not_spam"] = dspy.OutputField()

    # Note: Lists are possible but require careful prompting
    # Often better to use comma-separated strings
    tags: str = dspy.OutputField(desc="Comma-separated tags")
```

**Type Hint Impact**:
- DSPy uses types for output parsing
- Strong types help catch errors early
- Literal types constrain LM outputs
- Complex types (List, Dict) need careful field descriptions

---

## Common Signature Patterns

### 1. Classification
```python
class Classifier(dspy.Signature):
    """Classify input into predefined categories."""
    text: str = dspy.InputField(desc="Text to classify")
    category: Literal["A", "B", "C"] = dspy.OutputField(
        desc="Category: A for X, B for Y, C for Z"
    )
```

### 2. Generation
```python
class Generate(dspy.Signature):
    """Generate creative content based on prompt."""
    prompt: str = dspy.InputField(desc="Generation prompt")
    content: str = dspy.OutputField(desc="Generated content (100-200 words)")
```

### 3. Extraction
```python
class Extract(dspy.Signature):
    """Extract specific information from text."""
    document: str = dspy.InputField(desc="Source document")
    entity_type: str = dspy.InputField(desc="Type of entity to extract")
    entities: str = dspy.OutputField(desc="Comma-separated list of extracted entities")
```

### 4. Transformation
```python
class Transform(dspy.Signature):
    """Transform input text according to rules."""
    input_text: str = dspy.InputField(desc="Original text")
    transformation: str = dspy.InputField(desc="Transformation to apply")
    output_text: str = dspy.OutputField(desc="Transformed text")
```

### 5. Question Answering (with Context)
```python
class ContextualQA(dspy.Signature):
    """Answer questions using provided context."""
    context: str = dspy.InputField(desc="Background information")
    question: str = dspy.InputField(desc="Question to answer")
    answer: str = dspy.OutputField(desc="Answer based on context")
```

---

## Practical Design Guidelines

### Start Simple
```python
# Step 1: Minimal viable signature
class V1(dspy.Signature):
    """Do the thing."""
    input = dspy.InputField()
    output = dspy.OutputField()
```

### Add Clarity
```python
# Step 2: Clear task and types
class V2(dspy.Signature):
    """Classify sentiment of text."""
    text: str = dspy.InputField()
    sentiment: str = dspy.OutputField()
```

### Add Constraints
```python
# Step 3: Guide LM behavior
class V3(dspy.Signature):
    """Classify sentiment as positive, negative, or neutral."""
    text: str = dspy.InputField(desc="Text to analyze")
    sentiment: Literal["positive", "negative", "neutral"] = dspy.OutputField(
        desc="Sentiment classification"
    )
```

### Add Robustness
```python
# Step 4: Production-ready
class V4(dspy.Signature):
    """Classify sentiment with confidence scoring.

    Analyze text for emotional tone. Return neutral if ambiguous.
    """
    text: str = dspy.InputField(
        desc="Input text (10-1000 characters)"
    )
    sentiment: Literal["positive", "negative", "neutral"] = dspy.OutputField(
        desc="Overall emotional tone"
    )
    confidence: Literal["high", "medium", "low"] = dspy.OutputField(
        desc="Confidence in classification"
    )
    reasoning: str = dspy.OutputField(
        desc="Brief explanation (1 sentence)"
    )
```

---

## Next Steps

1. **Run Examples**: See `annotated_examples.py`
2. **Try Challenge**: See `../challenge/tasks.md`
3. **Compare Solutions**: See `../solution/solution.py`
4. **Review Takeaways**: See `../key_takeaways.md`

---

**For detailed code examples with inline comments, see `annotated_examples.py` in this directory.**
