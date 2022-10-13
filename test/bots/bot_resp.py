def ignorant_response(q):
    return "I don't know"


def math_response(q):
    """Expects "What is x + y?" request query
    and returns the result of expression"""
    print(q)
    print(repr(q))
    expression = q.replace("What is ", "").replace("?", "")
    print(f"expression = {expression}")
    return str(eval(expression))
