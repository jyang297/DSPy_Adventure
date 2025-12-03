# Module 04: Optimizers - Key Takeaways

## Core Concepts

### What Are DSPy Optimizers?
**Optimizers are algorithms that automatically improve your DSPy programs by modifying instructions, examples, or weights.**

```
Teleprompters (legacy) → Basic few-shot optimization
Optimizers (modern)    → Sophisticated multi-strategy optimization
```

---

## The Four Main Optimizers

### 1. MIPROv2 (Instruction Optimization)
```python
from dspy.optimizers import MIPROv2

optimizer = MIPROv2(
    metric=my_metric,
    num_candidates=10,  # Try 10 different instructions
    init_temperature=1.0
)
optimized = optimizer.compile(program, trainset=train_data)
```

**What It Does**: Proposes multiple instruction variants, tests them, picks best
**Best For**: Improving task descriptions and prompts
**Cost**: High (generates many candidates)
**Quality Gain**: Significant on instruction-sensitive tasks

---

### 2. BootstrapRS (Few-Shot Synthesis)
```python
from dspy.optimizers import BootstrapRS

optimizer = BootstrapRS(
    metric=my_metric,
    max_bootstrapped_demos=8,
    max_labeled_demos=4
)
optimized = optimizer.compile(program, trainset=train_data)
```

**What It Does**: Generates few-shot examples through execution traces + random search
**Best For**: When you lack good examples or want automatic demo generation
**Cost**: Medium (multiple LM calls per example)
**Quality Gain**: Good, especially with weak baselines

---

### 3. GEPA (Reflective Evolution)
```python
# Note: GEPA implementation varies by version
optimizer = GEPA(
    metric=my_metric,
    num_iterations=5,
    feedback_mode="llm"
)
optimized = optimizer.compile(program, trainset=train_data)
```

**What It Does**: Generate → Evaluate → Propose improvements → Adapt (iterative)
**Best For**: Complex tasks needing refinement through self-critique
**Cost**: Very high (multiple iterations with LM feedback)
**Quality Gain**: Excellent on tasks requiring nuanced improvements

---

### 4. BootstrapFinetune (Weight Optimization)
```python
from dspy.optimizers import BootstrapFinetune

optimizer = BootstrapFinetune(
    metric=my_metric,
    max_bootstrapped_demos=100
)
optimized = optimizer.compile(
    program,
    trainset=train_data,
    target="llama-7b"  # Model to finetune
)
```

**What It Does**: Generates training data via bootstrapping, then finetunes model weights
**Best For**: Maximum quality when you can finetune
**Cost**: Extremely high (requires finetuning infrastructure)
**Quality Gain**: Best possible, but requires more infrastructure

---

## Pattern Comparison: Docs vs. Reality

### Official Docs Say:
```python
optimizer = MIPROv2(metric=validate)
optimized = optimizer.compile(program, trainset=data)
```
**Philosophy**: Simple API, show concept

### Real Projects Do:
```python
from dspy.optimizers import MIPROv2
import logging
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_metric(example_hash, pred_hash):
    # Actual metric computation
    pass

def robust_metric(example, pred, trace=None):
    try:
        score = cached_metric(hash(str(example)), hash(str(pred)))
        logging.info(f"Score: {score}")
        return score
    except Exception as e:
        logging.error(f"Metric failed: {e}")
        return 0.0

optimizer = MIPROv2(
    metric=robust_metric,
    num_candidates=20,
    init_temperature=1.2,
    verbose=True
)

# Use subset for dev
dev_optimized = optimizer.compile(
    program,
    trainset=train_data[:100],
    max_steps=10
)

# Validate before production
val_score = evaluate(dev_optimized, val_data)
if val_score > threshold:
    prod_optimized = optimizer.compile(program, train_data)
    prod_optimized.save("production_v2.json")
```
**Philosophy**: Caching, validation, logging, incremental deployment

### Best Practice Is:
**Iterate with small datasets, validate gains, then optimize fully for production.**

---

## Key Differences: Why They Matter

| Aspect | Official Docs | Real Projects | Why Different |
|--------|---------------|---------------|---------------|
| **Caching** | None | Aggressive | Docs: simplicity<br>Projects: avoid redundant LM calls |
| **Validation** | Optional | Always | Docs: assume success<br>Projects: ensure improvement |
| **Dataset Size** | Full | Subset first | Docs: show complete process<br>Projects: iterate fast |
| **Logging** | Minimal | Comprehensive | Docs: reduce noise<br>Projects: debug failures |
| **Checkpointing** | Not shown | Regular | Docs: assume completion<br>Projects: handle crashes |

---

## Optimizer Selection Guide

