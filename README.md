# DSPy Learning Repository

**A Complete, Multi-Level, Project-Driven DSPy Course**

Learn DSPy through real GitHub projects, official documentation comparisons, and production-level implementations.

## Philosophy

This course teaches DSPy by:
1. **First reading project patterns** from real-world implementations
2. **Contrasting with official docs** to understand design decisions
3. **Completing challenges** that force you to apply both patterns
4. **Implementing solutions** using production-level best practices

## Course Structure

```
dspy-course/
├── metadata/           # Course overview, glossary, references
├── modules/            # 10 progressive learning modules
├── projects/           # Real-world project reproductions
└── templates/          # Reusable templates for learning
```

## Learning Path

### Fundamentals (Modules 01-03)
- **Module 01**: Signatures - Defining AI task contracts
- **Module 02**: Modules & Forward - Building composable components
- **Module 03**: Teleprompters - Understanding optimization concepts

### Optimization (Modules 04-05)
- **Module 04**: Optimizers - MIPROv2, BootstrapRS, GEPA
- **Module 05**: Bootstrapping - Synthesizing few-shot examples

### Advanced Applications (Modules 06-08)
- **Module 06**: RAG - Retrieval-Augmented Generation systems
- **Module 07**: Agents - Building autonomous AI agents
- **Module 08**: Evaluation-Driven Development - Metrics and iteration

### Production Readiness (Modules 09-10)
- **Module 09**: Error Handling & Quality Guards
- **Module 10**: Best Practices - Production patterns and scaling

## Key Features

### Multi-Layer Structure
Each module contains:
- `_meta/` - Learning objectives, difficulty, tags
- `guide/` - Heavily commented examples with doc vs. project comparisons
- `challenge/` - Practical tasks with starter code (comments only)
- `solution/` - Full runnable production-level code
- `key_takeaways.md` - Side-by-side pattern comparisons

### Pattern Comparison
Every module explicitly shows:
- ✅ **Official Docs Pattern**: What DSPy documentation teaches
- ⚡ **Community Project Pattern**: What real GitHub projects do
- 🎯 **Best Practice**: Which pattern works better in production and why

### Code-Dominant Learning
- Guides: More code than prose, heavily commented
- Challenges: Commented skeleton code to fill in
- Solutions: Production-ready, fully runnable implementations

## Referenced Projects

This course synthesizes patterns from:

**Official Resources:**
- [DSPy Official Documentation](https://dspy.ai)
- [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy)

**Community Projects:**
- [gabrielvanderlei/DSPy-examples](https://github.com/gabrielvanderlei/DSPy-examples)
- [Scale3-Labs/dspy-examples](https://github.com/Scale3-Labs/dspy-examples)
- [diicellman/dspy-gradio-rag](https://github.com/diicellman/dspy-gradio-rag)
- [Weaviate DSPy Recipes](https://github.com/weaviate/recipes)

## Getting Started

### Prerequisites
```bash
# Python 3.9+
pip install dspy-ai
pip install openai anthropic  # or your preferred LM provider
```

### Quick Start
```bash
# Start with Module 01
cd modules/01-signatures/guide/
python annotated_examples.py

# Try the challenge
cd ../challenge/
# Read tasks.md, edit starter_code.py

# Compare with solution
cd ../solution/
python solution.py
```

### Study Method

For each module:
1. **Read `_meta/objectives.md`** - Understand learning goals
2. **Study `guide/`** - Learn patterns and differences
3. **Attempt `challenge/tasks.md`** - Apply knowledge
4. **Compare with `solution/`** - Learn production patterns
5. **Review `key_takeaways.md`** - Solidify understanding

## Progressive Difficulty

- **Beginner** (01-03): Learn core concepts with simple examples
- **Intermediate** (04-06): Build optimized RAG systems
- **Advanced** (07-08): Create autonomous agents with evaluation
- **Production** (09-10): Handle errors and scale systems

## Why This Course is Different

1. **Project-Driven**: Learn from real code, not toy examples
2. **Pattern-Focused**: Understand why official docs differ from production code
3. **Comparison-Based**: See official vs. community patterns side-by-side
4. **Production-Level**: All solutions are runnable, scalable, best-practice code
5. **Multi-Layer**: Hierarchical structure reflects real engineering complexity

## Course Metadata

- **Total Modules**: 10
- **Estimated Time**: 40-60 hours (self-paced)
- **Level**: Beginner to Advanced
- **Last Updated**: 2025-12-03
- **DSPy Version**: Compatible with DSPy 2.5+

## Contributing

This is a learning repository. Improvements welcome:
- Better pattern comparisons
- Additional real-world project examples
- Updated API usage patterns
- Production debugging scenarios

## License

Educational use. All code examples follow DSPy's MIT License.

---

**Start Learning**: `cd modules/01-signatures/`
