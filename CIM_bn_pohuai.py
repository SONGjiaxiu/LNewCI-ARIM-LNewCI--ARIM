__author__='SONG Jiaxiu'
# -*- coding: utf-8 -*-
"""
This module implements LCI_ar.
"""

import linecache
import string
import os
import math
import time
import networkx as nx
import sys
from collections import Counter
import operator
import networkx as nx             
import matplotlib.pyplot as plt
from networkx.generators.atlas import *
import numpy as np
import random
import requests
import pandas as pd
import csv
from networkx.algorithms.isomorphism.isomorph import graph_could_be_isomorphic as isomorphic
import linecache
import matplotlib
from operator import itemgetter
from IC import runIC
from IC import runIC2
from IC import stdDeviation
from IC import runIC01
from IC import runIC02
from IC import runIC03
from IC import runIC04
from IC import runIC05
from IC import runIC06
from IC import runIC07
from IC import runIC08
from IC import runIC09
matplotlib.rcParams['font.family'] = 'sans-serif'  
matplotlib.rcParams['font.sans-serif'] = 'NSimSun,Times New Roman'# 中文设置成宋体，除此之外的字体设置成New Roman



sys.setrecursionlimit(2000000000)

def createGraph(filename) :
    G = nx.Graph()
    for line in open(filename) :
        strlist = line.split(',', 3)
        #n1 = int(strlist[0])
        #n2 = int(strlist[1])
        n1 = strlist[0]
        n2 = strlist[1]
        #weight = float(strlist[2])
        #G.add_weighted_edges_from([(n1, n2)]) 
        G.add_edge(n1,n2)
    return G
##构建网络的方式2
def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G

def createGraph1(filename) :
    G = nx.Graph()
    for line in open(filename) :
        strlist = line.split()
        n1 = int(strlist[0])
        n2 = int(strlist[1])
        #weight = float(strlist[w_index])
        #G.add_weighted_edges_from([(n1, n2)]) 
        G.add_edge(n1,n2)
    return G

def remove_node1(G,node):
    for k in G.neighbors(node):
        G.remove_edge(node,k)
    return G
#*******************************************************************************************#
##CI中心性的2阶实现
def Collective_Influence(G, l=2):
    Collective_Influence_Dic = {}
    node_set = G.nodes()
    for nid in node_set:
        CI = 0
        neighbor_set = []
        neighbor_hop_1 = G.neighbors(nid)
        neighbor_hop_2 = []
        for nnid in neighbor_hop_1:
            neighbor_hop_2  = list(set(neighbor_hop_2).union(set(G.neighbors(nnid))))
            #print '2_hop:', nnid, G.neighbors(nnid)
        #end for

        center = [nid]
        neighbor_set = list(   set(neighbor_hop_2).difference(   set(neighbor_hop_1).union(set(center))  )    )
        #print nid, neighbor_hop_1, neighbor_hop_2, neighbor_set

        total_reduced_degree = 0
        for id in neighbor_set:
            total_reduced_degree = total_reduced_degree + (G.degree(id)-1.0)
        #end

        CI = (G.degree(nid)-1.0) * total_reduced_degree
        Collective_Influence_Dic[nid] =round(CI,3) 
    #end for
    #print "Collective_Influence_Dic:",sorted(Collective_Influence_Dic.iteritems(), key=lambda d:d[1], reverse = True)

    return Collective_Influence_Dic
def Collective_Influence3(G, l=3):
    Collective_Influence_Dic = {}
    node_set = G.nodes()
    for nid in node_set:
        CI = 0
        neighbor_set = []
        neighbor_hop_1 = G.neighbors(nid)
        neighbor_hop_2 = []
        neighbor_hop_3 = []
        for nnid in neighbor_hop_1:
            neighbor_hop_2  = list(set(neighbor_hop_2).union(set(G.neighbors(nnid))))
            #print '2_hop:', nnid, G.neighbors(nnid)
        #end for
        for nnnid in neighbor_hop_2:
            neighbor_hop_3 =list(set(neighbor_hop_3).union(set(G.neighbors(nnid))))
        center = [nid]
        #neighbor_set = list(   set(neighbor_hop_2).difference(   set(neighbor_hop_1).union(set(center))  ) 
        neighbor_set = list(   set(neighbor_hop_3).difference(   set(neighbor_hop_2).union(set(neighbor_hop_1).union(set(center)) ) )   )
        #print nid, neighbor_hop_1, neighbor_hop_2, neighbor_set

        total_reduced_degree = 0
        for id in neighbor_set:
            total_reduced_degree = total_reduced_degree + (G.degree(id)-1.0)
        #end

        CI = (G.degree(nid)-1.0) * total_reduced_degree
        Collective_Influence_Dic[nid] =round(CI,3) 
    #end for
    #print "Collective_Influence_Dic:",sorted(Collective_Influence_Dic.iteritems(), key=lambda d:d[1], reverse = True)

    return Collective_Influence_Dic
