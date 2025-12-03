# Module 09: Error Handling & Quality Guards - Key Takeaways

## Core Concepts

### What Are Quality Guards?
**Defensive mechanisms that catch failures before they reach users.**

```
Without Guards: LM fails → User sees garbage
With Guards: LM fails → Fallback → User sees reasonable output
```

---

## The Five Layers of Defense

```
1. INPUT VALIDATION
   └─> Reject invalid inputs early

2. OUTPUT VALIDATION
   └─> Check LM outputs meet requirements

3. RETRY STRATEGIES
   └─> Try again on transient failures

4. FALLBACK MECHANISMS
   └─> Graceful degradation when all else fails

5. MONITORING & ALERTS
   └─> Track failures, alert humans
```

---

## Pattern Comparison: Docs vs. Reality

### Official Docs Say:
```python
# Simple, assume success
predictor = dspy.Predict(QA)
result = predictor(question="What is DSPy?")
print(result.answer)
```
**Philosophy**: Show happy path

### Real Projects Do:
```python
class RobustPredictor:
    def __init__(self, signature, max_retries=3, timeout=30):
        self.predictor = dspy.Predict(signature)
        self.fallback = dspy.Predict(SimpleFallbackSignature)
        self.max_retries = max_retries
        self.timeout = timeout
        self.failure_log = []

    def __call__(self, **kwargs):
        # Input validation
        validated_inputs = self.validate_inputs(kwargs)
        if not validated_inputs['valid']:
            return dspy.Prediction(
                answer=f"Invalid input: {validated_inputs['error']}",
                status="input_error"
            )

        # Retry loop
        for attempt in range(self.max_retries):
            try:
                # Call with timeout
                result = timeout_wrapper(
                    self.predictor,
                    timeout=self.timeout,
                    **kwargs
                )

                # Output validation
                if self.validate_output(result):
                    return result

                # Invalid output, retry
                logging.warning(f"Invalid output on attempt {attempt+1}")

            except TimeoutError:
                logging.error(f"Timeout on attempt {attempt+1}")
            except Exception as e:
                logging.error(f"Error on attempt {attempt+1}: {e}")
                self.failure_log.append({
                    'attempt': attempt,
                    'error': str(e),
                    'inputs': kwargs
                })

        # All retries failed, use fallback
        try:
            fallback_result = self.fallback(**kwargs)
            fallback_result.status = "fallback"
            return fallback_result
        except:
            # Ultimate fallback
            return dspy.Prediction(
                answer="I apologize, but I'm unable to process your request right now.",
                status="total_failure"
            )

    def validate_inputs(self, inputs):
        """Check inputs meet requirements."""
        if 'question' not in inputs:
            return {'valid': False, 'error': 'Missing question'}
        if len(inputs['question']) < 2:
            return {'valid': False, 'error': 'Question too short'}
        if len(inputs['question']) > 1000:
            return {'valid': False, 'error': 'Question too long'}
        return {'valid': True}

    def validate_output(self, output):
        """Check output meets requirements."""
        if not hasattr(output, 'answer'):
            return False
        if len(output.answer) < 5:
            return False
        if contains_harmful_content(output.answer):
            return False
        return True
```
**Philosophy**: Defense in depth, graceful degradation

### Best Practice Is:
**Validate inputs, retry failures, use fallbacks, log everything.**

---

## Key Differences: Why They Matter

| Aspect | Official Docs | Real Projects | Why Different |
|--------|---------------|---------------|---------------|
| **Input Validation** | None | Strict checks | Docs: assume valid<br>Projects: users send anything |
| **Retries** | Not shown | Exponential backoff | Docs: assume success<br>Projects: networks fail |
| **Fallbacks** | Not shown | Multiple levels | Docs: happy path<br>Projects: must not crash |
| **Logging** | Minimal | Comprehensive | Docs: reduce noise<br>Projects: debug production |
| **Timeouts** | Not set | Always set | Docs: simplicity<br>Projects: prevent hangs |

---

## Input Validation Patterns

### 1. Type Validation
```python
def validate_input_types(question: str, context: str = None) -> dict:
    errors = []

    if not isinstance(question, str):
        errors.append(f"question must be str, got {type(question)}")

    if context is not None and not isinstance(context, str):
        errors.append(f"context must be str, got {type(context)}")

    return {
        'valid': len(errors) == 0,
        'errors': errors
    }
```

### 2. Length Validation
```python
def validate_length(text: str, min_len: int = 1, max_len: int = 5000) -> dict:
    if len(text) < min_len:
        return {'valid': False, 'error': f'Too short (min: {min_len})'}

    if len(text) > max_len:
        return {'valid': False, 'error': f'Too long (max: {max_len})'}

    return {'valid': True}
```

