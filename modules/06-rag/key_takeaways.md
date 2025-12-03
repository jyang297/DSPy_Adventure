# Module 06: RAG (Retrieval-Augmented Generation) - Key Takeaways

## Core Concepts

### What Is RAG in DSPy?
**RAG combines retrieval (finding relevant information) with generation (creating answers) in an optimizable end-to-end pipeline.**

```
Traditional RAG: Retriever → Generator (separate, manual tuning)
DSPy RAG: dspy.Retrieve → dspy.ChainOfThought (end-to-end optimizable)
```

---

## Pattern Comparison: Docs vs. Reality

### Official Docs Say:
```python
class SimpleRAG(dspy.Module):
    def __init__(self, k=3):
        self.retrieve = dspy.Retrieve(k=k)
        self.generate = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.generate(context=context, question=question)
```
**Philosophy**: Simple composition, show concept

### Real Projects Do:
```python
class ProductionRAG(dspy.Module):
    def __init__(self, k=5, rerank=True, fallback=True):
        super().__init__()
        # Multi-stage retrieval
        self.retrieve = dspy.Retrieve(k=k*2)  # Get more for reranking
        self.rerank = dspy.ChainOfThought(RerankSignature) if rerank else None
        self.generate = dspy.ChainOfThought(GenerateSignature)
        self.fallback_generate = dspy.Predict(SimpleSignature) if fallback else None
        self.k = k

    def forward(self, question: str) -> dspy.Prediction:
        # Stage 1: Initial retrieval
        retrieved = self.retrieve(question)

        if not retrieved.passages:
            # No results fallback
            if self.fallback_generate:
                return self.fallback_generate(question=question)
            return dspy.Prediction(answer="No relevant information found.")

        # Stage 2: Reranking (optional)
        if self.rerank:
            reranked = self.rerank(
                passages=retrieved.passages,
                question=question
            )
            context = reranked.top_k_passages[:self.k]
        else:
            context = retrieved.passages[:self.k]

        # Stage 3: Generation with context
        try:
            result = self.generate(
                context="\n\n".join(context),
                question=question
            )
            return dspy.Prediction(
                answer=result.answer,
                context=context,
                reasoning=result.reasoning,
                confidence="high" if len(context) >= self.k else "low"
            )
        except Exception as e:
            # Generation failure fallback
            if self.fallback_generate:
                return self.fallback_generate(question=question)
            raise
```
**Philosophy**: Multi-stage, error handling, reranking, fallbacks

### Best Practice Is:
**Start simple, add reranking and fallbacks for production.**

---

## Key Differences: Why They Matter

| Aspect | Official Docs | Real Projects | Why Different |
|--------|---------------|---------------|---------------|
| **Reranking** | Not included | Often added | Docs: simplicity<br>Projects: improve precision |
| **Fallbacks** | Not shown | Critical | Docs: happy path<br>Projects: handle no-results |
| **Context Formatting** | Basic | Structured | Docs: show API<br>Projects: optimize for LM |
| **Retrieval Count** | Fixed k | Dynamic k+rerank | Docs: simple param<br>Projects: quality/cost balance |
| **Error Handling** | None | Comprehensive | Docs: assume success<br>Projects: production reliability |

---

## The RAG Pipeline Components

### 1. Retrieval
```python
retrieve = dspy.Retrieve(k=3)
results = retrieve(query="What is DSPy?")
print(results.passages)  # List of retrieved text
```
**Purpose**: Find relevant documents/passages
**Key Parameters**: k (number to retrieve)
**Integration**: Weaviate, Pinecone, Chroma, FAISS

---

### 2. Reranking (Optional)
```python
class Rerank(dspy.Signature):
    """Rerank passages by relevance to question."""
    passages: str = dspy.InputField(desc="Retrieved passages")
    question: str = dspy.InputField(desc="User question")
    top_passages: str = dspy.OutputField(desc="Most relevant passages, ranked")

reranker = dspy.ChainOfThought(Rerank)
```
**Purpose**: Improve retrieval precision
**When to Use**: High-stakes applications, large k
**Cost**: Additional LM call

