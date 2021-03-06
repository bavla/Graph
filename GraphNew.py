# -*- coding: UTF-8 -*-

# Graph
# network analysis package
# by Batagelj, V.: 12. September 2010
# last change: 12. January 2014
# last change: 29. August 2016

import re, sys, os, json, TQ, datetime, platform
import turtle as t
import webbrowser
from math import *
from random import random, randint, shuffle
from itertools import chain
from warnings import warn
from search import Search
from coloring import Coloring
from copy import copy, deepcopy

# http://www.w3schools.com/html/html_colornames.asp

class Graph(Search,Coloring):
    class graphError(RuntimeError): pass

    Colors = ['White','Black','Red','Blue','Green','Magenta','Cyan',
        'Yellow', 'Brown', 'Orange', 'Lime', 'Pink', 'Purple', 'Orchid',
        'Salmon', 'SeaGreen']
    INFTY = 1e10

    @staticmethod
    def location():
        return [platform.uname()[1], os.getcwd()]
    @staticmethod
    def turtleXY(T):
        return ((T[0]-0.5)*t.window_width(),(T[1]-0.5)*t.window_height())
    @staticmethod
    def extractTQ(s):
        l = s.find('['); r = s.rfind(']')
        S = s[l+1:r].split(','); tq = []
        for e in S:
            L = e.split('-'); t1 = eval(L[0])
            if len(L)>1: t2 = 999999999 if '*' in L[1] else eval(L[1])+1
            else: t2 = t1+1
            tq.append([t1,t2,1])
        return tq
    def initNode(self,e): return self._links[e][0]
    def termNode(self,e): return self._links[e][1]
    def twin(self,u,e):
        S={self.initNode(e),self.termNode(e)}
        if not (u in S):
            warn("Node {0} not on link {1}".format(u,e))
            return None
        elif len(S)==1: return u
        else: return (S-{u}).pop()
    def __init__(self,simple=False,mode=1,multirel=False,temporal=False,
        network="test",title="Test",):
        self._linkId = 0
        self._graph = {'simple': simple,'mode': mode,'multirel':multirel,
            'temporal':temporal,'network':network,'title':title,'meta':[],
            'legends':{}}
        self._graph['required'] = {"nodes":['id','mode','lab'],
            'links':['n1', 'n2', 'type']}                       
        self._nodes = {}
        self._links = {}
    def __Str__(self): return "Graph:\nNodes: "+ \
        str(list(self.nodes()))+"\nLinks: "+ \
        str([("A" if self._links[e][2] else "E")+str(e)+ \
        str((self.initNode(e),self.termNode(e))) for e in self.links()])
    def __len__(self): return len(self._nodes)
    def nodes(self):
        for u in self._nodes.keys(): yield u
    def nodesMode(self,mode):
        for u in self._nodes.keys():
            if 'mode' in self._nodes[u][3].keys():
                if self._nodes[u][3]['mode'] == mode: yield u
            elif mode == 1: yield u
    def links(self):
        for e in self._links.keys(): yield e
    def edges(self):
        for e in self._links.keys():
            if not self._links[e][2]: yield e
    def arcs(self):
        for a in self._links.keys():
            if self._links[a][2]: yield a
    def link(self,e): return self._links[e]
    def addNode(self,u,mode=1):
        if (not u in self._nodes):
            self._nodes[u] = [{},{},{},{}]
            if self._graph['mode'] > 1:
                self._nodes[u][3]['mode'] = mode
        else: raise self.graphError(
            "Node {0} already defined".format(u))
    def addEdge(self,u,v,w={},rel=None,lid=None):
        p,q = (u,v) if u < v else (v,u)
        linked = q in self._nodes[p][0]
        if not linked:
            if lid == None:
                self._linkId += 1; lid = self._linkId
            self._nodes[p][0][q] = [lid]
            self._nodes[q][0][p] = [lid]
            self._links[lid] = [p,q,False,rel,w]
        elif not self._graph['simple']:
            if lid == None:
                self._linkId += 1; lid = self._linkId
            self._nodes[p][0][q].append(lid)
            self._nodes[q][0][p].append(lid)
            self._links[lid] = [p,q,False,rel,w]
        else: raise self.graphError(
            "Link {0} already defined".format((u,v)))
        return lid
    def addArc(self,u,v,w={},rel=None,lid=None):
        linked = v in self._nodes[u][2]
        if not linked:
            if lid == None:
                self._linkId += 1; lid = self._linkId            
            self._nodes[u][2][v] = [lid]
            self._nodes[v][1][u] = [lid]
            self._links[lid] = [u,v,True,rel,w]
        elif not self._graph['simple']:
            if lid == None:
                self._linkId += 1; lid = self._linkId            
            self._nodes[u][2][v].append(lid)
            self._nodes[v][1][u].append(lid)
            self._links[lid] = [u,v,True,rel,w]
        else: raise self.graphError(
            "Link {0} already defined".format((u,v)))
        return lid
    def neighbors(self,u):
        return (set(self._nodes[u][0].keys()) |
                set(self._nodes[u][1].keys()) |
                set(self._nodes[u][2].keys()))
    def edgeNeighbors(self,u):
        return set(self._nodes[u][0].keys())
    def inArcNeighbors(self,u):
        return set(self._nodes[u][1].keys())
    def outArcNeighbors(self,u):
        return set(self._nodes[u][2].keys())
    def inNeighbors(self,u):
        return (set(self._nodes[u][0].keys()) |
                set(self._nodes[u][1].keys()))
    def outNeighbors(self,u):
        return (set(self._nodes[u][0].keys()) |
                set(self._nodes[u][2].keys()))
    def edgeStar(self,u):
        for L in self._nodes[u][0].values():
            for edge in L: yield edge
    def inArcStar(self,u):
        for L in self._nodes[u][1].values():
            for arc in L: yield arc
    def outArcStar(self,u):
        for L in self._nodes[u][2].values():
            for arc in L: yield arc
    def star(self,u):
        return chain(self.edgeStar(u),self.inArcStar(u),self.outArcStar(u))
    def inStar(self,u):
        return chain(self.edgeStar(u),self.inArcStar(u))
    def outStar(self,u):
        return chain(self.edgeStar(u),self.outArcStar(u))
    def __iter__(self):
        for v in self._nodes.keys(): yield v
    def delLink(self,e):
        u,v,directed,*r = self._links[e]
        if directed:
            self._nodes[u][2][v].remove(e); self._nodes[v][1][u].remove(e)
        else:
            self._nodes[u][0][v].remove(e); self._nodes[v][0][u].remove(e)
        del(self._links[e])
    def delNode(self,u):
        for e in self.star(u): self.delLink(e)
        del(self._nodes[u])
    def delLoops(self):
        for u in self._nodes:
            ed, ia, oa, np = self._nodes[u]
            le = ed.pop(u,None); li = ia.pop(u,None); lo = oa.pop(u,None)
            self._nodes[u] = [ed, ia, oa, np]
    def setGraph(self,key,val): self._graph[key] = val
    def getGraph(self,key): return self._graph[key]
    def setNode(self,u,key,val): self._nodes[u][3][key] = val
    def setNodes(self,key,val):
        for u in self._nodes.keys(): self._nodes[u][3][key] = val
    def getNode(self,u,key):
        return self._nodes[u][3][key] if key in self._nodes[u][3] else None
    def setLink(self,e,key,val): self._links[e][4][key] = val
    def getLink(self,e,key):
        return self._links[e][4][key] if key in self._links[e][4] else None
    def degree(self,u): return len(list(self.star(u)))
    def inDegree(self,u): return len(list(self.inStar(u)))
    def outDegree(self,u): return len(list(self.outNeighbors(u)))
    def pairs2edges(self):
        S = Graph()
        S._graph = deepcopy(self._graph)
        for u in self._nodes:
            ed,ia,oa,pr = self._nodes[u]
            S._nodes[u] = [{},{},{},pr]
        for p in self._links:
            u,v,d,r,w = self._links[p]
            if u<=v: lid=S.addEdge(u,v,w=w)       
        return S
    def reverse(self):
        R = Graph()
        R._graph = copy(self._graph)
        for v in self._nodes.keys():
            R._nodes[v] = [ dict(self._nodes[v][0]),
                dict(self._nodes[v][2]),dict(self._nodes[v][1]),
                dict(self._nodes[v][3]) ]
        for e in self._links.keys(): R._links[e] = dict(self._links[e])
        return R
    def transpose(self):
        if self._graph['mode'] == 1: return self.reverse()
        T = Graph()
        nr, nc = self._graph['dim']
        T._graph = deepcopy(self._graph)
        for v in self._nodes.keys():
            if self._nodes[v][3]['mode']==1:
                t = v+nc; mode = 2
            else: t = v-nr; mode = 1
            T.addNode(t)
            T._nodes[t][3] = dict(self._nodes[v][3])
            T._nodes[t][3]['mode'] = mode
        for p in self._links.keys():
            u,v,directed,r,w = self._links[p]
            if directed: T.addArc(v-nr,u+nc,w,r,lid=p)
            else: T.addEdge(v-nr,u+nc,w,r,lid=p)
        T._graph['dim'] = [nc,nr]
        return T
    def one2twoMode(self):
        T = Graph(); n = len(self._nodes)
        T._graph = copy(self._graph); T._graph['mode'] = 2
        for v in self._nodes.keys():
            T.addNode(v); T.addNode(v+n)
            T._nodes[v][3] = dict(self._nodes[v][3])
            T._nodes[v][3]['mode'] = 1
            T._nodes[v+n][3] = dict(self._nodes[v][3])
            T._nodes[v+n][3]['mode'] = 2
        for p in self._links.keys():
            u,v,k = p; q = (u,v+n,k)
            if k < 0: T.addArc(u,v+n,-k)
            else: T.addEdge(u,v+n,k)
            T._links[q] = dict(self._links[p])
        return T
    def two2oneEq(self,noDup=True):
        n1 = len(list(self.nodesMode(1)))
        n2 = len(list(self.nodesMode(2)))
        if n1 != n2: raise Graph.graphError(
            "Nonsquare two-mode network {0} != {1}".format(n1,n2))
        G = Graph()
        G._graph = copy(self._graph); G._graph['mode'] = 1
        for v in self.nodesMode(1):
            G.addNode(v); G._nodes[v][3] = dict(self._nodes[v][3])
            del(G._nodes[v][3]['mode'])
        for p in self._links.keys():
            u,v,k = p
            q = (u,v-n1,k) if (k < 0) or (u < v-n1) else (v-n1,u,k)
            u,v,k = q; add = True
