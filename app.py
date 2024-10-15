from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Define calculator operations
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b if b != 0 else "Division by zero error"

# Define route for rendering the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Define route to handle form submission and calculation
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        num1 = request.form['num1']
        num2 = request.form['num2']
        operation = request.form['operation']
        
        if not num1 or not num2:
            result = 'Both numbers are required'
        else:
            num1 = float(num1)
            num2 = float(num2)
        
            if operation == 'add':
                result = add(num1, num2)
            elif operation == 'subtract':
                result = subtract(num1, num2)
            elif operation == 'multiply':
                result = multiply(num1, num2)
            elif operation == 'divide':
                result = divide(num1, num2)
            else:
                result = 'Invalid Operation'
        
        return render_template('index.html', result=result, num1=num1, num2=num2, operation=operation)
    except ValueError:
        return render_template('index.html', result="Invalid Input", num1=request.form['num1'], num2=request.form['num2'], operation=request.form['operation'])

if __name__ == '__main__':
    app.run(debug=True, port=5001)
