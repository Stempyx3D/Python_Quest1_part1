data: str
operation: str

def calculator(data):
    def parse_data():
        parts = data.split()
        if len(parts) != 3:
            raise ValueError("Invalid expression format..")
        num1, operation, num2 = parts
        return float(num1), operation, float(num2)
    
    num1, operation, num2 = parse_data()
    if operation == "+":
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == "*":
        return num1 * num2
    elif operation == "/":
        if num2 == 0:
            return "∞"
        return num1 / num2

def print_result(result):
    print(round(result, 8))

while True:
    data = input("Enter the expression (like 2 + 3): ")
    result = calculator(data)
    print_result(result)
