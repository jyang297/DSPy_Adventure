# Getting Started with DSPy Learning Repository

## Welcome!

This is a comprehensive, project-driven DSPy learning course that teaches through **real-world patterns**, not just documentation examples.

---

## Quick Start (5 minutes)

### 1. Navigate to the Course
```bash
cd dspy-course/
```

### 2. Read the Overview
```bash
cat README.md
```

### 3. Start Module 01
```bash
cd modules/01-signatures/
cat guide/overview.md
python guide/annotated_examples.py
```

### 4. Try the Challenge
```bash
cd challenge/
cat tasks.md
# Edit starter_code.py and complete the tasks
```

---

## Repository Structure (What You Have)

```
dspy-course/
├── README.md                    ✅ Course introduction
├── GETTING_STARTED.md           ✅ This file
├── COURSE_STRUCTURE.md          ✅ Complete structure overview
├── VERSION                       ✅ 1.0.0
├── CHANGELOG.md                  ✅ Version history
│
├── metadata/                     ✅ All complete
│   ├── course_overview.md       📘 Learning philosophy & module breakdown
│   ├── glossary.md              📖 DSPy terminology reference
│   ├── references.md            🔗 Official docs & community links
│   ├── recommended-projects.json 📊 Structured project database
│   └── versioning.md            📋 Version management
│
├── modules/
│   ├── 01-signatures/           ✅ FULLY COMPLETE
│   │   ├── _meta/
│   │   │   ├── objectives.md    🎯 Learning goals
│   │   │   └── difficulty.json  📊 Metrics
│   │   ├── guide/
│   │   │   ├── overview.md      📘 Conceptual guide
│   │   │   └── annotated_examples.py 💻 6 commented examples
│   │   ├── challenge/
│   │   │   ├── tasks.md         ✏️ 4 tasks + bonus
│   │   │   └── starter_code.py  📝 Skeleton code
│   │   ├── solution/
│   │   │   └── solution.py      ✅ Production solutions
│   │   └── key_takeaways.md     📋 Summary
│   │
│   └── 02-10/                   🔨 Structure ready for content
│
├── templates/                    ✅ All complete
│   ├── guide-template.md
│   ├── challenge-template.md
│   └── takeaways-template.md
│
└── projects/                     📋 Structure ready for content
```

---

## What's Complete vs. What's Planned

### ✅ Complete (Ready to Use)
1. **Full Course Structure** - All directories and templates
2. **Module 01: Signatures** - Fully implemented with all files
3. **Metadata Files** - Complete documentation and references
4. **Template System** - Reusable for future modules
5. **Version Management** - VERSION, CHANGELOG, structure docs

### 📋 Planned (Next Steps)
1. **Modules 02-10** - Structure exists, needs content following Module 01 pattern
2. **Project Reproductions** - 3 real-world project implementations
3. **Additional Examples** - More advanced use cases

---

## Learning Path

### For Complete Beginners

**Week 1: Fundamentals**
1. Read `metadata/course_overview.md`
2. Study `metadata/glossary.md` (reference as needed)
3. Complete Module 01: Signatures (6-8 hours)
   - Read guide
   - Run examples
   - Complete challenges
   - Compare with solutions

**Week 2-4: Core Concepts**
- Module 02: Modules & Forward (when complete)
- Module 03: Teleprompters (when complete)
- Module 04: Optimizers (when complete)

**Week 5-8: Advanced Topics**
- Module 05: Bootstrapping
- Module 06: RAG Systems
- Module 07: Agents
- Module 08: Evaluation

**Week 9-10: Production**
- Module 09: Error Handling
- Module 10: Best Practices
- Final project

### For Experienced Developers

Skip to areas of interest:
- **RAG Systems**: Module 06 (when complete)
- **Agents**: Module 07 (when complete)
- **Production Patterns**: Modules 09-10 (when complete)
- **Optimization**: Modules 04-05 (when complete)

---

## How to Use Module 01 (Fully Complete)

### Step 1: Read Objectives (15 min)
```bash
cat modules/01-signatures/_meta/objectives.md
```
Understand what you'll learn and why it matters.

### Step 2: Study the Guide (60 min)
```bash
cat modules/01-signatures/guide/overview.md
```
Learn the three-pattern comparison:
- Official Docs (simple)
- Community Projects (descriptive)
- Production Systems (validated)

### Step 3: Run Examples (60 min)
```bash
python modules/01-signatures/guide/annotated_examples.py
```
See 6 progressively complex examples with inline comments.

**Note**: Examples will display without requiring an API key. To run actual LM calls, configure DSPy with your provider.

### Step 4: Attempt Challenges (120 min)
```bash
cat modules/01-signatures/challenge/tasks.md
```
Complete 4 tasks + bonus:
1. Basic Signature (15 min)
2. Multi-Field Signature (30 min)
3. Production-Ready Signature (45 min)
4. Pattern Comparison (30 min)
5. Bonus: Financial Analyzer (60 min)

Edit `starter_code.py` to implement solutions.

### Step 5: Compare Solutions (30 min)
```bash
cat modules/01-signatures/solution/solution.py
python modules/01-signatures/solution/solution.py
```
Study production-ready implementations and compare with your approach.

### Step 6: Review Takeaways (15 min)
```bash
cat modules/01-signatures/key_takeaways.md
```
Solidify understanding with side-by-side comparisons.

---

## Understanding the Three-Pattern Framework

Every concept is taught through three lenses:

### 1. Official Docs Pattern
**Goal**: Learning speed
**Characteristics**: Minimal, simple, quick to understand
**Use When**: Prototyping, learning basics