---

### 3. Generation
```python
class GenerateAnswer(dspy.Signature):
    """Answer question using context."""
    context: str = dspy.InputField(desc="Retrieved passages")
    question: str = dspy.InputField(desc="Question")
    answer: str = dspy.OutputField(desc="Answer based on context")

generator = dspy.ChainOfThought(GenerateAnswer)
```
**Purpose**: Create answer from retrieved context
**Module Types**: Predict (fast) or ChainOfThought (quality)

---

## Common RAG Patterns

### Pattern 1: Basic RAG
```python
class BasicRAG(dspy.Module):
    def __init__(self, k=3):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=k)
        self.generate = dspy.ChainOfThought(QA)

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.generate(context=context, question=question)
```
**Use**: Simple Q&A, prototype

---

### Pattern 2: RAG with Reranking
```python
class RerankingRAG(dspy.Module):
    def __init__(self, k=3):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=k*3)  # Over-retrieve
        self.rerank = dspy.ChainOfThought(Rerank)
        self.generate = dspy.ChainOfThought(QA)
        self.k = k

    def forward(self, question):
        passages = self.retrieve(question).passages
        reranked = self.rerank(passages=passages, question=question)
        top_k = reranked.top_passages[:self.k]
        return self.generate(context=top_k, question=question)
```
**Use**: Improve precision, production

---

### Pattern 3: Multi-Hop RAG
```python
class MultiHopRAG(dspy.Module):
    def __init__(self, k=3, hops=2):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=k)
        self.generate_query = dspy.ChainOfThought("context, question -> follow_up_query")
        self.final_generate = dspy.ChainOfThought(QA)
        self.hops = hops

    def forward(self, question):
        context = []

        # Initial retrieval
        passages = self.retrieve(question).passages
        context.extend(passages)

        # Multi-hop retrieval
        current_question = question
        for hop in range(self.hops - 1):
            # Generate follow-up query
            follow_up = self.generate_query(
                context="\n".join(context),
                question=current_question
            )
            # Retrieve more
            more_passages = self.retrieve(follow_up.follow_up_query).passages
            context.extend(more_passages)
            current_question = follow_up.follow_up_query

        # Final answer
        return self.final_generate(
            context="\n".join(context),
            question=question
        )
```
**Use**: Complex questions needing multiple sources

---

### Pattern 4: Self-Ask RAG
```python
class SelfAskRAG(dspy.Module):
    def __init__(self, k=3):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=k)
        self.decompose = dspy.ChainOfThought("question -> sub_questions")
        self.answer_sub = dspy.ChainOfThought(QA)
        self.synthesize = dspy.ChainOfThought("sub_answers -> final_answer")

    def forward(self, question):
        # Decompose into sub-questions
        decomp = self.decompose(question=question)
        sub_questions = decomp.sub_questions.split("\n")

        # Answer each sub-question
        sub_answers = []
        for sub_q in sub_questions:
            context = self.retrieve(sub_q).passages
            answer = self.answer_sub(context=context, question=sub_q)
            sub_answers.append(answer.answer)

        # Synthesize final answer
        return self.synthesize(sub_answers="\n".join(sub_answers))
```
**Use**: Complex reasoning over documents

---

## Critical Insights

### 1. Retrieval Quality Determines Everything
```python
# ❌ Bad: Poor retrieval = poor answers
# If retrieved passages don't contain answer, generation can't help

# ✅ Good: Monitor retrieval quality
def evaluate_retrieval(question, answer, passages):
    return any(answer.lower() in passage.lower() for passage in passages)

retrieval_quality = [
    evaluate_retrieval(q, a, retrieve(q).passages)
    for q, a in test_set
]
print(f"Retrieval covers {sum(retrieval_quality)/len(retrieval_quality):.1%} of answers")
```