#            print('p =',p,' q =',q)
            if k < 0: G.addArc(u,v,-k)
            elif not((q in G._links) and noDup): G.addEdge(u,v,k)
            else: add = False
            if add:
                G._links[q] = dict(self._links[p])
#                print('p =',p,' q =',q,self._links[p])
        return G
    def two2oneRows(self,key='w'):
        nr,nc = self._graph['dim']
        G = Graph(); G._graph['mode'] = 1; G._graph['nNodes'] = nr
        for v in self.nodesMode(1):
            G.addNode(v,1); G._nodes[v][3] = dict(self._nodes[v][3])
#            del(G._nodes[v][3]['mode'])
        for t in self.nodesMode(2):
            for p in self.inStar(t):
                u = self.twin(t,p); pw = self._links[p][4][key]
                for q in self.inStar(t):
                    v = self.twin(t,q); r = (u,v)
                    if not r in G._links: G._links[r] = [ u,v,True,None,{key:0} ]
                    G._links[r][4][key] += pw*self._links[q][4][key]
        return G
    def two2oneCols(self, key='w'):
        nr,nc = self._graph['dim']
        G = Graph(); G._graph['mode'] = 2; G._graph['nNodes'] = nc
        for v in range(nc):
            C.addNode(v+1,1); C._nodes[v+1][3] = dict(self._nodes[nr+v+1][3])