### 2. Community Projects Pattern
**Goal**: Team development
**Characteristics**: Descriptive, type hints, field descriptions
**Use When**: Development phase, collaboration

### 3. Production Pattern
**Goal**: Reliability
**Characteristics**: Validated, comprehensive, audit trails
**Use When**: Production deployments, high-stakes applications

**Key Insight**: Start with pattern 1, evolve to pattern 3 as requirements clarify.

---

## Referenced Projects

This course synthesizes patterns from:

### Official Resources
- [DSPy Official Site](https://dspy.ai) - Primary documentation
- [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) - 30.5k stars

### Community Projects
- [gabrielvanderlei/DSPy-examples](https://github.com/gabrielvanderlei/DSPy-examples) - Learning progression
- [Scale3-Labs/dspy-examples](https://github.com/Scale3-Labs/dspy-examples) - Production patterns
- [diicellman/dspy-gradio-rag](https://github.com/diicellman/dspy-gradio-rag) - Full-stack RAG
- [Weaviate DSPy Recipes](https://github.com/weaviate/recipes) - Vector store integration

See `metadata/references.md` for complete list.

---

## Prerequisites

### Required
- Python 3.9+
- Basic understanding of language models (GPT, Claude, etc.)
- Python classes and type hints knowledge

### Helpful
- Experience with prompt engineering
- Familiarity with ML concepts (embeddings, fine-tuning)
- Production API development experience

### To Run Examples
```bash
pip install dspy-ai
pip install openai  # or anthropic, or your LM provider
```

Configure your LM:
```python
import dspy
lm = dspy.LM("openai/gpt-4o-mini", api_key="your-key")
dspy.configure(lm=lm)
```

---

## Course Philosophy

### Code-Dominant Learning
- **Guides**: 70% code, 30% explanation
- **Challenges**: 100% commented code to complete
- **Solutions**: Production-ready, fully runnable

### Pattern Comparison
Every module answers:
- What does official documentation teach?
- What do real projects actually do?
- Why do they differ?
- What should YOU do?

### Progressive Complexity
```
Fundamentals → Optimization → Applications → Production
   (01-03)   →    (04-05)   →   (06-08)   →   (09-10)
```

---

## Support & Resources

### Course Resources
- `metadata/glossary.md` - DSPy terminology lookup
- `metadata/references.md` - External links
- `COURSE_STRUCTURE.md` - Complete structure overview

### Official DSPy Resources
- Documentation: https://dspy.ai
- GitHub: https://github.com/stanfordnlp/dspy
- Discord: DSPy community server

### Troubleshooting
- Check `metadata/glossary.md` for term definitions
- Review `metadata/references.md` for additional examples
- Read `COURSE_STRUCTURE.md` for navigation help

---

## Contribution

This course is a living repository. To contribute:
1. Complete modules 02-10 following Module 01 pattern
2. Add more real-world project examples
3. Update patterns as DSPy evolves
4. Improve explanations and examples

---

## Version Information

- **Course Version**: 1.0.0
- **DSPy Target**: 2.5+
- **Last Updated**: 2025-12-03
- **Status**: Module 01 complete, structure ready for 02-10

---

## Next Steps

### Right Now
1. Read `README.md` for course overview
2. Review `metadata/course_overview.md` for learning philosophy
3. Start Module 01: `cd modules/01-signatures/`

### This Week
1. Complete Module 01 challenges
2. Review your solutions vs. provided solutions
3. Study key takeaways

### Next Weeks
1. Wait for Modules 02-10 to be completed
2. Or contribute by filling in modules using the templates
3. Build a project using learned patterns

---

## Quick Reference

### File Types You'll Encounter

| File | Purpose | How to Use |
|------|---------|------------|
| `objectives.md` | Learning goals | Read first to understand module |
| `difficulty.json` | Metrics & skills | Check time estimates |
| `overview.md` | Conceptual guide | Study patterns and concepts |
| `annotated_examples.py` | Commented code | Run and read inline comments |
| `tasks.md` | Challenge tasks | Complete progressively |
| `starter_code.py` | Skeleton code | Fill in TODO sections |
| `solution.py` | Full solutions | Compare after attempting |
| `key_takeaways.md` | Summary | Review to solidify learning |

---

## FAQ

**Q: Do I need to complete modules in order?**
A: Module 01 is prerequisite for all others. After that, some flexibility exists (e.g., you can do Module 06 RAG before Module 05 Bootstrapping).

**Q: How long does Module 01 take?**
A: Minimum 4 hours (basics only), recommended 6 hours (complete), mastery 8+ hours (with bonus).

**Q: Can I skip the challenges?**
A: You CAN, but shouldn't. Challenges force you to apply concepts, which is where real learning happens.

**Q: What if I get stuck?**
A: Read the guide again, check the glossary, review annotated examples, or peek at solutions for hints.

**Q: Do I need an API key to learn?**
A: No! Examples display educational output without API calls. But to run actual LM predictions, yes, you'll need a configured LM.

**Q: When will modules 02-10 be complete?**
A: They're planned for incremental completion. Module 01 provides the complete pattern to follow.

---

## Success Metrics

You'll know you've mastered Module 01 when:
- ✅ You can write DSPy Signatures without reference
- ✅ You understand InputField vs. OutputField
- ✅ You know when to use type hints and Literal
- ✅ You can explain official docs vs. production patterns
- ✅ You've completed at least 3 challenge tasks
- ✅ You can design signatures for new tasks

---

## Let's Get Started!

```bash
cd modules/01-signatures/
cat _meta/objectives.md
# Begin your DSPy learning journey!
```

**Welcome to the course. Let's build something amazing with DSPy!** 🚀
