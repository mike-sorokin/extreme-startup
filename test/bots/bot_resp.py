def ignorant_response(q):
    return "I don't know"


def math_response(q):
    '''Expects "What is x + y?" request query
       and returns the result of expression '''
    return str(eval(q.replace("What is ", "").replace("?", "")))
