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
    G_Balance=l_Balance(G)
    G_Strength=l_Connection_strength(G)
    G_c=nx.clustering(G_init)
    ##等价
    # G_Robustness={} 
    # for (x,y) in G_init.edges(): make_link(G_R,x,y)
    # #print G_R
    # for v in G_R.keys():
    #     clustering_coefficient(G_R,v), " "+v
    #     G_Robustness[v]=clustering_coefficient(G_R,v)
    newCI={}
    newCI91={}
    newCI19={}
    newCI_B={}
    newCI_S={}
    for nid in G_Balance.keys():
        #newCI[nid]=round(float((0.5*G_Balance[nid]+0.5*G_Strength[nid])*G_CI_value[nid])/float(1+G_Robustness[nid]),3)
        #newCI[nid]=round(float(0.5*G_Balance[nid]/float(1+G_c[nid])*G_CI_value[nid]+0.5*G_Strength[nid]*G_CI_value[nid]),3)
        newCI[nid]=round(float((0.5*G_Balance[nid]+0.5*G_Strength[nid])*G_CI_value[nid])/float(1+G_c[nid]),3)
        #newCI[nid]=round(float((0.6*G_Strength[nid]+0.4*G_Balance[nid])/float(1+G_c[nid])*G_CI_value[nid]),3)
        newCI91[nid]=round(float((1.0*G_Balance[nid]+0*G_Strength[nid])*G_CI_value[nid])/float(1+G_c[nid]),3)
        newCI19[nid]=round(float((0*G_Balance[nid]+1.0*G_Strength[nid])*G_CI_value[nid])/float(1+G_c[nid]),3)
        newCI_B[nid]=round(float(1.0*G_Balance[nid]*G_CI_value[nid]),3)
        newCI_S[nid]=round(float(1.0*G_Strength[nid]*G_CI_value[nid]),3)
        #print nid, newCI

    return newCI,newCI91,newCI19,newCI_B,newCI_S
    #G_NewCI=dict(0.5*G_Balance)
    #list_G_CI_value

###*********************************对比方法********************************************
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
G_init=createGraph(r"C:\Python27\sjxwork\NewCI_Centrality_Code\Dataset_csv\political blogs.csv")
#G_init=createGraph(r"C:\Python27\sjxwork\NewCI_Centrality_Code\Dataset_csv\Yeast.csv")
#print G_init.edges()
G1 = nx.Graph()
with open(r"C:\Python27\sjxwork\LNewCI\Political blogs.txt") as f:
    n, m = f.readline().split()
    for line in f:
        u, v = map(int, line.split())
        try:
            G1[u][v]['weight'] += 1
        except:
            G1.add_edge(u,v, weight=1)
k=30
###度
# time_degree_start=time.time()
# G_degree=Degree_Centrality(G_init)
# time_degree=time.time()-time_degree_start
# # print "degree"
# # print time_degree
# Degree_sort=sorted(G_degree.iteritems(), key=lambda d:d[1], reverse = True)
# #print Degree_sort
# ##使用解包代替x[0]
# res_list_d = [x for x,_ in Degree_sort]
# # print res_list_d

# # file.write("degree_time"+str(time_degree)+'\n')
# # file.write(str(res_list_d)+'\n')

# ###介数
# time_Between_start=time.time()
# G_Between=Between_Centrality(G_init)
# time_between=time.time()-time_Between_start
# # print "between"
# # print time_between
# Between_sort=sorted(G_Between.iteritems(), key=lambda d:d[1], reverse = True)
# #print Between_sort
# res_list_b = [x for x,_ in Between_sort]
# # print res_list_b
# # file.write("time_between"+str(time_between)+'\n')
# # file.write(str(res_list_b)+'\n')
# s=res_list_b[0:k]
# time_between=time.time()-time_Between_start
# # print "between"
# print time_between
# S = map(int, s)



###接近度中心性
time_closeness_start=time.time()
G_Closeness=Closeness_Centrality(G_init)

Closeness_sort=sorted(G_Closeness.iteritems(), key=lambda d:d[1], reverse = True)
#print Closeness_sort
res_list_c = [x for x,_ in Closeness_sort]
# print res_list_c
# file.write("time_closeness"+str(time_closeness)+'\n')
# file.write(str(res_list_c)+'\n')
s=res_list_c[0:k]
time_closeness=time.time()-time_closeness_start
# print "closeness"
print time_closeness
S = map(int, s)

###PageRank中心性
# time_pagerank_start=time.time()
# G_Page_Rank=Eigen_Centrality(G_init)

# Page_Rank_sort=sorted(G_Page_Rank.iteritems(), key=lambda d:d[1], reverse = True)
# ##print Page_Rank_sort
# res_list_r = [x for x,_ in Page_Rank_sort]
# # print res_list_r
# # file.write("time_pagerank"+str(time_pagerank)+'\n')
# # file.write(str(res_list_r)+'\n')
# s=res_list_r[0:k]
# time_pagerank=time.time()-time_pagerank_start
# # print "pagerank"
# print time_pagerank
# S = map(int, s)

###k-核
# time_kshell_start=time.time()
# G_KShell=KShell_Centrality(G_init)

# KShell_sort=sorted(G_KShell.iteritems(), key=lambda d:d[1], reverse = True)
# #print KShell_sort
# res_list_k = [x for x,_ in KShell_sort]
# # print res_list_k

# # file.write("time_kshell"+str(time_kshell)+'\n')
# # file.write(str(res_list_k)+'\n')
# s=res_list_k[0:k]
# time_kshell=time.time()-time_kshell_start
# # print "k_core"
# print time_kshell
# S = map(int, s)
S1=[]
with open(r'C:\Users\Administrator\Desktop\Political blogs_IC_ci.txt', 'w') as gg:
    index=0
    for i in S:
        index=index+1
        S1.append(int(i))
        print S1
        iterations = 200 # number of iterations
        avg = 0
        SUM_LENGTH=0
        for j in range(iterations):
            T = runIC05(G1, S1)
            avg += float(len(T))/iterations
            SUM_LENGTH+=len(T)
        #gg.write(str(index)+' '+str(int(round(avg)))+'\n')
        gg.write(str(int(round(avg)))+'\n')