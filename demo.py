import networkx as nx
import pandas as pd
import numpy as np
import random
import sys

def setConfig(hq):

	G=nx.read_edgelist("edges_train_anon.txt")
	labels = "B"
	nx.set_node_attributes(G, labels, 'label')
	converted = "N"
	nx.set_node_attributes(G, converted, 'converted')

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
	for index, row in dfPrime.iterrows():
		loc = [row['x'], row['y']]
		if (np.linalg.norm(loc-hqLoc) <= (10/55)):
			try:
				G.nodes[str(row['id'])]['label'] = "A"
			except:
				pass
	#Can add time as another attribute if I want
	return(G)

def greedy(G):
	seeds = []
	for i in range(100):
		best = nx.degree(G)
		best = sorted(best, key=lambda x: x[1], reverse = True)
		G.remove_node(best[0][0])
		seeds.append(best[0][0])
	return seeds

def greedyAWeigthed(G):
	seeds = []
	#weird = ['42015', '39034', '21095', '16151', '33538']
	#G.remove_nodes_from(weird)
	for i in range(100):
		best = nx.degree(G)
		best = sorted(best, key=lambda x: x[1], reverse = True)
		best = best[0:250]
		for j in range(len(best)):
			for node,attr in G[str(best[j][0])].items():
				if G.nodes[node]['label'] == "A":
					best[j] = list(best[j])
					best[j][1] += 3.3
		best = sorted(best, key=lambda x: x[1], reverse = True)
		G.remove_node(best[0][0])
		seeds.append(best[0][0])
	return seeds

def propogate(seeds, G):
	errors = 0
	for i in range(len(seeds)):
#		try:
		G.nodes[seeds[i]]['converted'] = "Y"
		G = influence(G,seeds[i])		
#		except:
#			print(seeds[i])			
#			errors += 1
	print(errors)
	return G

def influence(G, seed):
	p = .3
	for node,attr in G[seed].items():
		effect = random.uniform(0, 1)
		if ((G.nodes[node]['label'] == "A") or (effect > p)) and (G.nodes[node]['converted'] == "N"):
			G.nodes[node]['converted'] = "Y"
			G = influence(G, node)
	return G

def main():
	sys.setrecursionlimit(3000)
	print("Short forms (case sensitive) are: NY, LN, Rio")
	response = input("Input city in short form:")
	G = setConfig(response)
	H = G.copy()
	seeds = greedyAWeigthed(G)
	#seeds = greedy(G)
	success = 0
	#This is to try and identify nodes that cause abberations
	setSeeds = set()
	badSeeds = set()
	bonusB = set()
	potents = set()
	for i in range(100):
		J = H.copy()
		results = propogate(seeds, J)
		converted = []
		for (p, d) in results.nodes(data=True):
    			if d['converted'] == "Y":
        			converted.append(p)
		success += (len(converted) - 100)
		print(len(converted))
	print(success/100)

	#Everything below this is to try and identify nodes that cause abberations
	"""
		if len(converted)>15000:
			setSeeds.update(converted)
		else:
			badSeeds.update(converted)
	bonusNodes = (setSeeds - badSeeds)
	for node in bonusNodes:
		if H.nodes[node]['label'] == "B":
			bonusB.add(node)
	potents = bonusB
	for i in range(100):
		J = H.copy()
		results = propogate(seeds, J)
		converted = []
		for (p, d) in results.nodes(data=True):
			if d['converted'] == "Y":
				converted.append(p)
		if len(converted)>15000:
			potents = potents.intersection(converted)
		print(len(potents))
	print(potents)
	"""
main()





#For testing on small graph
G = nx.Graph()
G.add_nodes_from([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
labels = "B"
nx.set_node_attributes(G, labels, 'label')
converted = "N"
nx.set_node_attributes(G, converted, 'converted')
G.add_edges_from([(1,3),(1,4),(1,5),(1,6), (6,2),(6,3),(6,4),(6,5),(2,7),(2,8),(2,9),(2,10),(3,11),(7,14),(15,14),(17,4),(19,17),(18,20),(20,13),(13,8)])	
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
results = propogate(seeds, H)
nodesAt5 = []
for (p, d) in results.nodes(data=True):
	if d['converted'] == "Y":
		nodesAt5.append(p)
#print(nodesAt5)
#Idea: Weight edges to nodes A higher than to nodes B	
#Idea: If nodes are either A or converted, don't count them, otherwise, count them
#Idea: run simulation 100 times each time
#Fix errors?
print("hello")
