# Module 10: Best Practices - Key Takeaways

## Core Principles

### Production DSPy Philosophy
**Combine all previous modules into reliable, scalable, maintainable systems.**

```
Development: Fast iteration, quick prototypes
Production: Reliability, monitoring, cost management
```

---

## The Production Checklist

```
☐ CODE QUALITY
  ├─ Type hints everywhere
  ├─ Comprehensive documentation
  ├─ Unit tests for modules
  └─ Integration tests for pipelines

☐ RELIABILITY
  ├─ Input validation
  ├─ Output validation
  ├─ Retry strategies
  ├─ Fallback mechanisms
  └─ Circuit breakers

☐ OBSERVABILITY
  ├─ Structured logging
  ├─ Metrics collection
  ├─ Distributed tracing
  └─ Alerting

☐ PERFORMANCE
  ├─ Caching strategies
  ├─ Batch processing
  ├─ Async where possible
  └─ Resource limits

☐ COST MANAGEMENT
  ├─ LM call tracking
  ├─ Cost budgets
  ├─ Cheaper LMs for dev
  └─ Smart caching

☐ SECURITY
  ├─ Input sanitization
  ├─ PII handling
  ├─ API key management
  └─ Rate limiting

☐ DEPLOYMENT
  ├─ CI/CD pipeline
  ├─ Canary deployments
  ├─ Rollback procedures
  └─ Health checks
```

---

## Pattern: Production-Ready Module

### Official Docs Pattern
```python
class SimpleQA(dspy.Module):
    def __init__(self):
        self.generate = dspy.ChainOfThought(QA)

    def forward(self, question):
        return self.generate(question=question)
```

### Production Pattern
```python
from typing import Optional
from dataclasses import dataclass
import logging
import time
from functools import lru_cache

@dataclass
class QAConfig:
    """Configuration for QA module."""
    max_retries: int = 3
    timeout: int = 30
    enable_cache: bool = True
    cache_size: int = 1000
    fallback_enabled: bool = True

class ProductionQA(dspy.Module):
    """Production-ready QA module with full error handling.

    Features:
    - Input/output validation
    - Retry with exponential backoff
    - Caching for repeated questions
    - Fallback mechanism
    - Comprehensive logging
    - Cost tracking
    """

    def __init__(self, config: Optional[QAConfig] = None):
        super().__init__()
        self.config = config or QAConfig()

        # Primary predictor
        self.generate = dspy.ChainOfThought(QASignature)

        # Fallback predictor (simpler)
        if self.config.fallback_enabled:
            self.fallback = dspy.Predict(SimpleFallbackSignature)

        # Cache
        if self.config.enable_cache:
            self._cache = lru_cache(maxsize=self.config.cache_size)(
                self._generate_answer
            )

        # Metrics
        self.metrics = {
            'total_calls': 0,
            'cache_hits': 0,
            'failures': 0,
            'fallback_used': 0,
            'total_cost': 0.0
        }

        # Logger
        self.logger = logging.getLogger(__name__)

    def forward(self, question: str, context: Optional[str] = None) -> dspy.Prediction:
        """Generate answer with full error handling.

        Args:
            question: User question (required)
            context: Optional context for answer

        Returns:
            dspy.Prediction with answer, confidence, and metadata
        """
        start_time = time.time()
        self.metrics['total_calls'] += 1

        # 1. Input validation
        validation_result = self._validate_input(question, context)
        if not validation_result['valid']:
            self.logger.warning(f"Invalid input: {validation_result['error']}")
            return dspy.Prediction(
                answer=f"Invalid input: {validation_result['error']}",
                confidence="none",
                status="invalid_input"
            )

        # 2. Check cache
        if self.config.enable_cache:
            cache_key = self._get_cache_key(question, context)
            try:
                result = self._cache(question, context)
                if result:
                    self.metrics['cache_hits'] += 1
                    self.logger.info(f"Cache hit for question: {question[:50]}")
                    return result
            except:
                pass  # Cache miss, continue

        # 3. Generate with retries
        try:
            result = self._generate_with_retry(question, context)
            result.latency = time.time() - start_time
            return result

        except Exception as e:
            self.logger.error(f"Generation failed: {e}", exc_info=True)
            self.metrics['failures'] += 1

            # 4. Try fallback
            if self.config.fallback_enabled:
                return self._use_fallback(question, context)

            # 5. Ultimate fallback
            return dspy.Prediction(
                answer="I apologize, but I'm unable to answer your question at this time.",
                confidence="none",
                status="error"
            )

    def _validate_input(self, question: str, context: Optional[str]) -> dict:
        """Validate inputs."""
        if not isinstance(question, str):
            return {'valid': False, 'error': 'Question must be string'}

        if len(question.strip()) < 2:
            return {'valid': False, 'error': 'Question too short'}

        if len(question) > 1000:
            return {'valid': False, 'error': 'Question too long (max 1000 chars)'}

        if context and len(context) > 10000:
            return {'valid': False, 'error': 'Context too long (max 10000 chars)'}

        return {'valid': True}

    def _generate_with_retry(self, question: str, context: Optional[str]) -> dspy.Prediction:
        """Generate with exponential backoff retry."""
        for attempt in range(self.config.max_retries):
            try:
                with timeout(self.config.timeout):
                    result = self.generate(
                        question=question,
                        context=context or ""
                    )

                    # Validate output
                    if self._validate_output(result):
                        return result

                    self.logger.warning(f"Invalid output on attempt {attempt+1}")

            except TimeoutError:
                self.logger.warning(f"Timeout on attempt {attempt+1}")
            except Exception as e:
                self.logger.error(f"Error on attempt {attempt+1}: {e}")

            # Exponential backoff
            if attempt < self.config.max_retries - 1:
                sleep_time = 2 ** attempt
                time.sleep(sleep_time)

        raise Exception("All retries exhausted")

    def _validate_output(self, output) -> bool:
        """Validate LM output."""
        if not hasattr(output, 'answer'):
            return False

        if len(output.answer.strip()) < 5:
            return False

        # Check for harmful content
        if self._contains_harmful_content(output.answer):
            return False

        return True

    def _use_fallback(self, question: str, context: Optional[str]) -> dspy.Prediction:
        """Use simpler fallback predictor."""
        self.logger.info("Using fallback predictor")
        self.metrics['fallback_used'] += 1

        try:
            result = self.fallback(question=question)
            result.status = "fallback"
            return result
        except:
            raise

    def get_metrics(self) -> dict:
        """Get usage metrics."""
        return {
            **self.metrics,
            'cache_hit_rate': (
                self.metrics['cache_hits'] / self.metrics['total_calls']
                if self.metrics['total_calls'] > 0 else 0
            ),
            'failure_rate': (
                self.metrics['failures'] / self.metrics['total_calls']
                if self.metrics['total_calls'] > 0 else 0
            )
        }

    def reset_metrics(self):
        """Reset metrics counters."""
        for key in self.metrics:
            self.metrics[key] = 0
```

