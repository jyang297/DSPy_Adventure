# Module 07: Agents - Key Takeaways

## Core Concepts

### What Are DSPy Agents?
**Agents are autonomous systems that reason about actions, use tools, and iteratively work toward goals.**

```
Traditional: LM generates → Done
Agent: LM reasons → Uses tools → Evaluates → Repeats until goal achieved
```

---

## Pattern Comparison: Docs vs. Reality

### Official Docs Say:
```python
agent = dspy.ReAct(
    signature="task -> action, result",
    tools=[search_tool, calculate_tool]
)
result = agent(task="Find population of Tokyo")
```
**Philosophy**: Simple API, show ReAct pattern

### Real Projects Do:
```python
class ProductionAgent(dspy.Module):
    def __init__(self, tools, max_iterations=10, timeout=60):
        super().__init__()
        self.tools = {tool.name: tool for tool in tools}
        self.react = dspy.ReAct(
            signature=AgentSignature,
            tools=list(self.tools.values())
        )
        self.max_iterations = max_iterations
        self.timeout = timeout
        self.history = []

    def forward(self, task: str) -> dspy.Prediction:
        start_time = time.time()

        for iteration in range(self.max_iterations):
            # Timeout check
            if time.time() - start_time > self.timeout:
                return dspy.Prediction(
                    answer="Task timed out",
                    history=self.history,
                    status="timeout"
                )

            try:
                # Agent step
                step_result = self.react(
                    task=task,
                    history="\n".join(self.history)
                )

                self.history.append(f"Step {iteration+1}: {step_result}")

                # Check termination
                if self.is_goal_achieved(step_result):
                    return dspy.Prediction(
                        answer=step_result.result,
                        history=self.history,
                        iterations=iteration+1,
                        status="success"
                    )

            except Exception as e:
                logging.error(f"Agent error at iteration {iteration}: {e}")
                return dspy.Prediction(
                    answer=f"Agent failed: {str(e)}",
                    history=self.history,
                    status="error"
                )

        # Max iterations reached
        return dspy.Prediction(
            answer="Max iterations reached without completing task",
            history=self.history,
            status="incomplete"
        )
```
**Philosophy**: Iteration limits, timeouts, error handling, history tracking

### Best Practice Is:
**Always add termination conditions, error handling, and iteration limits.**

---

## Key Agent Patterns

### 1. ReAct (Reasoning + Acting)
```python
class ReActAgent(dspy.Module):
    def __init__(self, tools):
        super().__init__()
        self.react = dspy.ReAct(
            signature="goal -> thought, action, observation",
            tools=tools
        )

    def forward(self, goal):
        return self.react(goal=goal)
```
**Pattern**: Think → Act → Observe → Repeat
**Use**: General-purpose agent tasks

---

### 2. Tool-Using Agent
```python
def search_tool(query: str) -> str:
    """Search the web for information."""
    return web_search(query)

def calculator_tool(expression: str) -> str:
    """Evaluate mathematical expressions."""
    return str(eval(expression))

tools = [search_tool, calculator_tool]

agent = dspy.ReAct(
    signature="task -> result",
    tools=tools
)
```
**Pattern**: Agent decides which tool to use when
**Use**: Tasks requiring external capabilities

---

### 3. Multi-Agent System
```python
class MultiAgentSystem(dspy.Module):
    def __init__(self):
        super().__init__()
        self.researcher = dspy.ReAct(ResearchSignature, tools=[search])
        self.analyst = dspy.ReAct(AnalysisSignature, tools=[calculate])
        self.coordinator = dspy.ChainOfThought(CoordinateSignature)

    def forward(self, task):
        # Coordinator decides which agent(s) to use
        plan = self.coordinator(task=task)

        if "research" in plan.approach:
            research = self.researcher(task=task)
        if "analysis" in plan.approach:
            analysis = self.analyst(data=research.result)

        # Synthesize results
        return self.coordinator(
            task=task,
            research=research.result,
            analysis=analysis.result
        )
```
**Pattern**: Multiple specialized agents coordinated
**Use**: Complex tasks benefiting from specialization

---

