import math, queue
from collections import Counter

class TreeNode(object):
    # we assume data is a tuple (frequency, character)
    def __init__(self, left=None, right=None, data=None):
        self.left = left
        self.right = right
        self.data = data
    def __lt__(self, other):
        return(self.data < other.data)
    def children(self):
        return((self.left, self.right))
    
def get_frequencies(fname):
    ## This function is done.
    ## Given any file name, this function reads line by line to count the frequency per character. 
    f=open(fname, 'r')
    C = Counter()
    for l in f.readlines():
        C.update(Counter(l))
    return(dict(C.most_common()))

# given a dictionary f mapping characters to frequencies, 
# create a prefix code tree using Huffman's algorithm
def make_huffman_tree(f):
    p = queue.PriorityQueue()
    # construct heap from frequencies, the initial items should be
    # the leaves of the final tree
    for c in f.keys():
        p.put(TreeNode(None,None,(f[c], c)))

    # greedily remove the two nodes x and y with lowest frequency,
    # create a new node z with x and y as children,
    # insert z into the priority queue (using an empty character "")
    while (p.qsize() > 1):
        # TODO
         left_node = p.get()
        right_node = p.get()

        # Create a new internal node with a frequency equal to the sum of the children's frequencies
        new_node = TreeNode(left_node, right_node, (left_node.value[0] + right_node.value[0], ""))

        # Insert the new internal node back into the priority queue
        p.put(new_node)

    # The remaining item in the priority queue is the root of the Huffman tree
    huffman_tree = p.get()
    
        
    # return root of the tree
    return p.get()

# perform a traversal on the prefix code tree to collect all encodings
def get_code(node, prefix="", code={}):
    # TODO - perform a tree traversal and collect encodings for leaves in code
    if node.left is None and node.right is None:
        code[node.value[1]] = prefix
    if node.left:
        get_code(node.left, prefix + "0", code)
    if node.right:
        get_code(node.right, prefix + "1", code)
    return code
# given an alphabet and frequencies, compute the cost of a fixed length encoding
def fixed_length_cost(f):
    # TODO
    fixed_code_length = 8  # You can adjust this to the desired fixed code length in bits
    cost = 0
    for char, freq in f.items():
        cost += fixed_code_length * freq
    return cost

# given a Huffman encoding and character frequencies, compute cost of a Huffman encoding
def huffman_cost(C, f):
    # TODO
    cost = 0
    for char, freq in f.items():
        if char in C:
            code = C[char]
            code_length = len(code)
            cost += code_length * freq
    return cost
    

f = get_frequencies('f1.txt')
print("Fixed-length cost:  %d" % fixed_length_cost(f))
T = make_huffman_tree(f)
C = get_code(T)
print("Huffman cost:  %d" % huffman_cost(C, f))
