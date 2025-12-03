# Module 05: Bootstrapping - Key Takeaways

## Core Concepts

### What Is Bootstrapping in DSPy?
**Bootstrapping is the technique of synthesizing training data by capturing and analyzing execution traces of your DSPy programs.**

```
Traditional: Hand-craft examples → Limited, expensive
Bootstrapping: Program generates its own examples → Scalable, automatic
```

---

## The Bootstrapping Process

```
1. EXECUTION
   ├─> Run program on inputs
   ├─> Capture all intermediate steps
   └─> Record LM calls and outputs

2. TRACE ANALYSIS
   ├─> Evaluate success via metric
   ├─> Filter failed executions
   └─> Extract successful patterns

3. DEMO SYNTHESIS
   ├─> Convert traces to few-shot examples
   ├─> Deduplicate similar examples
   └─> Select most informative demos

4. PROGRAM ENHANCEMENT
   ├─> Add demos to prompts
   ├─> Update program configuration
   └─> Create improved version

5. ITERATION (Optional)
   └─> Use enhanced program to bootstrap more examples
```

---

## Pattern Comparison: Docs vs. Reality

### Official Docs Say:
```python
from dspy.teleprompt import BootstrapFewShot

# Simple bootstrapping
bootstrap = BootstrapFewShot(metric=validate)
compiled = bootstrap.compile(program, trainset=examples)
```
**Philosophy**: Automatic, simple API

### Real Projects Do:
```python
from dspy.teleprompt import BootstrapFewShot
import logging
from collections import defaultdict

class BootstrapTracker:
    def __init__(self):
        self.traces = defaultdict(list)
        self.success_rate = {}

    def track(self, example_id, score):
        self.traces[example_id].append(score)

tracker = BootstrapTracker()

def tracked_metric(example, pred, trace=None):
    score = base_metric(example, pred)
    tracker.track(example.id, score)

    # Log trace details for analysis
    if trace and score > 0.8:
        logging.info(f"High-quality trace for {example.id}")
        save_trace_for_analysis(trace, example, pred)

    return score

bootstrap = BootstrapFewShot(
    metric=tracked_metric,
    max_bootstrapped_demos=8,
    max_labeled_demos=4,
    max_rounds=2,  # Multiple rounds of bootstrapping
    max_errors=5   # Tolerance for failures
)

# Use teacher program for better demos
teacher = advanced_program  # Better program generates better examples
compiled = bootstrap.compile(
    student=program,
    teacher=teacher,
    trainset=examples
)

# Analyze bootstrapping effectiveness
print(f"Success rate: {tracker.success_rate}")
print(f"Total traces: {len(tracker.traces)}")
```
**Philosophy**: Monitoring, quality control, iterative improvement

### Best Practice Is:
**Monitor trace quality, use teacher programs, iterate for better examples.**

---

## Key Differences: Why They Matter

| Aspect | Official Docs | Real Projects | Why Different |
|--------|---------------|---------------|---------------|
| **Trace Logging** | Not shown | Comprehensive | Docs: focus on concept<br>Projects: debug and improve |
| **Teacher Programs** | Optional | Recommended | Docs: simplicity<br>Projects: better example quality |
| **Quality Filtering** | Basic | Multi-criteria | Docs: show mechanism<br>Projects: ensure high quality |
| **Iteration** | Single round | Multiple rounds | Docs: simple demo<br>Projects: progressive improvement |
| **Deduplication** | Automatic | Custom logic | Docs: built-in default<br>Projects: task-specific |

---

## The Three Bootstrapping Patterns

### 1. Self-Bootstrapping (Simplest)
```python
# Program bootstraps from itself
bootstrap = BootstrapFewShot(metric=my_metric)
compiled = bootstrap.compile(
    student=program,
    trainset=examples
)
```
**When to Use**: Program is already decent
**Quality**: Good starting point
**Risk**: May amplify existing biases

---

### 2. Teacher-Student Bootstrapping (Better)
```python
# Better program teaches simpler one
teacher = dspy.ChainOfThought(ComplexSignature)
student = dspy.Predict(SimpleSignature)

bootstrap = BootstrapFewShot(metric=my_metric)
compiled = bootstrap.compile(
    student=student,
    teacher=teacher,  # Use reasoning from teacher
    trainset=examples
)
```
**When to Use**: Have a better (but expensive) program
**Quality**: Higher quality demos
**Benefit**: Student learns teacher's reasoning

