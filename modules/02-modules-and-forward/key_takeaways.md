# Module 02: Modules & Forward - Key Takeaways

## Core Concepts

### What Are DSPy Modules?
**Modules are composable components that encapsulate LM computation logic.**

```
Signature (what to do) + Module (how to do it) = Working System
```

---

## Pattern Comparison: Docs vs. Reality

### Official Docs Say:
```python
class BasicQA(dspy.Module):
    def __init__(self):
        self.generate_answer = dspy.Predict(QA)

    def forward(self, question):
        return self.generate_answer(question=question)
```
**Philosophy**: Simple inheritance, focus on concepts

### Real Projects Do:
```python
class ProductionQA(dspy.Module):
    def __init__(self, num_passages: int = 3):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate = dspy.ChainOfThought(QASignature)
        self.num_passages = num_passages

    def forward(self, question: str) -> dspy.Prediction:
        context = self.retrieve(question).passages
        prediction = self.generate(context=context, question=question)
        return dspy.Prediction(
            answer=prediction.answer,
            context=context,
            reasoning=prediction.reasoning
        )
```
**Philosophy**: Composition, type hints, configuration, explicit returns

### Best Practice Is:
**Start simple, add composition and configuration as complexity grows.**

---

## Key Differences: Why They Matter

| Aspect | Official Docs | Real Projects | Why Different |
|--------|---------------|---------------|---------------|
| **super().__init__()** | Often omitted | Always called | Docs: simplify examples<br>Projects: proper inheritance |
| **Type Hints** | Optional | Required | Docs: reduce noise<br>Projects: IDE support + docs |
| **Configuration** | Hardcoded | Parameters | Docs: show concept<br>Projects: reusability |
| **Return Types** | Direct output | dspy.Prediction | Docs: simplicity<br>Projects: structured returns |
| **Error Handling** | None | Try/except | Docs: focus on happy path<br>Projects: handle failures |

---

## The Three Critical Components

### 1. Class Definition
```python
class MyModule(dspy.Module):
    def __init__(self):
        super().__init__()  # Important for DSPy internals
```
**Impact**: Missing super() breaks optimization

### 2. Module Initialization
```python
def __init__(self):
    super().__init__()
    self.predictor = dspy.Predict(Signature)
    self.cot = dspy.ChainOfThought(Signature)
```
**Impact**: Predictors initialized here, not in forward()

### 3. Forward Method
```python
def forward(self, input_data):
    result = self.predictor(input=input_data)
    return result
```
**Impact**: This is called when you use module(input)

---

## Module Types Quick Reference

### dspy.Predict
```python
predictor = dspy.Predict(Signature)
result = predictor(question="What is DSPy?")
```
**When**: Direct prediction, no reasoning needed
**Speed**: Fast
**Quality**: Good for simple tasks

### dspy.ChainOfThought
```python
cot = dspy.ChainOfThought(Signature)
result = cot(question="Why is the sky blue?")
print(result.reasoning)  # Intermediate thoughts
print(result.answer)      # Final answer
```
**When**: Complex tasks needing reasoning
**Speed**: Slower (extra tokens)
**Quality**: Better on complex tasks

### dspy.ReAct
```python
agent = dspy.ReAct(Signature, tools=[search, calculate])
result = agent(task="Find population of Tokyo")
```
**When**: Need tool usage
**Speed**: Slowest (multiple LM calls)
**Quality**: Best for multi-step tasks

---

## Common Patterns

### 1. Single Predictor Module
```python
class Classifier(dspy.Module):
    def __init__(self):
        super().__init__()
        self.classify = dspy.Predict(ClassifySignature)

    def forward(self, text):
        return self.classify(text=text)
```
**Use**: Simple tasks, one LM call

### 2. Multi-Stage Pipeline
```python
class Pipeline(dspy.Module):
    def __init__(self):
        super().__init__()
        self.stage1 = dspy.Predict(Stage1Sig)
        self.stage2 = dspy.ChainOfThought(Stage2Sig)

    def forward(self, input_data):
        intermediate = self.stage1(input=input_data)
        final = self.stage2(context=intermediate.output)
        return final
```
**Use**: Multi-step processing

### 3. Conditional Logic Module
```python
class SmartQA(dspy.Module):
    def __init__(self):
        super().__init__()
        self.simple = dspy.Predict(QA)
        self.complex = dspy.ChainOfThought(QA)

    def forward(self, question):
        if len(question.split()) < 5:
            return self.simple(question=question)
        else:
            return self.complex(question=question)
```
**Use**: Optimize cost/quality trade-offs

### 4. Retrieval-Augmented Module
```python
class RAG(dspy.Module):
    def __init__(self, k=3):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=k)
        self.generate = dspy.ChainOfThought(GenerateAnswer)

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.generate(context=context, question=question)
```
**Use**: QA with external knowledge

---

## Critical Insights

### 1. Modules Enable Composition
```python
# Compose modules like LEGO blocks
class ComplexSystem(dspy.Module):
    def __init__(self):
        super().__init__()
        self.module1 = SimpleModule1()
        self.module2 = SimpleModule2()
```