---

## Best Practices by Category

### 1. Code Organization

#### Module Structure
```python
# ✅ Good: Organized, clear structure
project/
├── src/
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── qa.py
│   │   ├── rag.py
│   │   └── agent.py
│   ├── signatures/
│   │   ├── __init__.py
│   │   └── qa_signatures.py
│   ├── utils/
│   │   ├── validation.py
│   │   ├── retry.py
│   │   └── metrics.py
│   └── config/
│       └── settings.py
├── tests/
│   ├── test_qa.py
│   └── test_rag.py
├── requirements.txt
└── README.md
```

#### Configuration Management
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    # LM config
    lm_model: str = "openai/gpt-4o-mini"
    lm_api_key: str
    lm_temperature: float = 0.0

    # Module config
    max_retries: int = 3
    timeout: int = 30
    enable_cache: bool = True

    # Observability
    log_level: str = "INFO"
    enable_tracing: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
```

---

### 2. Performance Optimization

#### Caching Strategy
```python
from functools import lru_cache
import redis

# In-memory cache (development)
@lru_cache(maxsize=1000)
def cached_predict(question: str) -> str:
    return predictor(question=question).answer

# Distributed cache (production)
redis_client = redis.Redis(host='localhost', port=6379)

def redis_cached_predict(question: str) -> str:
    # Check cache
    cached = redis_client.get(f"qa:{question}")
    if cached:
        return json.loads(cached)

    # Generate
    result = predictor(question=question)

    # Store in cache (TTL: 1 hour)
    redis_client.setex(
        f"qa:{question}",
        3600,
        json.dumps(result.toDict())
    )

    return result
```

#### Batch Processing
```python
async def batch_process(questions: list[str], batch_size: int = 10):
    """Process questions in batches for efficiency."""
    results = []

    for i in range(0, len(questions), batch_size):
        batch = questions[i:i+batch_size]

        # Process batch in parallel
        tasks = [process_question(q) for q in batch]
        batch_results = await asyncio.gather(*tasks)

        results.extend(batch_results)

    return results
