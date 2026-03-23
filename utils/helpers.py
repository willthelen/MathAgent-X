import sympy as sp
from sympy import latex
import re

def safe_execute_sympy(code: str):
    try:
        local_dict = {"sp": sp, "sympy": sp}
        exec(code, local_dict)
        result = local_dict.get("result")
        return {"success": True, "result": result, "latex": latex(result) if result is not None else "No result"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def clean_latex(text):
    return re.sub(r'\\\(|\\\)', '$', text)