```
┌─────────────────────────────────────────────────────────────┐
│                    OPTIMIZER DECISION TREE                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Can you finetune?                                          │
│    ├─ YES → BootstrapFinetune (best quality)              │
│    └─ NO → Continue                                         │
│                                                             │
│  Is task instruction-sensitive?                             │
│    ├─ YES → MIPROv2 (optimize instructions)               │
│    └─ NO → Continue                                         │
│                                                             │
│  Need iterative refinement?                                 │
│    ├─ YES → GEPA (reflective improvement)                 │
│    └─ NO → Continue                                         │
│                                                             │
│  Need few-shot examples?                                    │
│    └─ YES → BootstrapRS (synthesize demos)                │
│                                                             │
│  Budget constrained?                                        │
│    └─ YES → BootstrapRS (most cost-effective)             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Critical Insights

### 1. Layer Optimizers for Best Results
```python
# Round 1: Bootstrap few-shot examples
stage1 = BootstrapRS(metric=my_metric, max_bootstrapped_demos=8)
program_v1 = stage1.compile(program, trainset)

# Round 2: Optimize instructions
stage2 = MIPROv2(metric=my_metric, num_candidates=10)
program_v2 = stage2.compile(program_v1, trainset)

# Round 3: Reflective refinement
stage3 = GEPA(metric=my_metric, num_iterations=3)
program_v3 = stage3.compile(program_v2, trainset)

# Result: Progressively better program
```

### 2. Validation Set Is Critical
```python
# ❌ Bad: No validation
optimized = optimizer.compile(program, trainset=all_data)

# ✅ Good: Hold out validation
train, val = split_data(all_data, 0.8)
optimized = optimizer.compile(program, trainset=train)
val_score = evaluate(optimized, val)

if val_score > baseline_score:
    deploy(optimized)
else:
    keep_baseline()
```

### 3. Optimization Can Overfit
```python
# Signs of overfitting:
train_score = 0.95  # High training score
val_score = 0.65    # Low validation score

# Solutions:
# 1. Reduce optimization intensity
optimizer = MIPROv2(num_candidates=5)  # Fewer candidates

# 2. Use early stopping
if val_score_not_improving_for_n_steps:
    break

# 3. Regularization via simpler instructions
optimizer = MIPROv2(prefer_simpler=True)
```

### 4. Different Tasks Need Different Optimizers
```python
# Classification (instruction-sensitive)
classifier_opt = MIPROv2(metric=accuracy)

# Generation (example-sensitive)
generator_opt = BootstrapRS(metric=quality_score)

# Complex reasoning (needs refinement)
reasoner_opt = GEPA(metric=reasoning_quality)

# Production deployment (need best quality)
production_opt = BootstrapFinetune(metric=composite_metric)
```

---

## Optimization Workflow Best Practices

### Development Phase
```python
# 1. Start with baseline
baseline = dspy.Predict(Signature)
baseline_score = evaluate(baseline, val_data)

# 2. Quick optimization (subset, fast optimizer)
quick_opt = BootstrapRS(max_bootstrapped_demos=2)
quick_prog = quick_opt.compile(baseline, trainset[:50])
quick_score = evaluate(quick_prog, val_data)

# 3. If improvement, invest more
if quick_score > baseline_score:
    better_opt = MIPROv2(num_candidates=10)
    better_prog = better_opt.compile(baseline, trainset[:200])
```

### Production Phase
```python
# 1. Full optimization with best hyperparameters
prod_opt = MIPROv2(
    metric=production_metric,
    num_candidates=20,
    verbose=True
)
prod_prog = prod_opt.compile(baseline, full_trainset)

# 2. Rigorous validation
train_score = evaluate(prod_prog, trainset)
val_score = evaluate(prod_prog, valset)
test_score = evaluate(prod_prog, holdout_testset)

# 3. A/B test against baseline
deploy_canary(prod_prog, traffic_percent=10)
monitor_metrics(days=7)

# 4. Full rollout if successful
if canary_success:
    deploy_full(prod_prog)
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: No Baseline Comparison
```python
# Bad: Optimize without knowing baseline
optimized = optimizer.compile(program, trainset)
```
**Fix**: Always measure baseline first
```python
baseline_score = evaluate(program, valset)
optimized = optimizer.compile(program, trainset)
optimized_score = evaluate(optimized, valset)
print(f"Improvement: {optimized_score - baseline_score}")
```

### ❌ Mistake 2: Using Training Set for Validation
```python
# Bad: Same data for optimization and validation
optimized = optimizer.compile(program, trainset=all_data)
score = evaluate(optimized, all_data)  # Overfitting!
```
**Fix**: Split data
```python
train, val = split_data(all_data, 0.8)
optimized = optimizer.compile(program, trainset=train)
score = evaluate(optimized, val)
```

### ❌ Mistake 3: Wrong Optimizer for Task
```python
# Bad: Using finetuning optimizer when you can't finetune
optimizer = BootstrapFinetune(...)  # Requires finetuning infrastructure!
```
**Fix**: Match optimizer to capabilities
```python
# If no finetuning, use prompt-based optimizers
optimizer = MIPROv2(...)  # or BootstrapRS or GEPA
```

### ❌ Mistake 4: No Cost Tracking
```python
# Bad: Blind optimization
optimized = expensive_optimizer.compile(program, huge_trainset)
```
**Fix**: Track and limit costs
```python
with cost_tracker():
    optimized = optimizer.compile(program, trainset)
    if cost_tracker.total_cost > budget:
        rollback()
```

