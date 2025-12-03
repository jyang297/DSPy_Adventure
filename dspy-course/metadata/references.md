# DSPy References & Resources

## Official Resources

### Primary Documentation
- **DSPy Official Site**: https://dspy.ai
  - Comprehensive tutorials and guides
  - API reference
  - Philosophy and design principles

- **DSPy GitHub Repository**: https://github.com/stanfordnlp/dspy
  - Source code (30.5k+ stars)
  - Official examples
  - Issue tracker and discussions
  - 360+ contributors

### Official Examples
- **Getting Started**: https://dspy.ai/tutorials/
- **RAG Tutorial**: https://github.com/stanfordnlp/dspy/blob/main/docs/docs/tutorials/rag/index.ipynb
- **Modules Guide**: https://dspy.ai/learn/programming/modules
- **Optimizers Guide**: https://dspy.ai/learn/optimizers/

### Research Papers
- **DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines**
  - Published: ICLR 2024
  - Authors: Stanford NLP Group
  - Focus: Core DSPy philosophy and optimization

- **8+ peer-reviewed papers** on various DSPy applications
  - Check: https://dspy.ai for latest research

---

## Community Projects

### Production-Grade Examples

#### 1. gabrielvanderlei/DSPy-examples
- **URL**: https://github.com/gabrielvanderlei/DSPy-examples
- **Focus**: Practical examples from simple classifiers to complex pipelines
- **Best For**: Learning progression from basics to advanced
- **Key Patterns**:
  - Basic signatures
  - Module composition
  - RAG implementations
  - Agent loops

#### 2. Scale3-Labs/dspy-examples
- **URL**: https://github.com/Scale3-Labs/dspy-examples
- **Focus**: Production patterns with observability
- **Best For**: Understanding monitoring and debugging
- **Key Patterns**:
  - Langtrace integration
  - Production error handling
  - Logging best practices
  - Performance monitoring

#### 3. diicellman/dspy-gradio-rag
- **URL**: https://github.com/diicellman/dspy-gradio-rag
- **Focus**: Full-stack RAG application
- **Best For**: End-to-end implementation reference
- **Key Patterns**:
  - FastAPI backend
  - Gradio frontend
  - Ollama integration
  - Vector store usage

#### 4. Weaviate DSPy Recipes
- **URL**: https://github.com/weaviate/recipes/tree/main/integrations/llm-agent-frameworks/dspy
- **Focus**: Vector database integration
- **Best For**: RAG with production vector stores
- **Key Patterns**:
  - Weaviate integration
  - Retrieval optimization
  - Hybrid search
  - Notebook tutorials

#### 5. Ronoh4/A-DSPy-based-RAG-with-LlamaIndex
- **URL**: https://github.com/Ronoh4/A-DSPy-based-RAG-with-LlamaIndex
- **Focus**: DSPy + LlamaIndex integration
- **Best For**: Combining DSPy with other frameworks
- **Key Patterns**:
  - LlamaParse for PDF processing
  - VectorStoreIndex integration
  - Hybrid DSPy/LlamaIndex pipelines

---

## Additional Learning Resources

### Curated Collections

#### Awesome-DSPy
- **URL**: https://github.com/nshkrdotcom/Awesome-DSPy
- **Content**: Curated list of DSPy resources
- **Includes**:
  - davila7/DSPy-101 (comprehensive intro course)
  - ten24bytes/dspy-demo (30+ Jupyter tutorials)
  - Community blog posts and articles

### Tutorial Repositories

#### DSPy-101 (davila7)
- Comprehensive introductory course
- Structured learning path
- Covers fundamentals through advanced topics

#### dspy-demo (ten24bytes)
- 30+ Jupyter notebooks
- Covers almost every DSPy feature
- Hands-on examples

---

## Real-World Applications

### Academic Projects
- **STORM**: Document generation system
- **IReRa**: Information retrieval and reasoning
- **PAPILLON**: Multi-document reasoning
- **PATH**: Planning and tool handling
- **WangLab@MEDIQA**: Medical QA system

### Production Deployments
- Multiple startups using DSPy in production
- Enterprise RAG systems
- AI agent platforms
- Automated research tools

---

## Blog Posts & Articles

### Key Articles

#### "Building and Optimizing Multi-Agent RAG Systems with DSPy and GEPA"
- **Author**: Isaac Kargar
- **URL**: https://kargarisaac.medium.com/building-and-optimizing-multi-agent-rag-systems-with-dspy-and-gepa-2b88b5838ce2
- **Topics**: Multi-agent systems, GEPA optimizer, RAG optimization
- **Published**: September 2024

#### "Context Engineering — A Comprehensive Hands-On Tutorial with DSPy"
- **Publication**: Towards Data Science
- **URL**: https://towardsdatascience.com/context-engineering-a-comprehensive-hands-on-tutorial-with-dspy/
- **Topics**: Context engineering principles, DSPy applications
- **Includes**: 1h 20m YouTube course

---

## Ecosystem Tools

