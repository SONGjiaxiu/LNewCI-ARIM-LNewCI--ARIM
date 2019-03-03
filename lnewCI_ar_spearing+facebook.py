__author__='SONG Jiaxiu'
# -*- coding: utf-8 -*-
"""
This module implements LnewCI_ar.
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
##********************************l阶邻域度均衡性******************************************
def l_Balance(G): #
    l_Balance_Dic = {}
    node_set = G.nodes()
    for nid in node_set:
        degree = G.degree(nid)
        Neighbor_Set = G.neighbors(nid)
        #degree_max = 0
        #degree_min = 0
        #print type(Neighbor_Set)
        seq_neibhood=[]
        for ngb in Neighbor_Set:
            #print ngb
            seq_neibhood.append(G.degree(ngb))
        #print seq_neibhood
        degree_max=max(seq_neibhood)
        #print degree_max
        degree_min=min(seq_neibhood)
        #print degree_min
        #total_neighbor_degree = total_neighbor_degree + G.degree(ngb)
        l_Balance_Dic[nid] =round(float(1.0 / float(float(degree_max-degree_min)/(degree_max+degree_min)+1) ),3 ) 
        #print l_Balance_Dic[nid]  
    #end for
    return l_Balance_Dic

##********************************************l阶邻域簇间连接强度************************************************************##
def l_Connection_strength(G):
    l_Connection_strength_Dic={}
    node_set=G.nodes()
    Connection_num=0

    #_l阶连通图的数量
      
    #print nid,i_2_nei   
    for nid in node_set:
       
        degree=G.degree(nid)
        Neighbor_Set=G.neighbors(nid)
        #print nid,Neighbor_Set
        #print len(Neighbor_Set)
   
        
        # i__nei=set(G.neighbors(i))
       
        ###current_1_neighbor=G.neighbors(nid)
        #print nid,current_1_neighbor
        ###current_2_neighbor=[]
        ###for nnid in current_1_neighbor:
            ###current_2_neighbor = list(set(current_2_neighbor).union(set(G.neighbors(nnid))))
        #print '2_hop:', nid,current_2_neighbor
        ###current_2_neighbor= list(  set(current_2_neighbor).difference( set(current_1_neighbor).union(set([nid]))  ) ) 
        #print nid ,current_2_neighbor 
        #print nid,Neighbor_Set
        
        if len(Neighbor_Set)==1:
            Connection_num=1
            #print nid 
            l_Connection_strength_Dic[nid]=1.0
            #print nid,l_Connection_strength_Dic[nid]

        elif len(Neighbor_Set)>1:
            G_conn=nx.Graph()
            #print nid, Neighbor_Set
            ##vi,j组合
            Cluster_head_connection_set=[]
            for i in range(0,len(Neighbor_Set)):
                #vi目标节点的邻居
                vi=Neighbor_Set[i]
                #print nid,Neighbor_Set[i]
                n_vi_2=[]
                ##n_vi 是vi的邻居
                for n_vi in G.neighbors(vi):
                    n_vi_2= list(set(n_vi_2).union(set(G.neighbors(n_vi))))
                n_vi_2=list(set(n_vi_2).difference(set(G.neighbors(vi)).union(set([nid]))))
                for j in range(i+1,len(Neighbor_Set)):
                    vj=Neighbor_Set[j]
                    #print vi,vj
                    fai_ij=list(set(n_vi_2).intersection(set(G.neighbors(vj))))
                    #print vi,vj,fai_ij
                    if fai_ij:
                        Cluster_head_connection_set.append(list([vi,vj]))
                        #
            #print nid,Cluster_head_connection_set
            for k in Cluster_head_connection_set:
                G_conn.add_edge(k[0],k[1])
            H=len(list(nx.connected_components(G_conn)))
            #print nid,H
            G_conn_nodenums=int(nx.number_of_nodes(G_conn))
            ##独立簇的数量
            independent_cluster_num=int(len(Neighbor_Set))-int(G_conn_nodenums )
            ##l-阶的连通数
            Connection_num=int(H)+int(independent_cluster_num)
            l_Connection_strength_Dic[nid]=round(float(Connection_num)/float(len(Neighbor_Set)),3)
            #print nid,l_Connection_strength_Dic[nid]
    return l_Connection_strength_Dic









##********************************************计算网络中节点局部聚类系数************************************************************##
def clustering_coefficient(G,v):
    neighbors = G[v].keys()
    if len(neighbors) == 1: return 0.0
    links = 0
    for w in neighbors:
        for u in neighbors:
            if u in G[w]: links += 0.5
    return round(2.0*links/(len(neighbors)*(len(neighbors)-1)),3)


##*********************************************************************************************


##*************************************CI(l变量时候)******************************************************##
#from __future__ import print_function
def Collective_Influenc(G, l):
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
        Collective_Influence_Dic[nid] = CI
    #end for
    #print "Collective_Influence_Dic:",sorted(Collective_Influence_Dic.iteritems(), key=lambda d:d[1], reverse = True)

    return Collective_Influence_Dic


##*****************************************lll********************************************************##

def New_Collective_Influence(G):
    G_CI_value=Collective_Influence(G)
    # G_Balance=l_Balance(G)
    # G_Strength=l_Connection_strength(G)
    G_c=nx.clustering(G)
    ##等价
    # G_Robustness={} 
    # for (x,y) in G_init.edges(): make_link(G_R,x,y)
    # #print G_R
    # for v in G_R.keys():
    #     clustering_coefficient(G_R,v), " "+v
    #     G_Robustness[v]=clustering_coefficient(G_R,v)
    newCI={}
    for nid in G_CI_value.keys():
        #newCI[nid]=round(float((0.5*G_Balance[nid]+0.5*G_Strength[nid])*G_CI_value[nid])/float(1+G_Robustness[nid]),3)
        #newCI[nid]=round(float(0.5*G_Balance[nid]/float(1+G_c[nid])*G_CI_value[nid]+0.5*G_Strength[nid]*G_CI_value[nid]),3)
        newCI[nid]=round(float(float(1+G_c[nid])*G_CI_value[nid]),3)
        #newCI[nid]=round(float((0.6*G_Strength[nid]+0.4*G_Balance[nid])/float(1+G_c[nid])*G_CI_value[nid]),3)
    return newCI
    #G_NewCI=dict(0.5*G_Balance)
    #list_G_CI_value
G=createGraph(r"C:\Python27\sjxwork\LNewCI\dataset0\facebookone.csv")
G1 = nx.Graph()
with open(r"C:\Python27\sjxwork\LNewCI\dataset0\facebook.txt") as f:
    n, m = f.readline().split()
    for line in f:
        u, v = map(int, line.split())
        try:
            G1[u][v]['weight'] += 1
        except:
            G1.add_edge(u,v, weight=1)
LCI={}
CI={}
LCIequalto0=[]
K_SORT={}
k=70 ###需要找的影响力节点组的个数
lamida=1
c=0 
###CI
time_CI_start=time.time()
CI_update={}
time_CI=time.time()-time_CI_start
print "ci"
#print CI
#while len(LCIequalto0)*lamida<k:
while c<10:
    LCI_CURRENT=[]
    CI=New_Collective_Influence(G)
    for nid in G.nodes():
        LCII=0
        neighbor_hop_1 = G.neighbors(nid)
        #print neighbor_hop_1
        for neighbor in neighbor_hop_1:
            #print neighbor
            if CI[nid]<CI[neighbor]:
                LCII=LCII+1
            else:
                pass
        LCI[nid]=LCII
        if LCI[nid]==0:
            LCIequalto0.append(nid)
            LCI_CURRENT.append(nid)
            CI_update[nid]=CI[nid]
        else:
            pass
    #print LCIequalto0
    LCIequalto0_len=len(LCIequalto0 )
    for nid in LCI_CURRENT:
        remove_node1(G,nid)
    c=c+1

sort_k=sorted(CI_update.iteritems(), key=lambda d:d[1], reverse = True)
id_sort_k= [x for x,_ in sort_k]
print len(id_sort_k)
print id_sort_k[0:k]
S=id_sort_k[0:50]
print S
S = map(int, S)
iterations = 100 # number of iterations
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
    print T1
    
print SUM_LENGTH1
#a = np.array(tt1)   
#print  np.std(tt1)
#print type(a)
#print   tt1
#print type(tt1)
#print stdDeviation(tt1)
print 'Avg1. Targeted', int(round(avg1)), 'nodes out of', len(G)
# gg.write(str(int(round(avg1)))+'\n')
print SUM_LENGTH2   
#print  np.std(tt2)
print 'Avg2. Targeted', int(round(avg2)), 'nodes out of', len(G)
# gg.write(str(int(round(avg2)))+'\n')
print SUM_LENGTH3 
#print  np.std(tt3)  
print 'Avg3. Targeted', int(round(avg3)), 'nodes out of', len(G)
# gg.write(str(int(round(avg3)))+'\n')
print SUM_LENGTH4
#print  np.std(tt4)   
print 'Avg4. Targeted', int(round(avg4)), 'nodes out of', len(G)
# gg.write(str(int(round(avg4)))+'\n')
print SUM_LENGTH5 
#print  np.std(tt5)  
print 'Avg5. Targeted', int(round(avg5)), 'nodes out of', len(G)
# gg.write(str(int(round(avg5)))+'\n')
print SUM_LENGTH6 
#print  np.std(tt6)  
print 'Avg6. Targeted', int(round(avg6)), 'nodes out of', len(G)
# gg.write(str(int(round(avg6)))+'\n')
print SUM_LENGTH7 
#print  np.std(tt7)  
print 'Avg7. Targeted', int(round(avg7)), 'nodes out of', len(G)
# gg.write(str(int(round(avg7)))+'\n')
print SUM_LENGTH8
#print  np.std(tt8)   
print 'Avg8. Targeted', int(round(avg8)), 'nodes out of', len(G)
# gg.write(str(int(round(avg8)))+'\n')
print SUM_LENGTH9
#print  np.std(tt9)   
print 'Avg9. Targeted', int(round(avg9)), 'nodes out of', len(G)
# gg.write(str(int(round(avg9)))+'\n')
print time.time() 


# console = []