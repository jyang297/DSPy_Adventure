# Module 03: Teleprompters - Key Takeaways

## Core Concepts

### What Are Teleprompters?
**Teleprompters (now called Optimizers) automatically improve your DSPy programs through prompt compilation.**

```
Manual Prompt Engineering → Hours of trial and error
DSPy Teleprompters → Automatic optimization with metrics
```

**Note**: "Teleprompter" is the legacy term. Modern DSPy uses "Optimizer" but the concept is the same.

---

## Pattern Comparison: Docs vs. Reality

### Official Docs Say:
```python
from dspy.teleprompt import BootstrapFewShot

teleprompter = BootstrapFewShot(metric=validate_answer)
compiled_program = teleprompter.compile(
    student=program,
    trainset=train_examples
)
```
**Philosophy**: Simple API, focus on concept

### Real Projects Do:
```python
from dspy.teleprompt import BootstrapFewShot
import logging

def robust_metric(example, pred, trace=None):
    try:
        score = validate_answer(example, pred)
        logging.info(f"Score: {score} for {example.question}")
        return score
    except Exception as e:
        logging.error(f"Metric failed: {e}")
        return 0.0

teleprompter = BootstrapFewShot(
    metric=robust_metric,
    max_bootstrapped_demos=8,
    max_labeled_demos=4,
    max_rounds=2,
    max_errors=5
)

with dspy.context(lm=fast_lm):  # Use cheaper LM for compilation
    compiled_program = teleprompter.compile(
        student=program,
        trainset=train_examples[:100],  # Subset for speed
        teacher=None  # or advanced_program
    )

# Save compiled program
compiled_program.save("optimized_model.json")
```
**Philosophy**: Production-ready with error handling, logging, cost optimization

### Best Practice Is:
**Start with simple compilation, add robustness and monitoring for production.**

---

## Key Differences: Why They Matter

| Aspect | Official Docs | Real Projects | Why Different |
|--------|---------------|---------------|---------------|
| **Metric Robustness** | Simple function | Try/except + logging | Docs: show concept<br>Projects: handle failures |
| **Dataset Size** | Full dataset | Subset for speed | Docs: show full process<br>Projects: iterate faster |
| **LM Choice** | Same LM | Cheaper LM | Docs: simplicity<br>Projects: cost optimization |
| **Saving Results** | Not shown | Always save | Docs: focus on API<br>Projects: reusability |
| **Parameters** | Defaults | Explicit config | Docs: reduce noise<br>Projects: reproducibility |

---

## Key Teleprompter Types

### 1. BootstrapFewShot (Most Common)
```python
from dspy.teleprompt import BootstrapFewShot

teleprompter = BootstrapFewShot(
    metric=my_metric,
    max_bootstrapped_demos=4  # Number of examples to generate
)
```
**What It Does**:
- Runs your program on training data
- Captures successful traces
- Uses them as few-shot examples

**When to Use**: You have unlabeled data or want automatic example generation

---

### 2. LabeledFewShot (Simplest)
```python
from dspy.teleprompt import LabeledFewShot

teleprompter = LabeledFewShot(k=3)  # Use 3 examples
compiled = teleprompter.compile(
    student=program,
    trainset=labeled_examples
)
```
**What It Does**:
- Simply adds k labeled examples to prompts
- No optimization, just few-shot

**When to Use**: You have good labeled examples and want simple few-shot

---

### 3. BootstrapFewShotWithRandomSearch
```python
from dspy.teleprompt import BootstrapFewShotWithRandomSearch

teleprompter = BootstrapFewShotWithRandomSearch(
    metric=my_metric,
    max_bootstrapped_demos=4,
    num_candidate_programs=10  # Try 10 variations
)
```
**What It Does**:
- Generates multiple candidate programs
- Evaluates each on validation set
- Returns best performer

**When to Use**: You want better quality and can afford more compute

---

## The Compilation Process

### Step-by-Step: What Happens During Compilation

```
1. TRACE COLLECTION
   ├─> Run program on training examples
   ├─> Capture successful executions
   └─> Extract intermediate reasoning

2. DEMO SELECTION
   ├─> Filter traces by metric score
   ├─> Deduplicate similar examples
   └─> Select most informative demos

3. PROMPT CONSTRUCTION
   ├─> Add demos to prompt
   ├─> Optimize demo order
   └─> Format for LM

4. VALIDATION (if using random search)
   ├─> Test on validation set
   ├─> Score each candidate
   └─> Return best program

5. RETURN COMPILED PROGRAM
   └─> New program with optimized prompts
```

---

## Critical Insights

