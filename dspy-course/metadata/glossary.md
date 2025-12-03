# DSPy Glossary

## Core Concepts

### Signature
**Definition**: A declarative specification of an AI task's inputs, outputs, and instructions.

**Official Docs Say**: "Signatures define what your language model should do"

**In Practice**: Signatures are contracts that decouple task definition from execution strategy. They enable swapping LMs and optimization strategies without rewriting logic.

**Example**:
```python
class QA(dspy.Signature):
    """Answer questions with short factoid answers."""
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()
```

**Related**: InputField, OutputField, Module

---

### Module
**Definition**: A composable component that encapsulates LM computation logic.

**Official Docs Say**: "Modules are like PyTorch modules but for language models"

**In Practice**: Modules implement the `forward()` method and can be composed into pipelines. They maintain state (like few-shot examples) and can be optimized end-to-end.

**Example**:
```python
class MyModule(dspy.Module):
    def __init__(self):
        self.predictor = dspy.ChainOfThought(QA)

    def forward(self, question):
        return self.predictor(question=question)
```

**Related**: Signature, Teleprompter, Optimizer

---

### Teleprompter
**Definition**: Legacy term for DSPy optimizers that "compile" high-level code into effective prompts.

**Official Docs Say**: "Teleprompters automatically optimize your prompts"

**In Practice**: The term is deprecated. Use "Optimizer" instead. Teleprompters were the original DSPy optimization algorithms (BootstrapFewShot, etc.). Modern DSPy uses more sophisticated optimizers.

**Example**:
```python
# Legacy (still works)
from dspy.teleprompt import BootstrapFewShot
teleprompter = BootstrapFewShot()

# Modern
from dspy.optimizers import BootstrapRS
optimizer = BootstrapRS()
```

**Related**: Optimizer, Compilation

---

### Optimizer
**Definition**: Algorithm that improves DSPy program quality by modifying prompts, examples, or weights.

**Official Docs Say**: "Optimizers compile your program using training data and a metric"

**In Practice**: Different optimizers suit different scenarios:
- **MIPROv2**: Best for instruction optimization
- **BootstrapRS**: Best for few-shot synthesis
- **GEPA**: Best for reflective improvement
- **BootstrapFinetune**: Best when you can finetune

**Example**:
```python
optimizer = dspy.MIPROv2(
    metric=validate_answer,
    num_candidates=10
)
optimized_program = optimizer.compile(
    program,
    trainset=train_data
)
```

**Related**: Teleprompter, Metric, Compilation

---

### Metric
**Definition**: Function that scores program outputs, guiding optimization.

**Official Docs Say**: "Metrics tell the optimizer what 'good' looks like"

**In Practice**: Metrics return numeric scores (higher = better). Can be simple (exact match) or complex (LM-as-judge). Critical for optimization success.

**Example**:
```python
def validate_answer(example, pred, trace=None):
    # Simple exact match
    return example.answer.lower() == pred.answer.lower()

# Or use built-in
from dspy.evaluate import answer_exact_match
```

**Related**: Optimizer, Evaluation

---

### Trace
**Definition**: Record of all LM calls and intermediate outputs during program execution.

**Official Docs Say**: Not explicitly defined in official docs

**In Practice**: Traces enable bootstrapping by capturing successful execution paths. Optimizers analyze traces to extract patterns and generate training data.

**Example**:
```python
# Traces captured automatically during evaluation
with dspy.context(trace=True):
    result = program(input)
    # Trace stored in dspy.settings
```

**Related**: Bootstrapping, Optimizer

---

### InputField
**Definition**: Signature field marking required input data.

**Official Docs Say**: "InputField() marks inputs to your signature"

**In Practice**: Can include descriptions that become part of the prompt. Supports type hints for validation.

**Example**:
```python
class Summarize(dspy.Signature):
    document: str = dspy.InputField(desc="Long text to summarize")
    # 'desc' appears in the prompt given to LM
```

**Related**: OutputField, Signature

---

### OutputField
**Definition**: Signature field marking expected output data.

**Official Docs Say**: "OutputField() marks outputs from your signature"

**In Practice**: Can include descriptions that guide LM generation. Crucial for structured output.

**Example**:
```python
class ExtractInfo(dspy.Signature):
    title: str = dspy.OutputField(desc="The main title")
    summary: str = dspy.OutputField(desc="3-sentence summary")
```

**Related**: InputField, Signature

---

