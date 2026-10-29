from functools import wraps

def shadow(limit=200):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            total = 0
            warned = False
            for row in func(*args, **kwargs):
                try:
                    operation, value = row.split()
                    amount = int(value)
                except ValueError:
                    continue
                else:
                    total += amount
                    print(row)
                    if total > limit and not warned:
                        print("Тіньовий ліміт перевищено. Активую схему")
                        warned = True
                    yield row
            return total
        return wrapper
    return decorator

def suspicious_counter(threshold=200):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            total = 0
            for row in func(*args, **kwargs):
                try:
                    operation, value = row.split()
                    amount = int(value)
                except ValueError:
                    continue
                else:
                    total += amount
                    if total > threshold:
                        excess = total - threshold
                        print("Підозріла сума понад поріг:", excess)
                    yield row
            return total
        return wrapper
    return decorator

@suspicious_counter(threshold=250)
@shadow(limit=200)
def transactions():
    rows = [
        "payment 120",
        "refund 50",
        "transfer 300",
        "payment abc",
        "я тобі потім закину"
    ]
    total = 0
    for row in rows:
        try:
            operation, value = row.split()
            amount = int(value)
        except ValueError:
            continue
        else:
            total += amount
            yield row
    return total
gen = transactions()
while True:
    try:
        next(gen)
    except StopIteration as stit:
        print("Фінальна сума:", stit.value)
        break