---

### 3. Iterative Bootstrapping (Best)
```python
# Multiple rounds of progressive improvement
program_v1 = basic_program

# Round 1: Initial bootstrap
bootstrap1 = BootstrapFewShot(metric=my_metric, max_bootstrapped_demos=4)
program_v2 = bootstrap1.compile(program_v1, trainset=examples[:50])

# Round 2: Use v2 as teacher
bootstrap2 = BootstrapFewShot(metric=my_metric, max_bootstrapped_demos=6)
program_v3 = bootstrap2.compile(
    student=program_v1,
    teacher=program_v2,  # Improved teacher
    trainset=examples[:100]
)

# Round 3: Full dataset
bootstrap3 = BootstrapFewShot(metric=my_metric, max_bootstrapped_demos=8)
program_v4 = bootstrap3.compile(
    student=program_v1,
    teacher=program_v3,
    trainset=examples
)
```
**When to Use**: Maximum quality needed
**Quality**: Best possible
**Cost**: Multiple compilation rounds

---

## Critical Insights

### 1. Trace Quality Determines Demo Quality
```python
# ❌ Bad: Accept all traces
def permissive_metric(example, pred, trace=None):
    return 0.5  # Everything gets 0.5!

# ✅ Good: High standards
def strict_metric(example, pred, trace=None):
    # Only perfect matches become demos
    return 1.0 if pred.answer == example.answer else 0.0

# ✅ Better: Partial credit with high threshold
def smart_metric(example, pred, trace=None):
    score = compute_quality(example, pred)
    # Only use demos with score > 0.8
    return score
```

### 2. Diversity in Demos Matters
```python
# ❌ Bad: All similar examples
demos = [
    "Q: What is 2+2? A: 4",
    "Q: What is 3+3? A: 6",
    "Q: What is 4+4? A: 8",
]  # Too similar!

# ✅ Good: Diverse examples
demos = [
    "Q: What is 2+2? A: 4",
    "Q: Who wrote Hamlet? A: Shakespeare",
    "Q: What is the capital of France? A: Paris",
]  # Covers different question types
```

DSPy's bootstrapping includes diversity mechanisms, but you can enhance:
```python
def diverse_metric(example, pred, trace=None, existing_demos=[]):
    quality = base_metric(example, pred)

    # Bonus for diversity
    diversity = compute_diversity(example, existing_demos)

    return 0.7 * quality + 0.3 * diversity
```

### 3. Teacher Programs Should Be Better, Not Just Different
```python
# ❌ Bad: Teacher is worse
teacher = dspy.Predict(SimpleSignature)  # Fast but low quality
student = dspy.ChainOfThought(ComplexSignature)  # Slower but better
# Student won't learn much from worse teacher!

# ✅ Good: Teacher is better
teacher = dspy.ChainOfThought(ComplexSignature)  # Better quality
student = dspy.Predict(SimpleSignature)  # Learns from better reasoning
```

### 4. Bootstrapping Can Compound Errors
```python
# Risk: Error propagation
Round 1: Program makes 10% mistakes → Demos include 10% bad examples
Round 2: Learn from demos → Now makes 15% mistakes
Round 3: Worse demos → 20% mistakes
# Degradation!

# Solution: Strict metrics + validation
def safe_metric(example, pred, trace=None):
    # Only near-perfect examples become demos
    return 1.0 if very_high_quality(pred) else 0.0

# Validate each round
if round_n_score < round_n_minus_1_score:
    print("Quality degrading, stop bootstrapping")
    return round_n_minus_1_program
```

---

## Common Bootstrapping Patterns

### Pattern 1: Simple Demo Generation
```python
# Just need few-shot examples
bootstrap = BootstrapFewShot(
    metric=my_metric,
    max_bootstrapped_demos=8
)
program_with_demos = bootstrap.compile(program, trainset)
```

