''' File for testing different files
'''
__author__ = 'ivanovsergey'

import networkx as nx
import numpy as np

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
#from degreeDiscount import degreeDiscountIC

#import matplotlib.pylab as plt
import os

if __name__ == '__main__':
    import time
    start = time.time()

    # read in graph
    G = nx.Graph()
    with open(r'C:\Python27\sjxwork\influence-maximization-master\influence-maximization-master\IC\Political blogs.txt') as f:
        n, m = f.readline().split()
        for line in f:
            u, v = map(int, line.split())
            try:
                G[u][v]['weight'] += 1
            except:
                G.add_edge(u,v, weight=1)
            # G.add_edge(u, v, weight=1)
    print 'Built graph G'
    print time.time() - start

    #calculate initial set
    #seed_size = 4
    #S = degreeDiscountIC(G, seed_size)
    #print 'Initial set of', seed_size, 'nodes chosen'
    S1=[]
    S=[]
    print time.time() - start
    #for node in S:
        #print str(node) 
    # write results S to file
    #with open('C:\Users\Administrator\Desktop\lcirS.txt', 'w') as f:
     #   for node in S:
      #      f.write(str(node) + os.linesep)
    with open('C:\Users\Administrator\Desktop\lcirS1.txt', 'w') as gg:
        with open(r'C:\Python27\sjxwork\influence-maximization-master\influence-maximization-master\PB30\cc.txt', 'rU') as f:
            for line in f:
                S1.append(int(line))
                #S1=map(int,line.split())
                #S=S1[0,]
                #S=S1
            print(S1)
            S=S1
        # calculate average activated set size
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
            T1 = runIC01(G, S)
            T2 = runIC02(G, S)
            T3 = runIC03(G, S)
            T4 = runIC04(G, S)
            T5 = runIC05(G, S)
            T6 = runIC06(G, S)
            T7 = runIC07(G, S)
            T8 = runIC08(G, S)
            T9 = runIC09(G, S)
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
            print tt1
            
        print SUM_LENGTH1
        #a = np.array(tt1)   
        #print  np.std(tt1)
        #print type(a)
        #print   tt1
        #print type(tt1)
        #print stdDeviation(tt1)
        print 'Avg1. Targeted', int(round(avg1)), 'nodes out of', len(G)
        gg.write(str(int(round(avg1)))+'\n')
        print SUM_LENGTH2   
        #print  np.std(tt2)
        print 'Avg2. Targeted', int(round(avg2)), 'nodes out of', len(G)
        gg.write(str(int(round(avg2)))+'\n')
        print SUM_LENGTH3 
        #print  np.std(tt3)  
        print 'Avg3. Targeted', int(round(avg3)), 'nodes out of', len(G)
        gg.write(str(int(round(avg3)))+'\n')
        print SUM_LENGTH4
        #print  np.std(tt4)   
        print 'Avg4. Targeted', int(round(avg4)), 'nodes out of', len(G)
        gg.write(str(int(round(avg4)))+'\n')
        print SUM_LENGTH5 
        #print  np.std(tt5)  
        print 'Avg5. Targeted', int(round(avg5)), 'nodes out of', len(G)
        gg.write(str(int(round(avg5)))+'\n')
        print SUM_LENGTH6 
        #print  np.std(tt6)  
        print 'Avg6. Targeted', int(round(avg6)), 'nodes out of', len(G)
        gg.write(str(int(round(avg6)))+'\n')
        print SUM_LENGTH7 
        #print  np.std(tt7)  
        print 'Avg7. Targeted', int(round(avg7)), 'nodes out of', len(G)
        gg.write(str(int(round(avg7)))+'\n')
        print SUM_LENGTH8
        #print  np.std(tt8)   
        print 'Avg8. Targeted', int(round(avg8)), 'nodes out of', len(G)
        gg.write(str(int(round(avg8)))+'\n')
        print SUM_LENGTH9
        #print  np.std(tt9)   
        print 'Avg9. Targeted', int(round(avg9)), 'nodes out of', len(G)
        gg.write(str(int(round(avg9)))+'\n')
        print time.time() - start

    

    console = []
    