### dspy.Predict
**Definition**: Basic module that performs direct prediction using a signature.

**Official Docs Say**: "Predict is the simplest DSPy module"

**In Practice**: Use for straightforward tasks without reasoning chains. Fast but may underperform on complex tasks.

**Example**:
```python
predictor = dspy.Predict(QA)
result = predictor(question="What is DSPy?")
```

**Related**: ChainOfThought, ReAct, Module

---

### dspy.ChainOfThought
**Definition**: Module that generates reasoning before the final answer.

**Official Docs Say**: "ChainOfThought adds a reasoning step"

**In Practice**: Significantly improves accuracy on complex tasks at the cost of additional tokens. Automatically adds a "reasoning" output field.

**Example**:
```python
cot = dspy.ChainOfThought(QA)
result = cot(question="Why is the sky blue?")
print(result.reasoning)  # Shows thought process
print(result.answer)     # Final answer
```

**Related**: Predict, ReAct

---

### dspy.ReAct
**Definition**: Module implementing the ReAct (Reasoning + Acting) agent pattern.

**Official Docs Say**: "ReAct enables tool use through reasoning and acting"

**In Practice**: Creates agents that alternate between reasoning about what to do and executing tools. Essential for building autonomous agents.

**Example**:
```python
class Agent(dspy.Module):
    def __init__(self):
        self.react = dspy.ReAct(
            signature=AgentSignature,
            tools=[search_tool, calculator_tool]
        )
```

**Related**: ChainOfThought, Agent, Tools

---

### Compilation
**Definition**: Process of transforming a DSPy program through optimization.

**Official Docs Say**: "Compilation improves your program automatically"

**In Practice**: Not literal code compilation. Instead, optimizers modify the program's prompts, few-shot examples, or weights based on training data and metrics.

**Example**:
```python
# Before: basic program
program = BasicQA()

# Compilation
optimizer = dspy.MIPROv2(metric=my_metric)
compiled_program = optimizer.compile(program, trainset=data)

# After: optimized program with better prompts/examples
```

**Related**: Optimizer, Teleprompter

---

### RAG (Retrieval-Augmented Generation)
**Definition**: Pattern where generation is conditioned on retrieved context.

**Official Docs Say**: "RAG combines retrieval with generation"

**In Practice**: DSPy modules retrieve relevant documents, then pass them to generator. The entire pipeline (retrieval + generation) can be optimized end-to-end.

**Example**:
```python
class RAG(dspy.Module):
    def __init__(self):
        self.retrieve = dspy.Retrieve(k=3)
        self.generate = dspy.ChainOfThought(GenerateAnswer)

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.generate(context=context, question=question)
```

**Related**: Retrieval, Generation, Module

---

### Few-Shot Examples
**Definition**: Input-output pairs shown to the LM before the actual task.

**Official Docs Say**: "Few-shot examples help the LM understand the task"

**In Practice**: DSPy optimizers automatically select and generate few-shot examples. Manual prompt engineering is replaced by metric-driven example selection.

**Example**:
```python
# DSPy handles this automatically after optimization
# Before optimization: no examples
# After optimization: program includes optimal examples
```

**Related**: Bootstrapping, Optimizer

---

### Bootstrapping
**Definition**: Technique for synthesizing training data from execution traces.

**Official Docs Say**: "Bootstrapping creates training data automatically"

**In Practice**: Run your program on inputs, capture successful traces, extract intermediate reasoning as few-shot examples. Enables self-improvement.

**Example**:
```python
optimizer = dspy.BootstrapRS(
    metric=validate,
    max_bootstrapped_demos=8
)
# Optimizer will run program, collect traces, extract examples
```

**Related**: Trace, Few-Shot Examples

---

### LM (Language Model)
**Definition**: The underlying model (GPT-4, Claude, etc.) that DSPy programs call.

**Official Docs Say**: "Configure your LM with dspy.configure()"

**In Practice**: DSPy abstracts LM details. Same code works with different LMs. Configuration is global but can be overridden per-module.

**Example**:
```python
import dspy

# Configure globally
lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)

# Or per-module
with dspy.context(lm=dspy.LM("anthropic/claude-3-5-sonnet")):
    result = module(input)
```

**Related**: Configuration, Settings

---

### Configuration
**Definition**: Global DSPy settings for LM, caching, and behavior.

**Official Docs Say**: "Use dspy.configure() to set up DSPy"

**In Practice**: Typically called once at program start. Can be overridden using context managers for different parts of pipeline.

