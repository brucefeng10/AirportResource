# -*- coding: UTF-8 -*- 
from gurobipy import *
import xlrd
m=5901
n=274
r=27
m_large=10
e=0.1


alpha=[]
summ=[]

hbhd=[]
hdtime=[[0]*m for i in range(m)]
hdtime_inin=[[0]*m for i in range(m)]#in-in
hdtime_inout=[[0]*m for i in range(m)]#in-out
hdtime_outin=[[0]*m for i in range(m)]#out-in
hdtime_outout=[[0]*m for i in range(m)]#out-out
jinchu=[]
passen=[]
nearjwhd=[]

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
            hdtime_inin[i][j]=1
        elif (cc[j]-bb[i])*(dd[j]-aa[i])<0:#in-out
            hdtime[i][j]=1
            hdtime_inout[i][j]=1
        elif (aa[j]-dd[i])*(bb[j]-cc[i])<0:#out-in
            hdtime[i][j]=1
            hdtime_outin[i][j]=1
        elif (cc[j]-dd[i])*(dd[j]-cc[i])<0:#out-out
            hdtime[i][j]=1
            hdtime_outout[i][j]=1


#6.2临时机位时序限制情况下的冲突矩阵;i表示影响别人的航班，j表示受影响的航班
ls=[[1]*m for i in range(m)]#i，j航班存在进出时间冲突时lsij为0，否则为1
for i in range(m):
    for j in range(m):
        if bb[j]>bb[i] and bb[j]<cc[i]:
            ls[i][j]=0
        elif cc[j]>bb[i] and cc[j]<cc[i]:
            ls[i][j]=0
#受临时机位影响的机位
ls_influence=[[0,1,2,3],[0,1,2,3],[7,8,9],[9,10,11,12,13],[9,10,11,12,13,14,15,237],
[18,19,20],[20,21,22,23,24,25],[21,22,23,24,25,26,240],[30,31,32,33,34,35,36],[29,30,31,32,33,34,35,36,37,242],
[38],[39,40,41,112,113],[39,40,41,42,112,113,114,245],[50,51,52,53,54],[49,50,51,52,53,54,55,247],[59,60,61,62,63,64,65,66,250],
[60,61,62,63,64],[65,66],[71,72,73,74,75],[70,71,72,73,74,75,76,77,252],[99,100,101,102],[99,100,101,102,103,254],
[202,203,204,232,233],[178,179,180,181,182,183,258],[181,182,183],[184,185,186],[184,185,186,187,188,189,259]]
            
#6.3公务机坪父子机位情况下的冲突矩阵:i表示影响别人的航班，j表示受影响的航班
fz=[[1]*m for i in range(m)]#i，j航班存在父子进出冲突时fzij为0，否则为1
for i in range(m):
    for j in range(m):
        if bb[j]>bb[i] and bb[j]<cc[i]:
            fz[i][j]=0
#受父机坪影响的机位
fujiping=[125,129,132]
fz_influence=[range(127,144),range(131,144),range(134,144)]           


    


with open('jwsjct.txt','r') as f1:
    for line in f1:
        alpha.append(map(float,line.split(',')))
'''
with open('hdsjct.txt','r') as f2: #in and out huadao is the same
    for line in f2:
        hdtime.append(map(float,line.split(',')))

with open('hdsjct_d.txt','r') as f2: #in and out huadao is different
    for line in f2:
        hdtime_d.append(map(float,line.split(',')))
'''
with open('summ.txt','r') as f3:
    for line in f3:
        summ.append(map(float,line.split(',')))
for i in range(m):
    summ[i][125]=0
    summ[i][129]=0
    summ[i][132]=0


with open('hbhd.txt','r') as f4:
    for line in f4:
        hbhd.append(map(float,line.split(',')))

with open('near_jwhd.txt','r') as f5:
    for line in f5:
        nearjwhd.append(map(float,line.split(',')))

with open('passenger.txt','r') as f6:
    for line in f6:
        passen.append(map(float,line.split(',')))

passenger=passen[0]
near=nearjwhd[0]
hdtype=nearjwhd[1]



print 1

