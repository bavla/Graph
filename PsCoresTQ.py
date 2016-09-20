gdir = 'c:/users/batagelj/work/python/graph/graph'
wdir = 'c:/users/batagelj/work/python/graph/JSON'
import sys, os, datetime, json
sys.path = [gdir]+sys.path; os.chdir(wdir)
import GraphNew as Graph
import TQ
# fJSON = 'ConnectivityWeighted.json'
# fJSON = "violenceE.json"
fJSON = 'stem.json'
# fJSON = 'Terror news 50.json'
# S = Graph.Graph.loadNetJSON(fJSON); G = S.pairs2edges()
# fJSON = 'ConnectivityTest.json'
# fJSON = 'ExampleB.json'
# fJSON = 'PathfinderTest.json'
G = Graph.Graph.loadNetJSON(fJSON)
G.delLoops()
print("Temporal Ps cores in: ",fJSON)
t1 = datetime.datetime.now()
print("started: ",t1.ctime(),"\n")
Tmin,Tmax = G._graph['time']
D = { u: G.TQnetSum(u) for u in G._nodes }
# print("Sum =",D,"\n")
Core = { u: [d for d in D[u] if d[2]==0] for u in G.nodes() }
# core number = 0
D = { u: [d for d in D[u] if d[2]>0] for u in G.nodes() }
D = { u: d for u,d in D.items() if d!=[] }
Dmin = { u: min([e[2] for e in d]) for u,d in D.items() }
step = 0
while len(D)>0:
   step += 1
   dmin,u = min( (v,k) for k,v in Dmin.items() )
   if step % 10 == 1:
      print("{0:3d}. dmin={1:3d}   node={2:4d}".format(step,dmin,u))
   cora = [ d for d in D[u] if d[2] == dmin ]
   cCore = TQ.TQ.complement(Core[u],Tmin,Tmax)
   core = TQ.TQ.extract(cCore,cora)
   if core!=[]:
      Core[u] = TQ.TQ.sum(Core[u],core)
      change = TQ.TQ.minus(core)
      D[u] = TQ.TQ.cutGE(TQ.TQ.sum(D[u],change),dmin) 
      for link in G.star(u):
         v = G.twin(u,link)
         if not(v in D): continue
         chLink = TQ.TQ.minus(TQ.TQ.extract(core,G.getLink(link,'tq')))
         if chLink==[]: continue
         diff = TQ.TQ.cutGE(TQ.TQ.sum(D[v],chLink),0)  
         D[v] = [ (sd,fd,max(vd,dmin)) for sd,fd,vd in diff ]
         if len(D[v])==0: del D[v]; del Dmin[v]
         else: Dmin[v] = min([e[2] for e in D[v]])
   if len(D[u])==0: del D[u]; del Dmin[u]
   else: Dmin[u] = min([e[2] for e in D[u]])
print("{0:3d}. dmin={1:3d}   node={2:4d}".format(step,dmin,u))
# print("\n-----\nCore =",Core)
t2 = datetime.datetime.now()
print("\nfinished: ",t2.ctime(),"\ntime used: ", t2-t1)