#            del(G._nodes[v-nr][3]['mode'])
        for t in self.nodesMode(1):
            for p in self.outStar(t):
                u = self.twin(t,p)-nr; pw = self._links[p][4][key]
                for q in self.outStar(t):
                    v = self.twin(t,q)-nr; r = (u,v)
                    if not r in G._links: G._links[r] = [ u,v,True,None,{key:0} ]
                    G._links[r][4][key] += pw*self._links[q][4][key]
        return G
    def multiply(A,B,key='w',oneMode=False):
        nar,nac = A._graph['dim']; nbr,nbc = B._graph['dim']
        if nac != nbr: raise Graph.graphError(
            "Noncompatible networks {0} != {1}".format(nac,nbr))
        if oneMode and (nar != nbc): raise Graph.graphError(
            "Product is not a one-mode network {0} != {1}".format(nar,nbc))
        C = Graph(); C._graph['mode'] = 2; C._graph['dim'] = [nar,nbc]
        for v in range(nar):
            C.addNode(v+1,1); C._nodes[v+1][3] = dict(A._nodes[v+1][3])
        if not oneMode:
            for v in range(nar,nar+nbc):
                C.addNode(v+1,2)
                C._nodes[v+1][3] = dict(B._nodes[v+1+nbr-nar][3])
        for t in A.nodesMode(2):
            for p in A.inStar(t):
                u = A.twin(t,p); Apw = A._links[p][4][key]
                for q in B.outStar(t-nar):
                    v = B.twin(t-nar,q)-nbr
                    if not oneMode: v = v+nar
                    r = (u,v)
                    if not r in C._links: C._links[r] = \
                       [ u, v, True, None, {key: 0} ]
                    C._links[r][4][key] += Apw*B._links[q][4][key]
        return C
    def TQnormal(self,key='tq'):
        N = deepcopy(self)
        for u in N.nodesMode(1):
            qu = TQ.TQ.invert(N.TQnetOutDeg(u),vZero=1)
            for p in N.outStar(u):
                N._links[p][4][key] = TQ.TQ.prod(qu,N._links[p][4][key])
        return N
    def TQtwo2oneRows(self,lType='edge',key='tq'):
        nr,nc = self._graph['dim']
        C = Graph(); C._graph['mode'] = 1; C._graph['nNodes'] = nr
        C._graph['temporal'] = True; C._graph['simple'] = True
        C._graph['network'] = self._graph['network']+'ROWS'
        C._graph['title'] = 'ROWS of '+self._graph['title']
        C._graph['time'] = self._graph['time']
        if 'legends' in self._graph: C._graph['legends']['Tlabs'] = \
            self._graph['legends']['Tlabs']
        C._graph['meta'] = self._graph['meta']
        C._graph['required'] = self._graph['required']
        C._graph['multirel'] = self._graph['multirel']
        for v in range(nr):
            C.addNode(v+1,1); C._nodes[v+1][3] = dict(self._nodes[v+1][3])
            C._nodes[v+1][3]['mode'] = 1
        for t in self.nodesMode(2):
            for p in self.inStar(t):
                u = self.twin(t,p); Apw = self._links[p][4][key]
                for q in self.inStar(t):
                    v = self.twin(t,q)
                    if u<=v:
                        s = TQ.TQ.prod(Apw,self._links[q][4][key])
                        if s==[]: continue
                        r = (u,v)
                        if (lType=='edge') or (lType=='double'):
                            if not r in C._links:
                                C.addEdge(u,v,lid=r,w={key: []})
                            if (u!=v) and (lType=='double'): s = TQ.TQ.sum(s,s)
                            C._links[r][4][key] = TQ.TQ.sum(C._links[r][4][key],s)
                        else:
                            if not r in C._links:
                                C.addArc(u,v,lid=r,w={key: []})
                            C._links[r][4][key] = TQ.TQ.sum(C._links[r][4][key],s)
                            if u!=v:
                                rr = (v,u)
                                if not rr in C._links:
                                    C.addArc(v,u,lid=rr,w={key: []})
                                C._links[rr][4][key] = C._links[r][4][key] 
        return C
    def TQtwo2oneCols(self,lType='edge',key='tq'):
        nr,nc = self._graph['dim']
        C = Graph(); C._graph['mode'] = 1; C._graph['nNodes'] = nc
        C._graph['temporal'] = True; C._graph['simple'] = True
        C._graph['network'] = self._graph['network']+'COLS'
        C._graph['title'] = 'COLS of '+self._graph['title']
        C._graph['time'] = self._graph['time']
        if 'legends' in self._graph: C._graph['legends']['Tlabs'] = \
            self._graph['legends']['Tlabs']
        C._graph['meta'] = self._graph['meta']
        C._graph['required'] = self._graph['required']
        C._graph['multirel'] = self._graph['multirel']
        for v in range(nc):
            C.addNode(v+1,1); C._nodes[v+1][3] = dict(self._nodes[nr+v+1][3])
            C._nodes[v+1][3]['mode'] = 1
        for t in self.nodesMode(1):
            for p in self.outStar(t):
                u = self.twin(t,p)-nr; Apw = self._links[p][4][key]
                for q in self.outStar(t):
                    v = self.twin(t,q)-nr
                    if u<=v:
                        s = TQ.TQ.prod(Apw,self._links[q][4][key])
                        if s==[]: continue
                        r = (u,v)
                        if (lType=='edge') or (lType=='double'):
                            if not r in C._links:
                                C.addEdge(u,v,lid=r,w={key: []})
                            if (u!=v) and (lType=='double'): s = TQ.TQ.sum(s,s)
                            C._links[r][4][key] = TQ.TQ.sum(C._links[r][4][key],s)
                        else:
                            if not r in C._links:
                                C.addArc(u,v,lid=r,w={key: []})
                            C._links[r][4][key] = TQ.TQ.sum(C._links[r][4][key],s)
                            if u!=v:
                                rr = (v,u)
                                if not rr in C._links:
                                    C.addArc(v,u,lid=rr,w={key: []})
                                C._links[rr][4][key] = C._links[r][4][key] 
        return C
    def TQmultiply(A,B,oneMode=False,keyA='tq',keyB='tq'):
        nar,nac = A._graph['dim']; nbr,nbc = B._graph['dim']
        if nac != nbr: raise Graph.graphError(
            "Noncompatible networks {0} != {1}".format(nac,nbr))
        if oneMode and (nar != nbc): raise Graph.graphError(
            "Product is not a one-mode network {0} != {1}".format(nar,nbc))
        C = Graph(); C._graph['mode'] = 2; C._graph['dim'] = [nar,nbc]
        C._graph['temporal'] = True; C._graph['simple'] = True
        C._graph['network'] = A._graph['network']+'X'+B._graph['network']
        C._graph['title'] = 'PROD of '+A._graph['title']+' + '+B._graph['title']
        C._graph['time'] = A._graph['time']
        if 'legends' in A._graph: C._graph['legends']['Tlabs'] = \
            A._graph['legends']['Tlabs']
        C._graph['meta'] = A._graph['meta']
        C._graph['required'] = A._graph['required']
        C._graph['multirel'] = A._graph['multirel']
        C._graph['mode'] = 1 if oneMode else 2
        C._graph['nNodes'] = nar if oneMode else nar+nbc 
        for v in range(nar):
            C.addNode(v+1,1); C._nodes[v+1][3] = dict(A._nodes[v+1][3])
        if not oneMode:
            for v in range(nar,nar+nbc):
                C.addNode(v+1,2)
                C._nodes[v+1][3] = dict(B._nodes[v+1+nbr-nar][3])
        for t in A.nodesMode(2):
            for p in A.inStar(t):
                u = A.twin(t,p); Apw = A._links[p][4][keyA]
                for q in B.outStar(t-nar):
                    s = TQ.TQ.prod(Apw,B._links[q][4][keyB])
                    if s==[]: continue
                    v = B.twin(t-nar,q)-nbr
                    if not oneMode: v = v+nar
                    r = (u,v)
                    if not r in C._links: C.addArc(u,v,lid=r,w={'tq':[]})
                    C._links[r][4]['tq'] = TQ.TQ.sum(C._links[r][4]['tq'],s)
        return C
    def TQactivity(self,Rows,Cols):
        s = []
        for u in Rows:
            for p in self.outStar(u):
                v = self.twin(u,p)
                if v in Cols: s = TQ.TQ.sum(s,self.getLink(p,'tq'))
        return(s)
    def TQnetDeg(self,u,key='tq'):
        deg = TQ.TQ.setConst(self._nodes[u][3]['act'],0)
        for p in self.star(u):
            deg = TQ.TQ.sum(deg,TQ.TQ.binary(self._links[p][4][key]))
        return deg
    def TQnetInDeg(self,u,key='tq'):
        deg = TQ.TQ.setConst(self._nodes[u][3]['act'],0)
        for p in self.inStar(u):
            deg = TQ.TQ.sum(deg,TQ.TQ.binary(self._links[p][4][key]))
        return deg
    def TQnetOutDeg(self,u,key='tq'):
        deg = TQ.TQ.setConst(self._nodes[u][3]['act'],0)
        for p in self.outStar(u):
            deg = TQ.TQ.sum(deg,TQ.TQ.binary(self._links[p][4][key]))
        return deg    
    def TQnetSum(self,u,key='tq'):
        s = TQ.TQ.setConst(self._nodes[u][3]['act'],0)
        for p in self.star(u):
            s = TQ.TQ.sum(s,self._links[p][4][key])
        return s
    def TQnetInSum(self,u,key='tq'):
        s = TQ.TQ.setConst(self._nodes[u][3]['act'],0)
        for p in self.inStar(u):
            s = TQ.TQ.sum(s,self._links[p][4][key])
        return s
    def TQnetOutSum(self,u,key='tq'):
        s = TQ.TQ.setConst(self._nodes[u][3]['act'],0)
        for p in self.outStar(u):
            s = TQ.TQ.sum(s,self._links[p][4][key])
        return s    
    def TQnetBin(self,key='tq'):
        B = deepcopy(self)
        for p in B._links:
            B._links[p][4][key] = TQ.TQ.binary(B._links[p][4][key])
        return B  
    def TQgraph2mat(self):
        onemode = self._graph['mode'] == 1
        if onemode:
            rows = self._nodes.keys(); cols = self._nodes.keys()
        else:
            rows = self.nodesMode(1); cols = self.nodesMode(2)
        nr = len(list(rows)); nc = len(list(cols))
        B = [[[] for v in range(nr)] for u in range(nc)]
        for p in self._links.keys():
            u = self._links[p][0]-1; v = self._links[p][1]-1
            if not onemode: v = v - nr
            B[u][v] = TQ.TQ.sum(B[u][v],self._links[p][4]['tq'])
            if onemode and not self._links[p][2]: B[v][u] = B[u][v]
        return B
    def Index(self): return { v[3]['lab']: k for k,v in self._nodes.items() }
    def TQgetLinkValue(self,i,lu,lv): return self._links[(i[lu],i[lv])][4]['tq']          
    def loadPajek(file):
        try: net = open(file,'r')
        except: raise Graph.graphError(
            "Problems with Pajek file {0}".format(file))
        G = Graph(); mode = 1; status = 0; meta = ''; rels = {}
        simple = False; temporal = False; multirel = False
        while True:
            line = net.readline()
            if not line: break
            if line[0] == '%':
                meta += line[1:]; continue
            if line[0] == '*':
                L = re.split('\s+',line.strip())
                control = L[0].lower()
                if control=='*vertices':
                    num = eval(L[1])
                    twoMode = len(L)>2
                    if twoMode:
                       G._graph['mode'] = 2
                       num1 = eval(L[2]); mode = 1
                       for v in range(num):
                           if v==num1: mode = 2
                           G.addNode(v+1,mode)
                       nr = num1; nc = num - num1
                    else:
                       for v in range(num): G.addNode(v+1)
                    status = 1; continue
                elif control=='*arcs':
                    status = 2
                    i = line.find(':')
                    if i>0:
                        S = line[i+1:].split(' ',1)
                        rel = eval(S[0]); rlab = eval(S[1])
                        rels[rel] = rlab; multirel = True
                    continue
                elif control=='*edges':
                    status = 3
                    i = line.find(':')
                    if i>0:
                        S = line[i+1:].split(' ',1)
                        rel = eval(S[0]); rlab = eval(S[1])
                        rels[rel] = rlab; multirel = True
                    continue
                else: continue
            elif status == 1:
                L = re.split('\"',line.strip())
                if len(L) > 1:
                    K = re.split('\s+',L[2].strip())
                    L = L[:2]; L.extend(K)
                else:
                    L = re.split('\s+',line.strip())
                node = eval(L[0]); name = L[1]
                G.setNode(node,'lab',name)
                if len(L) > 3:
                    G.setNode(node,'x',eval(L[2]))
                    G.setNode(node,'y',eval(L[3]))
                if '[' in line:
                    temporal = True; G.setNode(node,'act',Graph.extractTQ(line))
            elif status == 2:
                i = line.find(':')
                if i > 0:
                    multirel = True; rn = rel if i < 0 else eval(line[:i])
                L = re.split('\s+',line[i+1:].strip())
                u = eval(L[0]); v = eval(L[1])
                if len(L)>2:
                    w = {'w': eval(L[2])}
                    if '[' in line:
                        temporal = True; w = {'tq': Graph.extractTQ(line)}
                else: w = {'w': 1}
                if multirel: G.addArc(u,v,w=w,rel=rn)
                else: G.addArc(u,v,w=w)
            elif status == 3:
                i = line.find(':')
                if i > 0:
                    multirel = True; rn = rel if i < 0 else eval(line[:i])
                L = re.split('\s+',line[i+1:].strip())
                u = eval(L[0]); v = eval(L[1])
                if len(L)>2:
                    w = {'w': eval(L[2])}
                    if '[' in line:
                        temporal = True; w = {'tq': Graph.extractTQ(line)}
                else: w = {'w': 1}
                if u > v : v,u = u,v
                if multirel : G.addEdge(u,v,w=w,rel=rn)
                else: G.addEdge(u,v,w=w)
        net.close()
        G._graph['simple'] = simple
        G._graph['mode'] = mode
        if mode==2:
            G._graph['dim'] = ( nr, nc )       
        G._graph['temporal'] = temporal
        if len(rels)>0:
            G._graph['multirel'] = True
            G._graph['legends'] = {}
            G._graph['legends']['rels'] = rels
        if len(meta)>0:
            G._graph['meta'] = meta
        return G
    def loadNetJSON(file, encoding='utf-8'):
        try: js = open(file,'r',encoding=encoding)
        except: raise Graph.graphError(
            "Problems with Pajek file {0}".format(file))
        net = json.loads(js.read())
        mode = net['info'].get('mode',1)
        n = net['info'].get('nNodes',0)
        G = Graph()
        G._graph['mode'] = mode
        if mode==2:
            nr, nc = G._graph['dim'] = net['info'].get('dim',[0,0])
            if nr==0: raise Graph.graphError("Missing mode1 size")
        G._graph['title'] = net['info'].get('title',"INPUT network")        
        G._graph['network'] = net['info'].get('network',"network")        
        G._graph['simple'] = net['info'].get('simple',False)
        G._graph['meta'] = net['info'].get('meta',[])
        G._graph['multirel'] = net['info'].get('multirel',False)
        G._graph['directed'] = net['info'].get('directed',False)        
        G._graph['legends'] = net['info'].get('legends',{})
        G._graph['required'] = net['info'].get('required',{"nodes":[],"links":[]})        
        G._graph['trace'] = net['info'].get('trace',["loadNetJson"])        
        temporal = net['info'].get('temporal',False)
        G._graph['temporal'] = temporal
        if temporal:
            if 'time' in net['info']:
                Tmin = net['info']['time'].get('Tmin',1)
                Tmax = net['info']['time'].get('Tmax',999999999)
                G._graph['time'] = (Tmin,Tmax)
                G._graph['legends']['Tlabs'] = net['info']['time'].get('Tlabs',{})
            else: raise Graph.graphError("Missing Time info")
        for K in net['nodes']:
            L = K.copy(); vid = L.pop('id',None); G.addNode(vid,mode)
            G._nodes[vid][3] = L
        for K in net['links']:
            L = K.copy(); lid = L.pop('id',None);
            u = L.pop('n1',None); v = L.pop('n2',None)
            r = L.pop('id',None); t = L.pop('type','edge')
            if t=='arc': l = G.addArc(u,v,w=L,rel=r,lid=lid)
            else: l = G.addEdge(u,v,w=L,rel=r,lid=lid)            
        return G
    def saveNetJSON(self,file=None,indent=None):
        n = len(self._nodes)
        info = {}; nodes = {}; links = {};
        info['simple'] = self._graph.get('simple',False) 
        info['directed'] = len(list(self.edges()))==0
        temporal = self._graph.get('temporal',False)
        info['temporal'] = temporal
        info['org'] = 1
        info['mode'] = self._graph.get('mode',1)
        if info['mode']>1:
            info['dim'] = \
               [len(list(self.nodesMode(i+1))) for i in range(info['mode'])]
        info['network'] = self._graph.get('network',"test")
        info['title'] = self._graph.get('title',"testSAVE")
        info['multirel'] = self._graph.get('multirel',False)
        info['meta'] =  self._graph.get('meta',[]) 
        info['meta'].append({"date": datetime.datetime.now().ctime(),\
             "title": "saved from Graph to netJSON" })
        info['trace'] = self._graph.get('trace',[])
        info['required'] = self._graph.get('required',{})
        info['nNodes'] = n
        if temporal:
            minT, maxT = self._graph['time']
            leg = self._graph.get('legends',None)
            if leg != None: Tlabs = leg.get('Tlabs',
               { str(y):str(y) for y in range(minT,maxT+1)})
            info['time'] = { "Tmin": minT, "Tmax": maxT, "Tlabs": Tlabs }
        nodes = []
        for node in self._nodes:
            Node = self._nodes[node][3]; Node['id'] = node 
            nodes.append(Node)
        links = []
        for link in self._links:
            u,v,d,r,w = self._links[link]; Link = w 
            Link["type"] = "arc" if d else "edge"
            Link["n1"] = u; Link["n2"] = v
            if r!=None: Link["rel"] = r
            links.append(Link)      
        info['nArcs'] = len(list(self.arcs()))
        info['nEdges'] = len(list(self.edges()))
        if file==None: file = info['network']+'.json'
        net = {"netJSON": "basic", "info": info, "nodes": nodes, "links": links}
        js = open(file,'w')
        json.dump(net, js, ensure_ascii=False, indent=indent)
        js.close()
    def savePajek(self,file,coord=True):