### 1. Metrics Are Everything
```python
# ❌ Bad: Vague metric
def bad_metric(example, pred):
    return pred.answer != ""

# ✅ Good: Clear success criteria
def good_metric(example, pred):
    return example.answer.lower() in pred.answer.lower()

# ✅ Better: Partial credit
def better_metric(example, pred):
    if example.answer.lower() == pred.answer.lower():
        return 1.0
    elif example.answer.lower() in pred.answer.lower():
        return 0.5
    else:
        return 0.0
```

### 2. More Demos ≠ Always Better
```python
# Too few: Underfitting
max_bootstrapped_demos=1  # Not enough examples

# Just right: Balance
max_bootstrapped_demos=4-8  # Good starting point

# Too many: Overfitting + cost
max_bootstrapped_demos=20  # May overfit, expensive prompts
```

### 3. Compilation Is Expensive
```python
# Original program: N LM calls
program(inputs)  # N calls

# Compilation: N * M LM calls
teleprompter.compile(program, trainset)  # N examples * M attempts

# Compiled program: N LM calls (but better quality)
compiled_program(inputs)  # Same N calls, optimized
```
**Tradeoff**: Pay upfront compilation cost for better runtime quality

### 4. Teacher Programs Improve Results
```python
# Self-improvement: use same program
teleprompter.compile(student=program, teacher=program)

# Teacher-student: use better program as teacher
advanced_program = dspy.ChainOfThought(Sig)
basic_program = dspy.Predict(Sig)

teleprompter.compile(
    student=basic_program,
    teacher=advanced_program  # Learn from better program
)
```

---

## Common Patterns

### Pattern 1: Quick Compilation
```python
# For rapid iteration
teleprompter = BootstrapFewShot(metric=quick_metric)
compiled = teleprompter.compile(program, trainset[:10])
```

### Pattern 2: Production Compilation
```python
# For final deployment
teleprompter = BootstrapFewShotWithRandomSearch(
    metric=robust_metric,
    max_bootstrapped_demos=8,
    num_candidate_programs=20
)
compiled = teleprompter.compile(
    program,
    trainset=full_trainset,
    valset=validation_set
)
compiled.save("production_v1.json")
```

### Pattern 3: Iterative Refinement
```python
# Round 1: Quick compilation
v1 = basic_teleprompter.compile(program, trainset)

# Round 2: Use v1 as teacher
v2 = advanced_teleprompter.compile(
    student=program,
    teacher=v1,
    trainset=trainset
)

# Round 3: Random search
v3 = search_teleprompter.compile(v2, trainset, valset)
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: No Metric Validation
```python
# Bad: Metric can crash
def risky_metric(example, pred):
    return example.answer == pred.answer  # May not have 'answer'!
```
**Fix**: Add error handling
```python
def safe_metric(example, pred):
    try:
        return example.answer.lower() == pred.answer.lower()
    except:
        return 0.0
```

### ❌ Mistake 2: Using Full Dataset
```python
# Bad: Slow compilation
compiled = tp.compile(program, trainset=all_10k_examples)
```
**Fix**: Use subset for iteration
```python
# Good: Fast iteration
compiled = tp.compile(program, trainset=all_10k_examples[:100])
```

### ❌ Mistake 3: Not Saving Compiled Programs
```python
# Bad: Recompile every time
compiled = tp.compile(program, trainset)  # Expensive!
result = compiled(input)
```
**Fix**: Save and load
```python
# Good: Compile once, use many times
compiled.save("model.json")
# Later...
loaded = MyModule()
loaded.load("model.json")
```

### ❌ Mistake 4: Ignoring Compilation Failures
```python
# Bad: No error handling
compiled = tp.compile(program, trainset)
```
**Fix**: Handle failures
```python
# Good: Graceful fallback
try:
    compiled = tp.compile(program, trainset)
except Exception as e:
    print(f"Compilation failed: {e}")
    compiled = program  # Use unoptimized version
```

### ❌ Mistake 5: Wrong Metric
```python
# Bad: Metric doesn't align with goal
def wrong_metric(example, pred):
    return len(pred.answer) > 10  # Cares about length, not correctness!
```
**Fix**: Align metric with actual goal
```python
def right_metric(example, pred):
    return pred.answer.lower() == example.answer.lower()
```

---

## Metric Design Best Practices

### 1. Binary Metrics (Simplest)
```python
def binary_metric(example, pred, trace=None):
    return 1.0 if pred.answer == example.answer else 0.0
