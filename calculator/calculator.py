data1: float
data2: float
operation: str

def calculator(data1, data2, operation):
    def add():
        return data1 + data2
    def subtract():
        return data1 - data2
    def multiply():
        return data1 * data2
    def divide():
        if data2 == 0:
            return "∞"
        return data1 / data2
    
    if operation == "+":
        return add()
    elif operation == "-":
        return subtract()
    elif operation == "*":
        return multiply()
    elif operation == "/":
        return divide()

def print_result(result):
    print(round(result, 8))

while True:
    data1 = float(input("Enter the first number: "))
    operations = ["+", "-", "*", "/"]
    print("Choose an operation: +, -, *, /")
    operation = input("Enter the operation: ")
    while operation not in operations:
        print("Invalid operation. Please choose from +, -, *, /.")
        operation = input("Enter the operation: ")
    data2 = float(input("Enter the second number: "))
    result = calculator(data1, data2, operation)
    print_result(result)