# sprogramiraj še za dvodelna omrežja
        net = open(file,'w'); n=len(self._nodes)
        net.write('*vertices '+str(n)+'\n')
        ind = {}
        for (i,v) in enumerate(self._nodes):
            xy = self.getXY(v); ind[v] = i+1
            lab = self.getNode(v,'lab')
            if lab == None: lab = "v"+str(v)
            net.write(str(i+1)+' "'+lab+'"')
            if coord: net.write(' '+str(xy[0])+' '+str(xy[1])+' 0.5')
            net.write('\n')
        net.write('*arcs\n')
        for a in self.arcs():
            u,v,*r = self._links[a]
#            print(a,u,v,r)
            w = self.getLink(a,'w')
            if w == None: w = 1
            net.write(str(ind[u])+' '+str(ind[v])+' '+str(w)+'\n')
        net.write('*edges\n')
        for e in self.edges():
            u,v,*r = self._links[e]
#            print(e,u,v,r)
            w = self.getLink(e,'w')
            if w == None: w = 1
            net.write(str(ind[u])+' '+str(ind[v])+' '+str(w)+'\n')
        net.close()
    def twoMode2netJSON(yFile,netFile,jsonFile,instant=True,key='w',
                        replace=True,indent=None):
        def timer(): return datetime.datetime.now().ctime()
        G = Graph.loadPajek(netFile); F = Graph()
        for v in G.nodesMode(1): F.addNode(v)
        F.loadPajekClu('year',yFile)
        minT = min(F.getNode(v,'year') for v in F.nodes())
        maxT = max(F.getNode(v,'year') for v in F.nodes())
        nr = len(list(G.nodesMode(1))); nc = len(list(G.nodesMode(2)))
        for v in G.nodesMode(1): G.setNode(v,'act', [(F.getNode(v,'year'),maxT+1,1)])
        for v in G.nodesMode(2): G.setNode(v,'act', [(minT,maxT+1,1)])
        for e in G.links():
            u,v,*r = G._links[e]; t = F.getNode(u,'year')
            G._links[e][4]['tq'] = [(t,t+1,G._links[e][4][key])] if instant \
                else [(t,maxT+1,G._links[e][4][key])]
            if replace: del G._links[e][4][key]
        G.setGraph('title',"instant" if instant else "cumulative")
        G.setGraph('temporal',True); G.setGraph('mode',2); G.setGraph('dim',(nr,nc))
        G.setGraph('meta',[{"date":timer(),"title":"TwoMode2netJSON"}])
        G.setGraph('time',(minT,maxT)); G.setGraph('temporal',True)         
        G.setGraph('Tlabs',{str(y):str(y) for y in range(minT,maxT+1)});
        G.setGraph('trace',[timer(),Graph.location(),"Graph","twoMode2netJSON",
            [yFile,netFile],['input','input']])
        G.setGraph('required',{"nodes": ["id","mode","lab","act"],
            "links": ["n1","n2","type","tq"]}) # for JSON
        G.saveNetJSON(jsonFile,indent=indent)
        return G       
    def loadPajekClu(self,key,file):
        try:
            clu = open(file,'r')
        except:
            raise Graph.graphError(
                "Problems with Pajek file {0}".format(file))
        k = -1; n=len(self._nodes)
        while True:
            line = clu.readline()
            if not line: break
            if line[0] == '%': continue
            if line[0] == '*':
                L = re.split('\s+',line.strip())
                control = L[0].lower()
                if control=='*vertices':
                    num = eval(L[1])
                    if num != n: raise Graph.graphError(
                      "Partition size {0} != Graph size{1}".format(num,n))
                    k = 0; continue
            elif k >= 0:
                k += 1
                if k > num: break
                self.setNode(k,key,eval(line.strip()))
                continue
            else:
                raise Graph.graphError(
                    "Problems on Pajek file {0}".format(file))
        clu.close()
    def savePajekClu(self,key,file):
        clu = open(file,'w');  n=len(self._nodes)
        clu.write('*vertices '+str(n)+'\n')
        for i in range(n): clu.write(str(self.getNode(i+1,key))+'\n')
        clu.close()
    def loadPajekVec(self,key,file):
        try:
            vec = open(file,'r')
        except:
            raise Graph.graphError(
                "Problems with Pajek file {0}".format(file))
        k = -1; n=len(self._nodes)
        while True:
            line = vec.readline()
            if not line: break
            if line[0] == '%': continue
            if line[0] == '*':
                L = re.split('\s+',line.strip())
                control = L[0].lower()
                if control=='*vertices':
                    num = eval(L[1])
                    if num != n: raise Graph.graphError(
                      "Vector size {0} != Graph size{1}".format(num,n))
                    k = 0; continue
            elif k >= 0:
                k += 1
                if k > num: break
                self.setNode(k,key,eval(line.strip()))
                continue
            else:
                raise Graph.graphError(
                    "Problems on Pajek file {0}".format(file))
        vec.close()
    def savePajekVec(self,key,file):
        vec = open(file,'w');  n=len(self._nodes)
        vec.write('*vertices '+str(n)+'\n')
        for i in range(n): vec.write(str(self.getNode(i+1,key))+'\n')
        vec.close()
    def TQshow(tq,cdir,TQmax,Tmin,Tmax,w,h,tit,
        fill='steelblue',xLab=70,yLab=40):
        TQ = [ list(q) for q in tq ]
        js = open(cdir+'/barData.js','w')
        js.write('var barData = '+str(TQ)+';\n')
        js.write('var TQmax = '+str(TQmax)+';\n')
        js.write('var Tmin = '+str(Tmin)+';\n')
        js.write('var Tmax = '+str(Tmax)+';\n')
        js.write('var Width = '+str(w)+';\n')
        js.write('var Height = '+str(h)+';\n')
        js.write('var Title = "'+tit+'";\n')
        js.write('var Rfill = "'+fill+'";\n')
        js.write('var xLab = "'+str(xLab)+'";\n')
        js.write('var yLab = "'+str(yLab)+'";\n')
        js.close()  
    # https://pymotw.com/3/webbrowser/
    # import webbrowser
    # b = webbrowser.get('google-chrome')
    # b = webbrowser.get('mozilla')
        b = webbrowser.get('windows-default')
    #   b.open('c:/users/batagelj/work/python/graph/chart/barChart.html')
        b.open(cdir+'/TQchart.html')
    def getXY(self,u):
        if not('x' in self._nodes[u][3]): self._nodes[u][3]['x'] = random()
        if not('y' in self._nodes[u][3]): self._nodes[u][3]['y'] = random()
        return (self._nodes[u][3]['x'],self._nodes[u][3]['y'])
    def drawNode(self,u,rr=10,cols=('white','black')):
        xy = Graph.turtleXY(self.getXY(u))
        t.pu(); t.setpos(xy); t.pd()
        t.dot(rr,cols[1]); t.dot(rr-2,cols[0])
        t.pu(); t.setpos(xy[0]+rr/1.3,xy[1]-rr/2)
        t.pencolor('black')
        t.write(self._nodes[u][3].get('lab',str(u)))
    def drawLink(self,u,v,w=1,col='blue',arc=False):
        xy1 = Graph.turtleXY(self.getXY(u))
        xy2 = Graph.turtleXY(self.getXY(v))
        t.pu(); t.setpos(xy2); t.pd()
        t.pencolor(col); t.pensize(w); t.setpos(xy1)
        if arc:
            t.seth(t.towards(xy2)); d = 5+4*w; t.pu()
            xy = ((xy1[0]+xy2[0])/2,(xy1[1]+xy2[1])/2)
            t.setpos(xy); t.pd(); t.rt(20); t.bk(d);
            t.pu(); t.setpos(xy); t.pd()
            t.lt(40); t.bk(d)
    def draw(self,W,H,bg,col='col',d=15,colors=Colors):
        t.screensize(W,H,bg); t.title("Draw graf"); t.colormode(255)
        t.speed(0); t.clear(); t.ht()
        for e in self.links():
            u,v,directed,*r = self._links[e]
            if directed: self.drawLink(u,v,col='red',arc=True)
            else: self.drawLink(u,v)
        colored = col in self._nodes[u][3].keys()
        for v in self.nodes():
            fcol = colors[self.getNode(v,col)] if colored else 'yellow'
            self.drawNode(v,d,(fcol,'black'))
