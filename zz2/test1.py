from gurobipy import *
import xlrd
m=5901
n=205
r=25
m_large=10
e=0.1
'''
fname='bianhao.xlsx'
bk=xlrd.open_workbook(fname)

try:
    sh_alpha = bk.sheet_by_name("jwsjct")
    sh_summ = bk.sheet_by_name("summ4-205")
    sh_hbhd = bk.sheet_by_name("hbhd205")
    sh_near = bk.sheet_by_name("near_jwhd")
    sh_hdtime = bk.sheet_by_name("hdsjct")
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
passenger=sh_near.row_values(2)

a=[]
with open('nihao.txt','r') as f:
    for line in f:
        a.append(map(float,line.split(',')))
'''

alpha=[]
summ=[]
hbhd=[]

hdtime=[]

passen=[]
nearjwhd=[]

with open('jwsjct.txt','r') as f1:
    for line in f1:
        alpha.append(map(float,line.split(',')))

with open('hdsjct.txt','r') as f2:
    for line in f2:
        hdtime.append(map(float,line.split(',')))

with open('summ4-205.txt','r') as f3:
    for line in f3:
        summ.append(map(float,line.split(',')))

with open('hbhd205.txt','r') as f4:
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
    #z=mod.addVars(m,m,r,vtype=GRB.BINARY)
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
            if hdtime[i][j]==1:
                sum1=0
                for t in range(1,r):
                    if hbhd[i][t]==1 and hbhd[j][t]==1:
                        mod.addConstr(s[i]>=0.5*(y[i,t]+y[j,t]-1))
                        mod.addConstr(s[j]>=0.5*(y[i,t]+y[j,t]-1))

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
        
    mod.Params.TimeLimit = 3600

    mod.optimize()

    

    #for v in mod.getVars():
        #print(v.varName, v.x)

    print('Obj:', mod.objVal)

except GurobiError:
    print('Error reported')


'''
obtain the result
a=mod.x
b=[i for i,v in enumerate(a) if v==1]
f = open("C:\Users\Admin\Desktop\wordout.txt","w")
for i in b:
	f.write(str(i)+',')
f.close()

5901*205=1209705
