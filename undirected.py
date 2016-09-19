gdir = 'c:/users/batagelj/work/python/graph/graph'
wdir = 'c:/users/batagelj/work/python/graph/JSON'
import sys, os, datetime, json
sys.path = [gdir]+sys.path; os.chdir(wdir)
import GraphNew as Graph
import TQ
fJSON = "simpleViolence.json"
# fJSON = 'instXinstYed.json'
S = Graph.Graph.loadNetJSON(fJSON)
G = S.pairs2edges()
G.saveNetJSON(file='violenceTest.json',indent=1)
# G.saveNetJSON(file='stem.json',indent=1)
