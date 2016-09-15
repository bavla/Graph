gdir = 'c:/users/batagelj/work/python/graph/graph'
wdir = 'c:/users/batagelj/work/python/graph/JSON'
# indent = None
indent = 3
import sys; sys.path = [gdir]+sys.path; 
import os; os.chdir(wdir)
import datetime, json
import GraphNew as Graph
file='classE.net'
sex ='shapes.clu'
P = Graph.Graph.loadPajek(file)
P.loadPajekClu('sex',sex)
# P.draw(800,800,"#ffa0ff")
# info
n=len(P); mE = len(list(P.edges())); mA = len(list(P.arcs()))
ctime=datetime.datetime.now().ctime()
title="Borrowing of study materials among social informatics students"
meta=[{"date":ctime, "author": "Pajek2JSON"}]
info = {"network": "ClassE", "org": 1,
  "nNodes": n, "nArcs": mA, "nEdges": mE,
  "title": title, "meta": meta, "simple": True, "directed": False,
  "multirel": False, "mode": 1}
# nodes
nodes = []
for node in P.nodes():
  Node = {"id": node, "lab": P.getNode(node,"lab"),
    "x": P.getNode(node,"x"), "y": P.getNode(node,"y"),
    "sex": P.getNode(node,"sex")}      
  nodes.append(Node)  
# links
links = []
for e in P.links():
  link = P.link(e)
  if link[2]: ltype = "arc"
  else: ltype = "edge"
  Link = {"type": ltype, "n1": link[0], "n2": link[1],
    "w": P.getLink(e,'w')}
  links.append(Link)
# JSON
net = {"netJSON": "basic", "info": info, "nodes": nodes, "links": links}
js = open(info['network']+'.json','w')
json.dump(net, js, ensure_ascii=False, indent=indent)
js.close()
