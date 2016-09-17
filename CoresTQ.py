gdir = 'c:/users/batagelj/work/python/graph/graph'
wdir = 'c:/users/batagelj/work/python/graph/JSON'
import sys, os, datetime, json
sys.path = [gdir]+sys.path; os.chdir(wdir)
import GraphNew as Graph
import TQ 
G = Graph.Graph.loadNetJSON('ConnectivityTest.json')
# G = Graph.Graph.loadNetJSON('ExampleB.json')
# G = Graph.Graph.loadNetJSON('PathfinderTest.json')
D = { u: G.TQnetDeg(u) for u in G._nodes }
Core = { u: TQ.TQ.setConst(G.getNode(u,'tq'),99) for u in G.nodes() }
Dmin = { u: min([e[2] for e in d]) for u,d in D.items() }
step = 0
while (len(D)>0) and (step<100):
   step += 1
   dmin,u = min( (v,k) for k,v in Dmin.items() )
   pos = [i for i, d in enumerate(D[u]) if d[2] == dmin]
   core = [ D[u][p] for p in pos ]
   TQ.TQ.path()
   Core[u] = TQ.TQ.sum(Core[u],core)
   TQ.TQ.combinatorial()
   change = TQ.TQ.setConst(core,-1)
   D[u] = TQ.TQ.cut(TQ.TQ.sum(D[u],change),dmin)
   for link in G.star(u):
      v = G.twin(u,link)
      if not(v in D): continue
      diff = TQ.TQ.sum(D[v],change); Dv = []
      for e in diff:
          s,t,vd = e
          if vd < dmin:  # <= ?
              TQ.TQ.path(); Core[v] = TQ.TQ.sum(Core[v],[(s,t,dmin)])
              TQ.TQ.combinatorial()
          else: Dv.append(e)
      if len(Dv)>0:
          D[v] = Dv; Dmin[v] = min([e[2] for e in Dv])
      else: del D[v]; del Dmin[v]   
   if len(D[u])==0: del D[u]; del Dmin[u]
   else: Dmin[u] = min([e[2] for e in D[u]])
print("Core =",Core)