### Pattern 2: Hybrid Labeled + Bootstrapped
```python
# Combine labeled examples with bootstrapped ones
bootstrap = BootstrapFewShot(
    metric=my_metric,
    max_bootstrapped_demos=6,  # Generate 6
    max_labeled_demos=4         # Plus 4 labeled
)
program_with_demos = bootstrap.compile(program, trainset)
```

### Pattern 3: Progressive Complexity
```python
# Start simple, increase complexity
# Round 1: Easy examples
easy_bootstrap = BootstrapFewShot(max_bootstrapped_demos=4)
v1 = easy_bootstrap.compile(program, easy_examples)

# Round 2: Medium difficulty
medium_bootstrap = BootstrapFewShot(max_bootstrapped_demos=6)
v2 = medium_bootstrap.compile(v1, medium_examples)

# Round 3: Hard examples
hard_bootstrap = BootstrapFewShot(max_bootstrapped_demos=8)
v3 = hard_bootstrap.compile(v2, hard_examples)
```

### Pattern 4: Error Analysis Driven
```python
# Bootstrap specifically for error cases
baseline = program

# Find where baseline fails
errors = find_failure_cases(baseline, test_set)

# Bootstrap examples for error cases
error_bootstrap = BootstrapFewShot(metric=my_metric)
improved = error_bootstrap.compile(
    student=baseline,
    trainset=errors  # Focus on fixing errors
)
```

---

## Trace Analysis Best Practices

### 1. Log Traces for Analysis
```python
class TraceLogger:
    def __init__(self):
        self.traces = []

    def log_trace(self, example, pred, trace, score):
        self.traces.append({
            'example': example,
            'prediction': pred,
            'trace': trace,
            'score': score,
            'timestamp': time.time()
        })

logger = TraceLogger()

def logging_metric(example, pred, trace=None):
    score = base_metric(example, pred)
    logger.log_trace(example, pred, trace, score)
    return score
```

### 2. Analyze Successful Patterns
```python
# After bootstrapping
high_quality_traces = [
    t for t in logger.traces if t['score'] > 0.9
]

# What makes them successful?
successful_patterns = analyze_patterns(high_quality_traces)
print("Common patterns in successful traces:")
for pattern in successful_patterns:
    print(f"  - {pattern}")
```

### 3. Identify and Fix Failure Modes
```python
failed_traces = [
    t for t in logger.traces if t['score'] < 0.3
]

# Why did they fail?
failure_analysis = analyze_failures(failed_traces)
print("Common failure modes:")
for failure in failure_analysis:
    print(f"  - {failure}")
    print(f"    Fix: {suggest_fix(failure)}")
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Too Few Training Examples
```python
# Bad: Bootstrapping on tiny dataset
bootstrap = BootstrapFewShot(max_bootstrapped_demos=8)
compiled = bootstrap.compile(program, trainset=5_examples)  # Too few!
```
**Fix**: Need sufficient diversity
```python
# Good: Adequate training set
compiled = bootstrap.compile(program, trainset=100_examples)
```

### ❌ Mistake 2: Weak Metric
```python
# Bad: Metric that passes everything
def weak_metric(example, pred, trace=None):
    return 1.0 if pred.answer else 0.5  # Too permissive!
```
**Fix**: Strict quality standards
```python
def strong_metric(example, pred, trace=None):
    return 1.0 if perfect_match(example, pred) else 0.0
```

### ❌ Mistake 3: No Teacher Program
```python
# Suboptimal: Self-bootstrapping with weak program
bootstrap = BootstrapFewShot(metric=my_metric)
compiled = bootstrap.compile(weak_program, trainset)
```
**Fix**: Use better teacher
```python
teacher = strong_program  # Better reasoning
compiled = bootstrap.compile(
    student=weak_program,
    teacher=teacher,
    trainset=trainset
)
```

### ❌ Mistake 4: Not Validating Quality
```python
# Bad: Blind bootstrapping
compiled = bootstrap.compile(program, trainset)
# Deploy without checking!
```
**Fix**: Validate improvements
```python
baseline_score = evaluate(program, valset)
compiled = bootstrap.compile(program, trainset)
compiled_score = evaluate(compiled, valset)

if compiled_score > baseline_score:
    deploy(compiled)
