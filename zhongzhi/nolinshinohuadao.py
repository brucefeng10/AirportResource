# -*- coding: UTF-8 -*- 
from gurobipy import *
import xlrd
m=5901
n=205
r=24
m_large=10
e=0.1



print 1

alpha=[]
summ=[]
hbhd=[]




with open('jwsjct.txt','r') as f1:
    for line in f1:
        alpha.append(map(float,line.split(',')))

hdtime=[[0]*m for i in range(m)]
jinchu=[]
with open('jinchushijian.txt','r') as f1:#hua jin shi jian and hua chu shi jian
    for line in f1:
        jinchu.append(map(float,line.split(',')))
aa=jinchu[0]#进机位时开始占用滑道时间
bb=jinchu[1]#进机位时间
cc=jinchu[2]#出机位时间
dd=jinchu[3]#出机位时占用滑道结束时间
for i in range(m-1):
    for j in range(i+1,m):
        if (aa[j]-bb[i])*(bb[j]-aa[i])<0:#in-in
            hdtime[i][j]=1
            
        elif (cc[j]-bb[i])*(dd[j]-aa[i])<0:#in-out
            hdtime[i][j]=1
            
        elif (aa[j]-dd[i])*(bb[j]-cc[i])<0:#out-in
            hdtime[i][j]=1
            
        elif (cc[j]-dd[i])*(dd[j]-cc[i])<0:#out-out
            hdtime[i][j]=1
            


with open('summ4-205.txt','r') as f3:
    for line in f3:
        summ.append(map(float,line.split(',')))

for i in range(m):
    summ[i][125]=0
    summ[i][129]=0
    summ[i][132]=0

with open('hbhd205-24.txt','r') as f4:
    for line in f4:
        hbhd.append(map(float,line.split(',')))

nearjwhd=[]
with open('near_jwhd24.txt','r') as f5:
    for line in f5:
        nearjwhd.append(map(float,line.split(',')))
near=nearjwhd[0]
hdtype=nearjwhd[1]

passen=[]
with open('passenger.txt','r') as f6:
    for line in f6:
        passen.append(map(float,line.split(',')))

passenger=passen[0]




print 2

try:

    # Create a new model
    mod = Model("phase1")


    # Create variables
    
    x=mod.addVars(m,n,vtype=GRB.BINARY)
    y=mod.addVars(m,r,vtype=GRB.BINARY)
    #s=mod.addVars(m,vtype=GRB.BINARY)


    print 3

    # Set objective
    ob1=0
    ob2=0
    ob3=0
    ob4=0
    ob5=0
    for i in range(m):
        for k in range(n):
            if summ[i][k]==1:
                ob1+=x[i,k]
                ob2+=x[i,k]*near[k]
                ob3+=x[i,k]*near[k]*passenger[i]
        #ob5=ob5+s[i]

    objt=(ob1*10+ob2*3-ob4-ob5)/(5901+0.0)+3*ob3/2233564.0
    
    mod.setObjective(objt, GRB.MAXIMIZE)

    print 4
    '''
    # Add constraint1
    for i in range(m-1):
        for j in range(i+1,m):
            if hdtime[i][j]==1:
                for t in range(1,r):
                    if hbhd[i][t]==1 and hbhd[j][t]==1:
                        mod.addConstr(s[i]>=0.5*(y[i,t]+y[j,t]-1))
                        mod.addConstr(s[j]>=0.5*(y[i,t]+y[j,t]-1))

    print 5
    
    # Add constraint3
    for i in range(m):
        sum21=0
        sum22=0
        for t in range(r):
            sum21+=y[i,t]*(t+1)

        for k in range(n):
            sum22+=x[i,k]*hdtype[k]

        mod.addConstr(sum21==sum22)
    
    print 6
    '''
    # Add constraint4
    for i in range(m):
        sum3=0
        for k in range(n):
            sum3+=x[i,k]
            if summ[i][k]==0:
                mod.addConstr(x[i,k]<=0)
        mod.addConstr(sum3<=1)

    '''
        sum4=0
        for t in range(r):
            sum4+=y[i,t]
            
        mod.addConstr(sum4<=1)
    '''
    print 7
    
    # Add constraint5
    for k in range(n):
        for i in range(m-1):
            if summ[i][k]==1:
                for j in range(i+1,m):
                    if summ[j][k]==1 and alpha[i][j]==0:
                        mod.addConstr(x[i,k]+x[j,k]<=1)

    print 8
        
    mod.Params.TimeLimit = 10000

    mod.optimize()

    

    #for v in mod.getVars():
        #print(v.varName, v.x)

    print('Obj:', mod.objVal)

except GurobiError:
    print('Error reported')