**Example**:
```python
dspy.configure(
    lm=dspy.LM("openai/gpt-4o"),
    cache=True,  # Cache LM calls
    trace=True   # Enable tracing
)
```

**Related**: LM, Context

---

### Agent
**Definition**: Autonomous system that reasons about actions and uses tools to accomplish goals.

**Official Docs Say**: Limited official documentation on agents

**In Practice**: Built using dspy.ReAct or custom modules. Agents loop: observe → reason → act → repeat. Community has many agent patterns.

**Example**:
```python
class ResearchAgent(dspy.Module):
    def __init__(self):
        self.react = dspy.ReAct(
            signature="goal -> action, result",
            tools=[search, summarize, synthesize]
        )
```

**Related**: ReAct, Tools

---

### Tool
**Definition**: Python function that agents can call to interact with external systems.

**Official Docs Say**: "Tools give agents capabilities beyond text generation"

**In Practice**: Tools are wrapped Python functions with clear signatures. DSPy passes tool descriptions to LM, which decides when to call them.

**Example**:
```python
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information."""
    # Implementation
    return results

# Register as tool
tools = [search_wikipedia]
agent = dspy.ReAct(signature=AgentSig, tools=tools)
```

**Related**: Agent, ReAct

---

### Evaluation
**Definition**: Process of measuring program quality on a test set.

**Official Docs Say**: "Use dspy.Evaluate to test your program"

**In Practice**: Evaluation drives optimization. Run program on test data, compute metrics, iterate. DSPy provides evaluation harness.

**Example**:
```python
from dspy.evaluate import Evaluate

evaluator = Evaluate(
    devset=test_data,
    metric=my_metric,
    num_threads=4
)

score = evaluator(program)
```

**Related**: Metric, Optimizer

---

## Advanced Concepts

### MIPROv2
**Meaning**: Optimization algorithm that proposes multiple instruction candidates and selects best via discrete search.

**Use When**: You need better task instructions without few-shot examples.

---

### BootstrapRS
**Meaning**: Bootstrap with Random Search. Generates few-shot examples through execution traces.

**Use When**: You want few-shot examples but don't have labeled data.

---

### GEPA
**Meaning**: Generate, Evaluate, Propose, Adapt. Reflective optimization using LM feedback.

**Use When**: Iterative improvement through self-critique.

---

### BootstrapFinetune
**Meaning**: Generate training data via bootstrapping, then finetune LM weights.

**Use When**: You can finetune and want maximum performance.

---

### SemanticF1
**Meaning**: Built-in metric comparing semantic similarity of outputs.

**Use When**: Exact match is too strict, but you need automated evaluation.

---

### Context Manager
**Meaning**: Python `with` statement for temporary DSPy configuration.

**Use When**: You need different settings for part of your program.

**Example**:
```python
with dspy.context(lm=different_lm):
    result = module(input)
```

---

## Terminology Differences

### Official Docs vs. Community

| Official Term | Community Term | Preferred |
|--------------|----------------|-----------|
| Teleprompter | Optimizer | Optimizer |
| Compilation | Optimization | Either |
| Demos | Few-shot examples | Either |
| Trainset | Training data | Either |
| Devset | Validation data | Either |

### DSPy vs. Other Frameworks

| DSPy | LangChain | PyTorch |
|------|-----------|---------|
| Module | Chain | Module |
| Signature | Prompt Template | N/A |
| Optimizer | N/A (manual) | Optimizer |
| Predict | LLM call | Forward |

---

## Quick Reference

**Core Abstractions**:
- Signature → what to do
- Module → how to do it
- Optimizer → make it better
- Metric → define "better"

**Common Modules**:
- `Predict` → direct prediction
- `ChainOfThought` → reasoning + prediction
- `ReAct` → agent with tools
- `Retrieve` → fetch relevant context

**Common Optimizers**:
- `MIPROv2` → optimize instructions
- `BootstrapRS` → synthesize examples
- `GEPA` → reflective improvement
- `BootstrapFinetune` → finetune weights

**Common Patterns**:
- RAG → Retrieve + Generate
- Agent → ReAct + Tools
- Pipeline → Compose modules
- Ensemble → Multiple programs → vote

---

## Resources

- Official Glossary: https://dspy.ai/learn/programming/signatures
- API Reference: https://dspy.ai/api/
- Community Patterns: See `projects/` directory

**Last Updated**: 2025-12-03
