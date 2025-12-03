# Module 08: Evaluation-Driven Development - Key Takeaways

## Core Concepts

### What Is Evaluation-Driven Development?
**Build → Measure → Improve → Repeat: Let metrics guide every decision.**

```
Traditional: Build → Hope it works → Deploy
DSPy EDD: Build → Evaluate → Optimize → Evaluate → Deploy
```

---

## The Evaluation Loop

```
1. DEFINE METRICS
   └─> What does "good" look like?

2. CREATE EVAL SET
   └─> Representative test cases

3. BASELINE EVALUATION
   └─> Measure current performance

4. ITERATE
   ├─> Modify system
   ├─> Re-evaluate
   └─> Compare to baseline

5. OPTIMIZE
   ├─> Use metrics to guide optimization
   └─> Validate improvements

6. DEPLOY
   └─> Only if metrics improved
```

---

## Pattern Comparison: Docs vs. Reality

### Official Docs Say:
```python
from dspy.evaluate import Evaluate

evaluator = Evaluate(
    devset=test_examples,
    metric=my_metric
)
score = evaluator(program)
print(f"Score: {score}")
```
**Philosophy**: Simple evaluation API

### Real Projects Do:
```python
from dspy.evaluate import Evaluate
import logging
import json
from datetime import datetime

class ProductionEvaluator:
    def __init__(self, metric, devset, name="eval"):
        self.metric = metric
        self.devset = devset
        self.name = name
        self.results_history = []

    def evaluate(self, program, save_results=True):
        evaluator = Evaluate(
            devset=self.devset,
            metric=self.metric,
            num_threads=4,  # Parallel evaluation
            display_progress=True
        )

        # Run evaluation
        score = evaluator(program)

        # Detailed per-example results
        detailed_results = []
        for example in self.devset:
            try:
                pred = program(**example.inputs())
                example_score = self.metric(example, pred)

                detailed_results.append({
                    'example_id': example.id,
                    'score': example_score,
                    'prediction': pred.toDict(),
                    'expected': example.toDict()
                })
            except Exception as e:
                logging.error(f"Evaluation failed for {example.id}: {e}")
                detailed_results.append({
                    'example_id': example.id,
                    'error': str(e)
                })

        # Save results
        if save_results:
            self.save_evaluation({
                'timestamp': datetime.now().isoformat(),
                'program_name': program.__class__.__name__,
                'overall_score': score,
                'num_examples': len(self.devset),
                'detailed_results': detailed_results
            })

        return score, detailed_results

    def save_evaluation(self, results):
        filename = f"eval_{self.name}_{results['timestamp']}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)

    def compare_programs(self, baseline, candidate):
        """A/B test two programs."""
        baseline_score, _ = self.evaluate(baseline)
        candidate_score, _ = self.evaluate(candidate)

        improvement = candidate_score - baseline_score
        print(f"Baseline: {baseline_score:.3f}")
        print(f"Candidate: {candidate_score:.3f}")
        print(f"Improvement: {improvement:+.3f}")

        return improvement > 0
```
**Philosophy**: Comprehensive tracking, per-example analysis, comparison

### Best Practice Is:
**Track everything, analyze failures, compare systematically.**

---

## Key Differences: Why They Matter

| Aspect | Official Docs | Real Projects | Why Different |
|--------|---------------|---------------|---------------|
| **Detailed Results** | Overall score | Per-example analysis | Docs: simple output<br>Projects: debug failures |
| **Result Tracking** | Not shown | Saved to files | Docs: one-time eval<br>Projects: track over time |
| **Parallelization** | Not mentioned | Multi-threaded | Docs: simplicity<br>Projects: speed |
| **Error Handling** | Crashes | Logged + continue | Docs: assume success<br>Projects: robustness |
| **Comparison** | Manual | Automated A/B tests | Docs: basic concept<br>Projects: systematic |

---

## Metric Design Principles

### 1. Alignment with Business Goals
```python
# ❌ Bad: Metric doesn't match goal
# Goal: Customer satisfaction
def bad_metric(example, pred):
    return len(pred.answer) > 10  # Just checks length!

# ✅ Good: Metric matches goal
def good_metric(example, pred):
    # Checks correctness, relevance, tone
    correctness = check_answer(example, pred)
    relevance = check_relevance(pred, example.context)
    tone = check_tone(pred.answer, example.expected_tone)
    return 0.5*correctness + 0.3*relevance + 0.2*tone
```

### 2. Fast Enough for Iteration
```python
# ❌ Bad: Slow metric blocks iteration
def slow_metric(example, pred):
    # Calls expensive LM-as-judge every time
    return llm_judge_quality(example, pred)  # 2 seconds per example!

# ✅ Good: Fast metric for dev, slow for final
def fast_dev_metric(example, pred):
    # Simple heuristics for quick iteration
    return simple_check(example, pred)  # 0.01 seconds

def comprehensive_prod_metric(example, pred):
    # Detailed check for final evaluation
    return detailed_check(example, pred)  # 2 seconds
```

