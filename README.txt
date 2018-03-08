Jacob Lewis
JML2309
3/8/18

Data Challenge 1

Total average profit: London: $27977.71
			  NY: $28040.09
			 Rio: $27897.71

For this data challenge, I wrote an algorithm that selects an optimal seed set to influence instagram users with p=.3.

Required python packages: Anaconda, networkx, sys, random, pandas, numpy

I begin by constructing a graph from the edge list provided in the assignment. Once I have built this graph, I create a dataframe that stores all of the checkin data from the second data file provided. I shrink the dataframe by preserving only the first checkin of each user, and then assign a city label to each node with data in the dataframe. I consider only those nodes that have checkin data, and remove all other nodes. Once My graph is prepared, I prompt the user for a city to set as the A label, and and add A labels to all nodes from this city and B nodes to all others. Additionally, each node is given a 'converted' label, which is set to N at the start. This is my graph preparation.

To select seeds, I added some heuristic adaptions to a greedy algorithm. For 100 iterations, my algorithm returns the nodes of the graph and their degree, in descending order. For the 250 nodes of largest degree, I reweight their edges by weighing each edge to a node of label B as 1 and each edge to a node of label A as 3.3. This incorporates the expected value of each connection of each seed node. I called this a reweighted greedy seed set.  

I noticed that the results were not normally distributed as would be expected. There was actually a narrow range of outcomes, between 15500 and 16500, but every 10 or so runs there would be an outcome in the 12000's. This suggests that there are some B nodes that act as gate keepers to another favorably distributed subset of the graph, and if they are converted, that portion of the graph more or less converts, but not otherwise. I wrote an algorithm to identify these nodes that every so often are not converted, and was able to narrow them down based on which nodes showed up in this set every time. Unfortunately, I ran out of time before being able to successfully identify these nodes, but with more time, adding these gatekeeper nodes to the seed set is liable to raise the average profit by about 300. 

Lastly, I noticed that the first few nodes always through an error, regardless of which seeds I removed. I figured out that by changing the maximum recursion depth from 1000 to 15000, my algorithm was able to take advantage of the "celebrity" nodes, that influence thousands of people with their conversion. Hence, by changing the maximum recursion depth from 1000 to 15000, I was able to convert 27977.71 nodes.

Seed set is printed at the start of algorithm after city is selected.
