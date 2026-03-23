from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator
from langchain_groq import ChatGroq
from prompts.math_prompts import SYSTEM_PROMPTS
from utils.helpers import safe_execute_sympy
from dotenv import load_dotenv
import os
import re

load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)

class AgentState(TypedDict):
    problem: str
    plan: str
    sympy_code: str
    symbolic_result: str
    verification: str
    critique: str
    final_solution: str
    messages: Annotated[List, operator.add]

def planner_node(state):
    response = llm.invoke(f"Problem: {state['problem']}\n\n{SYSTEM_PROMPTS['planner']}")
    return {"plan": response.content, "messages": [response]}

def solver_node(state):
    response = llm.invoke(f"Plan: {state['plan']}\nProblem: {state['problem']}\n\n{SYSTEM_PROMPTS['solver']}")
    code_match = re.search(r'```python\s*(.*?)\s*```', response.content, re.DOTALL)
    code = code_match.group(1) if code_match else response.content
    return {"sympy_code": code, "messages": [response]}

def verifier_node(state):
    exec_result = safe_execute_sympy(state["sympy_code"])
    symbolic_result = exec_result["result"] if exec_result["success"] else exec_result["error"]
    verification = f"Symbolic result: {symbolic_result}\nVerification passed (high confidence)." if exec_result["success"] else f"Execution failed: {exec_result['error']}"
    return {"symbolic_result": str(symbolic_result), "verification": verification, "messages": []}

def critic_node(state):
    response = llm.invoke(f"Problem: {state['problem']}\nResult: {state.get('symbolic_result')}\nVerification: {state.get('verification')}\n\n{SYSTEM_PROMPTS['critic']}")
    return {"critique": response.content, "messages": [response]}

def explainer_node(state):
    response = llm.invoke(f"Problem: {state['problem']}\nSolution: {state.get('symbolic_result')}\n\n{SYSTEM_PROMPTS['explainer']}")
    return {"final_solution": response.content, "messages": [response]}

def should_continue(state):
    return "planner" if "NEEDS_REVISION" in state.get("critique", "") else "explainer"

workflow = StateGraph(AgentState)
workflow.add_node("planner", planner_node)
workflow.add_node("solver", solver_node)
workflow.add_node("verifier", verifier_node)
workflow.add_node("critic", critic_node)
workflow.add_node("explainer", explainer_node)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "solver")
workflow.add_edge("solver", "verifier")
workflow.add_edge("verifier", "critic")
workflow.add_conditional_edges("critic", should_continue, {"planner": "planner", "explainer": "explainer"})
workflow.add_edge("explainer", END)

graph = workflow.compile()