### 3. Content Validation
```python
def validate_content(text: str) -> dict:
    # Check for harmful content
    if contains_pii(text):
        return {'valid': False, 'error': 'Contains PII'}

    if contains_profanity(text):
        return {'valid': False, 'error': 'Contains inappropriate content'}

    if is_prompt_injection(text):
        return {'valid': False, 'error': 'Potential injection attempt'}

    return {'valid': True}
```

---

## Output Validation Patterns

### 1. Structure Validation
```python
def validate_output_structure(output, required_fields: list) -> bool:
    for field in required_fields:
        if not hasattr(output, field):
            logging.error(f"Missing required field: {field}")
            return False

        value = getattr(output, field)
        if value is None or (isinstance(value, str) and not value.strip()):
            logging.error(f"Empty field: {field}")
            return False

    return True
```

### 2. Format Validation
```python
def validate_format(output) -> bool:
    # Check answer format
    if not output.answer:
        return False

    # Check for required format patterns
    if requires_json(output):
        try:
            json.loads(output.answer)
        except:
            return False

    # Check length constraints
    if len(output.answer) < 10 or len(output.answer) > 500:
        return False

    return True
```

### 3. Safety Validation
```python
def validate_safety(output) -> bool:
    # Check for harmful content
    if contains_harmful_content(output.answer):
        logging.warning("Output contains harmful content")
        return False

    # Check for hallucinations
    if appears_hallucinated(output.answer, output.context):
        logging.warning("Output may be hallucinated")
        return False

    # Check for off-topic
    if is_off_topic(output.answer, output.question):
        logging.warning("Output is off-topic")
        return False

    return True
```

---

## Retry Strategies

### 1. Simple Retry
```python
def simple_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            logging.warning(f"Attempt {attempt+1} failed: {e}")
    return None
```

### 2. Exponential Backoff
```python
import time

def exponential_backoff_retry(func, max_retries=5, base_delay=1):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise

            delay = base_delay * (2 ** attempt)  # 1, 2, 4, 8, 16 seconds
            logging.warning(f"Attempt {attempt+1} failed, waiting {delay}s: {e}")
            time.sleep(delay)
```

### 3. Retry with Different Parameters
```python
def adaptive_retry(predictor, question, max_retries=3):
    # Try with different LM parameters
    temperatures = [0.0, 0.3, 0.7]  # Decreasing randomness

    for attempt, temp in enumerate(temperatures[:max_retries]):
        try:
            with dspy.context(lm=dspy.LM(model, temperature=temp)):
                result = predictor(question=question)

                if validate_output(result):
                    return result

        except Exception as e:
            logging.warning(f"Attempt {attempt+1} (temp={temp}) failed: {e}")

    return None
```

---

## Fallback Mechanisms

### 1. Simpler Model Fallback
```python
class FallbackModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.primary = dspy.ChainOfThought(ComplexSignature)
        self.fallback = dspy.Predict(SimpleSignature)

    def forward(self, question):
        try:
            # Try complex model first
            result = self.primary(question=question)
            if validate(result):
                return result
        except:
            pass

        # Fall back to simple model
        return self.fallback(question=question)
```

### 2. Cached Response Fallback
```python
class CachedFallback:
    def __init__(self, predictor):
        self.predictor = predictor
        self.cache = {}

    def __call__(self, question):
        try:
            result = self.predictor(question=question)
            self.cache[question] = result  # Cache successful result
            return result
        except:
            # Try cache first
            if question in self.cache:
                logging.info("Using cached result")
                return self.cache[question]

            # Try similar question
            similar_q = find_similar_question(question, self.cache.keys())
            if similar_q:
                logging.info("Using similar cached result")
                return self.cache[similar_q]

            raise  # No fallback available
```

### 3. Rule-Based Fallback
```python
def rule_based_fallback(question, context):
    """Simple rule-based system as ultimate fallback."""

    # Pattern matching
    if "what is" in question.lower():
        # Extract entity and return definition
        entity = extract_entity(question)
        return f"{entity} is defined as: [definition from context]"

    if "when" in question.lower():
        # Extract dates from context
        dates = extract_dates(context)
        return f"Relevant dates: {', '.join(dates)}"

    # Default
    return "I don't have enough information to answer that question."
```

---

## Error Categories and Handling

### 1. Transient Errors (Retry)
```python
# Network errors, API rate limits, temporary unavailability
TRANSIENT_ERRORS = (TimeoutError, ConnectionError, RateLimitError)

def handle_with_retry(func):
    try:
        return func()
    except TRANSIENT_ERRORS as e:
        # Retry makes sense
        return retry_with_backoff(func)
```

### 2. Validation Errors (Reject Early)
```python
# Invalid inputs, malformed requests
def handle_validation_error(error):
    return {
        'success': False,
        'error': 'Invalid input',
        'details': str(error),
        'user_message': 'Please check your input and try again.'
    }
```

### 3. LM Failures (Fallback)
```python
# LM produces garbage, refuses to respond, hallucinated
def handle_lm_failure(primary_predictor, fallback_predictor, inputs):
    try:
        result = primary_predictor(**inputs)
        if validate(result):
            return result
    except:
        pass

    # Use fallback
    return fallback_predictor(**inputs)
```

