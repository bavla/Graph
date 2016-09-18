gdir = 'c:/users/batagelj/work/python/graph/graph'
wdir = 'c:/users/batagelj/work/python/graph/JSON'
import sys, os, datetime, json
sys.path = [gdir]+sys.path; os.chdir(wdir)
import TQ
G = TQ.TQ.Ianus2Mat('terror50.ten')
TQ.TQ.Ianus2netJSON(G,indent=3)

# G = TQ.TQ.Ianus2Mat('exampleB.ten')
# TQ.TQ.Ianus2netJSON(G) 
# G = TQ.TQ.Ianus2Mat('simpleViolence.ten')
# TQ.TQ.Ianus2netJSON(G)
# G = TQ.TQ.Ianus2Mat('testBetw.ten')
# TQ.TQ.Ianus2netJSON(G) 
# G = TQ.TQ.Ianus2Mat('testConn.ten')
# TQ.TQ.Ianus2netJSON(G)
# G = TQ.TQ.Ianus2Mat('testPF.ten')
# TQ.TQ.Ianus2netJSON(G)
