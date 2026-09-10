data: str
operation: str


def calculate_simple(data1, data2, operation):
    if operation == "+":
        return data1 + data2
    if operation == "-":
        return data1 - data2
    if operation == "*":
        return data1 * data2
    if operation == "/":
        if data2 == 0:
            return "∞"
        return data1 / data2
    raise ValueError("Invalid operation")


def tokenizer(expression):
    expr = expression.replace(" ", "")
    tokens = []
    index = 0

    while index < len(expr):
        char = expr[index]

        if char.isdigit() or char == ".":
            start = index
            dot_count = 0
            while index < len(expr) and (expr[index].isdigit() or expr[index] == "."):
                if expr[index] == ".":
                    dot_count += 1
                index += 1
            number = expr[start:index]
            if dot_count > 1:
                raise ValueError("Invalid number")
            tokens.append(number)
            continue

        if char in "+-*/()":
            tokens.append(char)
            index += 1
            continue

        raise ValueError(f"Invalid character: {char}")

    return tokens


def calculator(data, data2=None, operation=None):
    if operation is None and data2 is None:
        tokens = tokenizer(str(data))
        index = 0

        def parse_expression():
            nonlocal index
            value = parse_term()
            while index < len(tokens) and tokens[index] in ("+", "-"):
                op = tokens[index]
                index += 1
                right = parse_term()
                if op == "+":
                    value += right
                else:
                    value -= right
            return value

        def parse_term():
            nonlocal index
            value = parse_factor()
            while index < len(tokens) and tokens[index] in ("*", "/"):
                op = tokens[index]
                index += 1
                right = parse_factor()
                if op == "*":
                    value *= right
                else:
                    if right == 0:
                        return "∞"
                    value /= right
            return value

        def parse_factor():
            nonlocal index
            if index < len(tokens) and tokens[index] in ("+", "-"):
                op = tokens[index]
                index += 1
                value = parse_factor()
                return value if op == "+" else -value

            if index < len(tokens) and tokens[index] == "(":
                index += 1
                value = parse_expression()
                if index >= len(tokens) or tokens[index] != ")":
                    raise ValueError("Missing closing parenthesis")
                index += 1
                return value

            if index < len(tokens) and tokens[index].replace(".", "").isdigit():
                value = float(tokens[index])
                index += 1
                return value

            raise ValueError("Invalid expression")

        result = parse_expression()
        if index != len(tokens):
            raise ValueError("Invalid expression")
        return result

    if operation is not None:
        return calculate_simple(float(data), float(data2), operation)

    raise ValueError("Invalid input")


def print_result(result):
    if result == "∞":
        print(result)
        return
    print(round(float(result), 8))


while True:
    data = input("Enter the expression (like 2 + (3 * 4)): ")
    result = calculator(data)
    print_result(result)
