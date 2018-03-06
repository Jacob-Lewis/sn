import networkx as nx
import pandas as pd
import numpy as np
import random


def setConfig(hq):

	G=nx.read_edgelist("edges_train_anon.txt")
	labels = "B"
	nx.set_node_attributes(G, labels, 'label')
	converted = "N"
	nx.set_node_attributes(G, converted, 'converted')
	print(G.nodes['4853'])
	print(G.number_of_nodes())

	df = pd.read_table("checkins_train_anon.txt", names = ["id", "time", "x", "y", "nonsense"])
	NY = np.array([40.730610, -73.935242])
	LN = np.array([51.509865, -0.118092])
	Rio = np.array([-22.970722, - 43.182365])

	if hq == "NY":
		hqLoc = NY
	elif hq == "LN":
		hqLoc = LN
	else:
		hqLoc = Rio
	
	labels = {}
	time = {}
	dfPrime = df.drop_duplicates(subset=['id'])
	print(dfPrime.shape)
	for index, row in dfPrime.iterrows():
		loc = [row['x'], row['y']]
		if (np.linalg.norm(loc-hqLoc) <= (10/55)):
			try:
				G.nodes[str(row['id'])]['label'] = "A"
			except:
				pass
		if index % 5000 == 0:
			print(index)
	print("labels: ")
	#Can add time as another attribute if I want
	print(G.nodes['48646']['label'])
	return(G)

def greedy(G):
	seeds = []
	for i in range(100):
		best = nx.degree(G)
		best = sorted(best, key=lambda x: x[1], reverse = True)
		G.remove_node(best[0][0])
		seeds.append(best[0][0])
	return seeds

def propogate(seeds, G):
	errors = 0
	for i in range(len(seeds)):
		try:
			G.nodes[seeds[i]]['converted'] = "Y"
			G = influence(G,seeds[i])		
		except:
			errors += 1
	print(errors)
	return G

def influence(G, seed):
	p = .93
	for node,attr in G[seed].items():
		effect = random.uniform(0, 1)
		if ((G.nodes[node]['label'] == "A") or (effect > p)) and (G.nodes[node]['converted'] == "N"):
			G.nodes[node]['converted'] = "Y"
			G = influence(G, node)
	return G

def main():
	response = input("Input city in short form:")
	G = setConfig(response)
	H = G.copy()
	seeds = greedy(G)
	results = propogate(seeds, H)
	converted = []
	for (p, d) in results.nodes(data=True):
    		if d['converted'] == "Y":
        		converted.append(p)
	print(len(converted))
main()

G = nx.Graph()
G.add_nodes_from([1,2,3,4,5,6,7,8,9,10])
labels = "B"
nx.set_node_attributes(G, labels, 'label')
converted = "N"
nx.set_node_attributes(G, converted, 'converted')
G.add_edges_from([(1,3),(1,4),(1,5),(1,6), (6,2),(6,3),(6,4),(6,5),(2,7),(2,8),(2,9),(2,10)])	
H = G.copy()
demo = [2]
seeds = []
for i in range(10):
	best = nx.degree(G)
	best = sorted(best, key=lambda x: x[1], reverse = True)
	G.remove_node(best[0][0])
	seeds.append(best[0][0])
best = nx.degree(G)
best = sorted(best, key=lambda x: x[1], reverse = True)
seeds = seeds[0:2]
#print(seeds)
#results = propogate(seeds, H)
nodesAt5 = []
#for (p, d) in results.nodes(data=True):
#    if d['converted'] == "Y":
#        nodesAt5.append(p)
#print(nodesAt5)
#Idea: Weight edges to nodes A higher than to nodes B	
#Idea: If nodes are either A or converted, don't count them, otherwise, count them
#Idea: run simulation 100 times each time
print("hello")