### ❌ Mistake 5: No Checkpointing
```python
# Bad: 6-hour optimization with no checkpoints
optimized = optimizer.compile(program, trainset)  # Crashes at 5.5 hours!
```
**Fix**: Save intermediate results
```python
optimizer = MIPROv2(checkpoint_dir="./checkpoints")
optimized = optimizer.compile(program, trainset)
# Can resume if crashed
```

---

## Optimizer Comparison Table

| Optimizer | Cost | Time | Quality | Use Case |
|-----------|------|------|---------|----------|
| **BootstrapRS** | $ | Fast | Good | Few-shot synthesis, cost-effective |
| **MIPROv2** | $$ | Medium | Great | Instruction optimization |
| **GEPA** | $$$ | Slow | Excellent | Complex tasks, refinement |
| **BootstrapFinetune** | $$$$ | Very Slow | Best | Production, maximum quality |

---

## Metric Design for Optimizers

### 1. Fast Metrics (for iteration)
```python
def fast_metric(example, pred, trace=None):
    # Simple exact match
    return 1.0 if pred.answer == example.answer else 0.0
```
**Use**: Development, quick feedback

### 2. Comprehensive Metrics (for production)
```python
def comprehensive_metric(example, pred, trace=None):
    accuracy = check_accuracy(example, pred)
    relevance = check_relevance(pred, example.context)
    fluency = check_fluency(pred.answer)
    safety = check_safety(pred.answer)
    return 0.4*accuracy + 0.3*relevance + 0.2*fluency + 0.1*safety
```
**Use**: Production optimization

### 3. Trace-Aware Metrics (advanced)
```python
def trace_aware_metric(example, pred, trace=None):
    if trace is None:
        return basic_metric(example, pred)

    # Check reasoning quality
    reasoning_steps = len(trace)
    efficient = 1.0 if reasoning_steps < 5 else 0.5

    correctness = check_answer(example, pred)

    return 0.7 * correctness + 0.3 * efficient
```
**Use**: Optimize both quality and efficiency

---

## When to Use Which Optimizer

### Use BootstrapRS When:
- ✅ Need few-shot examples
- ✅ Budget constrained
- ✅ Fast iteration required
- ✅ Task is example-driven

### Use MIPROv2 When:
- ✅ Instructions matter a lot
- ✅ Want multiple variants tested
- ✅ Have moderate budget
- ✅ Task is instruction-sensitive

### Use GEPA When:
- ✅ Complex, nuanced tasks
- ✅ Iterative refinement helps
- ✅ Can afford expensive optimization
- ✅ Quality is paramount

### Use BootstrapFinetune When:
- ✅ Have finetuning infrastructure
- ✅ Maximum quality needed
- ✅ High-volume production use
- ✅ Can amortize finetuning cost

---

## Testing Your Understanding

You've mastered optimizers if you can:

1. ✅ Name the 4 main optimizer types
2. ✅ Explain what each optimizer does
3. ✅ Choose appropriate optimizer for a task
4. ✅ Layer multiple optimizers
5. ✅ Validate optimization improvements
6. ✅ Understand cost/quality trade-offs
7. ✅ Design metrics for optimizers

---

## Connection to Other Modules

### Optimizers Build On:
- **Module 02 (Modules)**: Optimizers improve modules
- **Module 03 (Teleprompters)**: Modern evolution of teleprompters

### Optimizers Feed Into:
- **Module 05 (Bootstrapping)**: Deep dive into bootstrap mechanics
- **Module 08 (Evaluation)**: Metrics are shared between both

---

## Quick Reference Card

```python
# Optimizer Selection Cheat Sheet

# Fast & Cheap: Few-shot examples
from dspy.optimizers import BootstrapRS
opt = BootstrapRS(metric=my_metric, max_bootstrapped_demos=8)

# Medium Cost: Instruction optimization
from dspy.optimizers import MIPROv2
opt = MIPROv2(metric=my_metric, num_candidates=10)

# Expensive: Reflective improvement
# (Implementation varies, check docs)
opt = GEPA(metric=my_metric, num_iterations=5)

# Most Expensive: Finetuning
from dspy.optimizers import BootstrapFinetune
opt = BootstrapFinetune(metric=my_metric, max_bootstrapped_demos=100)

# Compile
optimized = opt.compile(program, trainset=train_data)

# Validate
score = evaluate(optimized, val_data)
```

---

## Final Checklist

Before moving to Module 05, ensure:

- [ ] Understand the 4 main optimizer types
- [ ] Know when to use each optimizer
- [ ] Can layer optimizers for better results
- [ ] Understand validation importance
- [ ] Can track optimization costs
- [ ] Know how to prevent overfitting
- [ ] Can design metrics for optimization

---

## Next Steps

1. **Practice** using different optimizers on same task
2. **Compare** their results and costs
3. **Move On** to Module 05: Bootstrapping (deep dive)
4. **Remember** Optimization is about systematic improvement

---

**Key Mantra**: *Choose optimizer by task needs, validate improvements, watch costs.*
