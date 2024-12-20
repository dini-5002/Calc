# Stack-Based Calculator 

This project is a **Data Structures and Algorithms (DSA)** implementation of a stack-based calculator. It evaluates mathematical expressions by converting them to postfix notation (Reverse Polish Notation) and computing the result. The backend is implemented using Python and Flask for demonstration purposes, while the focus remains on the algorithmic aspects of the calculator.

## Features

### Supported Operations
- **Arithmetic**:
  - Addition (`+`)
  - Subtraction (`-`)
  - Multiplication (`*`)
  - Division (`/`)
  - Percentage (`%`)
- **Exponentiation**:
  - Power (`^`).
- **Factorials**:
  - Calculation of factorial (`!`).
- **Trigonometric Functions**:
  - Sine (`sin`)
  - Cosine (`cos`)
  - Tangent (`tan`)
  - Supports both **degrees** and **radians**.
- **Logarithmic Functions**:
  - Base-10 Logarithm (`log`)
  - Natural Logarithm (`ln`)
- **Square Root**:
  - Compute square root (`sqrt`).
- **Constants**:
  - π (Pi)
  - e (Euler's number)

### DSA Implementation
- **Custom Stack**: Used to handle operator precedence, parentheses, and postfix evaluation.
- **Postfix Conversion**: Converts infix expressions to postfix notation for easier computation.
- **Expression Fixer**: Prepares and validates input expressions to handle implicit multiplication, whitespace, and function calls.

### Outputs
1. **Postfix Expression**: Displays the postfix conversion of the input expression.
2. **Calculated Result**: Evaluates the postfix expression to provide the final result.
3. **Precision**: Results are calculated with up to 15 decimal places.

### Error Handling
- **Expression Validation**:
  - Mismatched parentheses.
  - Invalid or unsupported characters.
  - Missing arguments for functions like `sin`, `cos`, `tan`, `sqrt`.
- **Mathematical Errors**:
  - Division by zero.
  - Square root or logarithm of a negative number.

## API Endpoints

### `/calculate`
**Method**: `POST`  
**Description**: Accepts a mathematical expression, validates it, converts it to postfix, and evaluates it.  

**Request Body**:
```json
{
  "expression": "<expression string>",
  "use_degrees": "true | false"
}
```
- `expression`: String containing the mathematical expression.
- `use_degrees`: Boolean indicating whether to use degrees (true) or radians (false) for trigonometric calculations.

**Response**:
- On Success:
```json
{
  "postfix_expression": "<postfix expression>",
  "result": "<calculated result>",
  "use_degrees": "true | false"
}
```
- On Failure:
```json
{
  "error": "<error message>"
}
```

## Example Usage

### Input Expression
```json
{
  "expression": "3 + 5 * ( 2 ^ 3 ) - 6 / 2",
  "use_degrees": false
}
```

### Outputs
- **Postfix Expression**: `3 5 2 3 ^ * + 6 2 / -`
- **Calculated Result**: `41.000000000000000`

## Technical Highlights

1. **Custom Stack Implementation**: The stack is used extensively for:
   - Managing operators and parentheses during infix-to-postfix conversion.
   - Postfix expression evaluation.
2. **Mathematical Function Evaluation**:
   - Built-in support for advanced operations like trigonometry, logarithms, and square roots.
   - Support for constants like `π` and `e`.
3. **DSA Principles**:
   - Efficient handling of operator precedence and associativity.
   - Robust error-checking for invalid expressions.

## Setup and Execution

1. Clone the repository:
     ```bash
       git clone <repository-url>
       cd <repository-folder>
     ```
   
2. Backend Setup (Flask):

   1.	Navigate to the backend directory:
     ```bash
       cd Calc/backend
     ```
   2.	Create and activate a virtual environment:
     ```bash
       python -m venv 
       source venv/bin/activate  # On macOS/Linux
       venv\Scripts\activate     # On Windows
     ```
   3.	Install the required Python dependencies:
     ```bash
       pip install -r requirements.txt
     ```
   4.	Run the Flask server: 
      ```bash
        python app.py
      ```
    By default, the Flask app will be available at http://127.0.0.1:5000/.


 3. Frontend Setup :
  
    1.	Navigate to the frontend directory:
       ```bash
         cd Calc/frontend
       ```
    2.	Install the required Node.js dependencies: 
       ```bash
         npm install i
       ```
    3.	Start the React development server:   
       ```bash
         npm start
       ```
  
     By default, the React app will be available at http://localhost:3000/.

## Usage Guidelines

- The input expression can be given through buttons, or it can also be manually typed in the input area.
- Every opening bracket must have a corresponding closing bracket to avoid raising errors.
- For trigonometric, square root, and logarithmic functions, brackets are optional when the input to those functions is simple (involves just numbers with no operations).
- Users can also give expressions within expressions, like inside a sine function or a cosine function. When providing such inputs, users can include brackets inside the sub-expression only if the brackets are associated with a function themselves.

### Example Input Expression
```json
{
  "expression": "sin( 5 + 3cos(45) - 5!) + log( 3^2 + 3ln(e) - 20%)",
  "use_degrees": true
}
```

## Acknowledgment
This project is a part of the End-Term Evaluation of the course MA 253/CS 253 under the guidance of Dr. Subhra Mazumdar.
