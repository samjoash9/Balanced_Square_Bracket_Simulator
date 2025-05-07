def replace_nth(s, old, new, n):
    start = 0
    
    # Loop to find the nth occurrence of 'old'
    for _ in range(n):
        # Find the next occurrence of 'old' starting from 'start'
        index = s.find(old, start)
        
        # If 'old' is not found, then we just return the original string
        if index == -1:
            return s
        
        # Update 'start' to just after the found index to search forward
        start = index + 1

    # Rebuilding the string the string: 
    # putting 'new' before 'old', then the remaining after 'old'
    return s[:index] + new + s[index + len(old):]

def replace_last(s, old, new):
    # Find the last occurrence of the substring 'old' in the string 's'
    index = s.rfind(old)
    
    # If 'old' is not found, then we simply return the original string
    if index == -1:
        return s

    # the same logic with the replace_nth 
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

    # this will determine which S should we replace (used in replace_nth function)
    pointer = 1

    # loop for each character in the input
    for i in input_string:
        # if reading (
        if i == '[':
            # transform S to (S)S
            stack = replace_nth(stack, "S", "[S]S", pointer)
            res.append("S => " + stack)
        else:
            # we move to the next 'S' 
            pointer += 1

    # delete all S from right to left
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
def build_parse_tree(s):
    class TreeNode:
        def __init__(self, label):
            self.label = label        # Node label (e.g., 'S', '[', ']', 'ε', etc.)
            self.children = []        # List of child nodes for the tree structure

    def helper(sub):
        # Base case: if the substring is empty, return an ε (epsilon) node
        if not sub:
            return TreeNode("ε")

        # If the current substring starts with an opening square bracket
        if sub[0] == '[':
            depth = 0  # Track the bracket depth to find the matching closing bracket

            for i in range(len(sub)):
                if sub[i] == '[': # we increase the depth if we find '['
                    depth += 1
                elif sub[i] == ']': # and decrease if ']'
                    depth -= 1

                # When depth is 0, we've found the matching closing bracket (an occurence of balance)
                if depth == 0:
                    inner = sub[1:i]      # will hold the what's inside the brackets
                    rest = sub[i+1:]      # will hold the remaining string 

                    node = TreeNode("S")  # Create a non-terminal node (S)
                    node.children.append(TreeNode("[")) # Add opening bracket node
                    
                    # Recursively parse inside brackets
                    node.children.append(helper(inner))
                    node.children.append(TreeNode("]")) # Add closing bracket node

                    # parse the remaining string by recursing
                    node.children.append(helper(rest)) 
                    return node

        # If the string doesn't start with '[', or brackets are unmatched
        return TreeNode("INVALID")

    return helper(s) # recurse