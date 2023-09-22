from Node import Node
import graphviz
import json

class Tree:
    def __init__(self, metric, second_metric):
        self.root = None
        self.metric = metric
        self.second_metric = second_metric

    def height(self, node):
        if node is None:
            return 0
        return node.height

    def get_balance(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)

    def rotate_right(self, y):
        if y is None or y.left is None:
            return y

        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = max(self.height(y.left), self.height(y.right)) + 1
        x.height = max(self.height(x.left), self.height(x.right)) + 1

        return x

    def rotate_left(self, x):
        if x is None or x.right is None:
            return x

        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = max(self.height(x.left), self.height(x.right)) + 1
        y.height = max(self.height(y.left), self.height(y.right)) + 1

        return y

    def insert(self, root, data):
        if root is None:
            return Node(data)

        if data[self.metric] < root.data[self.metric]:
            root.left = self.insert(root.left, data)
            root.left.parent = root  # Configura la referencia al padre
        elif data[self.metric] > root.data[self.metric]:
            root.right = self.insert(root.right, data)
            root.right.parent = root
        else:
            if data[self.second_metric] < root.data[self.second_metric]:
                root.left = self.insert(root.left, data)
            else:
                root.right = self.insert(root.right, data)

        root.height = 1 + max(self.height(root.left), self.height(root.right))

        balance = self.get_balance(root)

        if balance > 1:
            if data[self.metric] < root.left.data[self.metric]:
                return self.rotate_right(root)
            else:
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)

        if balance < -1:
            if data[self.metric] > root.right.data[self.metric]:
                return self.rotate_left(root)
            else:
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root)

        return root

    def insert_node(self, data):
        self.root = self.insert(self.root, data)

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, root, key):
        if root is None or root.data[self.metric] == key:
            return root

        if key < root.data[self.metric]:
            return self._search(root.left, key)

        return self._search(root.right, key)

    def print_tree(self):
        self._print_tree(self.root)

    def _print_tree(self, root):
        if root:
            self._print_tree(root.left)
            print(root.data.title)
            self._print_tree(root.right)
    def search_tree_by_keyword(self, keyword):
        list = []
        self._search_tree_by_keyword(self.root, keyword, list)
        json_string = json.dumps(list)
        return json_string

    def _search_tree_by_keyword(self, root, keyword, list):
        if root:
            self._search_tree_by_keyword(root.left, keyword, list)
            if keyword.lower() in root.data.title.lower():
                list.append(root.data.to_dict()) 
            self._search_tree_by_keyword(root.right, keyword, list)
    def search_node(self, id):
        return self._search_node(self.root, id)

    def _search_node(self, node, id):
        if node:
            if node.data.id == id:
                return node
            left_result = self._search_node(node.left, id)
            if left_result:
                return left_result
            return self._search_node(node.right, id)
    def visualize(self, output_file="avl_tree"):
        dot = graphviz.Digraph(format='png', filename=output_file)
        def add_nodes_and_edges(node):
            if node:
                dot.node(str(node.data[self.metric]), label=str(node.data[self.metric]))
                if node.left:
                    dot.edge(str(node.data[self.metric]), str(node.left.data[self.metric]))
                    add_nodes_and_edges(node.left)
                if node.right:
                    dot.edge(str(node.data[self.metric]), str(node.right.data[self.metric]))
                    add_nodes_and_edges(node.right)
        add_nodes_and_edges(self.root)
        dot.render(view=True)    
    def find_parent(self, node):
        if node is None:
            return None  # No hay padre si el nodo es nulo
        return node.parent

    def find_grandparent(self, node):
        if node is None or node.parent is None:
            return None  # No hay abuelo si el nodo o su padre son nulos
        return node.parent.parent
    def find_uncle(self, node):
        parent = self.find_parent(node)
        grandparent = self.find_grandparent(node)

        if parent is None or grandparent is None:
            return None  # No hay tío si no hay padre o abuelo

        if grandparent.left == parent:
            return grandparent.right  # El tío está en el lado derecho del abuelo
        else:
            return grandparent.left  # El tío está en el lado izquierdo del abuelo
    def get_level(self, node):
        if node is None:
            return -1  # El nivel de un nodo nulo es -1
        return 1 + max(self.get_level(node.left), self.get_level(node.right))
    def get_balance_factor(self, node):
        if node is None:
            return 0  # El factor de balanceo de un nodo nulo es 0
        return self.height(node.left) - self.height(node.right)