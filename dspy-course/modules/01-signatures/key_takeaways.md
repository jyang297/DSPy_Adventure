# Module 01: Signatures - Key Takeaways

## Core Concepts

### What Are Signatures?
**Signatures are declarative contracts that specify what your LM should do, not how.**

```
Traditional Prompting:   String manipulation, brittle, hard to optimize
DSPy Signatures:         Structured contracts, reusable, automatically optimizable
```

---

## Pattern Comparison: Docs vs. Reality

### Official Docs Say:
```python
class QA(dspy.Signature):
    """Answer questions."""
    question = dspy.InputField()
    answer = dspy.OutputField()
```
**Philosophy**: Simple, focused on learning concepts

### Real Projects Do:
```python
class QA(dspy.Signature):
    """Answer questions accurately using context.

    If uncertain, indicate confidence level.
    """
    question: str = dspy.InputField(
        desc="User's question requiring factual answer"
    )
    context: str = dspy.InputField(
        desc="Retrieved information to answer from"
    )
    answer: str = dspy.OutputField(
        desc="Concise answer (1-2 sentences) based on context"
    )
    confidence: Literal["high", "medium", "low"] = dspy.OutputField(
        desc="Answer confidence level"
    )
```
**Philosophy**: Detailed, focused on reliability

### Best Practice Is:
**Start with docs pattern, evolve to production pattern as requirements clarify.**

```
Prototype → Development → Production
  V1    →      V2       →     V3
```

---

## Key Differences: Why They Matter

| Aspect | Official Docs | Real Projects | Why Different |
|--------|---------------|---------------|---------------|
| **Type Hints** | Optional | Recommended | Docs: avoid overwhelming beginners<br>Projects: need IDE support + validation |
| **Field Descriptions** | Minimal | Detailed | Docs: teach concept quickly<br>Projects: guide LM behavior precisely |
| **Output Fields** | 1-2 | 3-5 | Docs: keep simple<br>Projects: need metadata (confidence, reasoning) |
| **Docstring** | 1 line | Multi-line | Docs: state task simply<br>Projects: document edge cases |
| **Validation** | None | Literal types | Docs: demonstrate flexibility<br>Projects: prevent invalid outputs |

---

## The Three Critical Components

### 1. Docstring (Task-Level Instruction)
```python
"""What the LM should accomplish overall."""
```
- Becomes part of the prompt
- Sets context and tone
- Should be 1-3 sentences
- Include key constraints

**Impact**: Weak docstrings → confused LM behavior

---

### 2. InputField (What Goes In)
```python
field_name: type = dspy.InputField(desc="guidance for LM")
```
- Marks required inputs
- Type hints help validation
- Descriptions guide LM interpretation
- Can have multiple inputs

**Impact**: Vague descriptions → inconsistent parsing

---

### 3. OutputField (What Comes Out)
```python
field_name: type = dspy.OutputField(desc="format specification")
```
- Marks expected outputs
- Type hints enable parsing
- Descriptions constrain generation
- Use Literal for categories

**Impact**: Missing constraints → unpredictable outputs

---

## Type Hints: When and Why

### Basic Types
```python
text: str          # String data
count: int         # Integer
score: float       # Decimal number
flag: bool         # True/False
```

### Constrained Types (Critical for Production)
```python
from typing import Literal

category: Literal["spam", "ham"]  # Only these values allowed
sentiment: Literal["positive", "negative", "neutral"]
confidence: Literal["high", "medium", "low"]
```

**Why Literal Matters**:
- Prevents invalid outputs
- Enables downstream validation
- Makes debugging easier
- Catches errors before users see them

---

## Field Descriptions: The LM's Guide

### Bad Description
```python
answer = dspy.OutputField(desc="the answer")
```
**Problems**: Vague, no format, no constraints

### Good Description
```python
answer: str = dspy.OutputField(
    desc="Concise answer (1-2 sentences) based on provided context"
)
```
**Better Because**: Specifies length, format, and source

### Excellent Description
```python
answer: str = dspy.OutputField(
    desc="Direct answer (20-150 words). Must cite context. "
         "Use 'Insufficient information' if context inadequate."
)
```
**Best Because**: Length range, citation requirement, fallback behavior

---

## Common Patterns

### 1. Classification
```python
class Classifier(dspy.Signature):
    """Classify input into categories."""
    input: str = dspy.InputField(desc="Text to classify")
    category: Literal["A", "B", "C"] = dspy.OutputField(desc="Category")
```

### 2. Extraction
```python
class Extractor(dspy.Signature):
    """Extract specific information."""
    text: str = dspy.InputField(desc="Source text")
    entities: str = dspy.OutputField(desc="Comma-separated entities")
```

### 3. Generation
```python
class Generator(dspy.Signature):
    """Generate content from prompt."""
    prompt: str = dspy.InputField(desc="Generation prompt")
    content: str = dspy.OutputField(desc="Generated content (100-200 words)")
```

### 4. QA with Context
```python
class QA(dspy.Signature):
    """Answer using context."""
    context: str = dspy.InputField(desc="Background info")
    question: str = dspy.InputField(desc="Question")
    answer: str = dspy.OutputField(desc="Answer from context")
```

