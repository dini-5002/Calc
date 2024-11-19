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

def my_letter(c):
    """Checks if a character starts a mathematical function."""
    return c in ['s', 'c', 't', 'P', 'p', 'e', 'l']

def my_end_letter(c):
    """Checks if a character starts a mathematical function."""
    return c in ['n', 't', 's', 'g']

def my_end_letter2(c):
    """Checks if a character starts a mathematical function."""
    return c in ['I', 'i', 'e']

def func_word(t):
    return t in ["sin", "cos", "tan", "qrt"]

def get_factorial(x):
    """Returns the factorial of a number using memoization."""
    if x <= 1:
        return 1
    if x in dp:
        return dp[x]
    dp[x] = x * get_factorial(x - 1)
    return dp[x]

def is_operator(c):
    """Checks if a character is a valid mathematical operator."""
    return c in ['/', '*', '+', '-', '^', '(', ')', '!', '%', '=']

def priority(c):
    """Returns the priority of mathematical operators."""
    if c in ['-', '+']:
        return 0
    if c in ['/', '*']:
        return 1
    if c == '^':
        return 2
    return -1

def transform_ll(s):
    """Converts a string of digits to an integer."""
    ans = 0
    for char in s:
        ans = ans * 10 + (ord(char) - ord('0'))
    return ans

def fix_string(s, flag):
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
            print(s,'1')
        elif (s[i] in ['!', '%'] and s[i + 1] == '(') or (s[i] in ['!', '%'] and my_letter(s[i + 1])) or (s[i] in ['!', '%'] and s[i + 1].isdigit()):
            s = s[:i + 1] + '*' + s[i + 1:]
            print(s,'2')
        elif (s[i] == ')' and my_letter(s[i + 1])) or (s[i].isdigit() and my_letter(s[i + 1])):
            s = s[:i + 1] + '*' + s[i + 1:]
            print(s,'3')
        elif (my_end_letter2(s[i]) and s[i+1] == '(') or (my_end_letter2(s[i]) and my_letter(s[i+1])) or (my_end_letter2(s[i]) and s[i+1].isdigit()):
            s = s[:i + 1] + '*' + s[i + 1:]
            print(s,'4')
        elif (my_end_letter(s[i]) and s[i + 1] == '('):
            print(s,'5')
            j = i+1
            while j < len(s):
                if s[j] == ')':
                    in_s = ''
                    if s[i+2:j]:
                        in_s = fix_string(s[i+2:j], flag)
                    s = s[:i + 1] + str(start_algorithm(in_s, flag)) + s[j + 1:]
                    print(s,'6')
                    break
                elif (s[j].isdigit() and my_letter(s[j + 1])) or (my_end_letter2(s[j]) and s[j+1].isdigit()):
                    s = s[:j + 1] + '*' + s[j + 1:]
                    print(s)
                    j += 1
                j += 1
        elif func_word(s[i-2:i+1]) or func_word(s[i-3:]):
            print(my_letter(s[i+1]), s[i+1].isdigit())
            if (not s[i+1].isdigit()) and (not my_letter(s[i+1])):
                print(s,'7')
                raise ValueError("Trigonometric or Square Root function doesn't have value to evaluate")
        i += 1

    return s

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
    elif func == "ln":
        if value < 0:
            raise ValueError("Natural Log of a negative number is not allowed.")
        return math.log(value)
    elif func == "log":
        if value < 0:
            raise ValueError("Log of a negative number is not allowed.")
        return math.log10(value)
    else:
        raise ValueError(f"Unknown function: {func}")

def start_algorithm(s, flag):
    """Converts an infix expression to postfix and evaluates it."""
    postfix = []
    operators = Stack()
    check = 0
    i = 0
    isNegative = False

    while i < len(s):
        if s[i] == '=':
            break
        elif s[i] == 'e':
            postfix.append(E)
        elif (s[i:i + 2]).lower() == 'pi':
            postfix.append(PI)
            i += 1
        elif s[i].isdigit():
            num = ""
            while i < len(s) and (s[i].isdigit() or s[i] == '.'):
                num += s[i]
                i += 1
            postfix.append(float(num) if '.' in num else int(num))
            i -= 1
        elif s[i:i + 2] == "ln":
            i += 2
            num = ""
            if my_letter(s[i]):
                if s[i] == 'p':
                    value = PI
                    i += 1
                elif s[i] == 'e':
                    value = E
            else:
                if s[i] == '-':
                    isNegative=True
                    i += 1
                while i < len(s) and (s[i].isdigit() or s[i] == '.'):
                    num += s[i]
                    i += 1
                i -= 1
                value = float(num) if '.' in num else int(num)
                if isNegative:
                    value = -1*value
            postfix.append(evaluate_function("ln", value, flag))
        elif s[i:i + 3] in ["sin", "cos", "tan", "log"]:
            func = s[i:i + 3]
            i += 3
            num = ""
            if my_letter(s[i]):
                if s[i] == 'p':
                    value = PI
                    i += 1
                elif s[i] == 'e':
                    value = E
            else:
                if s[i] == '-':
                    isNegative=True
                    i += 1
                while i < len(s) and (s[i].isdigit() or s[i] == '.'):
                    num += s[i]
                    i += 1
                i -= 1
                value = float(num) if '.' in num else int(num)
                if isNegative:
                    value = -1*value
            postfix.append(evaluate_function(func, value, flag))
        elif s[i:i + 4] == "sqrt":
            i += 4
            num = ""
            if my_letter(s[i]):
                if s[i] == 'p':
                    value = PI
                    i += 1
                elif s[i] == 'e':
                    value = E
            else:
                while i < len(s) and (s[i].isdigit() or s[i] == '.'):
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
        elif is_operator(s[i]):
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

    print("Postfix Expression: ", " ".join(map(str, postfix)))

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
        flag = 1 if use_degrees else 0
        expression = fix_string(expression, flag)

        # Evaluate the expression
        result = start_algorithm(expression, flag)
        result = f"{result:.15f}"
        
        return jsonify({'result': result, 'use_degrees': use_degrees})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
