import json
import pandas as pd
import eel
from Tree import Tree

# Cargar el dataset
data = pd.read_csv("co_properties_final.csv")

# Calcular la métrica price / surface_total y almacenarla en una nueva columna "metric"
data["metric"] = data["price"] / data["surface_total"]
data["id"] = range(1, len(data) + 1)

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
    eel.renderResults(results)
@eel.expose
def on_windows_close():
    quit()
@eel.expose
def getNodo(num):
    nodo = avl_tree.search_node(num)
    data = nodo.data.to_dict()
    json_string = json.dumps(data)
    eel.renderNode(json_string)
@eel.expose
def getParentescos(nodoID):
    nodo = avl_tree.search_node(nodoID)
    padre = avl_tree.find_parent(nodo) 
    abuelo = avl_tree.find_grandparent(nodo)
    tio = avl_tree.find_uncle(nodo)
    resultados = [padre.data.to_dict(), abuelo.data.to_dict(), tio.data.to_dict()]
    json_string = json.dumps(resultados)
    eel.renderParentescos(json_string)
@eel.expose
def nivelBalance(nodoID):
    nodo = avl_tree.search_node(nodoID)
    nivel = avl_tree.get_level(nodo)
    balance = avl_tree.get_balance_factor(nodo)
    mensaje = "El nivel del nodo es "+str(nivel)+" y el balance es de "+ str(balance)
    eel.renderNivelBalance(mensaje)
eel.init('ui')
eel.start('index.html')