### 2. forward() Is the Entry Point
```python
module = MyModule()
result = module(input="test")  # Calls forward() automatically
```

### 3. State Lives in __init__
```python
# ✅ Good: Predictors in __init__
def __init__(self):
    self.pred = dspy.Predict(Sig)

# ❌ Bad: Predictors in forward()
def forward(self, x):
    pred = dspy.Predict(Sig)  # Creates new predictor every call!
```

### 4. Modules Are Optimizable
```python
# Entire module can be optimized end-to-end
optimizer = dspy.MIPROv2(metric=my_metric)
optimized_module = optimizer.compile(module, trainset=data)
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Forgetting super().__init__()
```python
# Bad
class MyModule(dspy.Module):
    def __init__(self):
        self.pred = dspy.Predict(Sig)  # Missing super()!
```
**Fix**: Always call `super().__init__()` first

### ❌ Mistake 2: Creating Predictors in forward()
```python
# Bad
def forward(self, question):
    pred = dspy.Predict(QA)  # Created every call!
    return pred(question=question)
```
**Fix**: Initialize predictors in `__init__()`

### ❌ Mistake 3: No Return Value
```python
# Bad
def forward(self, x):
    result = self.pred(input=x)
    print(result)  # Don't print, return!
```
**Fix**: Always return the result

### ❌ Mistake 4: Modifying Signature in forward()
```python
# Bad
def forward(self, x):
    self.pred.signature = NewSig  # Don't change at runtime!
```
**Fix**: Create separate predictors for different signatures

### ❌ Mistake 5: Side Effects Without Safeguards
```python
# Bad
def forward(self, x):
    self.cache.append(x)  # State mutation can break optimization
```
**Fix**: Use stateless forward() or document side effects clearly

---

## Module Composition Strategies

### Strategy 1: Sequential Pipeline
```python
output1 = module1(input)
output2 = module2(output1)
output3 = module3(output2)
```
**When**: Linear processing flow

### Strategy 2: Parallel Processing
```python
result1 = module1(input)
result2 = module2(input)
combined = combine_results(result1, result2)
```
**When**: Independent operations

### Strategy 3: Conditional Branching
```python
if condition:
    result = module_a(input)
else:
    result = module_b(input)
```
**When**: Different paths based on input

### Strategy 4: Iterative Refinement
```python
result = initial_module(input)
for i in range(max_iterations):
    result = refinement_module(result)
    if quality_check(result):
        break
```
**When**: Iterative improvement needed

---

## When to Use Which Module Type

### Use dspy.Predict When:
- ✅ Simple, direct tasks
- ✅ Speed is critical
- ✅ Input → Output is straightforward
- ✅ No reasoning needed

### Use dspy.ChainOfThought When:
- ✅ Complex reasoning required
- ✅ Quality > Speed
- ✅ Want to see intermediate steps
- ✅ Multi-step logic

### Use dspy.ReAct When:
- ✅ Need external tools
- ✅ Multi-step planning required
- ✅ Iterative problem-solving
- ✅ Dynamic decision-making

### Use Custom Modules When:
- ✅ Combining multiple predictors
- ✅ Complex business logic
- ✅ Conditional execution
- ✅ Reusable components

---

## Testing Your Understanding

You've mastered modules if you can:

1. ✅ Inherit from dspy.Module correctly
2. ✅ Initialize predictors in __init__
3. ✅ Implement forward() method
4. ✅ Compose multiple modules
5. ✅ Choose appropriate module types
6. ✅ Handle errors gracefully
7. ✅ Write reusable, configurable modules

---

## Connection to Other Modules

### Modules Build On:
- **Module 01 (Signatures)**: Modules use Signatures to define tasks

### Modules Feed Into:
- **Module 03 (Teleprompters)**: Optimizers work on modules
- **Module 06 (RAG)**: RAG systems are complex modules
- **Module 07 (Agents)**: Agents are specialized modules

---

## Quick Reference Card

```python
# Basic Module Template
class MyModule(dspy.Module):
    def __init__(self, config_param=default):
        super().__init__()  # Always call this!
        self.predictor = dspy.Predict(Signature)
        self.config = config_param

    def forward(self, input_data: str) -> dspy.Prediction:
        result = self.predictor(input=input_data)
        return result

# Usage
module = MyModule(config_param=value)
output = module(input_data="test")
```

---

## Final Checklist

Before moving to Module 03, ensure:

- [ ] Can create basic dspy.Module subclass
- [ ] Know when to use Predict vs. ChainOfThought
- [ ] Understand forward() method purpose
- [ ] Can compose multiple modules
- [ ] Know difference: __init__ vs. forward
- [ ] Can add configuration parameters
- [ ] Understand module optimization concept

---

## Next Steps

1. **Review** Module 01 (Signatures) + Module 02 (Modules) together
2. **Practice** building 3-5 different module types
3. **Move On** to Module 03: Teleprompters (optimization concepts)
4. **Remember** Modules = reusable, composable, optimizable components

---

**Key Mantra**: *Signatures define WHAT, Modules define HOW, Optimizers improve BOTH.*
