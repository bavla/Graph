gdir = 'c:/users/batagelj/work/python/graph/graph'
wdir = 'c:/users/batagelj/work/python/graph/JSON'
import sys, os, datetime, json
sys.path = [gdir]+sys.path; os.chdir(wdir)
import TQ
G = TQ.TQ.Ianus2Mat('IITy.ten')
# G = TQ.TQ.Ianus2Mat('terror50.ten')
# G = TQ.TQ.Ianus2Mat('exampleB.ten')
# G = TQ.TQ.Ianus2Mat('simpleViolence.ten')
# G = TQ.TQ.Ianus2Mat('testBetw.ten')
# G = TQ.TQ.Ianus2Mat('testConn.ten')
# G = TQ.TQ.Ianus2Mat('testPF.ten')
# TQ.TQ.Ianus2netJSON(G) 
TQ.TQ.Ianus2netJSON(G,indent=3)
