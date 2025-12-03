# DSPy Course Overview

## Mission

Transform developers into proficient DSPy practitioners by teaching through **real-world project patterns**, not just documentation examples.

## Core Approach

### The Learning Triangle

```
    Real GitHub Projects
           /  \
          /    \
         /      \
Official Docs  Your Implementation
```

Every concept is taught through three lenses:
1. What the **official documentation** teaches
2. How **production projects** actually implement it
3. Why they differ and what **you should do**

## Course Philosophy

### Code-First Learning
- **Guides**: 70% code, 30% prose
- **Challenges**: 100% commented code skeletons
- **Solutions**: Production-ready implementations
- **Theory**: Only what's needed to understand the code

### Pattern-Driven Teaching
Instead of "here's how to use Signature", we teach:
- ✅ **Official Pattern**: Simple signature definition
- ⚡ **Production Pattern**: Signature with validation, error handling, type hints
- 🎯 **Why Different**: Official focuses on learning, production needs reliability

### Progressive Complexity
```
Modules 01-03: Fundamentals
  ↓ Master core DSPy concepts
Modules 04-05: Optimization
  ↓ Learn to improve system quality
Modules 06-08: Advanced Applications
  ↓ Build real-world AI systems
Modules 09-10: Production Readiness
  ↓ Deploy with confidence
```

## Learning Outcomes

### After Completing This Course

**Foundational Skills:**
- Write DSPy Signatures that properly constrain LM behavior
- Compose Modules into complex AI pipelines
- Use Teleprompters to optimize system performance

**Intermediate Skills:**
- Implement optimizers (MIPROv2, BootstrapRS, GEPA)
- Build RAG systems with proper retrieval and generation
- Create autonomous agents with tool usage

**Advanced Skills:**
- Design evaluation-driven development workflows
- Implement production error handling and quality guards
- Scale DSPy systems for real-world deployment

**Meta Skills:**
- Read DSPy source code to understand implementation details
- Evaluate trade-offs between different DSPy patterns
- Adapt community patterns to your specific use case

## Module Breakdown

### Module 01: Signatures (4-6 hours)
**Goal**: Define precise input/output contracts for LM tasks

**Key Concepts:**
- InputField and OutputField
- Docstrings as instructions
- Type hints and validation

**Project Reference**: gabrielvanderlei/DSPy-examples basic signatures

**Deliverable**: Working classifier with custom signature

---

### Module 02: Modules & Forward (4-6 hours)
**Goal**: Build composable AI components

**Key Concepts:**
- dspy.Module inheritance
- forward() method
- dspy.Predict vs dspy.ChainOfThought
- Module composition

**Project Reference**: Scale3-Labs/dspy-examples module patterns

**Deliverable**: Multi-stage pipeline with 3+ modules

---

### Module 03: Teleprompters (3-5 hours)
**Goal**: Understand DSPy's optimization philosophy

**Key Concepts:**
- Prompt compilation vs manual engineering
- Optimizer types overview
- Metric-driven improvement

**Project Reference**: Official dspy repo examples/teleprompters

**Deliverable**: Optimized QA system showing before/after metrics

---

### Module 04: Optimizers (6-8 hours)
**Goal**: Master DSPy optimization algorithms

**Key Concepts:**
- MIPROv2 for instruction proposals
- BootstrapRS for few-shot synthesis
- GEPA for reflective evolution
- BootstrapFinetune for weight tuning

**Project Reference**: Weaviate recipes optimizer patterns

**Deliverable**: Comparison report of 3+ optimizers on same task

---

### Module 05: Bootstrapping (5-7 hours)
**Goal**: Synthesize high-quality training data

**Key Concepts:**
- Trace-based example generation
- Few-shot demonstration selection
- Bootstrapping pipelines

**Project Reference**: diicellman/dspy-gradio-rag bootstrapping approach

**Deliverable**: Self-improving system with bootstrapped examples

---

### Module 06: RAG (8-10 hours)
**Goal**: Build production-grade retrieval systems

**Key Concepts:**
- Vector store integration
- Retrieval strategies
- Generation conditioning
- RAG pipeline optimization

