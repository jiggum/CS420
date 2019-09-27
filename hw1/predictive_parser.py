import re

LEFTWARD = False
OPERATOR_PRIORITY = { '+': 1, '-': 1, '*': 2}

def is_operator(token):
    return token in OPERATOR_PRIORITY

def get_operator_priority(token):
    return OPERATOR_PRIORITY[token]

class Node:
    def __init__(self, parent, token, left=None, right=None):
        self.left = left
        self.right = right
        self.parent = parent
        self.token = token

    def set_left(self, left):
        self.left = left
        return self.left

    def set_right(self, right):
        self.right = right
        return self.right

    def is_head(self):
        return self.parent != None and self.parent.token == None

    def set_token(self, token):
        if (not is_operator(token)):
            next_node = Node(self, token)
            if (self.left == None):
                self.left = next_node
                return self.set_left(next_node)
            if (self.right == None):
                return self.set_right(next_node)
            raise ValueError
        else:
            if (not is_operator(self.token)):
                if (self.is_head()):
                    new_head = Node(self.parent, token, self)
                    return self.parent.set_left(new_head)
                return self.parent.flow_up(token)
            else:
                return self.flow_up(token)

    def flow_up(self, token):
        if ((not is_operator(self.token)) or (not is_operator(token))):
            raise ValueError

        if (get_operator_priority(self.token) < get_operator_priority(token)):
            return self.set_right(Node(self, token, left = self.right))
        else:
            if (self.is_head()):
                return self.parent.set_left(Node(self.parent, token, left=self))
            else:
                return self.parent.flow_up(token)

    def print(self, leftward=False):
        left_print = '' if self.left == None else self.left.print(leftward=leftward)
        right_print = '' if self.right == None else self.right.print(leftward=leftward)
        if (leftward):
            return self.token + right_print + left_print
        return self.token + left_print + right_print

    def is_valid(self):
        if (self.left == None and self.right == None):
            return True
        if (self.left != None and self.right != None):
            return self.left.is_valid() and self.right.is_valid()
        return False

class ParsingTree:
    def __init__(self):
        self.root = Node(None, None)
        self.last_node = self.root

    def get_head(self):
        return self.root.left

    def set_head(self, token):
        return self.root.set_left(Node(self.root, token, left=self.get_head()))

    def append_token(self, token):
        if self.get_head() == None:
            self.last_node = self.set_head(token)
        else:
            self.last_node = self.last_node.set_token(token)

    def print(self, leftward=False):
        if (not self.is_valid()):
            return 'incorrect syntax'
        return self.get_head().print(leftward=leftward)

    def is_valid(self):
        if self.get_head() == None:
            return False
        return self.get_head().is_valid()

def tokenizer(str):
    return re.findall(r'([a-z]|[0-9]+|[*+-])', str)

def main():
    f_r = open("input.txt", 'r')
    f_w = open("output.txt", 'w')
    inputs = f_r.readlines()
    f_r.close()

    for line in inputs:
        input = line.strip()
        parser = ParsingTree()
        tokens = tokenizer(input)
        if LEFTWARD:
            tokens.reverse()
        for token in tokens:
            parser.append_token(token)
        f_w.write(parser.print(leftward=LEFTWARD)+'\n')

    f_w.close()

if __name__ == "__main__":
    main()