### 4. Catastrophic Errors (Fail Gracefully)
```python
# System out of memory, database down
def handle_catastrophic_error():
    return {
        'success': False,
        'error': 'System temporarily unavailable',
        'user_message': 'We apologize for the inconvenience. Please try again later.',
        'should_alert': True
    }
```

---

## Critical Insights

### 1. Fail Fast on Invalid Inputs
```python
# ✅ Good: Check inputs before expensive LM call
if not validate_input(question):
    return error_response("Invalid input")

result = expensive_lm_call(question)  # Only if valid
```

### 2. Timeouts Prevent Hangs
```python
# ❌ Bad: No timeout
result = predictor(question=question)  # Could hang forever!

# ✅ Good: Always set timeout
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("LM call timed out")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)  # 30 second timeout
try:
    result = predictor(question=question)
finally:
    signal.alarm(0)  # Cancel alarm
```

### 3. Log Everything for Debugging
```python
import logging

logging.basicConfig(level=logging.INFO)

def robust_call(predictor, **kwargs):
    logging.info(f"Calling predictor with inputs: {kwargs}")

    try:
        result = predictor(**kwargs)
        logging.info(f"Success: {result}")
        return result
    except Exception as e:
        logging.error(f"Failed: {e}", exc_info=True)
        raise
```

### 4. Circuit Breakers Prevent Cascading Failures
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.state = 'closed'  # closed, open, half-open

    def call(self, func):
        if self.state == 'open':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'half-open'  # Try again
            else:
                raise Exception("Circuit breaker open")

        try:
            result = func()
            if self.state == 'half-open':
                self.state = 'closed'  # Success, close circuit
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = 'open'  # Open circuit

            raise
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: No Input Validation
```python
# Bad: Accept anything
result = predictor(question=user_input)
```
**Fix**: Validate first

### ❌ Mistake 2: Infinite Retries
```python
# Bad: Could retry forever
while True:
    try:
        return predictor(question)
    except:
        continue
```
**Fix**: Limit retries

### ❌ Mistake 3: Silent Failures
```python
# Bad: Swallow exceptions
try:
    result = predictor(question)
except:
    pass  # User never knows what happened!
```
**Fix**: Log and inform user

### ❌ Mistake 4: No Fallback
```python
# Bad: Crash if LM fails
result = predictor(question)  # Throws exception → crash
```
**Fix**: Always have fallback

### ❌ Mistake 5: Exposing Internal Errors
```python
# Bad: Show stack trace to users
except Exception as e:
    return str(e)  # "OpenAI API key invalid" exposed!
```
**Fix**: User-friendly messages

---

## Testing Your Understanding

You've mastered error handling if you can:

1. ✅ Validate inputs before processing
2. ✅ Implement retry strategies
3. ✅ Create fallback mechanisms
4. ✅ Set appropriate timeouts
5. ✅ Log failures comprehensively
6. ✅ Handle errors gracefully
7. ✅ Write user-friendly error messages

---

## Connection to Other Modules

### Error Handling Builds On:
- **Module 08 (Evaluation)**: Eval reveals failure modes
- **Module 02 (Modules)**: Wrap modules with guards

### Error Handling Feeds Into:
- **Module 10 (Best Practices)**: Production patterns

---

## Quick Reference Card

```python
# Robust Module Template

class RobustModule(dspy.Module):
    def __init__(self, max_retries=3, timeout=30):
        super().__init__()
        self.predictor = dspy.ChainOfThought(Signature)
        self.fallback = dspy.Predict(SimpleSignature)
        self.max_retries = max_retries
        self.timeout = timeout

    def forward(self, **kwargs):
        # 1. Validate inputs
        if not self.validate_inputs(kwargs):
            return error_prediction("Invalid input")

        # 2. Retry with backoff
        for attempt in range(self.max_retries):
            try:
                result = timeout_wrapper(
                    self.predictor,
                    timeout=self.timeout,
                    **kwargs
                )

                # 3. Validate output
                if self.validate_output(result):
                    return result

            except Exception as e:
                logging.error(f"Attempt {attempt+1} failed: {e}")

        # 4. Fallback
        try:
            return self.fallback(**kwargs)
        except:
            return error_prediction("Service unavailable")
```

---

## Final Checklist

Before moving to Module 10, ensure:

- [ ] Can validate inputs effectively
- [ ] Understand retry strategies
- [ ] Can implement fallbacks
- [ ] Know timeout importance
- [ ] Can handle different error types
- [ ] Understand graceful degradation
- [ ] Can log failures properly

---

## Next Steps

1. **Add** error handling to your modules
2. **Test** failure scenarios
3. **Move On** to Module 10: Best Practices
4. **Remember** Plan for failure, not just success

---

**Key Mantra**: *Validate inputs, retry transients, fallback gracefully, log everything.*
