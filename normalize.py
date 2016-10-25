gdir = 'c:/users/batagelj/work/python/graph/graph'
# wdir = 'c:/users/batagelj/work/python/graph/JSON/test'
wdir = 'c:/users/batagelj/work/python/graph/JSON/SN5'
import sys, os, datetime, json
sys.path = [gdir]+sys.path; os.chdir(wdir)
from GraphNew import Graph
# from copy import deepcopy
import TQ
# file = 'WAtestInst.json'
# file = 'WAtestCum.json'
file = 'WAcCum.json'
t1 = datetime.datetime.now()
print("started: ",t1.ctime(),"\n")
WA = Graph.loadNetJSON(file)
t2 = datetime.datetime.now()
print("\nloaded: ",t2.ctime(),"\ntime used: ", t2-t1)
N = WA.TQnormal()
t3 = datetime.datetime.now()
print("\nnormalized: ",t3.ctime(),"\ntime used: ", t3-t2)
# Cc = N.TQtwo2oneCols(lType='arc')
Cc = N.TQtwo2oneCols()
t4 = datetime.datetime.now()
print("\nnormalized collaboration: ",t4.ctime(),"\ntime used: ", t4-t3)
# fjson = 'CcITest.json'
# fjson = 'CcCtest.json'
fjson = 'CcCSN5.json'
Cc.saveNetJSON(fjson,indent=2)
t5 = datetime.datetime.now()
print("\nsave to file: ",t5.ctime(),"\ntime used: ", t5-t4)
