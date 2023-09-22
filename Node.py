class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1
        self.parent = None  # Agrega esta referencia al padre

