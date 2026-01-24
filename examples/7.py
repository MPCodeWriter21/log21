import ast
import operator
from functools import reduce

import log21

# `safe_eval` Based on https://stackoverflow.com/a/9558001/1113207
# Supported Operators
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Pow: operator.pow,
    ast.BitXor: operator.xor,
    ast.USub: operator.neg
}


def safe_eval(expr: str):
    """Safely evaluate a mathematical expression.

    >>> eval_expr('2^6')
    4
    >>> eval_expr('2**6')
    64
    >>> eval_expr('1 + 2*3**(4^5) / (6 + -7)')
    -5.0

    :param expr: expression to evaluate
    :raises SyntaxError: on invalid expression
    :return: result of the evaluation
    """
    try:
        return _eval(ast.parse(expr, mode='eval').body)
    except (TypeError, KeyError, SyntaxError):
        log21.error(f'Invalid expression: {expr}')
        raise


def _eval(node: ast.AST):
    """Internal implementation of `safe_eval`.

    :param node: AST node to evaluate
    :raises TypeError: on invalid node
    :raises KeyError: on invalid operator
    :raises ZeroDivisionError: on division by zero
    :raises ValueError: on invalid literal
    :raises SyntaxError: on invalid syntax
    :return: result of the evaluation
    """
    if isinstance(node, ast.Constant):  # <number>
        return node.value
    if isinstance(node, ast.BinOp):     # <left> <operator> <right>
        return operators[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp):   # <operator> <operand> e.g., -1
        return operators[type(node.op)](_eval(node.operand))
    raise TypeError(node)


# Example code
def addition(*numbers: float):
    """Addition of numbers.

    Args:
        numbers (float): numbers to add
    """
    if len(numbers) < 2:
        log21.error('At least two numbers are required! Use `-n`.')
        return
    log21.info(f'Result: {sum(numbers)}')


def multiplication(*numbers: float):
    """Multiplication of numbers.

    Args:
        numbers (float): numbers to multiply
    """
    if len(numbers) < 2:
        log21.error('At least two numbers are required! Use `-n`.')
        return
    log21.info(f'Result: {reduce(lambda x, y: x * y, numbers)}')


def calc(*inputs: str, verbose: bool = False):
    """Calculate numbers.

    :param inputs: numbers and operators
    """
    expression = ' '.join(inputs)

    if len(expression) < 3:
        log21.error('At least two numbers and one operator are required! Use `-i`.')
        return

    if verbose:
        log21.basic_config(level='DEBUG')

    log21.debug(f'Expression: {expression}')
    try:
        log21.info(f'Result: {safe_eval(expression)}')
    except (TypeError, KeyError, SyntaxError):
        pass


if __name__ == "__main__":
    log21.argumentify({'add': addition, 'mul': multiplication, 'calc': calc})
