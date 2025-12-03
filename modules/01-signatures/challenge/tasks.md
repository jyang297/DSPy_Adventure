# Module 01: Signatures - Challenge Tasks

## Overview
Apply your understanding of DSPy Signatures by completing these progressively challenging tasks.

**Time Estimate**: 2-3 hours
**Difficulty**: Beginner to Intermediate

---

## Setup

1. Open `starter_code.py` in this directory
2. Complete each task by filling in the commented sections
3. Run your code to test (you'll need a DSPy LM configured)
4. Compare your solution with `../solution/solution.py`

---

## Task 1: Basic Signature (15 min)

**Difficulty**: ⭐ Beginner

### Goal
Create a simple signature for a task you're familiar with.

### Requirements
Write a Signature for **blog post title generation**:
- **Input**: A topic (string)
- **Output**: A catchy title (string)
- Include a clear docstring
- Use proper InputField and OutputField

### Success Criteria
- [ ] Signature compiles without errors
- [ ] Docstring clearly describes the task
- [ ] Uses InputField and OutputField correctly

### Hints
- Start with the official docs pattern (simple)
- Focus on clarity in your docstring
- Think about what makes a "good" title

---

## Task 2: Multi-Field Signature (30 min)

**Difficulty**: ⭐⭐ Beginner-Intermediate

### Goal
Create a signature with multiple inputs and outputs.

### Requirements
Write a Signature for **product review analysis**:
- **Inputs**:
  - Product name (string)
  - Review text (string)
- **Outputs**:
  - Sentiment (should be constrained to: positive, negative, neutral)
  - Rating prediction (1-5 stars)
  - Key points from review (comma-separated)

### Success Criteria
- [ ] Uses type hints (str, Literal, etc.)
- [ ] Includes field descriptions using `desc` parameter
- [ ] Sentiment uses Literal type to constrain values
- [ ] Clear docstring with task overview

### Hints
- Use `from typing import Literal`
- Field descriptions guide the LM's behavior
- Think about edge cases (short reviews, ambiguous sentiment)

---

## Task 3: Production-Ready Signature (45 min)

**Difficulty**: ⭐⭐⭐ Intermediate

### Goal
Create a production-ready signature with validation and robustness features.

### Requirements
Write a Signature for **meeting notes extraction**:
- **Inputs**:
  - Meeting transcript (string)
  - Optional: Meeting type (formal/casual)
- **Outputs**:
  - Key decisions made (numbered list format)
  - Action items (with owners if mentioned)
  - Next steps (3-5 bullets)
  - Confidence in extraction (high/medium/low)

### Production Features Required
- Comprehensive docstring with edge case handling
- All fields have detailed descriptions
- Use Literal for categorical fields
- Specify output formats in descriptions
- Include confidence/quality metadata
- Handle missing information gracefully

### Success Criteria
- [ ] Follows production pattern (see guide)
- [ ] Specifies output formats clearly
- [ ] Includes confidence/metadata field
- [ ] Handles edge cases (unclear transcript, no decisions)
- [ ] Field descriptions include format examples

### Hints
- Look at the ProductionQA example in the guide
- Specify what to do when information is missing
- Think about downstream consumers of this data
- Consider auditability (can you trace outputs to inputs?)

---

## Task 4: Pattern Comparison (30 min)

**Difficulty**: ⭐⭐⭐ Intermediate

### Goal
Understand the trade-offs between different signature patterns.

### Requirements
Take the **email response generation** task and implement THREE versions:
1. **V1**: Official docs pattern (minimal)
2. **V2**: Community pattern (descriptive)
3. **V3**: Production pattern (validated)

For each version, document:
- What's different from the previous version
- Why you made those changes
- When you'd use this version

### Success Criteria
- [ ] Three distinct signature versions
- [ ] Clear progression in complexity
- [ ] Documentation of trade-offs
- [ ] Understand when to use each

### Hints
- Start simple, add layers of detail
- Each version should be functional
- Think about: team size, stakes, debugging needs

---

## Bonus Task: Signature Design Challenge (60 min)

**Difficulty**: ⭐⭐⭐⭐ Advanced

### Goal
Design a complex signature for a real-world scenario.

### Scenario
You're building a **financial report analyzer** for a compliance team. The system must:
- Extract key financial metrics
- Identify red flags or anomalies
- Provide confidence levels
- Cite evidence from source documents
- Handle both quarterly and annual reports

### Requirements
Design a production-ready Signature that:
- Handles multiple report types
- Extracts structured financial data
- Includes compliance checks
- Provides audit trail
- Has clear fallback behavior

### Success Criteria
- [ ] Comprehensive docstring with compliance requirements
- [ ] Multiple inputs (report text, report type, etc.)
- [ ] Structured outputs (metrics, flags, evidence)
- [ ] Strong typing (Literal for categories)
- [ ] Evidence/audit fields
- [ ] Clear handling of missing data

### Hints
- Think like a compliance officer: what do they need?
- Audit trails are critical in finance
- Confidence levels help risk management
- Be explicit about edge cases
- Consider downstream systems (databases, dashboards)

---

## Self-Assessment

After completing the challenges, rate yourself:

### Understanding
- [ ] Can explain what Signatures are and why they're useful
- [ ] Understand the difference between InputField and OutputField
- [ ] Know when to use type hints and field descriptions

### Application
- [ ] Can write basic signatures without reference
- [ ] Can design multi-field signatures for complex tasks
- [ ] Know how to use Literal for categorical outputs

### Analysis
- [ ] Understand trade-offs: simple vs. detailed signatures
- [ ] Can explain official docs vs. production patterns
- [ ] Know when to evolve a signature from V1 to V2 to V3

---

## Common Pitfalls

Watch out for these common mistakes:

### Pitfall 1: Missing Docstring
```python
# ❌ Bad
class MySignature(dspy.Signature):
    input = dspy.InputField()
    output = dspy.OutputField()
```

**Fix**: Always include a task-level docstring

### Pitfall 2: Vague Field Descriptions
```python
# ❌ Bad
answer: str = dspy.OutputField(desc="The answer")

# ✅ Good
answer: str = dspy.OutputField(
    desc="Concise answer (1-2 sentences) based on provided context"
)
```

### Pitfall 3: No Type Constraints for Categories
```python
# ❌ Bad - LM can output anything
sentiment: str = dspy.OutputField()

# ✅ Good - Constrained to valid values
sentiment: Literal["positive", "negative", "neutral"] = dspy.OutputField()
```

### Pitfall 4: Too Many Outputs at Once
```python
# ❌ Bad - LM may skip or hallucinate
class TooComplex(dspy.Signature):
    input: str = dspy.InputField()
    out1: str = dspy.OutputField()
    out2: str = dspy.OutputField()
    out3: str = dspy.OutputField()
    out4: str = dspy.OutputField()
    out5: str = dspy.OutputField()
    out6: str = dspy.OutputField()
```

**Fix**: Start with 2-3 outputs, add more only if needed

---

## Testing Your Signatures

To test your signatures (requires DSPy + LM setup):

```python
import dspy

# Configure your LM
lm = dspy.LM("openai/gpt-4o-mini", api_key="your-key")
dspy.configure(lm=lm)

# Test your signature
predictor = dspy.Predict(YourSignature)
result = predictor(input_field="test value")
print(result.output_field)
```

---

## Next Steps

1. Complete tasks 1-3 at minimum
2. Attempt task 4 for deeper understanding
3. Try the bonus if you want a challenge
4. Compare your solutions with `../solution/solution.py`
5. Review `../key_takeaways.md` to solidify learning

---

## Need Help?

- **Stuck?** Review `../guide/overview.md`
- **Need examples?** Check `../guide/annotated_examples.py`
- **Ready to compare?** See `../solution/solution.py`

**Remember**: There's no single "right" answer. Focus on clarity, appropriate detail level for your use case, and learning the trade-offs between patterns.

---

**Good luck! Remember to start simple and iterate.**