---

## Evolution Strategy

### Start Simple (V1)
```python
class Task(dspy.Signature):
    """Do the thing."""
    input = dspy.InputField()
    output = dspy.OutputField()
```
**When**: Learning, prototyping, quick tests

### Add Clarity (V2)
```python
class Task(dspy.Signature):
    """Do the specific thing with guidelines."""
    input: str = dspy.InputField(desc="What input means")
    output: str = dspy.OutputField(desc="Expected output format")
```
**When**: Development, team collaboration

### Add Robustness (V3)
```python
class Task(dspy.Signature):
    """Do the thing with quality controls.

    Handle edge cases: X, Y, Z.
    """
    input: str = dspy.InputField(desc="Input (format, constraints)")
    output: str = dspy.OutputField(desc="Output (format, fallbacks)")
    confidence: Literal["high", "medium", "low"] = dspy.OutputField(
        desc="Quality indicator"
    )
```
**When**: Production, high-stakes, compliance

---

## Critical Insights

### 1. Signatures Enable Optimization
Unlike string prompts, signatures can be automatically optimized:
- DSPy can generate better instructions
- Few-shot examples can be synthesized
- Different LMs can be swapped seamlessly

### 2. Separation of Concerns
```
Signature (what) ≠ Module (how)
```
- Signature: task specification
- Module: execution strategy (Predict, ChainOfThought, etc.)
- Same signature works with different modules

### 3. Documentation IS the Prompt
Your docstrings and descriptions literally become the prompt:
```python
"""This text appears in the prompt to the LM."""
desc="This guides how the LM interprets the field"
```

### 4. Multiple Outputs = Structured Data
Instead of:
```
"Extract title, author, and date from text"
→ Parse unstructured output
```

Do:
```python
title: str = dspy.OutputField()
author: str = dspy.OutputField()
date: str = dspy.OutputField()
```
→ Get structured object

---

## Common Mistakes to Avoid

### ❌ Mistake 1: No Docstring
```python
class Bad(dspy.Signature):
    input = dspy.InputField()
```
**Fix**: Always include task-level instruction

### ❌ Mistake 2: Vague Descriptions
```python
answer: str = dspy.OutputField(desc="the answer")
```
**Fix**: Specify format, length, constraints

### ❌ Mistake 3: Unconstrained Categories
```python
sentiment: str = dspy.OutputField()  # Can be anything!
```
**Fix**: Use Literal["positive", "negative", "neutral"]

### ❌ Mistake 4: Too Many Outputs
```python
# 10+ output fields
```
**Fix**: Start with 2-3, add more only if LM handles them well

### ❌ Mistake 5: Over-Specification
```python
desc="The answer must be exactly 47 words, written in iambic pentameter..."
```
**Fix**: Balance detail with flexibility

---

## When to Use Which Pattern

### Use Official Docs Pattern When:
- ✅ Learning DSPy
- ✅ Quick prototypes
- ✅ Demonstrating concepts
- ✅ Simple, one-off tasks

### Use Community Pattern When:
- ✅ Team development
- ✅ Moderate complexity
- ✅ Need some LM guidance
- ✅ Multiple stakeholders

### Use Production Pattern When:
- ✅ User-facing applications
- ✅ High-stakes decisions
- ✅ Compliance requirements
- ✅ Need audit trails
- ✅ Consistency is critical

---

## Testing Your Understanding

You've mastered signatures if you can:

1. ✅ Explain why signatures are better than string prompts
2. ✅ Write a basic signature without reference
3. ✅ Add appropriate type hints and descriptions
4. ✅ Use Literal types for categorical outputs
5. ✅ Know when to add more detail vs. keep it simple
6. ✅ Understand the official docs vs. production trade-off
7. ✅ Design signatures for complex tasks
8. ✅ Debug LM behavior by refining signatures

---

## Connection to Other Modules

### Signatures Feed Into:
- **Module 02**: Signatures are used by Modules (Predict, ChainOfThought)
- **Module 03**: Optimizers improve Signatures automatically
- **Module 04**: Advanced optimizers generate better instructions
- **Module 06**: RAG systems use specialized Signatures
- **Module 08**: Metrics evaluate Signature effectiveness

### Key Principle:
**Good signatures are the foundation of good DSPy programs.**

---

## Final Checklist

Before moving to Module 02, ensure:

- [ ] You can write basic signatures
- [ ] You understand InputField vs. OutputField
- [ ] You know how to use field descriptions
- [ ] You can apply type hints appropriately
- [ ] You understand the docs vs. production trade-off
- [ ] You can explain when to use Literal types
- [ ] You've completed at least 3 challenge tasks

---

## Next Steps

1. **Review** your challenge solutions vs. provided solutions
2. **Practice** writing signatures for 3-5 different tasks
3. **Move On** to Module 02: Modules & Forward
4. **Remember** to start simple and evolve as needed

---

**Remember**: There's no single "right" signature. The best signature balances clarity, constraints, and flexibility for YOUR specific use case.

**Key Mantra**: *Start with official docs pattern, evolve to production pattern as requirements clarify.*
