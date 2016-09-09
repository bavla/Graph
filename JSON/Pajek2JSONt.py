gdir = 'c:/users/batagelj/work/python/graph/graph'
wdir = 'c:/users/batagelj/work/python/graph/JSON'
# indent = None
indent = 3
import sys, os, datetime, json
sys.path = [gdir]+sys.path; os.chdir(wdir)
import GraphNew as Graph
file='violenceM.net'
P = Graph.Graph.loadPajek(file)
# info
n=len(P); mE = len(list(P.edges())); mA = len(list(P.arcs()))
ctime=datetime.datetime.now().ctime()
title="Franzosi's violence network"
meta=[{"date":ctime, "author": "Pajek2JSON"}]
meta.append(P.getGraph('meta'))
info = {"network": "violenceM", "org": 1, "nNodes": n, 
  "nArcs": mA, "nEdges": mE, "title": title, "meta": meta}
# nodes
nodes = []
for node in P.nodes():
  Node = {"id": node, "lab": P.getNode(node,"lab"), "tq": P.getNode(node,"tq")}
  nodes.append(Node)  
# links
links = []
for e in P.links():
  link = P.link(e); ltype = "arc" if link[2] else "edge"
  Link = {"type": ltype, "n1": link[0], "n2": link[1],
    "rel": link[3], "tq": P.getLink(e,'tq')}
  links.append(Link)
# JSON
net = {"netJSON": "basic", "info": info, "nodes": nodes, "links": links}
js = open(info['network']+'.json','w')
json.dump(net, js, ensure_ascii=False, indent=indent)
js.close()