```

---

### 3. Cost Management

#### Track LM Costs
```python
class CostTracker:
    """Track LM API costs."""

    COSTS_PER_1K_TOKENS = {
        'gpt-4': {'input': 0.03, 'output': 0.06},
        'gpt-3.5-turbo': {'input': 0.0015, 'output': 0.002},
    }

    def __init__(self):
        self.total_cost = 0.0
        self.calls = []

    def track_call(self, model: str, input_tokens: int, output_tokens: int):
        costs = self.COSTS_PER_1K_TOKENS.get(model, {'input': 0, 'output': 0})

        call_cost = (
            (input_tokens / 1000) * costs['input'] +
            (output_tokens / 1000) * costs['output']
        )

        self.total_cost += call_cost
        self.calls.append({
            'model': model,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'cost': call_cost
        })

        return call_cost

tracker = CostTracker()
```

#### Cost Optimization Strategies
```python
# 1. Use cheaper models for dev
if settings.environment == 'development':
    lm = dspy.LM("openai/gpt-3.5-turbo")
else:
    lm = dspy.LM("openai/gpt-4")

# 2. Cache aggressively
@lru_cache(maxsize=10000)
def expensive_call(question):
    return predictor(question=question)

# 3. Use shorter prompts in production
if settings.environment == 'production':
    # Optimized, shorter prompts
    compiled_program = load_optimized("production_v1.json")
else:
    # Verbose prompts for debugging
    program = BasicProgram()
```

---

### 4. Monitoring & Observability

#### Structured Logging
```python
import structlog

logger = structlog.get_logger()

def process_question(question: str):
    logger.info(
        "question_processing_started",
        question_length=len(question),
        user_id=get_user_id()
    )

    try:
        result = predictor(question=question)

        logger.info(
            "question_processing_completed",
            answer_length=len(result.answer),
            latency_ms=result.latency * 1000
        )

        return result

    except Exception as e:
        logger.error(
            "question_processing_failed",
            error=str(e),
            error_type=type(e).__name__
        )
        raise
```

#### Metrics Collection
```python
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
qa_requests = Counter('qa_requests_total', 'Total QA requests')
qa_latency = Histogram('qa_latency_seconds', 'QA latency')
qa_errors = Counter('qa_errors_total', 'Total QA errors', ['error_type'])
active_requests = Gauge('qa_active_requests', 'Currently processing requests')

def monitored_predict(question: str):
    qa_requests.inc()
    active_requests.inc()

    try:
        with qa_latency.time():
            result = predictor(question=question)
        return result

    except Exception as e:
        qa_errors.labels(error_type=type(e).__name__).inc()
        raise

    finally:
        active_requests.dec()
```

---

### 5. Security Best Practices

#### Input Sanitization
```python
def sanitize_input(text: str) -> str:
    """Remove potentially harmful content."""
    # Remove PII
    text = remove_pii(text)

    # Remove prompt injection attempts
    text = remove_injection_patterns(text)

    # Limit length
    text = text[:1000]

    return text
```

#### API Key Management
```python
# ❌ Bad: Hardcoded keys
lm = dspy.LM("openai/gpt-4", api_key="sk-...")

# ✅ Good: Environment variables
import os
lm = dspy.LM("openai/gpt-4", api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Better: Secret management service
from cloud_secrets import get_secret
lm = dspy.LM("openai/gpt-4", api_key=get_secret("openai_api_key"))
```

#### Rate Limiting
```python
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=100, period=60)  # 100 calls per minute
def rate_limited_predict(question: str):
    return predictor(question=question)
```

---

### 6. Testing Strategies

#### Unit Tests
```python
import pytest

def test_qa_module_basic():
    """Test basic QA functionality."""
    qa = ProductionQA()
    result = qa(question="What is 2+2?")

    assert hasattr(result, 'answer')
    assert len(result.answer) > 0

def test_qa_module_validation():
    """Test input validation."""
    qa = ProductionQA()

    # Too short
    result = qa(question="a")
    assert result.status == "invalid_input"

    # Too long
    result = qa(question="a" * 2000)
    assert result.status == "invalid_input"

def test_qa_module_retry():
    """Test retry mechanism."""
    qa = ProductionQA(config=QAConfig(max_retries=3))

    # Mock failures
    with mock.patch.object(qa.generate, '__call__', side_effect=[
        Exception("Fail 1"),
        Exception("Fail 2"),
        dspy.Prediction(answer="Success!")
    ]):
        result = qa(question="Test question")
        assert result.answer == "Success!"
```

#### Integration Tests
```python
def test_full_pipeline():
    """Test entire pipeline end-to-end."""
    # Setup
    rag = ProductionRAG()

    # Execute
    result = rag(question="What is DSPy?")

    # Verify
    assert result.answer
    assert result.context
    assert result.confidence in ['high', 'medium', 'low']