#       t.done()
        t.exitonclick()
    def onCircle(self,p=None):
        if p == None: p = self.nodes()
        n = len(self._nodes); a = 2*pi/n
        for (i,v) in enumerate(p):
            self.setNode(v,'x',0.5+0.45*sin(i*a))
            self.setNode(v,'y',0.5+0.45*cos(i*a))
    def ErdosRenyiGraph(n,m):
        G = Graph()
        for v in range(n): G.addNode(v+1)
        for i in range(m):
            while True:
                u = randint(1,n); v = randint(1,n)
                edge = (u,v,1) if u < v else (v,u,1)
                if not edge in G._links: break
            G.addEdge(u,v)
        return G
    def seqColoring(self,key='col'):
        fresh = 0; pal = set(range(1,20))
        for v in self.nodes(): self.setNode(v,key,fresh)
        p=list(self._nodes.keys()); shuffle(p)
        used = set()
        for v in p:
            free = used - \
                {self.getNode(u,key) for u in self.neighbors(v)}
            if len(free)==0:
                col = pal.pop()
                if len(pal) == 0: pal.add(col+1)
                free.add(col); used.add(col)
            self.setNode(v,key,free.pop())
        return len(used)

    def acyImportance(self,alpha,key='aImp'):
#   CDG, Paris, 21.10.2012
        for v in self.nodes():
            self.setNode(v,'outD',self.outDegree(v))
        for v in self.topologicalOrder():
            s = 1
            for u in self.inNeighbors(v):
                s = s + alpha*self.getNode(u,key)/self.getNode(u,'outD')
            self.setNode(v,key,s)

    def acyProbFlow(self,key='aPflow'):
