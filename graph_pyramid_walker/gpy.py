import sys
import os
import random
from random import shuffle

level_to_vertex_map = {}
vertex_to_level_map = {}
vertex_map = {}

# TODO : implement pyramid structures for weighted graphs
def pyramid(vertex_list,edge_dict,pfile,branching_factor=4) :
	if len(vertex_list)== 1:
		level_to_vertex_map[0] = [vertex_list[0],vertex_list[0]]
		vertex_to_level_map[vertex_list[0]] = 0
		return 0
	for edge,weight in edge_dict.items():
		pfile.write(str(edge[0])+" "+str(edge[1])+" " + str(weight) + "\n")

	next_vertex_list = []
	start = vertex_list[-1]
	start = start + 1
	rand_vertex_list = []
	for i in vertex_list:
		rand_vertex_list.append(i)
	shuffle(rand_vertex_list)
	for i in range(0,len(rand_vertex_list),branching_factor):
		next_vertex_list.append(start)
		for j in range(i,i+branching_factor):
			if j>= len(rand_vertex_list):
				break
			pfile.write( str(start)+" "+ str(rand_vertex_list[j])+" 1.0\n")
			vertex_map[rand_vertex_list[j]] = start
		start+=1

	next_edge_dict = {}
	for edge,weight in edge_dict.items():
		# preventing self loops in next layer , since effect of self loops on deep walk is unknown
		t = ( vertex_map[edge[0]],vertex_map[edge[1]] )
		if t[0] == t[1]:
			continue;
		if t not in next_edge_dict.keys():
			next_edge_dict[t] = 1
		else:
			next_edge_dict[t] = next_edge_dict[t] + weight
	level = 1 + pyramid(next_vertex_list,next_edge_dict,pfile,branching_factor)

	level_to_vertex_map[level] = [vertex_list[0],vertex_list[-1]]
	for vertex in vertex_list:
		vertex_to_level_map[vertex] = level
	return level




file = open(sys.argv[1],"r")

vlist = []
edict = {}
for string_temp1 in file.read().strip("\n").split("\n"):
	l = []
	for string_temp2 in string_temp1.split(" "):		
		number = int(string_temp2)
		vlist.append(number)
		l.append(number)
	t = (l[0],l[1])
	edict[t] = 1.0
	edict[(t[1],t[0])] = 1.0

vlist = list(dict.fromkeys(vlist))
pfile = open(sys.argv[1]+".pyramid","w")
pyramid(vlist,edict,pfile,2)
print "Pyramid Generated at " +sys.argv[1]+".pyramid \n"+ "Level view of the pyramid : "
print level_to_vertex_map
print vertex_map
# print vertex_map
# print "\nRunning node2vec on the graph pyramid "+sys.argv[1]+".pyramid\n" 
# str1 = "deepwalk --format edgelist --input ~/Documents/btp/deepwalk-master/example_graphs/"+sys.argv[1]+".pyramid --out out"
# str1 = "./node2vec -i:graph/test1.edgelist.pyramid -o:emb/test1.emb -l:3 -d:24 -p:0.3 -dr -v -w"
# os.system(str1)	



