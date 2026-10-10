import ast,operator as op
from langchain_core.tools import StructuredTool
from pydantic import BaseModel,Field
OPS={ast.Add:op.add,ast.Sub:op.sub,ast.Mult:op.mul,ast.Div:op.truediv,ast.Pow:op.pow,ast.Mod:op.mod,ast.USub:op.neg}
class CalculatorInput(BaseModel): expression:str=Field(min_length=1,max_length=200)
def _eval(n):
    if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)): return float(n.value)
    if isinstance(n,ast.UnaryOp) and type(n.op) in OPS: return OPS[type(n.op)](_eval(n.operand))
    if isinstance(n,ast.BinOp) and type(n.op) in OPS: return OPS[type(n.op)](_eval(n.left),_eval(n.right))
    raise ValueError("Unsupported calculator expression")
def calculate(expression):
    tree=ast.parse(expression,mode="eval")
    if sum(1 for _ in ast.walk(tree))>30: raise ValueError("Expression too complex")
    return str(_eval(tree.body))
calculator_tool=StructuredTool.from_function(func=calculate,name="calculator",description="Safely evaluate basic arithmetic; never execute Python",args_schema=CalculatorInput)
