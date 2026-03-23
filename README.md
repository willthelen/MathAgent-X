# MathAgent-X

**Autonomous Multi-Agent Mathematical Reasoning Engine**

LangGraph + Groq + SymPy system that solves university-level math problems (calculus, linear algebra, ODEs, optimization, basic proofs) with verified step-by-step solutions, self-critique, LaTeX export, and plots.

### Features
- Natural-language input
- Multi-agent workflow with ReAct + self-refine loop
- Symbolic solving + numerical verification
- Interactive Streamlit UI
- Export .tex and markdown

### Tech
LangGraph, LangChain-Groq (Llama-3.3-70B), SymPy, SciPy, Matplotlib, Streamlit

### Quick Start
```bash
streamlit run app.py
```

Made by Will Thelen, Junior Mathematics Undergraduate at SLU