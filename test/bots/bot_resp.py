def ignorant_response(q):
    return "I don't know"


def math_response(q):
    """Expects "What is x + y?" request query
    and returns the result of expression"""
    expression = q.replace("What is ", "").replace("?", "")
    return str(eval(expression))
