from langchain.tools import tool


@tool
def calculate(expression: str) -> float:
    """
    Evaluate a mathematical expression like '3+3*9'.
    """
    print("Got expression:", expression)

    return eval(expression)