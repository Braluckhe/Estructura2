import pandas as pd
import eel
from Tree import Tree

# Cargar el dataset
data = pd.read_csv("co_properties_final.csv")

# Calcular la métrica price / surface_total y almacenarla en una nueva columna "metric"
data["metric"] = data["price"] / data["surface_total"]

# Crear un árbol AVL
metric = "metric"
second_metric = "surface_covered"
avl_tree = Tree(metric, second_metric)

# Insertar datos en el árbol AVL
for index, row in data.iterrows():
    avl_tree.insert_node(row)

@eel.expose
def search_by_keyword(keyword):
    results = avl_tree.search_tree_by_keyword(keyword)
    print(results)
    eel.renderResults(results)
@eel.expose
def on_windows_close():
    quit()
eel.init('ui')
eel.start('index.html')