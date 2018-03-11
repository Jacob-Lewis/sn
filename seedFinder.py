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
	for i in range(len(seeds)):
		G.nodes[seeds[i]]['converted'] = "Y"
		G = influence(G,seeds[i])		
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
	sys.setrecursionlimit(15000)
	print("New system recursion limit: " + str(sys.getrecursionlimit()))

	print("Short forms (case sensitive) are: NY, LN, Rio")
	response = input("Input city in short form:")
	
	"""
	#The below code is for creating the proper files
	if response == "NY":
		fileName = "NewYork"
	elif response == "LN":
		fileName = "London"
	elif response == "Rio":
		fileName = "Rio"
	else: 
		print("You did not input a valid input. Please input the city according to the directions above. Thank you.")
		sys.exit()
	"""
	G = setConfig(response)
	H = G.copy()
	seeds = greedyAWeigthed(G)
	
	"""
	#As is this code
	fileName = fileName + '.txt'
	with open(fileName, 'a') as out_file:
		for item in seeds:
 			 out_file.write("%s\n" % item)
	"""
	success = 0
	for i in range(100):
		J = H.copy()
		results = propogate(seeds, J)
		converted = []
		for (p, d) in results.nodes(data=True):
    			if d['converted'] == "Y":
        			converted.append(p)
		success += (len(converted) - 100)
		print("profit in iteration " + str(i) + ": " + str(len(converted)))
	print("average profit: " + str(success/100))

main()




