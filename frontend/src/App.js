import React, { useState } from 'react';

const ScientificCalculator = () => {
  const [expression, setExpression] = useState('');
  const [result, setResult] = useState('');
  const [postfix, setPostfix] = useState(''); // State for storing the postfix expression
  const [mode, setMode] = useState('degrees');
  const [error, setError] = useState('');
  const [theme, setTheme] = useState('light'); // Theme state

  const handleCalculate = async () => {
    console.log(expression)
    setResult('');
    setError('');
    try {
      const response = await fetch('http://localhost:5000/calculate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          expression,
          use_degrees: mode === 'degrees',
        }),
      });

      const data = await response.json();
      if (response.ok) {
        setResult(data.result);
        setPostfix(data.postfix); // Assuming the backend sends the postfix expression
        setError('');
      } else {
        setError(data.error || 'An error occurred');
      }
    } catch (err) {
      setError('Failed to connect to the server');
    }
  };

  const appendToExpression = (value) => {
    if (value==='π') {
      setExpression((prev) => prev + 'pi');
    }
    else if (value==='√') {
      setExpression((prev) => prev + 'sqrt(');
    }
    else {
      setExpression((prev) => prev + value);
    }
  };

  const clearExpression = () => {
    setExpression('');
    setResult('');
    setPostfix(''); // Clear postfix expression as well
    setError('');
  };

  const deleteLastChar = () => {
    setExpression((prev) => prev.slice(0, -1));
  };

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === 'dark' ? 'light' : 'dark'));
  };

  const Button = ({ onClick, className = '', children }) => (
    <button
      onClick={onClick}
      className={`px-4 py-2 rounded-lg text-lg font-semibold transition-colors ${className}`}
    >
      {children}
    </button>
  );

  const handlePress = (event) => {
    if (event.key === 'Enter') {
      handleCalculate(); // Call the button click handler
    }
  };

  const isDark = theme === 'dark';

  // Function to add decimal point to the expression
  const appendDecimal = () => {
    const lastNumber = expression.split(/[+\-*/^()]+/).pop();
    if (!lastNumber.includes('.')) {
      setExpression((prev) => prev + '.');
    }
  };

  return (
    <div
      className={`min-h-screen transition-all duration-300 ${isDark ? 'bg-gray-900 text-white' : 'bg-gray-100 text-black'} flex items-center justify-center`}
    >
      <div
        className={`rounded-2xl shadow-xl w-full max-w-md p-6 ${isDark ? 'bg-gray-800' : 'bg-white'}`}  
      >
        <div className="flex justify-between items-center mb-6">
          <div className="text-2xl font-bold">STAN Scientific Calculator</div>
          <button
            onClick={toggleTheme}
            className={`p-2 rounded-lg ${isDark ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-200 hover:bg-gray-300'}`}
          >
            {isDark ? 'Light Mode' : 'Dark Mode'}
          </button>
        </div>

        {/* Mode Selection */}
        <div className="flex justify-center space-x-4 mb-6">
          <label className="flex items-center space-x-2">
            <input
              type="radio"
              checked={mode === 'degrees'}
              onChange={() => setMode('degrees')}
              className="form-radio h-4 w-4"
            />
            <span>Degrees</span>
          </label>
          <label className="flex items-center space-x-2">
            <input
              type="radio"
              checked={mode === 'radians'}
              onChange={() => setMode('radians')}
              className="form-radio h-4 w-4"
            />
            <span>Radians</span>
          </label>
        </div>

        {/* Display */}
        <div className="space-y-2 mb-4">
          <input
            value={expression}
            placeholder='Type an expression or use the buttons'
            onChange={(e) => setExpression(e.target.value)}
            onKeyDown={handlePress}
            className={`w-full p-4 text-right text-lg font-mono border rounded-lg ${isDark ? 'bg-gray-700 border-gray-600' : 'bg-gray-100 border-gray-300'}`}
            
          />
          {postfix && (
            <div className="text-right text-xl font-mono font-bold p-2">
              <strong>Postfix: </strong>{postfix}
            </div>
          )}
          {result && (
            <div className="text-right text-xl font-mono font-bold p-2">
              <strong>Result: </strong>{result}
            </div>
          )}
          {error && (
            <div className="text-red-500 text-sm text-center p-2">
              {error}
            </div>
          )}
        </div>

        {/* Calculator Buttons */}
        <div className="grid grid-cols-4 gap-2">
          {/* Basic Operations */}
          {['(', ')', '!', '%'].map((item) => (
            <Button
              key={item}
              onClick={() => appendToExpression(item)}
              className={`${isDark ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-200 hover:bg-gray-300'}`}
            >
              {item}
            </Button>
          ))}
          {['sin', 'cos', 'tan', 'log', 'ln'].map((item) => (
            <Button
              key={item}
              onClick={() => appendToExpression(`${item}(`)}
              className={`${isDark ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-200 hover:bg-gray-300'}`}
            >
              {item}
            </Button>
          ))}
          {['^', '√', 'π', 'e'].map((item) => (
            <Button
              key={item}
              onClick={() => appendToExpression(item)}
              className={`${isDark ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-200 hover:bg-gray-300'}`}
            >
              {item}
            </Button>
          ))}
          {[...Array(10).keys()].reverse().map((num) => (
            <Button
              key={num}
              onClick={() => appendToExpression(num.toString())}
              className={`${isDark ? 'bg-gray-700 hover:bg-gray-600' : 'bg-blue-100 hover:bg-blue-200'}`}
            >
              {num}
            </Button>
          ))}
          {/* Add the new operation buttons */}
          {['+', '-', '*', '/'].map((item) => (
            <Button
              key={item}
              onClick={() => appendToExpression(item)}
              className={`${isDark ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-200 hover:bg-gray-300'}`}
            >
              {item}
            </Button>
          ))}
          {/* Decimal Button */}
          <Button
            onClick={appendDecimal}
            className={`${isDark ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-200 hover:bg-gray-300'}`}
          >
            .
          </Button>
          <Button
            onClick={clearExpression}
            className={`col-span-2 ${isDark ? 'bg-red-500 hover:bg-red-600 text-white' : 'bg-red-500 hover:bg-red-600 text-white'}`}
          >
            Clear
          </Button>
          <Button
            onClick={deleteLastChar}
            className={`${isDark ? 'bg-yellow-500 hover:bg-yellow-600 text-white' : 'bg-yellow-500 hover:bg-yellow-600 text-white'}`}
          >
            ⌫
          </Button>
          <Button
            onClick={handleCalculate}
            className={`${isDark ? 'bg-green-500 hover:bg-green-600 text-white' : 'bg-green-500 hover:bg-green-600 text-white'}`}
          >
            =
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ScientificCalculator;
