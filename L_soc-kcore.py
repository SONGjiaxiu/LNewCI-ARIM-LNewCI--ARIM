__author__='SONG Jiaxiu'
# -*- coding: utf-8 -*-
"""
This module implements NewCI.
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
from IC_p2p import runIC
from IC_p2p import runIC2
from IC_p2p import stdDeviation
from IC_p2p import runIC01
from IC_p2p import runIC02
from IC_p2p import runIC03
from IC_p2p import runIC04
from IC_p2p import runIC05
from IC_p2p import runIC06
from IC_p2p import runIC07
from IC_p2p import runIC08
from IC_p2p import runIC09
matplotlib.rcParams['font.family'] = 'sans-serif'  
matplotlib.rcParams['font.sans-serif'] = 'NSimSun,Times New Roman'# 中文设置成宋体，除此之外的字体设置成New Roman

##########********************数据存放文件****************
file = open(r"C:\Users\Administrator\Desktop\3th_result\mianyitu\router\email.txt", "w+")
#file = open(r"C:\Users\Administrator\Desktop\3th_result\newCI_parm\Celegans.txt", "w+")
#file = open(r"C:\Users\Administrator\Desktop\3th_result\newCI_parm\Email.txt", "w+")
#file = open(r"C:\Users\Administrator\Desktop\3th_result\newCI_parm\jazz.txt", "w+")
#file = open(r"C:\Users\Administrator\Desktop\3th_result\newCI_parm\power.txt", "w+")
#file = open(r"C:\Users\Administrator\Desktop\3th_result\newCI_parm\Router.txt", "w+")
#file = open(r"C:\Users\Administrator\Desktop\3th_result\newCI_parm\Yeast.txt", "w+")


#*******************************************************************************************#
##构建网络
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

def Degree_Centrality(G):
    Degree_Centrality = nx.degree_centrality(G)
    #print "Degree_Centrality:", sorted(Degree_Centrality.iteritems(), key=lambda d:d[1], reverse = True)
    return Degree_Centrality

def Between_Centrality(G):
    Bet_Centrality = nx.betweenness_centrality(G)
    #print "Bet_Centrality:", sorted(Bet_Centrality.iteritems(), key=lambda d:d[1], reverse = True)
    return Bet_Centrality

def Closeness_Centrality(G):
    Closeness_Centrality = nx.closeness_centrality(G)
    #print "Closeness_Centrality:", sorted(Closeness_Centrality.iteritems(), key=lambda d:d[1], reverse = True)
    return Closeness_Centrality

def Page_Rank(G):	
    PageRank_Centrality = nx.pagerank(G, alpha=0.85)
    #print "PageRank_Centrality:", sorted(PageRank_Centrality.iteritems(), key=lambda d:d[1], reverse = True)
    return PageRank_Centrality

def Eigen_Centrality(G):
    Eigen_Centrality = nx.eigenvector_centrality_numpy(G)
    #print "Eigen_Centrality:", sorted(Eigen_Centrality.iteritems(), key=lambda d:d[1], reverse = True)
    return Eigen_Centrality

def KShell_Centrality(G):
    #网络的kshell中心性
    #The k-core is found by recursively pruning nodes with degrees less than k.
    #The k-shell is the subgraph of nodes in the k-core but not in the (k+1)-core.
    nodes = {}
    core_number = nx.core_number(G) #The core number of a node is the largest value k of a k-core containing that node.
    for k in list(set(core_number.values())):
        nodes[k] = list(n for n in core_number if core_number[n]==k)
    print core_number #{'1': 2, '0': 2, '3': 2, '2': 2, '4': 1}字典（节点：KShell值）
    #print nodes.keys(),nodes
    KShell_Centrality = core_number
    return KShell_Centrality

###********************************************************************************************************



#D:\rengongdata\networks\a.csv
#G_init=createGraph(r"C:\Python27\sjxwork\NewCI_Centrality_Code\karate1.csv")
#G_init=createGraph(r"C:\Python27\sjxwork\NewCI_Centrality_Code\Dataset_csv\Power.csv")
#G_init=createGraph(r"C:\Python27\sjxwork\NewCI_Centrality_Code\Dataset_csv\Email.csv")
#G_init=createGraph(r"C:\Python27\sjxwork\NewCI_Centrality_Code\Dataset_csv\jazz.csv")
#G_init=createGraph(r"C:\Python27\sjxwork\NewCI_Centrality_Code\Dataset_csv\Power.csv")
#G_init=createGraph(r"C:\Python27\sjxwork\NewCI_Centrality_Code\karate1.csv")
G_init=createGraph(r"C:\Users\Administrator\Desktop\dataset\216\soc_00.csv")
#G_init=createGraph(r"C:\Python27\sjxwork\NewCI_Centrality_Code\Dataset_csv\Yeast.csv")
#print G_init.edges()
G1 = nx.Graph()
with open(r"C:\Users\Administrator\Desktop\dataset\216\soc_00.txt") as f:
    n, m = f.readline().split()
    for line in f:
        u, v = map(int, line.split())
        try:
            G1[u][v]['weight'] += 1
        except:
            G1.add_edge(u,v, weight=1)
k=50
###度

###k-核
time_kshell_start=time.time()
G_KShell=KShell_Centrality(G_init)
time_kshell=time.time()-time_kshell_start
# print "k_core"
# print time_kshell
KShell_sort=sorted(G_KShell.iteritems(), key=lambda d:d[1], reverse = True)
#print KShell_sort
res_list_k = [x for x,_ in KShell_sort]
# print res_list_k

# file.write("time_kshell"+str(time_kshell)+'\n')
# file.write(str(res_list_k)+'\n')
s=res_list_k[0:k]
S = map(int, s)
iterations = 50 # number of iterations
avg1 = 0
avg2 = 0
avg3 = 0
avg4 = 0
avg5 = 0
avg6 = 0
avg7 = 0
avg8 = 0
avg9 = 0
SUM_LENGTH1=0
SUM_LENGTH2=0
SUM_LENGTH3=0
SUM_LENGTH4=0
SUM_LENGTH5=0
SUM_LENGTH6=0
SUM_LENGTH7=0
SUM_LENGTH8=0
SUM_LENGTH9=0
tt1=[]
tt2=[]
tt3=[]
tt4=[]
tt5=[]
tt6=[]
tt7=[]
tt8=[]
tt9=[]
for i in range(iterations):
    T1 = runIC01(G1, S)
    T2 = runIC02(G1, S)
    T3 = runIC03(G1, S)
    T4 = runIC04(G1, S)
    T5 = runIC05(G1, S)
    T6 = runIC06(G1, S)
    T7 = runIC07(G1, S)
    T8 = runIC08(G1, S)
    T9 = runIC09(G1, S)
    avg1 += float(len(T1))/iterations
    avg2 += float(len(T2))/iterations
    avg3 += float(len(T3))/iterations
    avg4 += float(len(T4))/iterations
    avg5 += float(len(T5))/iterations
    avg6 += float(len(T6))/iterations
    avg7 += float(len(T7))/iterations
    avg8 += float(len(T8))/iterations
    avg9 += float(len(T9))/iterations
    SUM_LENGTH1+=len(T1)
    SUM_LENGTH2+=len(T2)
    SUM_LENGTH3+=len(T3)
    SUM_LENGTH4+=len(T4)
    SUM_LENGTH5+=len(T5) 
    SUM_LENGTH6+=len(T6)
    SUM_LENGTH7+=len(T7)
    SUM_LENGTH8+=len(T8)
    SUM_LENGTH9+=len(T9)
    #print type(T1)
    #print type(SUM_LENGTH1)
    tt1.append(len(T1))
    #a = np.array(tt1)
    tt2.append(len(T2))
    tt3.append(len(T3))
    tt4.append(len(T4))
    tt5.append(len(T5))
    tt6.append(len(T6))
    tt7.append(len(T7))
    tt8.append(len(T8))
    tt9.append(len(T9))
    #print T1
    
#print SUM_LENGTH1
#a = np.array(tt1)   
#print  np.std(tt1)
#print type(a)
#print   tt1
#print type(tt1)
#print stdDeviation(tt1)
print 'Avg1. Targeted', int(round(avg1)), 'nodes out of', len(G_init)
# gg.write(str(int(round(avg1)))+'\n')
print SUM_LENGTH2   
#print  np.std(tt2)
print 'Avg2. Targeted', int(round(avg2)), 'nodes out of', len(G_init)
# gg.write(str(int(round(avg2)))+'\n')
print SUM_LENGTH3 
#print  np.std(tt3)  
print 'Avg3. Targeted', int(round(avg3)), 'nodes out of', len(G_init)
# gg.write(str(int(round(avg3)))+'\n')
print SUM_LENGTH4
#print  np.std(tt4)   
print 'Avg4. Targeted', int(round(avg4)), 'nodes out of', len(G_init)
# gg.write(str(int(round(avg4)))+'\n')
print SUM_LENGTH5 
#print  np.std(tt5)  
print 'Avg5. Targeted', int(round(avg5)), 'nodes out of', len(G_init)
# gg.write(str(int(round(avg5)))+'\n')
print SUM_LENGTH6 
#print  np.std(tt6)  
print 'Avg6. Targeted', int(round(avg6)), 'nodes out of', len(G_init)
# gg.write(str(int(round(avg6)))+'\n')
print SUM_LENGTH7 
#print  np.std(tt7)  
print 'Avg7. Targeted', int(round(avg7)), 'nodes out of', len(G_init)
# gg.write(str(int(round(avg7)))+'\n')
print SUM_LENGTH8
#print  np.std(tt8)   
print 'Avg8. Targeted', int(round(avg8)), 'nodes out of', len(G_init)
# gg.write(str(int(round(avg8)))+'\n')
print SUM_LENGTH9
#print  np.std(tt9)   
print 'Avg9. Targeted', int(round(avg9)), 'nodes out of', len(G_init)
# gg.write(str(int(round(avg9)))+'\n')
print time.time() 