```
**Use**: Clear right/wrong tasks

### 2. Partial Credit Metrics
```python
def partial_metric(example, pred, trace=None):
    if pred.answer == example.answer:
        return 1.0
    elif example.answer in pred.answer:
        return 0.5
    else:
        return 0.0
```
**Use**: Reward partial correctness

### 3. Composite Metrics
```python
def composite_metric(example, pred, trace=None):
    accuracy = 1.0 if pred.answer == example.answer else 0.0
    relevance = compute_relevance(pred.answer, example.context)
    return 0.7 * accuracy + 0.3 * relevance
```
**Use**: Multiple quality dimensions

### 4. LM-as-Judge Metrics
```python
def llm_judge_metric(example, pred, trace=None):
    judge_prompt = f"Is '{pred.answer}' a good answer to '{example.question}'?"
    score = judge_lm(judge_prompt)
    return score
```
**Use**: Subjective quality (expensive!)

---

## When to Use Which Teleprompter

### Use LabeledFewShot When:
- ✅ You have high-quality labeled examples
- ✅ Want simplest approach
- ✅ Don't need optimization
- ✅ Examples are already good few-shots

### Use BootstrapFewShot When:
- ✅ Have unlabeled data
- ✅ Want automatic example generation
- ✅ Need fast iteration
- ✅ Metrics are well-defined

### Use BootstrapFewShotWithRandomSearch When:
- ✅ Quality is critical
- ✅ Can afford computation cost
- ✅ Have validation set
- ✅ Want best possible results

---

## Compilation Cost vs. Benefit

### Cost Factors:
- **Training Set Size**: Larger = more expensive
- **Teleprompter Type**: Random search > Bootstrap > Labeled
- **Number of Demos**: More demos = more LM calls during compilation
- **LM Choice**: GPT-4 compilation costs > GPT-3.5

### Benefit Factors:
- **Task Complexity**: Complex tasks benefit more
- **Quality Improvement**: Can be 10-50% accuracy gain
- **Runtime Cost**: Better programs may use fewer tokens
- **User Experience**: Better outputs = happier users

### Optimization Strategy:
```python
# Development: Fast, cheap
dev_tp = BootstrapFewShot(max_bootstrapped_demos=2)
with dspy.context(lm=cheap_lm):
    dev_compiled = dev_tp.compile(program, trainset[:50])

# Production: Slow, expensive, quality
prod_tp = BootstrapFewShotWithRandomSearch(
    max_bootstrapped_demos=8,
    num_candidate_programs=20
)
with dspy.context(lm=best_lm):
    prod_compiled = prod_tp.compile(program, full_trainset, valset)
```

---

## Testing Your Understanding

You've mastered teleprompters if you can:

1. ✅ Explain what compilation does
2. ✅ Write effective metrics
3. ✅ Choose appropriate teleprompter type
4. ✅ Balance compilation cost vs. benefit
5. ✅ Save and load compiled programs
6. ✅ Handle compilation failures gracefully
7. ✅ Understand teacher-student compilation

---

## Connection to Other Modules

### Teleprompters Build On:
- **Module 01 (Signatures)**: Metrics evaluate signature outputs
- **Module 02 (Modules)**: Teleprompters optimize entire modules

### Teleprompters Feed Into:
- **Module 04 (Optimizers)**: Modern optimizers expand on teleprompter concepts
- **Module 08 (Evaluation)**: Metrics are central to both

---

## Quick Reference Card

```python
# Basic Compilation Template
from dspy.teleprompt import BootstrapFewShot

# 1. Define metric
def my_metric(example, pred, trace=None):
    return float(pred.answer == example.answer)

# 2. Create teleprompter
teleprompter = BootstrapFewShot(
    metric=my_metric,
    max_bootstrapped_demos=4
)

# 3. Compile
compiled_program = teleprompter.compile(
    student=my_program,
    trainset=training_examples
)

# 4. Save
compiled_program.save("optimized.json")

# 5. Use
result = compiled_program(input="test")
```

---

## Final Checklist

Before moving to Module 04, ensure:

- [ ] Understand what teleprompters/optimizers do
- [ ] Can write basic metrics
- [ ] Know the main teleprompter types
- [ ] Understand compilation cost/benefit
- [ ] Can save and load compiled programs
- [ ] Grasp the difference: LabeledFewShot vs. BootstrapFewShot
- [ ] Understand when optimization is worth it

---

## Next Steps

1. **Practice** writing metrics for different tasks
2. **Experiment** with different teleprompter types
3. **Move On** to Module 04: Optimizers (modern optimization algorithms)
4. **Remember** Compilation = automatic prompt engineering

---

**Key Mantra**: *Good metrics + Good teleprompter = Better programs automatically.*