### 4. Hierarchical Agent
```python
class HierarchicalAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.planner = dspy.ChainOfThought(PlanSignature)
        self.executor = dspy.ReAct(ExecuteSignature, tools=tools)
        self.evaluator = dspy.ChainOfThought(EvaluateSignature)

    def forward(self, goal):
        # High-level planning
        plan = self.planner(goal=goal)

        # Execute each step
        results = []
        for step in plan.steps:
            result = self.executor(task=step)
            results.append(result)

            # Evaluate progress
            eval = self.evaluator(
                goal=goal,
                completed_steps=results
            )

            if eval.goal_achieved:
                break

        return dspy.Prediction(
            result=results[-1].result,
            steps=results
        )
```
**Pattern**: Plan → Execute → Evaluate → Repeat
**Use**: Complex multi-step tasks

---

## Critical Insights

### 1. Agents Need Clear Termination Conditions
```python
# ❌ Bad: No termination
while True:
    step = agent.step()

# ✅ Good: Multiple termination conditions
max_iterations = 10
max_time = 60
goal_threshold = 0.9

for i in range(max_iterations):
    if time.time() - start > max_time:
        break  # Timeout
    if goal_achieved(state):
        break  # Success
    if stuck_detector(history):
        break  # Stuck in loop

    step = agent.step()
```

### 2. Tool Reliability Is Critical
```python
# ❌ Bad: Tools can crash agent
def unreliable_tool(query):
    result = api.call(query)  # Can fail!
    return result

# ✅ Good: Tools handle errors
def reliable_tool(query):
    try:
        result = api.call(query, timeout=10)
        return result
    except TimeoutError:
        return "Tool timed out, please try again"
    except Exception as e:
        return f"Tool error: {str(e)}"
```

### 3. Agent State Management
```python
class StatefulAgent(dspy.Module):
    def __init__(self, tools):
        super().__init__()
        self.tools = tools
        self.state = {
            'history': [],
            'observations': [],
            'goal_progress': 0.0
        }

    def forward(self, goal):
        self.state['goal'] = goal

        for iteration in range(10):
            # Agent uses state for context
            action = self.decide_action(self.state)
            observation = self.execute_action(action)

            # Update state
            self.state['history'].append(action)
            self.state['observations'].append(observation)
            self.state['goal_progress'] = self.evaluate_progress()

            if self.state['goal_progress'] >= 1.0:
                break
```

### 4. Multi-Agent Coordination
```python
# Pattern: Message passing between agents
class CoordinatedAgents(dspy.Module):
    def __init__(self):
        super().__init__()
        self.agent_a = SpecialistAgentA(tools_a)
        self.agent_b = SpecialistAgentB(tools_b)
        self.message_queue = []

    def forward(self, task):
        # Agent A works first
        result_a = self.agent_a(task=task)

        # Pass result to Agent B
        self.message_queue.append({
            'from': 'agent_a',
            'to': 'agent_b',
            'content': result_a.result
        })

        result_b = self.agent_b(
            task=task,
            input_from_a=result_a.result
        )

        return self.synthesize(result_a, result_b)
```

---

## Common Agent Patterns

### Pattern 1: Research Agent
```python
class ResearchAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.search = search_tool
        self.react = dspy.ReAct(
            signature="topic -> findings",
            tools=[self.search]
        )

    def forward(self, topic):
        return self.react(topic=topic)
```

### Pattern 2: Data Analysis Agent
```python
class AnalysisAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        tools = [calculate, visualize, statistical_test]
        self.react = dspy.ReAct(
            signature="data, question -> analysis",
            tools=tools
        )

    def forward(self, data, question):
        return self.react(data=data, question=question)
```

### Pattern 3: Code Generation Agent
```python
class CodeAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        tools = [write_code, run_tests, debug]
        self.react = dspy.ReAct(
            signature="specification -> code",
            tools=tools
        )

    def forward(self, specification):
        return self.react(specification=specification)
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: No Iteration Limit
```python
# Bad: Infinite loop possible
while not goal_achieved:
    agent.step()
```
**Fix**: Always limit iterations

### ❌ Mistake 2: Tools Without Error Handling
```python
# Bad
def tool(query):
    return api.call(query)  # Can crash
```
**Fix**: Wrap in try/except

### ❌ Mistake 3: No State Tracking
```python
# Bad: Agent has no memory
for i in range(10):
    result = agent(task)  # Forgets previous iterations!
```
**Fix**: Pass history or maintain state

### ❌ Mistake 4: Unclear Tool Descriptions
```python
# Bad
def tool(x):
    """Does something."""
    return process(x)