try:

    # Create a new model
    mod = Model("phase2")


    # Create variables
    x=mod.addVars(m,n,vtype=GRB.BINARY)
    y=mod.addVars(m,r,vtype=GRB.BINARY)
    s=mod.addVars(m,vtype=GRB.BINARY)
    
    print 2

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
        ob5+=s[i]

    objt=(ob1*10+ob2*3-ob4-ob5)/(m+0.0)+3*ob3/2233564.0
    
    mod.setObjective(objt, GRB.MAXIMIZE)

    print 3
    
    # Add constraint1
    for i in range(m-1):
        for j in range(i+1,m):
            for t in range(1,25):
                if hbhd[i][t]==1 and hbhd[j][t]==1 and hdtime[i][j]==1:
                    mod.addConstr(s[i]>=0.5*(y[i,t]+y[j,t]-1))
                    mod.addConstr(s[j]>=0.5*(y[i,t]+y[j,t]-1))

            for t in range(25,r):
                if hbhd[i][t]==1 and hbhd[j][t]==1 and hdtime_inin[i][j]+hdtime_outout[i][j]>=1:#in-in or out-out
                    mod.addConstr(s[i]>=0.5*(y[i,t]+y[j,t]-1))
                    mod.addConstr(s[j]>=0.5*(y[i,t]+y[j,t]-1))
    '''
            #huadao 9 and 26
            if hbhd[i][8]==1 and hbhd[j][25]==1 and hdtime_inin[i][j]+hdtime_outin[i][j]>=1:
                mod.addConstr(s[i]>=0.5*(y[i,8]+y[j,25]-1))
                mod.addConstr(s[j]>=0.5*(y[i,8]+y[j,25]-1))
            if hbhd[i][25]==1 and hbhd[j][8]==1 and hdtime_inin[i][j]+hdtime_inout[i][j]>=1:
                mod.addConstr(s[i]>=0.5*(y[i,25]+y[j,8]-1))
                mod.addConstr(s[j]>=0.5*(y[i,25]+y[j,8]-1))

            #huadao 26 and 27
            if hbhd[i][25]==1 and hbhd[j][26]==1 and hdtime_outout[i][j]>=1:
                mod.addConstr(s[i]>=0.5*(y[i,25]+y[j,26]-1))
                mod.addConstr(s[j]>=0.5*(y[i,25]+y[j,26]-1))
            if hbhd[i][26]==1 and hbhd[j][25]==1 and hdtime_outout[i][j]>=1:
                mod.addConstr(s[i]>=0.5*(y[i,26]+y[j,25]-1))
                mod.addConstr(s[j]>=0.5*(y[i,26]+y[j,25]-1))
    '''

    print 4
    
    # Add constraint2
    for i in range(m):
        sum21=0
        sum22=0

        for t in range(r):
            sum21+=y[i,t]*(t+1)

        for k in range(n):
            sum22+=x[i,k]*hdtype[k]

        mod.addConstr(sum21==sum22)

    print 5
    
    # Add constraint3
    for i in range(m):
        sum3=0
        for k in range(n):
            sum3+=x[i,k]
            if summ[i][k]==0:
                mod.addConstr(x[i,k]<=0)
        sum4=0

        for t in range(r):
            sum4+=y[i,t]
            
        mod.addConstr(sum3<=1)
        mod.addConstr(sum4<=1)

    print 6
    
    # Add constraint4
    for k in range(n):
        for i in range(m-1):
            if summ[i][k]==1:
                for j in range(i+1,m):
                    if summ[j][k]==1 and alpha[i][j]==0:
                        mod.addConstr(x[i,k]+x[j,k]<=1)

    print 7
        
    # Add constraint 6.2临时机位
    for i in range(m):
        for j in range(n):
            if ls[i][j]==0:
                for k in range(234,261):#临时机位
                    for l in ls_influence[k-234]:#临时机位影响的机位
                        if l<=204:
                            if summ[i][k]==1 and summ[j][l]==1:
                                mod.addConstr(x[i,k]+x[j,l]<=1)
                        else:
                            if summ[i][k]==1 and summ[j][l]==1:
                                mod.addConstr(x[i,k]+x[j,l]<=1)        

    print 8

    # Add constraint 6.3父子机坪
    #子机坪和父机坪的约束
    for i in range(m):
        for j in range(m):
            if i!=j and alpha[i][j]==0:
                mod.addConstr(x[i,124]<=1-x[j,125])
                mod.addConstr(x[i,126]<=1-x[j,125])
                mod.addConstr(x[i,128]<=1-x[j,129])
                mod.addConstr(x[i,130]<=1-x[j,129])
                mod.addConstr(x[i,131]<=1-x[j,132])
                mod.addConstr(x[i,133]<=1-x[j,132])
    
    print 9
    #父机坪和受父机坪影响的机位约束
    for i in range(m):
        for j in range(m):
            if i!=j and fz[i][j]==0:
                for k in fujiping:
                    for l in fz_influence[fujiping.index(k)]:
                        if summ[i][k]==1 and summ[j][l]:
                            mod.addConstr(1-x[i,k]+fz[i][j]>=x[j,l])
            
    print 10

    # Add constraint 6.1超远机坪
    #A集合表示第一个大型机位（501），C集合表示最后一个大型机位（515），B集合表示中间的大型机位
    for i in range(m):
        for j in range(m):
            if alpha[i][j]==0:
                if summ[i][205]==1 and summ[j][190]==1:
                    mod.addConstr(x[i,205]<=1-x[j,190])
                if summ[i][220]==1 and summ[j][190]==1:
                    mod.addConstr(x[i,]<=1-x[j,190])
                    
                if summ[i][219]==1 and summ[j][204]==1:
                    mod.addConstr(x[i,219]<=1-x[j,204])
                if summ[i][233]==1 and summ[j][204]==1:
                    mod.addConstr(x[i,205]<=1-x[j,190])
                    
                for k in range(206,219):
                    for l in range(191,205):
                        if summ[i][k]==1 and summ[j][l]==1:
                            mod.addConstr(x[i,k]<=1-x[j,l])
                for k in range(261,274):
                    for l in range(191,205):
                        if summ[i][k]==1 and summ[j][l]==1:
                            mod.addConstr(x[i,k]<=1-x[j,l])
                for k in range(221,234):
                    for l in range(191,205):
                        if summ[i][k]==1 and summ[j][l]==1:
                            mod.addConstr(x[i,k]<=1-x[j,l])
                            
    print 11
    #加强约束
    for i in range(m):
        for j in range(m):
            if alpha[i][j]==0:
                #A、B集合里面中间停了，下一个机位的左机位就不能停
                for k in range(206,219):
                    if summ[i][k]==1 and summ[j][k+14]==1:
                        mod.addConstr(x[i,k]<=1-x[j,k+14])
                #B集合中左机位停了，右机位就不能停，反之亦然
                for k in range(206,219):
                    if summ[i][k]==1 and summ[j][k+55]==1:
                        mod.addConstr(x[i,k]<=1-x[j,k+55])
    
    print 12
    
    
    mod.Params.TimeLimit = 200

    mod.optimize()

    

    #for v in mod.getVars():
        #print(v.varName, v.x)

    print('Obj:', mod.objVal)

except GurobiError:
    print('Error reported')
