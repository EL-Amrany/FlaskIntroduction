import numpy as np
import csv
from xml.dom import minidom

class PageRank():
    
    #Constructor
    def __init__(self,lambda_=0.85,epsilon=1e-6,max_iter=100,n=11):
        self.lambda_=lambda_
        self.epsilon=epsilon
        self.max_iter=max_iter
        self.n=n

    #Page Rank for Transition Probability Matrix
    def PageRank_TP(self,P):    
        R_n=np.zeros((self.n,1))    
        for i in range(R_n.shape[0]):
            R_n[i,0]=1/self.n
        norm=1
        for l in range(self.max_iter):
            if norm>self.epsilon:
                R_n1=np.sum(P*R_n,axis=0).reshape(-1,1) 
                norm=np.linalg.norm(R_n1.reshape(-1,)-R_n.reshape(-1,))
                R_n =R_n1
            else:
                break           
        return R_n

    #Page Rank for Adjacency Matrix
    def PageRank_A(self,A):        
        P=np.zeros(A.shape)
        for i in range(A.shape[0]):
            sum_i=np.sum(A[i])
            for j in range(A.shape[1]):
                if sum_i==0:
                    P[i,j]=1/A.shape[0]
                else:
                    P[i,j]=((self.lambda_/sum_i)*A[i,j])+((1-self.lambda_)/A.shape[0])
        return self.PageRank_TP(P)
    
    #Page Rank using CSV File
    def PageRank_csv(self,xml_file='test.csv',lambda_=0.85,epsilon=1e-6,mode='Adjacency'):
            if mode=='Adjacency':
                with open(xml_file, newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    A=[]
                    for row in reader:
                        A.append(np.array(row[0].split()).astype(int))
                A=np.array(A)
                return self.PageRank_A(A)
            if mode=='Transition_probability':
                P=[]
                with open(xml_file, newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        P.append(np.array(row[0].split()).astype(float))
                P=np.array(P)
                return self.PageRank_TP(P)
                
    #Page Rank using an XML File
    def Page_Rank_xmlFile(self,xmlFile):
        file = minidom.parse(xmlFile)
        nodes = file.getElementsByTagName('node')
        A=np.zeros((len(nodes),len(nodes)))
        edges = file.getElementsByTagName('edge')
        for edge in edges :
            i=int(edge.attributes['source'].value)
            j=int(edge.attributes['destination'].value)
            A[i-1,j-1]=1
        return self.PageRank_A(A)  
    
    #Page Rank for a graph (Graphnx class)
    def PageRank_Graph(self,DG):       
        A=np.zeros((len(DG),len(DG)))
        for k, nbrs in DG.adj.items():
            for nbr, _ in nbrs.items():
                A[k-1,nbr-1]=1
        return self.PageRank_A(A)  
    