### 2. Context Window Limitations
```python
# Problem: k=10 passages × 500 tokens = 5000 tokens
# May exceed context window or degrade quality

# Solution 1: Rerank and limit
retrieved = retrieve(question, k=20)
reranked = rerank(retrieved, k=5)  # Keep only top 5

# Solution 2: Summarize passages
summarized = [summarize(p) for p in passages]
context = "\n".join(summarized)

# Solution 3: Dynamic k based on passage length
total_tokens = 0
selected = []
for passage in passages:
    if total_tokens + len(passage) < 4000:
        selected.append(passage)
        total_tokens += len(passage)
```

### 3. Optimizing RAG End-to-End
```python
# DSPy can optimize retrieval + generation together
from dspy.optimizers import BootstrapRS

def rag_metric(example, pred, trace=None):
    # Reward both retrieval and generation quality
    retrieval_score = eval_retrieval(example, trace)
    generation_score = eval_generation(example, pred)
    return 0.4 * retrieval_score + 0.6 * generation_score

optimizer = BootstrapRS(metric=rag_metric)
optimized_rag = optimizer.compile(rag_system, trainset)
```

### 4. Fallback Strategies Are Critical
```python
# No results scenario
if not retrieved.passages:
    # Option 1: Return "I don't know"
    return "No relevant information found."

    # Option 2: Try broader search
    retrieved = retrieve_with_relaxed_params(question)

    # Option 3: Use parametric knowledge
    return fallback_generator(question=question)  # No context
```

---

## Vector Store Integration

### Weaviate Example
```python
import weaviate

client = weaviate.Client("http://localhost:8080")

# Configure DSPy to use Weaviate
rm = dspy.WeaviateRM(
    weaviate_client=client,
    weaviate_collection_name="Documents",
    k=5
)
dspy.settings.configure(rm=rm)

# Now dspy.Retrieve uses Weaviate
retrieve = dspy.Retrieve(k=3)
```

### Pinecone Example
```python
import pinecone

pinecone.init(api_key="your-key")

# Custom retriever
class PineconeRetriever:
    def __init__(self, index_name, k=3):
        self.index = pinecone.Index(index_name)
        self.k = k

    def __call__(self, query):
        # Embed query (use your embedding model)
        query_embedding = embed(query)

        # Search Pinecone
        results = self.index.query(
            vector=query_embedding,
            top_k=self.k
        )

        # Format for DSPy
        passages = [match.metadata['text'] for match in results.matches]
        return dspy.Prediction(passages=passages)
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: k Too Small
```python
retrieve = dspy.Retrieve(k=1)  # Too few!
```
**Fix**: Start with k=3-5, increase if needed

### ❌ Mistake 2: No Context Formatting
```python
# Bad: Raw passage list
context = retrieved.passages
```
**Fix**: Format for readability
```python
context = "\n\n---\n\n".join([
    f"Passage {i+1}:\n{p}"
    for i, p in enumerate(retrieved.passages)
])
```

### ❌ Mistake 3: Ignoring Retrieval Failures
```python
# Bad: Assume retrieval always succeeds
passages = retrieve(question).passages
answer = generate(context=passages, question=question)
```
**Fix**: Handle empty results
```python
passages = retrieve(question).passages
if not passages:
    return "No relevant information found."
answer = generate(context=passages, question=question)
```

### ❌ Mistake 4: Not Optimizing Retrieval
```python
# Bad: Fixed retrieval, only optimize generation
optimizer.compile(rag.generate, trainset)
```
**Fix**: Optimize entire pipeline
```python
optimizer.compile(rag, trainset)  # Optimizes retrieval + generation
```

### ❌ Mistake 5: No Retrieval Quality Metrics
```python
# Bad: Only measure final answer quality
def metric(example, pred):
    return pred.answer == example.answer
```
**Fix**: Measure retrieval too
```python
def comprehensive_metric(example, pred, trace=None):
    # Check if retrieval found relevant info
    if trace:
        retrieval_contains_answer = any(
            example.answer.lower() in p.lower()
            for p in trace.get('passages', [])
        )
        retrieval_score = 1.0 if retrieval_contains_answer else 0.0
    else:
        retrieval_score = 0.5  # Can't check

    # Check answer quality
    answer_score = 1.0 if pred.answer == example.answer else 0.0

    return 0.3 * retrieval_score + 0.7 * answer_score