# Good
def tool(query: str) -> str:
    """Search Wikipedia for information.

    Args:
        query: Search query (2-100 words)

    Returns:
        Top 3 search results as formatted text
    """
    return wikipedia_search(query)
```

### ❌ Mistake 5: No Goal Achievement Check
```python
# Bad: Agent runs all iterations even if done
for i in range(10):
    result = agent.step()

# Good: Exit when done
for i in range(10):
    result = agent.step()
    if is_goal_achieved(result):
        break
```

---

## Tool Design Best Practices

### 1. Clear Tool Signatures
```python
def search_web(query: str, num_results: int = 3) -> str:
    """Search the web and return results.

    Args:
        query: Search query string
        num_results: Number of results to return (default: 3)

    Returns:
        Formatted search results as string
    """
    # Implementation
```

### 2. Consistent Return Types
```python
# ✅ All tools return strings (easy for LM to process)
def tool1(x) -> str: ...
def tool2(x) -> str: ...

# Or all return structured data
def tool1(x) -> dict: ...
def tool2(x) -> dict: ...
```

### 3. Error Messages as Returns
```python
def tool(query):
    try:
        result = api.call(query)
        return f"Success: {result}"
    except Exception as e:
        return f"Error: {str(e)}. Please try a different query."
```

---

## Agent Optimization

### 1. Optimize Tool Selection
```python
# Metric that rewards efficient tool use
def efficiency_metric(example, pred, trace=None):
    # Correct answer
    correctness = 1.0 if pred.result == example.result else 0.0

    # Number of tool calls (fewer is better)
    if trace:
        tool_calls = len(trace.get('tool_uses', []))
        efficiency = 1.0 / (1.0 + tool_calls * 0.1)
    else:
        efficiency = 0.5

    return 0.7 * correctness + 0.3 * efficiency
```

### 2. Optimize Agent Reasoning
```python
# Use better teacher agent
teacher_agent = dspy.ChainOfThought(ComplexAgentSignature)
student_agent = dspy.ReAct(SimpleAgentSignature, tools=tools)

optimizer = BootstrapRS(metric=agent_metric)
optimized_agent = optimizer.compile(
    student=student_agent,
    teacher=teacher_agent,
    trainset=agent_tasks
)
```

---

## Testing Your Understanding

You've mastered agents if you can:

1. ✅ Build ReAct agent with tools
2. ✅ Implement termination conditions
3. ✅ Handle agent failures gracefully
4. ✅ Design reliable tools
5. ✅ Track agent state/history
6. ✅ Coordinate multiple agents
7. ✅ Optimize agent efficiency

---

## Connection to Other Modules

### Agents Build On:
- **Module 02 (Modules)**: Agents are complex modules
- **Module 06 (RAG)**: Agents often use RAG as a tool

### Agents Feed Into:
- **Module 08 (Evaluation)**: Agent metrics are complex
- **Module 10 (Best Practices)**: Production agent patterns

---

## Quick Reference Card

```python
# Production Agent Template

class ProductionAgent(dspy.Module):
    def __init__(self, tools, max_iterations=10):
        super().__init__()
        self.react = dspy.ReAct(
            signature="task, history -> action, observation",
            tools=tools
        )
        self.max_iterations = max_iterations
        self.history = []

    def forward(self, task: str) -> dspy.Prediction:
        for i in range(self.max_iterations):
            try:
                result = self.react(
                    task=task,
                    history="\n".join(self.history)
                )

                self.history.append(f"Step {i+1}: {result}")

                if self.is_complete(result):
                    return dspy.Prediction(
                        answer=result.observation,
                        iterations=i+1
                    )
            except Exception as e:
                return dspy.Prediction(
                    answer=f"Agent error: {e}",
                    iterations=i+1
                )

        return dspy.Prediction(
            answer="Task incomplete",
            iterations=self.max_iterations
        )
```

---

## Final Checklist

Before moving to Module 08, ensure:

- [ ] Can build ReAct agent
- [ ] Understand tool design
- [ ] Know termination conditions
- [ ] Can handle agent errors
- [ ] Understand multi-agent systems
- [ ] Can track agent state
- [ ] Know agent optimization strategies

---

## Next Steps

1. **Build** an agent for a specific task
2. **Design** robust tools with error handling
3. **Move On** to Module 08: Evaluation
4. **Remember** Agents need clear goals and limits

---

**Key Mantra**: *Good tools + Clear goals + Proper limits = Reliable agents.*
