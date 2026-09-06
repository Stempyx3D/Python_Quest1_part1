def expression_simple(data):
    parts = data.split()
    if len(parts) == 0:
        raise ValueError("Invalid expression format.")
    if parts[0] == "-":
        if len(parts) < 2:
            raise ValueError("Invalid expression format.")
        parts = [parts[0] + parts[1]] + parts[2:]
    i = 0
    
    while i < len(parts) - 1:
        if parts[i] in ['+', '-', '*', '/'] and parts[i+1] == '-':
            if i + 2 >= len(parts):
                raise ValueError("Invalid expression format.")
            parts = parts[:i + 1] + ['-' + parts[i + 2]] + parts[i + 3:]
            continue
        i += 1
    if len(parts) == 1:
        return parts[0]

    while '*' in parts or '/' in parts:
        multiply_index = parts.index('*') if '*' in parts else len(parts)
        divide_index = parts.index('/') if '/' in parts else len(parts)
        index = min(multiply_index, divide_index)
        num1 = parts[index - 1]
        operation = parts[index]
        num2 = parts[index + 1]
        if operation == '*':
            evaluation = str(float(num1) * float(num2))
        elif operation == '/':
            if float(num2) == 0:
                return "∞"
            evaluation = str(float(num1) / float(num2))
        parts = parts[:index - 1] + [evaluation] + parts[index + 2:]

    while '+' in parts or '-' in parts:
        if len(parts) == 1:
            break
        add_index = parts.index('+') if '+' in parts else len(parts)
        subtract_index = parts.index('-') if '-' in parts else len(parts)
        index = min(add_index, subtract_index)
        if index == 0:
            if len(parts) < 2:
                raise ValueError("Invalid expression format.")
            parts = ['-' + parts[1]] + parts[2:]
            continue
        num1 = parts[index - 1]
        operation = parts[index]
        num2 = parts[index + 1]
        if operation == '+':
            evaluation = str(float(num1) + float(num2))
        elif operation == '-':
            evaluation = str(float(num1) - float(num2))
        parts = parts[:index - 1] + [evaluation] + parts[index + 2:]
    return parts[0]

def calculator(data):
    allowed = "0123456789+-*/() . "
    for char in data:
        if char not in allowed:
            raise ValueError("Invalid expression format.")
    
    data = data.replace(" ", "")
    data_cleaned = ""
    for i in range(len(data)):
        data_cleaned += data[i]
        if i < len(data) - 1:
            if data[i].isdigit() and data[i+1] == '(':
                data_cleaned += " * "
            elif data[i] == ')' and data[i+1].isdigit():
                data_cleaned += " * "
            elif data[i] == ')' and data[i+1] == '(':
                data_cleaned += " * "
    data = data_cleaned     
        
    for operation in ["+", "-", "*", "/", "(", ")"]:
        data = data.replace(operation, f" {operation} ")
    while "(" in data:
        start = data.rfind("(")
        end = data.find(")", start)
        if end == -1:
            raise ValueError("Invalid expression format.")
        expression_inner = data[start + 1:end]
        expression_result = expression_simple(expression_inner)
        if expression_result == "∞":
            return "∞"
        data = data[:start] + f" {expression_result} " + data[end + 1:]
    result = expression_simple(data)
    return result
    
def print_result(result):
    if result == "∞":
        print("∞")
    else:
        print(round(float(result), 8))

while True:
    data = input("Enter the expression (like 2 + 3): ")
    result = calculator(data)
    print_result(result)
