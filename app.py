import streamlit as st
from graph import graph
from utils.helpers import clean_latex
import time

st.set_page_config(page_title="MathAgent-X", layout="wide")
st.title("🧠 MathAgent-X")
st.caption("Autonomous Multi-Agent Mathematical Reasoning Engine | Junior Math Undergrad Portfolio")

problem = st.text_area("Enter math problem (calculus, linear algebra, ODEs, optimization, proofs):", height=150, placeholder="Solve the integral of x*sin(x) or find eigenvalues of [[2,1],[1,2]]...")

if st.button("Solve with Agents", type="primary"):
    if not problem:
        st.error("Enter a problem")
    else:
        with st.spinner("Agents working (Planner → Solver → Verifier → Critic loop)..."):
            start = time.time()
            result = graph.invoke({"problem": problem})
            st.success(f"Done in {time.time()-start:.1f}s")

            st.subheader("Final Explanation")
            st.markdown(result.get("final_solution", "No output"))

            if "symbolic_result" in result:
                st.subheader("Symbolic Result (LaTeX)")
                latex_code = clean_latex(str(result["symbolic_result"]))
                st.latex(latex_code)
                st.download_button("Download .tex", latex_code, "solution.tex", "text/plain")

            st.subheader("Agent Trace")
            with st.expander("Full trace (for debugging/portfolio demo)"):
                st.write(result)

st.info("Test problems: 'Differentiate x**2 * sin(x)', 'Solve y'' + y = 0', 'Find eigenvalues of matrix [[1,2],[3,4]]'")