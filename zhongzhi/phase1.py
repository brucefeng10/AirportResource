from gurobipy import *
import xlrd
m=690
n=202
r=27
m_large=10
e=0.1

fname='bianhao.xlsx'
bk=xlrd.open_workbook(fname)

try:
    sh_alpha = bk.sheet_by_name("timematch")
    sh_summ = bk.sheet_by_name("summ")
    sh_hbhd = bk.sheet_by_name("hbhd")
    sh_near = bk.sheet_by_name("near_jwhd")
    sh_hdtime = bk.sheet_by_name("hdmatch")
except:
    print "no sheet in %s named Sheet1" % fname

print 1

alpha=[[0]*m for i in range(m)]
summ=[[0]*n for i in range(m)]
hbhd=[[0]*r for i in range(m)]
near=[0]*n
hdtime=[[0]*m for i in range(m)]
hdtype=[0]*n



for i in range(m):
    for j in range(m):
        alpha[i][j]=sh_alpha.cell_value(i,j)
        hdtime[i][j]=sh_hdtime.cell_value(i,j)

    for k in range(n):
        summ[i][k]=sh_summ.cell_value(i,k)

    for t in range(r):
        hbhd[i][t]=sh_hbhd.cell_value(i,t)


near=sh_near.row_values(0)
hdtype=sh_near.row_values(1)

print 2

try:

    # Create a new model
    mod = Model("phase1")


    # Create variables
    
    x=mod.addVars(m,n,vtype=GRB.BINARY)
    y=mod.addVars(m,r,vtype=GRB.BINARY)
    #z=mod.addVars(m,m,r,vtype=GRB.BINARY)
    s=mod.addVars(m,vtype=GRB.BINARY)
    '''
    x = [[0]*n for i in range(m)]
    y = [[0]*r for i in range(m)]
    z = [[[0]*r for j in range(m)] for i in range(m)]
    s = [0]*m

    
    for i in range(m):
        for k in range(n):
            x[i][k]=mod.addVar(vtype=GRB.BINARY)
        for t in range(r):
            y[i][t]=mod.addVar(vtype=GRB.BINARY)
        s[i]=mod.addVar(vtype=GRB.BINARY)
    
    for t in range(r):
        for i in range(m):
            for j in range(m):
                z[i][j][t]=mod.addVar(vtype=GRB.BINARY)
    '''
    print 3

    # Set objective
    ob1=0
    ob2=0
    ob3=m
    for i in range(m):
        for k in range(n):
            if summ[i][k]==1:
                ob1+=x[i,k]
                ob2+=x[i,k]*near[k]
        ob3=ob3-s[i]

    objt=(ob1*3+ob2*2+ob3)/(m+0.0)
    
    mod.setObjective(objt, GRB.MAXIMIZE)

    print 4
    
    # Add constraint1
    for i in range(m-1):
        for j in range(i+1,m):
            if hdtime[i][j]==1:
                sum1=0
                for t in range(1,r):
                    if hbhd[i][t]==1 and hbhd[j][t]==1:
                        #sum1+=z[i,j,t]
                        mod.addConstr(s[i]>=0.5*(y[i,t]+y[j,t]-1))
                        mod.addConstr(s[j]>=0.5*(y[i,t]+y[j,t]-1))

    print 5
    '''
    # Add constraint2
    for t in range(r):
        for i in range(m-1):
            if hbhd[i][t]==1:
                for j in range(i+1,m):
                    if hbhd[j][t]==1 and hdtime[i][j]==1:
                        mod.addConstr(m_large*z[i,j,t]-e>=y[i,t]+y[j,t]-2)
                        mod.addConstr(m_large*(z[i,j,t]-1)<=y[i,t]+y[j,t]-2)
    
    print 7
    '''
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

    # Add constraint4
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

    print 7
    
    # Add constraint5
    for k in range(n):
        for i in range(m-1):
            if summ[i][k]==1:
                for j in range(i+1,m):
                    if summ[j][k]==1 and alpha[i][j]==0:
                        mod.addConstr(x[i,k]+x[j,k]<=1)

    print 8
        
    mod.Params.TimeLimit = 200

    mod.optimize()

    

    #for v in mod.getVars():
        #print(v.varName, v.x)

    print('Obj:', mod.objVal)

except GurobiError:
    print('Error reported')
