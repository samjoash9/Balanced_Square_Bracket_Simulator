def replace_nth(s, old, new, n):
    start = 0
    for _ in range(n):
        index = s.find(old, start)
        if index == -1:
            return s 
        start = index + 1  

    return s[:index] + new + s[index + len(old):]

def replace_last(s, old, new):
    index = s.rfind(old)
    if index == -1:
        return s
    return s[:index] + new + s[index + len(old):]

def leftmost_derivation(input_string):
    res = ['S']
    stack = "S"

    for i in input_string:
        if i == '[':
            # need to generate 'AS'
            stack = stack.replace("S", "[S]S", 1)
            res.append("S => " +stack)
        else:
            stack = stack.replace("S", "", 1)
            res.append("S => " + stack)
    
    # pop all S 
    stack = stack.replace("S", "")
    res.append("S => " + stack)

    return res

def rightmost_derivation(input_string):
    res = ['S']
    stack = "S"

    pointer = 1

    for i in input_string:
        # if reading (
        if i == '[':
            # transform S to (S)S
            stack = replace_nth(stack, "S", "[S]S", pointer)
            res.append("S => " + stack)
        else:
            pointer += 1

    # delete all S
    for i in range(pointer):
        stack = replace_last(stack, "S", "")
        res.append("S => " + stack)

    return res

# THE LEFTMOST DEFINITION FOR AMBIGUOUS GRAMMAR
# def leftmost_derivation(input_string):
#     res = ['S']
#     stack = "S"

#     for i in input_string:
#         if i == '(':
#             # need to generate 'AS'
#             stack = stack.replace("S", "AS", 1)
#             res.append(stack)

#             # then tranform into '(S)'
#             stack = stack.replace("A", "(S)", 1)
#             res.append(stack)
#         else:
#             stack = stack.replace("S", "", 1)
#             res.append(stack)
    
#     # pop all S 
#     stack = stack.replace("S", "")
#     res.append(stack)

#     return res