### 3. Interpretable Scores
```python
# ❌ Bad: Opaque score
def opaque_metric(example, pred):
    return magic_formula(example, pred)  # What does 0.73 mean?

# ✅ Good: Interpretable components
def interpretable_metric(example, pred):
    scores = {
        'accuracy': accuracy_check(example, pred),
        'relevance': relevance_check(example, pred),
        'fluency': fluency_check(pred.answer)
    }
    # Can see which component is weak
    return sum(scores.values()) / len(scores), scores
```

---

## Common Metric Patterns

### 1. Binary Metrics
```python
def binary_metric(example, pred, trace=None):
    """Perfect match or nothing."""
    return 1.0 if pred.answer == example.answer else 0.0
```
**Use**: Clear right/wrong tasks (classification, exact match)

### 2. Fuzzy Matching Metrics
```python
def fuzzy_metric(example, pred, trace=None):
    """Partial credit for close matches."""
    from difflib import SequenceMatcher

    similarity = SequenceMatcher(
        None,
        pred.answer.lower(),
        example.answer.lower()
    ).ratio()

    return similarity  # 0.0 to 1.0
```
**Use**: Generated text with variations

### 3. Composite Metrics
```python
def composite_metric(example, pred, trace=None):
    """Multiple quality dimensions."""
    accuracy = check_factual_accuracy(example, pred)
    relevance = check_relevance(example, pred)
    completeness = check_completeness(example, pred)

    # Weighted combination
    return {
        'overall': 0.5*accuracy + 0.3*relevance + 0.2*completeness,
        'accuracy': accuracy,
        'relevance': relevance,
        'completeness': completeness
    }
```
**Use**: Multi-faceted quality assessment

### 4. LM-as-Judge Metrics
```python
judge_lm = dspy.LM("openai/gpt-4")

def llm_judge_metric(example, pred, trace=None):
    """Use LM to judge quality."""
    judge_prompt = f"""
    Question: {example.question}
    Expected Answer: {example.answer}
    Actual Answer: {pred.answer}

    Rate the actual answer's quality (0-10):
    - Accuracy (0-10):
    - Relevance (0-10):
    - Overall Score (0-10):
    """

    with dspy.context(lm=judge_lm):
        judgment = judge_lm(judge_prompt)

    return parse_score(judgment) / 10.0
```
**Use**: Subjective quality, complex criteria (expensive!)

---

## Evaluation Set Design

### 1. Representative Coverage
```python
# ✅ Good: Covers different scenarios
eval_set = [
    # Easy examples
    Example(question="What is 2+2?", answer="4"),

    # Medium examples
    Example(question="Who wrote Hamlet?", answer="Shakespeare"),

    # Hard examples
    Example(question="Explain quantum entanglement", answer="..."),

    # Edge cases
    Example(question="", answer="Error: empty question"),
    Example(question="..." * 1000, answer="Error: too long"),
]
```

### 2. Stratified Sampling
```python
# Ensure different types represented
eval_set = []
for category in ['easy', 'medium', 'hard']:
    examples = get_examples_by_difficulty(category)
    eval_set.extend(sample(examples, k=10))  # 10 of each
```

### 3. Adversarial Examples
```python
# Include cases where system likely fails
eval_set += [
    # Ambiguous questions
    Example(question="What's the capital?", answer="Needs country specified"),

    # Contradictory information
    Example(context="...", question="...", answer="..."),

    # Out-of-domain
    Example(question="Alien biology?", answer="No reliable information"),
]
```

---

## Critical Insights

### 1. Metrics Guide Optimization
```python
# Poor metric → Poor optimization
def bad_metric(example, pred):
    return random.random()  # Random scores!

optimizer = MIPROv2(metric=bad_metric)
# Will optimize for nothing useful

# Good metric → Good optimization
def good_metric(example, pred):
    return meaningful_quality_score(example, pred)

optimizer = MIPROv2(metric=good_metric)
# Will optimize for actual quality
```

### 2. Evaluation Set Quality Matters
```python
# ❌ Bad: Tiny, unrepresentative eval set
eval_set = [Example("test", "test")]  # 1 example!

# ✅ Good: Diverse, representative eval set
eval_set = create_diverse_eval_set(
    size=100,
    coverage=['easy', 'medium', 'hard'],
    edge_cases=True
)
```

### 3. Multiple Metrics Reveal More
```python
# Single metric can miss issues
accuracy_only = 0.95  # Looks great!
# But might have terrible relevance

# Multiple metrics show full picture
metrics = {
    'accuracy': 0.95,  # Good
    'relevance': 0.60,  # Problem!
    'fluency': 0.85,   # Okay
    'safety': 0.99     # Good
}
# Now we see relevance needs work
```

### 4. Iterate Based on Failures
```python
# Analyze failures
failures = [ex for ex in eval_results if ex['score'] < 0.5]

# Group by failure type
failure_types = group_by_pattern(failures)
print("Common failures:")
for ftype, examples in failure_types.items():
    print(f"  {ftype}: {len(examples)} cases")

# Fix specific failure modes
for ftype in failure_types:
    improve_system_for(ftype)
    re_evaluate()
```