else:
    investigate_why_worse()
```

### ❌ Mistake 5: Too Many Demos
```python
# Bad: Overloading with demos
bootstrap = BootstrapFewShot(max_bootstrapped_demos=50)
```
**Fix**: Start small, increase if needed
```python
# Good: Reasonable number
bootstrap = BootstrapFewShot(max_bootstrapped_demos=4-8)
```

---

## When to Use Bootstrapping

### Use Bootstrapping When:
- ✅ You lack high-quality labeled examples
- ✅ Need to generate diverse training data
- ✅ Want to capture program's successful patterns
- ✅ Have unlabeled data to work with
- ✅ Can define good metrics

### Don't Use Bootstrapping When:
- ❌ You have excellent labeled examples already
- ❌ Your base program is terrible (bootstrap from better program first)
- ❌ You can't define a good metric
- ❌ Training set is too small (<20 examples)

---

## Bootstrapping Cost Analysis

### Costs:
- **Compilation**: N training examples × M attempts per example
- **LM Calls**: Can be expensive with large training sets
- **Time**: Multiple rounds can take hours

### Optimization Strategies:
```python
# 1. Use cheaper LM for compilation
with dspy.context(lm=cheap_lm):
    compiled = bootstrap.compile(program, trainset)

# 2. Use subset for development
dev_compiled = bootstrap.compile(program, trainset[:50])

# 3. Cache metric evaluations
@lru_cache(maxsize=1000)
def cached_metric(example_hash, pred_hash):
    # Expensive metric computation
    pass

# 4. Limit rounds and demos
bootstrap = BootstrapFewShot(
    max_bootstrapped_demos=4,  # Fewer demos
    max_rounds=1               # Single round
)
```

---

## Testing Your Understanding

You've mastered bootstrapping if you can:

1. ✅ Explain how bootstrapping generates examples
2. ✅ Understand trace capture and analysis
3. ✅ Know when to use teacher-student bootstrapping
4. ✅ Can design metrics for quality filtering
5. ✅ Understand iterative bootstrapping
6. ✅ Can validate bootstrapping improvements
7. ✅ Know common failure modes and fixes

---

## Connection to Other Modules

### Bootstrapping Builds On:
- **Module 03 (Teleprompters)**: Bootstrapping is core to teleprompters
- **Module 04 (Optimizers)**: BootstrapRS uses these techniques

### Bootstrapping Feeds Into:
- **Module 06 (RAG)**: Bootstrap RAG examples
- **Module 08 (Evaluation)**: Trace analysis informs evaluation

---

## Quick Reference Card

```python
# Basic Bootstrapping Template

from dspy.teleprompt import BootstrapFewShot

# 1. Define strict metric
def quality_metric(example, pred, trace=None):
    # High standards for demos
    return 1.0 if perfect_match(example, pred) else 0.0

# 2. Optional: Create better teacher
teacher = dspy.ChainOfThought(BetterSignature)

# 3. Bootstrap
bootstrap = BootstrapFewShot(
    metric=quality_metric,
    max_bootstrapped_demos=8,
    max_labeled_demos=4
)

# 4. Compile (optionally with teacher)
compiled = bootstrap.compile(
    student=program,
    teacher=teacher,  # Optional
    trainset=training_examples
)

# 5. Validate
baseline_score = evaluate(program, valset)
compiled_score = evaluate(compiled, valset)
improvement = compiled_score - baseline_score
```

---

## Final Checklist

Before moving to Module 06, ensure:

- [ ] Understand what bootstrapping does
- [ ] Know how traces are captured and used
- [ ] Can explain teacher-student bootstrapping
- [ ] Understand demo quality importance
- [ ] Can validate bootstrapping improvements
- [ ] Know when bootstrapping helps vs. hurts
- [ ] Can design metrics for bootstrapping

---

## Next Steps

1. **Practice** bootstrapping on different tasks
2. **Experiment** with teacher-student configurations
3. **Move On** to Module 06: RAG (apply bootstrapping to RAG)
4. **Remember** Bootstrap quality depends on metric quality

---

**Key Mantra**: *Good metrics + Good teacher = Good bootstrapped examples.*
