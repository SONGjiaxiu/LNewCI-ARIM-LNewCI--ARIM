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
        if len(Neighbor_Set)==0:
            l_Balance_Dic[nid]=0.0
        else:
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
        elif len(Neighbor_Set)==0:
            l_Connection_strength_Dic[nid]=0.0
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
##*****************************************lll********************************************************##

def New_Collective_Influence(G):
    G_CI_value=Collective_Influence(G)
    G_Balance=l_Balance(G)
    G_Strength=l_Connection_strength(G)
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
        newCI[nid]=round(float((0.5*G_Balance[nid]+0.5*G_Strength[nid])*G_CI_value[nid])/float(1+G_c[nid]),3)
        #newCI[nid]=round(float(0.5*G_Balance[nid]/float(1+G_c[nid])*G_CI_value[nid]+0.5*G_Strength[nid]*G_CI_value[nid]),3)
        #newCI[nid]=round(float(float(1+G_c[nid])*G_CI_value[nid]),3)
        #newCI[nid]=round(float((0.6*G_Strength[nid]+0.4*G_Balance[nid])/float(1+G_c[nid])*G_CI_value[nid]),3)
    return newCI
    #G_NewCI=dict(0.5*G_Balance)
    #list_G_CI_value
G=createGraph(r"C:\Python27\sjxwork\LNewCI\dataset0\USA airportsN_0.csv")
G1 = nx.Graph()
with open(r"C:\Python27\sjxwork\LNewCI\dataset0\usa.txt") as f:
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
k=30 ###需要找的影响力节点组的个数
lamida=1
c=0
###CI
time_CI_start=time.time()
CI_update={}
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
    #print len(LCI_CURRENT)
    for nid in LCI_CURRENT:
        #remove_node1(G,nid)
        G.remove_node(nid)
        #print 'hhhhhhhhhhh'+str(G.number_of_edges())
    #print 'hAAhhhhhhhh'+str(G.number_of_edges())
    c=c+1
time_CI=time.time()-time_CI_start
print time_CI
sort_k=sorted(CI_update.iteritems(), key=lambda d:d[1], reverse = True)
id_sort_k= [x for x,_ in sort_k]
print len(id_sort_k)
print id_sort_k[0:k]
S=id_sort_k[0:30]
print S
S = map(int, S)
largest_cc_list=[]
remove_rate=[]

for i in range(0,len(S)):
    print S[i]
    #G1=remove_node1(G1,S[i])
    #print G1.number_of_edges()
    G1.remove_node(int(S[i]))
    if list(nx.connected_components(G1)):
        #print list(nx.connected_components(G))
        largest_cc = len(max(nx.connected_components(G1), key=len))
    else:
        largest_cc=0
    H=len(list(nx.connected_components(G1)))
    largest_cc_list.append(largest_cc)
    remove_rate.append(float(largest_cc)/float(1574))
    
print largest_cc_list
print remove_rate

with open(r'C:\Users\Administrator\Desktop\Political blogs_IC_ci.txt', 'w') as gg:
    #gg.write(str(index)+' '+str(int(round(avg)))+'\n')
    gg.write(str(remove_rate)+'\n')
        

# console = []