---

## The EDD Workflow

### Step 1: Baseline
```python
baseline_program = BasicQA()
baseline_score = evaluate(baseline_program, eval_set)
print(f"Baseline: {baseline_score:.3f}")
```

### Step 2: Hypothesis
```python
# "Adding Chain-of-Thought will improve accuracy"
hypothesis_program = ImprovedQA()  # Uses CoT
```

### Step 3: Test Hypothesis
```python
hypothesis_score = evaluate(hypothesis_program, eval_set)
improvement = hypothesis_score - baseline_score
print(f"Hypothesis: {hypothesis_score:.3f} ({improvement:+.3f})")
```

### Step 4: Analyze
```python
# Which examples improved?
improved = [ex for ex in eval_set if
            score(hypothesis, ex) > score(baseline, ex)]
print(f"Improved {len(improved)}/{len(eval_set)} examples")

# Which got worse?
regressed = [ex for ex in eval_set if
             score(hypothesis, ex) < score(baseline, ex)]
print(f"Regressed {len(regressed)} examples")
analyze_regressions(regressed)
```

### Step 5: Iterate or Deploy
```python
if hypothesis_score > baseline_score + min_improvement:
    # Deploy hypothesis as new baseline
    baseline_program = hypothesis_program
    baseline_score = hypothesis_score
else:
    # Try different approach
    next_hypothesis = try_different_approach()
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: No Baseline
```python
# Bad: Optimize without knowing starting point
optimized = optimizer.compile(program, trainset)
```
**Fix**: Always measure baseline first

### ❌ Mistake 2: Overfitting to Eval Set
```python
# Bad: Same data for dev and eval
optimized = optimize(program, eval_set)
score = evaluate(optimized, eval_set)  # Overfitted!
```
**Fix**: Split data (train/dev/test)

### ❌ Mistake 3: Ignoring Per-Example Results
```python
# Bad: Only look at overall score
overall_score = 0.85  # Seems good...
```
**Fix**: Analyze failures
```python
# Good: Examine individual failures
failures = get_failures(eval_results)
analyze_failure_patterns(failures)
```

### ❌ Mistake 4: Slow Metrics Block Iteration
```python
# Bad: 10 second metric × 100 examples = 17 minutes per eval!
def slow_metric(example, pred):
    return expensive_llm_judge(example, pred)
```
**Fix**: Fast metric for dev, slow for final

### ❌ Mistake 5: Metrics Don't Match Goals
```python
# Bad: Optimize for speed when goal is quality
def metric(example, pred, trace=None):
    return 1.0 / (response_time + 0.1)  # Rewards fast, not correct!
```
**Fix**: Align metrics with actual goals

---

## Testing Your Understanding

You've mastered evaluation-driven development if you can:

1. ✅ Design metrics aligned with goals
2. ✅ Create representative eval sets
3. ✅ Measure baselines before optimizing
4. ✅ Analyze per-example results
5. ✅ Iterate based on evaluation insights
6. ✅ Track evaluation history
7. ✅ Avoid overfitting to eval set

---

## Connection to Other Modules

### EDD Builds On:
- **Module 03 (Teleprompters)**: Uses metrics for optimization
- **Module 04 (Optimizers)**: Metrics guide optimization

### EDD Feeds Into:
- **Module 09 (Error Handling)**: Eval reveals errors
- **Module 10 (Best Practices)**: EDD is a best practice

---

## Quick Reference Card

```python
# Evaluation-Driven Development Template

# 1. Define metric
def my_metric(example, pred, trace=None):
    return quality_score(example, pred)

# 2. Create eval set
eval_set = create_diverse_eval_set(size=100)

# 3. Measure baseline
from dspy.evaluate import Evaluate
evaluator = Evaluate(devset=eval_set, metric=my_metric)
baseline_score = evaluator(baseline_program)

# 4. Iterate
hypothesis_program = improve(baseline_program)
hypothesis_score = evaluator(hypothesis_program)

# 5. Compare
if hypothesis_score > baseline_score:
    deploy(hypothesis_program)
else:
    try_different_approach()

# 6. Analyze failures
failures = [ex for ex in eval_set
            if my_metric(ex, hypothesis_program(**ex.inputs())) < 0.5]
analyze_patterns(failures)
```

---

## Final Checklist

Before moving to Module 09, ensure:

- [ ] Can design aligned metrics
- [ ] Know how to create eval sets
- [ ] Understand baseline → iterate → improve loop
- [ ] Can analyze per-example results
- [ ] Know how to avoid overfitting
- [ ] Can track evaluation history
- [ ] Understand metric trade-offs

---

## Next Steps

1. **Define** metrics for your task
2. **Create** comprehensive eval set
3. **Move On** to Module 09: Error Handling
4. **Remember** Measure everything, iterate based on data

---

**Key Mantra**: *Good metrics + Good eval set + Systematic iteration = Better systems.*