#   Jena-Frankfurt, 5.7.2013
#   ~ acyImportance; alpha=1, standardized wo feed-back
        nInit = 0
        for v in self.nodes():
            self.setNode(v,'outD',self.outDegree(v))
            if self.inDegree(v)==0: nInit += 1
        for v in self.topologicalOrder():
            s = 0
            for u in self.inNeighbors(v):
                s = s + self.getNode(u,key)/self.getNode(u,'outD')
            if s==0: s = 1/nInit
            self.setNode(v,key,s)

# Transitive skeleton
# Piran, 26.12.2013
    def existsPath(self,K,u,h):
        F = set()
        for t in K:
            N = self.outArcNeighbors(t)
            if u in N: return True
            F = F | set({z for z in N if h[z-1] < h[u-1]})
        if len(F)==0: return False
        return self.existsPath(F,u,h)

    def tSkelet(self):
        print('Transitive skeleton')
        self.depth(); h = [0]*len(self)
        for i in range(len(self)): h[i] = self.getNode(i+1,'depth')
        p = [v+1 for (v,h) in sorted(list(enumerate(h)), key=lambda q: q[1])]
        p.reverse(); S = deepcopy(self)
        for v in p:
            for u in S.outArcNeighbors(v):
                if (h[u-1]-h[v-1])==1:
                    # print("accept",v,u)
                    continue
                T = set(S.outArcNeighbors(v)) - {u}
                K = {t for t in T if h[t-1]<h[u-1]}
                if len(K)==0: continue
                if S.existsPath(K,u,h):
                    S.delArc(v,u) #; print('delete',v,u)
        return S

    def cSkelet(self):
        print('Transitive skeleton count')
        self.depth(); hMax = 0
        for i in range(len(self)): hMax = max(hMax,self.getNode(i+1,'depth'))
        print('max depth = ',hMax)
        h = [0]*(hMax+1)
        for (u,v,k) in self.links():
           d = self.getNode(v,'depth') - self.getNode(u,'depth')
           h[d] += 1
        return h

# if __name__ == '__main__':