```

---

### 7. Deployment Best Practices

#### Health Checks
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    """Health endpoint for load balancer."""
    try:
        # Check LM connectivity
        test_result = predictor(question="test")

        return {
            'status': 'healthy',
            'lm_available': True,
            'version': settings.version
        }
    except:
        return {
            'status': 'unhealthy',
            'lm_available': False
        }, 503
```

#### Canary Deployment
```python
import random

def route_request(question: str):
    """Route to stable or canary version."""
    if random.random() < 0.1:  # 10% to canary
        return canary_predictor(question=question)
    else:
        return stable_predictor(question=question)
```

---

## Common Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: No Configuration Management
```python
# Bad: Hardcoded everywhere
lm = dspy.LM("openai/gpt-4")  # What about different environments?
```

### ❌ Anti-Pattern 2: No Error Tracking
```python
# Bad: Errors disappear
try:
    result = predictor(question)
except:
    pass  # Who knows what failed?
```

### ❌ Anti-Pattern 3: No Cost Tracking
```python
# Bad: Surprise $10k bill
for question in millions_of_questions:
    predictor(question)  # $$$!
```

### ❌ Anti-Pattern 4: Synchronous Processing
```python
# Bad: Process serially
for q in questions:
    process(q)  # Slow!
```

### ❌ Anti-Pattern 5: No Monitoring
```python
# Bad: Black box in production
result = predictor(question)  # No idea if it's working
```

---

## Production Deployment Checklist

Before deploying to production:

- [ ] **Code Quality**
  - [ ] Type hints on all functions
  - [ ] Docstrings on all modules/classes
  - [ ] Code reviewed
  - [ ] Linted and formatted

- [ ] **Testing**
  - [ ] Unit tests pass (>80% coverage)
  - [ ] Integration tests pass
  - [ ] Load testing completed
  - [ ] Failure scenarios tested

- [ ] **Reliability**
  - [ ] Input validation implemented
  - [ ] Retry logic added
  - [ ] Fallbacks configured
  - [ ] Timeouts set
  - [ ] Circuit breakers added

- [ ] **Observability**
  - [ ] Structured logging configured
  - [ ] Metrics exposed
  - [ ] Distributed tracing enabled
  - [ ] Alerts configured

- [ ] **Performance**
  - [ ] Caching implemented
  - [ ] Batch processing where possible
  - [ ] Resource limits set
  - [ ] Load tested

- [ ] **Security**
  - [ ] Input sanitization
  - [ ] API keys in secrets manager
  - [ ] Rate limiting enabled
  - [ ] PII handling compliant

- [ ] **Cost Management**
  - [ ] Cost tracking implemented
  - [ ] Budget alerts configured
  - [ ] Cheaper LMs for dev
  - [ ] Cache hit rate >50%

- [ ] **Deployment**
  - [ ] CI/CD pipeline configured
  - [ ] Canary deployment plan
  - [ ] Rollback procedure documented
  - [ ] Health checks implemented
  - [ ] Runbook created

---

## Final Wisdom

### The Three Production Truths

1. **Everything That Can Fail, Will Fail**
   - Plan for failures at every level
   - Have fallbacks for your fallbacks
   - Test failure scenarios

2. **You Can't Improve What You Don't Measure**
   - Log everything important
   - Track metrics continuously
   - Monitor in real-time

3. **Cost Matters**
   - LM calls are expensive
   - Cache aggressively
   - Use cheaper models where possible

---

## Testing Your Understanding

You've mastered best practices if you can:

1. ✅ Build production-ready modules
2. ✅ Implement comprehensive error handling
3. ✅ Add observability (logs, metrics, traces)
4. ✅ Manage costs effectively
5. ✅ Deploy with confidence
6. ✅ Monitor and debug production systems
7. ✅ Follow security best practices

---

## Final Checklist

Course completion checklist:

- [ ] Completed all 10 modules
- [ ] Can build signatures (Module 01)
- [ ] Can compose modules (Module 02)
- [ ] Understand optimization (Modules 03-05)
- [ ] Can build RAG systems (Module 06)
- [ ] Can create agents (Module 07)
- [ ] Practice evaluation-driven development (Module 08)
- [ ] Implement error handling (Module 09)
- [ ] Follow production best practices (Module 10)

---

## Congratulations!

You've completed the DSPy course. You now have the knowledge to:

- Build DSPy systems from scratch
- Optimize them systematically
- Deploy them to production
- Monitor and maintain them

**Next Steps**:
1. Build a real project
2. Deploy to production
3. Share your learnings
4. Contribute back to community

---

**Final Mantra**: *Build fast, measure everything, deploy confidently.*

**Thank you for learning DSPy!** 🎓
