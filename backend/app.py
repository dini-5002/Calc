import math
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

# Constants
MOD = int(1e9 + 7)
PI = 3.141592653589793
E = 2.718281828459045
dp = {}

class Stack:
    """Custom Stack implementation."""
    def __init__(self):
        self.items = []

    def push(self, item):
        """Push an item onto the stack."""
        self.items.append(item)

    def pop(self):
        """Pop an item from the stack."""
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("Pop from an empty stack.")

    def peek(self):
        """Peek at the top item of the stack without removing it."""
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        """Check if the stack is empty."""
        return len(self.items) == 0

    def __len__(self):
        """Return the size of the stack."""
        return len(self.items)

    def __str__(self):
        """String representation of the stack."""
        return str(self.items)

def evaluate_function(func, value, flag):
    """Evaluates mathematical functions like sin, cos, tan, sqrt."""
    if func == "sin":
        return math.sin(math.radians(value)) if flag else math.sin(value)
    elif func == "cos":
        return math.cos(math.radians(value)) if flag else math.cos(value)
    elif func == "tan":
        return math.tan(math.radians(value)) if flag else math.tan(value)
    elif func == "sqrt":
        if value < 0:
            raise ValueError("Square root of a negative number is not allowed.")
        return math.sqrt(value)
    else:
        raise ValueError(f"Unknown function: {func}")

def fix_string(s):
    """Prepares and validates the input expression."""
    s = ''.join(s.split())

    if not s:
        raise ValueError("Expression cannot be empty.")

    if s[0] == '-':
        s = '0' + s
    if s[-1] == '=':
        s = s[:-1]

    i = 0
    while i < len(s) - 1:
        if (s[i].isdigit() and s[i + 1] == '(') or (s[i] == ')' and s[i + 1].isdigit()):
            s = s[:i + 1] + '*' + s[i + 1:]
        elif (s[i] in ['!', '%'] and s[i + 1] == '('):
            s = s[:i + 1] + '*' + s[i + 1:]
        i += 1

    return s

def start_algorithm(s, flag, last):
    """Converts an infix expression to postfix and evaluates it."""
    postfix = []
    operators = Stack()
    check = 0
    i = 0

    while i < len(s):
        if s[i] == '=':
            break
        elif s[i:i + 3] == 'ans':
            postfix.append(last)
            i += 2
        elif s[i] == 'e':
            postfix.append(E)
        elif s[i:i + 2] == 'PI':
            postfix.append(PI)
            i += 1
        elif s[i].isdigit():
            num = ""
            while i < len(s) and (s[i].isdigit() or s[i] == '.'):
                num += s[i]
                i += 1
            postfix.append(float(num) if '.' in num else int(num))
            i -= 1
        elif s[i:i + 3] in ["sin", "cos", "tan"]:
            func = s[i:i + 3]
            i += 3
            num = ""
            while i < len(s) and (s[i].isdigit() or s[i] == '.' or s[i] == '-'):
                num += s[i]
                i += 1
            i -= 1
            value = float(num) if '.' in num else int(num)
            postfix.append(evaluate_function(func, value, flag))
        elif s[i:i + 4] == "sqrt":
            i += 4
            num = ""
            while i < len(s) and (s[i].isdigit() or s[i] == '.' or s[i] == '-'):
                num += s[i]
                i += 1
            i -= 1
            value = float(num) if '.' in num else int(num)
            postfix.append(evaluate_function("sqrt", value, flag))
        elif s[i] == '%':
            x = postfix.pop() / 100
            postfix.append(x)
        elif s[i] == '!':
            x = math.factorial(int(postfix.pop()))
            postfix.append(float(x))
        elif s[i] in ['/', '*', '+', '-', '^', '(', ')']:
            if s[i] == '(':
                operators.push(s[i])
                check += 1
            elif s[i] == ')':
                check -= 1
                while operators.peek() and operators.peek() != '(':
                    postfix.append(operators.pop())
                if operators.peek() == '(':
                    operators.pop()
            else:
                while (not operators.is_empty() and operators.peek() != '('
                       and priority(s[i]) <= priority(operators.peek())):
                    postfix.append(operators.pop())
                operators.push(s[i])
        else:
            raise ValueError(f"Invalid character: {s[i]}")
        i += 1

    if check != 0:
        raise ValueError("Mismatched parentheses in the expression.")

    while not operators.is_empty():
        postfix.append(operators.pop())

    stack = Stack()
    for token in postfix:
        if isinstance(token, (int, float)):
            stack.push(token)
        else:
            b = stack.pop()
            a = stack.pop() if not stack.is_empty() else 0
            if token == '+':
                stack.push(a + b)
            elif token == '-':
                stack.push(a - b)
            elif token == '*':
                stack.push(a * b)
            elif token == '/':
                if b == 0:
                    raise ZeroDivisionError("Division by zero.")
                stack.push(a / b)
            elif token == '^':
                stack.push(math.pow(a, b))
            else:
                raise ValueError(f"Unknown operator: {token}")

    return stack.pop() if not stack.is_empty() else 0

@app.route('/calculate', methods=['POST'])
def calculate_expression():
    """Handles the POST request for calculation."""
    data = request.get_json()
    expression = data.get('expression')
    use_degrees = data.get('use_degrees', False)

    # Prepare expression
    try:
        # Fix the expression and determine whether to use degrees or radians
        expression = fix_string(expression)
        flag = 1 if use_degrees else 0

        # Evaluate the expression
        result = start_algorithm(expression, flag, 0)
        
        return jsonify({'result': result, 'use_degrees': use_degrees})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
