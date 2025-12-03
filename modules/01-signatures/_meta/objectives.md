# Module 01: Signatures - Learning Objectives

## Overview
Master DSPy's declarative way to define LM task contracts through Signatures.

## Primary Learning Objective
**Understand how to define precise, reusable input/output specifications that work across different LMs and optimization strategies.**

---

## Specific Objectives

### Knowledge (Understand)
By the end of this module, you will understand:

1. **What Signatures Are**
   - Declarative task specifications
   - Input/output contracts for LMs
   - Separation of "what" from "how"

2. **Why Signatures Matter**
   - Enable LM-agnostic programming
   - Allow automatic optimization
   - Improve code reusability

3. **Official vs. Community Patterns**
   - Official docs focus on simplicity
   - Production code adds validation
   - Type hints become crucial at scale

### Skills (Apply)
By the end of this module, you will be able to:

1. **Define Basic Signatures**
   ```python
   class TaskName(dspy.Signature):
       """Clear task description."""
       input_field: str = dspy.InputField()
       output_field: str = dspy.OutputField()
   ```

2. **Use Field Descriptions**
   - Add `desc` parameter to guide LM
   - Write clear, actionable descriptions
   - Balance detail vs. brevity

3. **Apply Type Hints**
   - Use Python type annotations
   - Understand how DSPy interprets types
   - Validate inputs/outputs

4. **Compose Signatures**
   - Multiple input fields
   - Multiple output fields
   - Optional vs. required fields

### Analysis (Evaluate)
By the end of this module, you will be able to:

1. **Compare Patterns**
   - Analyze official vs. community signatures
   - Identify when to use each approach
   - Evaluate trade-offs

2. **Debug Signatures**
   - Recognize common signature mistakes
   - Fix ambiguous descriptions
   - Improve LM behavior through better contracts

3. **Optimize Signatures**
   - Refine field descriptions iteratively
   - Choose appropriate types
   - Balance specificity and flexibility

---

## Key Questions to Answer

After completing this module, you should be able to answer:

1. What is a Signature and why use one instead of a string prompt?
2. How do InputField and OutputField differ in purpose?
3. When should you add a `desc` parameter to a field?
4. What role do docstrings play in Signatures?
5. How do type hints affect DSPy's behavior?
6. Why do production projects add more validation than official examples?
7. When is a simple signature better than a detailed one?

---

## Prerequisites

### Required
- Python basics (classes, type hints)
- Understanding of function signatures
- Familiarity with docstrings

### Helpful
- Experience with prompt engineering
- Knowledge of LM capabilities and limitations
- Understanding of data validation concepts

---

## Learning Outcomes

### Beginner Level
- [ ] Can define a basic Signature with 1 input and 1 output
- [ ] Understands the role of docstrings
- [ ] Can add field descriptions

### Intermediate Level
- [ ] Can define multi-field Signatures
- [ ] Uses type hints appropriately
- [ ] Understands official vs. community patterns

### Advanced Level
- [ ] Can design Signatures for complex tasks
- [ ] Knows when to split vs. combine Signatures
- [ ] Can debug LM behavior through Signature refinement

---

## Success Criteria

You've mastered this module when:

1. **Understanding**
   - You can explain Signatures to a teammate
   - You recognize good vs. bad Signature design
   - You understand the official docs vs. production trade-offs

2. **Application**
   - Your Signatures compile without errors
   - LMs produce expected output formats
   - Your code is reusable across different LMs

3. **Analysis**
   - You can critique existing Signatures
   - You know when to add more detail vs. keep it simple
   - You can adapt patterns to new use cases

---

## Time Investment

- **Minimum**: 4 hours (basics only)
- **Recommended**: 6 hours (complete module)
- **Mastery**: 8+ hours (extra challenges)

### Breakdown
- Read objectives: 15 min
- Study guide: 90 min
- Run examples: 60 min
- Challenge attempt: 120 min
- Compare with solution: 30 min
- Review takeaways: 15 min

---

## Connection to Other Modules

### Prerequisites
- None (this is Module 01)

### Leads To
- **Module 02**: Uses Signatures in Modules
- **Module 03**: Optimizers improve Signatures
- **Module 06**: RAG systems use specialized Signatures

### Related
- **Module 08**: Signatures enable metric definition
- **Module 09**: Validation patterns for Signatures

---

## Assessment

No formal test, but check yourself:

1. **Quick Test**
   - Write a Signature for email classification (spam/not spam)
   - Add appropriate field descriptions
   - Include type hints

2. **Reflection Questions**
   - Why did you choose those field descriptions?
   - What happens if you remove the docstring?
   - How would you modify this for a different LM?

3. **Real-World Application**
   - Pick a task you prompt LMs for regularly
   - Convert your prompt to a Signature
   - Compare the two approaches

---

## Resources for This Module

### Official Documentation
- https://dspy.ai/learn/programming/signatures
- https://dspy.ai/api/signatures

### Community Examples
- gabrielvanderlei/DSPy-examples (basic signatures)
- stanfordnlp/dspy examples/

### Related Concepts
- Python type hints: PEP 484
- Pydantic (similar validation approach)
- OpenAPI schemas (similar contract concept)

---

## Next Steps

After completing this module:

1. **Immediate**: Move to Module 02 (Modules)
2. **Practice**: Write Signatures for 5 different tasks
3. **Explore**: Read community Signature patterns
4. **Apply**: Use Signatures in a real project

---

**Module Version**: 1.0.0
**DSPy Compatibility**: 2.5+
**Last Updated**: 2025-12-03
**Status**: Stable