```

---

## RAG Optimization Strategies

### 1. Retrieval Optimization
```python
# Optimize query formulation
class QueryOptimizer(dspy.Module):
    def __init__(self, k=3):
        super().__init__()
        self.rewrite = dspy.ChainOfThought("question -> optimized_query")
        self.retrieve = dspy.Retrieve(k=k)

    def forward(self, question):
        # Rewrite question for better retrieval
        optimized = self.rewrite(question=question)
        return self.retrieve(optimized.optimized_query)
```

### 2. Generation Optimization
```python
# Optimize how context is used
class ContextOptimizedRAG(dspy.Module):
    def __init__(self, k=3):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=k)
        self.summarize_context = dspy.ChainOfThought(
            "passages -> concise_summary"
        )
        self.generate = dspy.ChainOfThought(QA)

    def forward(self, question):
        passages = self.retrieve(question).passages

        # Summarize before generating
        summary = self.summarize_context(passages=passages)

        return self.generate(
            context=summary.concise_summary,
            question=question
        )
```

### 3. Hybrid Optimization
```python
# Combine retrieval improvements + generation improvements
optimizer = BootstrapRS(metric=rag_metric)

# Optimize with multiple strategies
optimized_rag = optimizer.compile(
    rag_system,
    trainset=train_data,
    teacher=advanced_rag_system  # Learn from better system
)
```

---

## When to Use RAG

### Use RAG When:
- ✅ Answers require external knowledge
- ✅ Information changes frequently
- ✅ Need to cite sources
- ✅ Large knowledge base exists
- ✅ Can't fit all knowledge in prompt

### Don't Use RAG When:
- ❌ All knowledge fits in prompt
- ❌ No external knowledge base
- ❌ Latency is critical (RAG adds retrieval time)
- ❌ Questions don't need factual grounding

---

## Testing Your Understanding

You've mastered RAG if you can:

1. ✅ Build basic RAG pipeline
2. ✅ Integrate with vector stores
3. ✅ Implement reranking
4. ✅ Handle retrieval failures
5. ✅ Optimize RAG end-to-end
6. ✅ Measure retrieval quality
7. ✅ Implement multi-hop retrieval

---

## Connection to Other Modules

### RAG Builds On:
- **Module 02 (Modules)**: RAG is a complex module
- **Module 04 (Optimizers)**: RAG can be optimized end-to-end

### RAG Feeds Into:
- **Module 07 (Agents)**: Agents often use RAG as a tool
- **Module 10 (Best Practices)**: RAG in production

---

## Quick Reference Card

```python
# Production RAG Template

class ProductionRAG(dspy.Module):
    def __init__(self, k=5):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=k)
        self.generate = dspy.ChainOfThought(GenerateAnswer)

    def forward(self, question: str) -> dspy.Prediction:
        # Retrieve
        retrieved = self.retrieve(question)

        # Handle no results
        if not retrieved.passages:
            return dspy.Prediction(
                answer="No relevant information found.",
                confidence="none"
            )

        # Format context
        context = "\n\n".join(retrieved.passages)

        # Generate
        result = self.generate(context=context, question=question)

        return dspy.Prediction(
            answer=result.answer,
            context=retrieved.passages,
            reasoning=result.reasoning
        )

# Usage
rag = ProductionRAG(k=5)
result = rag(question="What is DSPy?")
```

---

## Final Checklist

Before moving to Module 07, ensure:

- [ ] Can build basic RAG pipeline
- [ ] Understand retrieval → generation flow
- [ ] Know how to integrate vector stores
- [ ] Can implement reranking
- [ ] Understand fallback strategies
- [ ] Can optimize RAG end-to-end
- [ ] Know when RAG is appropriate

---

## Next Steps

1. **Build** a RAG system for your domain
2. **Integrate** with vector store
3. **Move On** to Module 07: Agents
4. **Remember** Retrieval quality determines RAG quality

---

**Key Mantra**: *Good retrieval + Good generation = Good RAG system.*
