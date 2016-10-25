gdir = 'c:/users/batagelj/work/python/graph/graph'
wdir = 'c:/users/batagelj/work/python/graph/JSON/test'
import sys, os, datetime, json
sys.path = [gdir]+sys.path; os.chdir(wdir)
from GraphNew import Graph
# from copy import deepcopy
import TQ
# file = 'C:/Users/batagelj/work/Python/graph/JSON/test/WAtestInst.json'
file = 'WAtestInst.json'
WA = Graph.loadNetJSON(file)
N = WA.TQnormal()
Cc = N.TQtwo2oneCols()