### LM Providers (Compatible with DSPy)
- **OpenAI**: GPT-4, GPT-3.5, etc.
- **Anthropic**: Claude 3.5, Claude 3 family
- **Open Source**: Ollama, Llama, Mistral
- **Hosted**: Cohere, AI21, Replicate

### Vector Stores (for RAG)
- **Weaviate**: Native DSPy integration
- **Pinecone**: Vector database
- **Chroma**: Lightweight option
- **Qdrant**: Production-grade
- **FAISS**: Local/fast

### Observability Tools
- **Langtrace**: LLM observability (Scale3-Labs)
- **LangSmith**: LangChain ecosystem
- **Weights & Biases**: ML experiment tracking
- **Arize**: ML observability

---

## API Documentation

### Core APIs
- **Signatures**: https://dspy.ai/api/signatures
- **Modules**: https://dspy.ai/api/modules
- **Optimizers**: https://dspy.ai/api/optimizers
- **Metrics**: https://dspy.ai/api/metrics

### Advanced APIs
- **Retrieval**: https://dspy.ai/api/retrieval
- **Agents**: Limited official docs (see community examples)
- **Fine-tuning**: https://dspy.ai/api/finetuning

---

## Community Channels

### Discussion Forums
- **Discord**: DSPy community server
  - Active discussions
  - Help from maintainers
  - Pattern sharing

- **GitHub Discussions**: https://github.com/stanfordnlp/dspy/discussions
  - Feature requests
  - Architecture discussions
  - Community showcase

### Social Media
- **Twitter/X**: Follow #DSPy hashtag
- **LinkedIn**: DSPy community posts
- **Reddit**: r/LanguageModels discussions

---

## Related Frameworks

### Comparison Context

#### LangChain
- **Focus**: Pre-built chains and tools
- **DSPy Advantage**: Automatic optimization, less manual prompt engineering
- **Use Together**: DSPy can use LangChain tools

#### LlamaIndex
- **Focus**: Data ingestion and indexing
- **DSPy Advantage**: End-to-end optimization of retrieval + generation
- **Use Together**: LlamaIndex for indexing, DSPy for pipeline

#### Guidance
- **Focus**: Constrained generation
- **DSPy Advantage**: Full pipeline optimization, not just generation
- **Use Together**: Guidance for output structure, DSPy for pipeline

#### Haystack
- **Focus**: NLP pipeline framework
- **DSPy Advantage**: LM-specific optimizations
- **Use Together**: Haystack for traditional NLP, DSPy for LM components

---

## Version Tracking

### DSPy Releases
- **Current Stable**: 2.5+ (as of 2025)
- **Breaking Changes**: Check release notes
- **Migration Guides**: https://dspy.ai/migration

### API Stability
- **Core APIs** (Signatures, Modules): Stable
- **Optimizers**: Evolving (new algorithms added frequently)
- **Experimental**: Agent APIs, advanced optimizers

---

## Contributing Back

### How to Contribute
1. **Bug Reports**: GitHub issues
2. **Feature Requests**: GitHub discussions
3. **Code Contributions**: Pull requests
4. **Documentation**: Docs improvements
5. **Examples**: Share your patterns

### Contribution Ideas
- New optimizer implementations
- Better error messages
- Integration with new LM providers
- Real-world case studies
- Performance benchmarks

---

## Course-Specific References

### Module-Specific Resources

**Module 01 (Signatures)**:
- Official: https://dspy.ai/learn/programming/signatures
- Example: gabrielvanderlei/DSPy-examples/signatures

**Module 02 (Modules)**:
- Official: https://dspy.ai/learn/programming/modules
- Example: Scale3-Labs/dspy-examples/modules

**Module 03-05 (Optimizers)**:
- Official: https://dspy.ai/learn/optimizers/
- Example: Weaviate recipes optimizers

**Module 06 (RAG)**:
- Official: https://dspy.ai/tutorials/rag/
- Example: diicellman/dspy-gradio-rag

**Module 07 (Agents)**:
- Community: Multi-agent systems (Isaac Kargar article)
- Example: Various community agent examples

**Module 08 (Evaluation)**:
- Official: https://dspy.ai/learn/evaluation/
- Example: Scale3-Labs observability patterns

**Module 09-10 (Production)**:
- Community: Scale3-Labs production patterns
- Best Practices: Aggregated from production deployments

---

## Quick Links

**Start Here**:
- [Official Docs](https://dspy.ai)
- [GitHub Repo](https://github.com/stanfordnlp/dspy)
- [Quick Start Tutorial](https://dspy.ai/tutorials/)

**Get Help**:
- [Discord Community](https://discord.gg/dspy)
- [GitHub Issues](https://github.com/stanfordnlp/dspy/issues)
- [Stack Overflow #dspy](https://stackoverflow.com/questions/tagged/dspy)

**Stay Updated**:
- [Release Notes](https://github.com/stanfordnlp/dspy/releases)
- [Blog](https://dspy.ai/blog/)
- [Twitter #DSPy](https://twitter.com/search?q=%23DSPy)

---

**Last Updated**: 2025-12-03
**Maintainer**: This course repository
**Contributions**: Welcome via pull requests
