Jacob Lewis
JML2309

Data Challenge 1

For this data challenge, I wrote an algorithm that selects an optimal seed set to influence instagram users with p=.3.
My algorithm begins by selecting a region to assign label A to, based on user input. Once all the nodes are labeled appropriately, 

With A edge weight = 10, average after 100 for LN was 15831. With weight 3.3, average was 15754. 
I noticed that the results were not normally distributed as would be expected. There was actually a narrow range of outcomes, between 15500 and 16500, but every 10 or so runs there would be an outcome in the 12000's. This suggests that there are some B nodes that act as gate keepers to another favorably distributed subset of the graph, and if they are converted, that portion of the graph more or less converts, but not otherwise. If these nodes could be identified, that would be useful. 

By changing the maximum recursion depth from 1000 to 15000, I was able to convert 27977.71 nodes.