**Project Reference**: diicellman/dspy-gradio-rag, Weaviate recipes

**Deliverable**: End-to-end RAG system with API

---

### Module 07: Agents (8-10 hours)
**Goal**: Create autonomous AI agents

**Key Concepts:**
- dspy.ReAct module
- Tool definition and usage
- Agent loops and termination
- Multi-agent coordination

**Project Reference**: Community multi-agent systems

**Deliverable**: Agent with 3+ tools solving complex tasks

---

### Module 08: Evaluation-Driven Development (5-7 hours)
**Goal**: Iterate systems using metrics

**Key Concepts:**
- Custom metrics
- Built-in metrics (SemanticF1, answer_exact_match)
- Evaluation datasets
- Metric-guided optimization

**Project Reference**: Official dspy metrics examples

**Deliverable**: System with comprehensive evaluation suite

---

### Module 09: Error Handling & Quality Guards (4-6 hours)
**Goal**: Build reliable production systems

**Key Concepts:**
- LM failure modes
- Retry strategies
- Output validation
- Fallback mechanisms

**Project Reference**: Production patterns from Scale3-Labs

**Deliverable**: Robust system with error recovery

---

### Module 10: Best Practices (6-8 hours)
**Goal**: Deploy DSPy at scale

**Key Concepts:**
- Caching strategies
- Logging and monitoring
- Cost optimization
- Multi-LM orchestration

**Project Reference**: Production deployments analysis

**Deliverable**: Production-ready deployment checklist + example

---

## Time Investment

**Minimum**: 40 hours (fast track, skip some challenges)
**Recommended**: 60 hours (complete all challenges)
**Mastery**: 80+ hours (build custom projects)

## Prerequisites

### Required
- Python 3.9+ proficiency
- Understanding of language models (GPT, Claude, etc.)
- Basic ML concepts (embeddings, fine-tuning)

### Helpful
- Experience with prompt engineering
- Familiarity with LangChain or similar frameworks
- Production API development experience

### Not Required
- Deep learning expertise
- Academic NLP background
- DSPy prior experience

## Learning Strategy

### For Each Module

1. **Scan** (15 min)
   - Read `_meta/objectives.md`
   - Skim `key_takeaways.md`
   - Understand the goal

2. **Study** (60-90 min)
   - Work through `guide/overview.md`
   - Run `guide/annotated_examples.py`
   - Compare official vs project patterns

3. **Practice** (90-120 min)
   - Read `challenge/tasks.md`
   - Implement in `challenge/starter_code.py`
   - Don't peek at solution yet

4. **Compare** (30-45 min)
   - Run `solution/solution.py`
   - Compare your approach
   - Identify gaps in understanding

5. **Consolidate** (15-30 min)
   - Re-read `key_takeaways.md`
   - Note differences between your implementation and solution
   - Document learnings

### Study Groups

This course works well in groups:
- **Weekly meetings**: Cover 1 module per week
- **Code reviews**: Share challenge solutions
- **Pattern discussions**: Debate doc vs project approaches

## Assessment

No formal tests, but you'll know you've mastered a module when:
- ✅ You can explain why official docs differ from production code
- ✅ Your challenge solution runs without errors
- ✅ You understand every line in the solution code
- ✅ You can adapt the pattern to a different use case

## Next Steps After Course

1. **Build a Project**: Pick from `projects/` directory
2. **Contribute**: Add patterns to the community
3. **Deploy**: Put a DSPy system in production
4. **Teach**: Help others learn through your insights

## Support Resources

- Official Docs: https://dspy.ai
- Discord: DSPy community server
- GitHub Issues: stanfordnlp/dspy
- This Repo Issues: For course-specific questions

## Updates

This course tracks DSPy's rapid development:
- **Semantic Versioning**: Course version X.Y.Z
- **DSPy Compatibility**: Listed in each module's metadata
- **Pattern Updates**: New community patterns added quarterly

**Current Version**: 1.0.0
**DSPy Target**: 2.5+
**Last Updated**: 2025-12-03