def Collective_Influence4(G, l=4):
    Collective_Influence_Dic = {}
    node_set = G.nodes()
    for nid in node_set:
        CI = 0
        neighbor_set = []
        neighbor_hop_1 = G.neighbors(nid)
        neighbor_hop_2 = []
        neighbor_hop_3 = []
        neighbor_hop_4 = []
        for nnid in neighbor_hop_1:
            neighbor_hop_2  = list(set(neighbor_hop_2).union(set(G.neighbors(nnid))))
            #print '2_hop:', nnid, G.neighbors(nnid)
        #end for
        for nnnid in neighbor_hop_2:
            neighbor_hop_3 =list(set(neighbor_hop_3).union(set(G.neighbors(nnid))))
        for nnnnid in neighbor_hop_3:
            neighbor_hop_4 =list(set(neighbor_hop_4).union(set(G.neighbors(nnid))))    
        center = [nid]
        #neighbor_set = list(   set(neighbor_hop_2).difference(   set(neighbor_hop_1).union(set(center))  ) 
        neighbor_set = list(   set(neighbor_hop_4).difference( set(neighbor_hop_2).union(set(neighbor_hop_2).union(set(neighbor_hop_1).union(set(center)) ))   )   )
        #print nid, neighbor_hop_1, neighbor_hop_2, neighbor_set

        total_reduced_degree = 0
        for id in neighbor_set:
            total_reduced_degree = total_reduced_degree + (G.degree(id)-1.0)
        #end

        CI = (G.degree(nid)-1.0) * total_reduced_degree
        Collective_Influence_Dic[nid] =round(CI,3) 
    #end for
    #print "Collective_Influence_Dic:",sorted(Collective_Influence_Dic.iteritems(), key=lambda d:d[1], reverse = True)

    return Collective_Influence_Dic
G=createGraph(r"C:\Users\Administrator\Desktop\dataset\216\ca-GrQc.csv")
#G=createGraph(r"C:\Python27\sjxwork\LNewCI\political blogs.csv")
G1 = nx.Graph()
with open(r"C:\Users\Administrator\Desktop\dataset\216\ca-GrQc.txt") as f:
    n, m = f.readline().split()
    for line in f:
        u, v = map(int, line.split())
        try:
            G1[u][v]['weight'] = 1
        except:
            G1.add_edge(u,v, weight=1)
LCI={}
CI={}
s_CI=[]
K_SORT={}
k=30 ###需要找的影响力节点组的个数
lamida=1
c=1
###CI
time_CI_start=time.time()
CI_update={}

print "ci"
print CI
while c<=k:
    LCI_CURRENT=[]
    CI=Collective_Influence3(G)
    CI_sort=sorted(CI.iteritems(), key=lambda d:d[1], reverse = True)
    id_CI_k= [x for x,_ in CI_sort]
    #print id_CI_k[0]
    s_CI.append(id_CI_k[0])
    # for k in G.neighbors(id_CI_k[0]):
    #     G.remove_edge(id_CI_k[0],k)
    #
    #G=remove_node1(G,id_CI_k[0]) 
    G.remove_node(id_CI_k[0])
    #print G.number_of_edges()
    c=c+1
print s_CI
time_CI=time.time()-time_CI_start
print time_CI
S=s_CI
print s_CI
S = map(int, S)
largest_cc_list=[]
remove_rate=[]
H_list=[]
for i in range(0,len(S)):
    G1=remove_node1(G1,S[i])
    #G1=remove_node1(G1,S[i])
    G1.remove_node(S[i])
    largest_cc = len(max(nx.connected_components(G1), key=len))
    #largest_cc = len(list(nx.connected_components(G1)))
    print largest_cc
    '''
    if list(nx.connected_components(G1)):
        #print list(nx.connected_components(G))
        largest_cc = len(max(nx.connected_components(G1), key=len))
        #print largest_cc
    else:
        largest_cc=0
    print
    ''' 
    H=len(list(nx.connected_components(G1)))
    largest_cc_list.append(largest_cc)
    remove_rate.append(float(largest_cc)/float(1781))
    H_list.append(H)
print largest_cc_list
print remove_rate
print H_list# 
# console = []
with open(r'C:\Users\Administrator\Desktop\Political blogs_IC_ci.txt', 'w') as gg:
    #gg.write(str(index)+' '+str(int(round(avg)))+'\n')
    gg.write(str(remove_rate)+'\n')
        

# console = []